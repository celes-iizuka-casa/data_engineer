#!/usr/bin/env python3
"""Regenerate explicit Spark/Hive DDL files from split INSERT SQL files."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


DECLARATION_PATTERN = re.compile(
    r"^[ \t]*(?P<prefix>--[ \t]*)?"
    r"(?P<verb>CREATE|ALTER)\s+(?:OR\s+REPLACE\s+)?"
    r"(?P<object>VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"(?P<schema>`?(?:dx_ve|gold)`?)\.(?P<table>`?[A-Za-z0-9_]+`?)\s+AS\b",
    re.IGNORECASE | re.MULTILINE,
)
INSERT_PATTERN = re.compile(
    r"\bINSERT\s+OVERWRITE\s+TABLE\s+gold\.(?P<table>`?[A-Za-z0-9_]+`?)\b",
    re.IGNORECASE,
)
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
STAR_ITEM_RE = re.compile(r"^\s*(?:DISTINCT\s+)?(?:(?P<alias>[A-Za-z_][A-Za-z0-9_]*)\.)?\*\s*$", re.IGNORECASE)


@dataclass(frozen=True)
class ColumnSpec:
    name: str
    comment: str | None


@dataclass(frozen=True)
class ParsedItem:
    raw: str
    leading_comment: str | None
    inline_comment: str | None


def sanitize_comment(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return cleaned.replace("'", "''")


def normalize_table_comment(value: str) -> str:
    cleaned = value.strip()
    cleaned = re.sub(
        r"^(?:dx_ve|gold)\.[A-Za-z0-9_]+[_-]?",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
    cleaned = re.sub(r"^vbi\d+(?:_en)?[_-]?", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip() or value.strip()


def quote_identifier(name: str) -> str:
    return name if IDENTIFIER_RE.fullmatch(name) else f"`{name.replace('`', '')}`"


def strip_quotes(name: str) -> str:
    if len(name) >= 2 and name[0] == name[-1] and name[0] in {"`", '"', "'"}:
        return name[1:-1]
    return name


def remove_line_comments(text: str) -> str:
    return re.sub(r"--[^\r\n]*", "", text)


def scanner_find_keyword(text: str, keyword: str, start: int = 0, depth_required: int | None = None) -> int:
    keyword_lower = keyword.lower()
    quote: str | None = None
    line_comment = False
    block_comment = False
    depth = 0
    i = start
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if line_comment:
            if ch in "\r\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            if ch == "\\" and quote in {"'", '"'}:
                i += 2
                continue
            if ch == quote:
                if quote in {"'", '"'} and nxt == quote:
                    i += 2
                    continue
                quote = None
            i += 1
            continue
        if ch == "-" and nxt == "-":
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue
        if ch in {"'", '"', "`"}:
            quote = ch
            i += 1
            continue
        if ch == "(":
            depth += 1
            i += 1
            continue
        if ch == ")":
            depth = max(0, depth - 1)
            i += 1
            continue
        if depth_required is not None and depth != depth_required:
            i += 1
            continue
        if ch.isalpha():
            j = i + 1
            while j < len(text) and (text[j].isalnum() or text[j] == "_"):
                j += 1
            token = text[i:j].lower()
            prev_ok = i == 0 or not (text[i - 1].isalnum() or text[i - 1] == "_")
            next_ok = j == len(text) or not (text[j].isalnum() or text[j] == "_")
            if prev_ok and next_ok and token == keyword_lower:
                return i
            i = j
            continue
        i += 1
    return -1


def skip_ws_and_comments(text: str, index: int) -> int:
    while index < len(text):
        if text[index].isspace():
            index += 1
            continue
        if text[index : index + 2] == "--":
            end = text.find("\n", index)
            index = len(text) if end == -1 else end + 1
            continue
        if text[index : index + 2] == "/*":
            end = text.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unclosed block comment")
            index = end + 2
            continue
        break
    return index


def read_identifier(text: str, index: int) -> tuple[str, int]:
    index = skip_ws_and_comments(text, index)
    if index >= len(text):
        raise ValueError("Identifier expected but text ended")
    if text[index] == "`":
        end = text.find("`", index + 1)
        if end == -1:
            raise ValueError("Unclosed quoted identifier")
        return text[index + 1 : end], end + 1
    end = index
    while end < len(text) and (text[end].isalnum() or text[end] in {"_", "."}):
        end += 1
    if end == index:
        raise ValueError("Identifier expected")
    return text[index:end], end


def extract_parenthesized(text: str, index: int) -> tuple[str, int]:
    if text[index] != "(":
        raise ValueError("Expected opening parenthesis")
    quote: str | None = None
    line_comment = False
    block_comment = False
    depth = 0
    start = index + 1
    i = index
    while i < len(text):
        ch = text[i]
        nxt = text[i + 1] if i + 1 < len(text) else ""
        if line_comment:
            if ch in "\r\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            if ch == "*" and nxt == "/":
                block_comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            if ch == "\\" and quote in {"'", '"'}:
                i += 2
                continue
            if ch == quote:
                if quote in {"'", '"'} and nxt == quote:
                    i += 2
                    continue
                quote = None
            i += 1
            continue
        if ch == "-" and nxt == "-":
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            block_comment = True
            i += 2
            continue
        if ch in {"'", '"', "`"}:
            quote = ch
            i += 1
            continue
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[start:i], i + 1
        i += 1
    raise ValueError("Unclosed parenthesized block")


def split_select_items(select_list: str) -> list[str]:
    items: list[str] = []
    quote: str | None = None
    line_comment = False
    block_comment = False
    depth = 0
    chunk: list[str] = []
    i = 0
    while i < len(select_list):
        ch = select_list[i]
        nxt = select_list[i + 1] if i + 1 < len(select_list) else ""
        if line_comment:
            chunk.append(ch)
            if ch in "\r\n":
                line_comment = False
            i += 1
            continue
        if block_comment:
            chunk.append(ch)
            if ch == "*" and nxt == "/":
                chunk.append(nxt)
                block_comment = False
                i += 2
            else:
                i += 1
            continue
        if quote:
            chunk.append(ch)
            if ch == "\\" and quote in {"'", '"'}:
                if i + 1 < len(select_list):
                    chunk.append(select_list[i + 1])
                i += 2
                continue
            if ch == quote:
                if quote in {"'", '"'} and nxt == quote:
                    chunk.append(nxt)
                    i += 2
                    continue
                quote = None
            i += 1
            continue
        if ch == "-" and nxt == "-":
            chunk.append(ch)
            chunk.append(nxt)
            line_comment = True
            i += 2
            continue
        if ch == "/" and nxt == "*":
            chunk.append(ch)
            chunk.append(nxt)
            block_comment = True
            i += 2
            continue
        if ch in {"'", '"', "`"}:
            quote = ch
            chunk.append(ch)
            i += 1
            continue
        if ch == "(":
            depth += 1
            chunk.append(ch)
            i += 1
            continue
        if ch == ")":
            depth = max(0, depth - 1)
            chunk.append(ch)
            i += 1
            continue
        if ch == "," and depth == 0:
            j = i + 1
            while j < len(select_list) and select_list[j] in " \t":
                j += 1
            if select_list[j : j + 2] == "--":
                while j < len(select_list) and select_list[j] not in "\r\n":
                    chunk.append(select_list[j])
                    j += 1
                if j < len(select_list):
                    chunk.append(select_list[j])
                    j += 1
            item = "".join(chunk).strip()
            if item:
                items.append(item)
            chunk = []
            i = j
            continue
        chunk.append(ch)
        i += 1
    tail = "".join(chunk).strip()
    if tail:
        items.append(tail)
    return items


def extract_trailing_comment(item: str) -> str | None:
    inline_comments: list[str] = []
    for line in item.splitlines():
        if "--" not in line:
            continue
        code, comment = line.split("--", 1)
        if code.strip():
            inline_comments.append(comment)
    if not inline_comments:
        return None
    return sanitize_comment(inline_comments[-1])


def extract_leading_comment(item: str) -> str | None:
    lines = item.splitlines()
    captured: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if captured:
                break
            continue
        if stripped.startswith("--"):
            captured.append(stripped[2:].strip())
            continue
        break
    if len(captured) != 1:
        return None
    return sanitize_comment(captured[0])


def remove_leading_comment_lines(item: str) -> str:
    lines = item.splitlines()
    kept: list[str] = []
    started = False
    for line in lines:
        if not started and re.match(r"^\s*--", line):
            continue
        if not started and not line.strip():
            continue
        started = True
        kept.append(line)
    return "\n".join(kept).strip()


def strip_metadata_prefix(sql_text: str) -> str:
    lines = sql_text.splitlines()
    start = 0
    while start < len(lines):
        line = lines[start].strip()
        if not line or line.startswith("--"):
            start += 1
            continue
        break
    return "\n".join(lines[start:]).strip()


def derive_column_name(item: str, index: int) -> str:
    without_comments = remove_line_comments(remove_leading_comment_lines(item)).strip()
    without_comments = re.sub(r"^\s*DISTINCT\s+", "", without_comments, flags=re.IGNORECASE)
    alias_match = re.search(r"\bAS\s+(`[^`]+`|[A-Za-z_][A-Za-z0-9_]*|[^\s,()]+)\s*$", without_comments, re.IGNORECASE)
    if alias_match:
        return strip_quotes(alias_match.group(1))
    bare = re.fullmatch(r"(?:[A-Za-z_][A-Za-z0-9_]*\.)?(`[^`]+`|[A-Za-z_][A-Za-z0-9_]*)", without_comments)
    if bare:
        return strip_quotes(bare.group(1))
    tail = re.search(r"(`[^`]+`|[A-Za-z_][A-Za-z0-9_]*)\s*$", without_comments)
    if tail:
        return strip_quotes(tail.group(1))
    return f"col_{index:03d}"


def split_ctes(query_text: str) -> tuple[dict[str, str], str]:
    ctes: dict[str, str] = {}
    index = skip_ws_and_comments(query_text, 0)
    if query_text[index : index + 4].lower() != "with":
        return ctes, query_text[index:]
    index += 4
    while True:
        name, index = read_identifier(query_text, index)
        name = name.split(".")[-1].lower()
        index = skip_ws_and_comments(query_text, index)
        if query_text[index : index + 2].lower() != "as":
            raise ValueError(f"CTE AS expected for {name}")
        index += 2
        index = skip_ws_and_comments(query_text, index)
        body, index = extract_parenthesized(query_text, index)
        ctes[name] = body.strip()
        index = skip_ws_and_comments(query_text, index)
        if index < len(query_text) and query_text[index] == ",":
            index += 1
            continue
        return ctes, query_text[index:].strip()


def query_body_from_sql(sql_text: str) -> str:
    sql_text = strip_metadata_prefix(sql_text)
    insert_match = INSERT_PATTERN.search(sql_text)
    if not insert_match:
        raise ValueError("INSERT OVERWRITE TABLE gold.<table> not found")
    return (sql_text[: insert_match.start()] + sql_text[insert_match.end() :]).strip()


def resolve_star_columns(item: str, current_query: str, ctes: dict[str, str]) -> list[ColumnSpec] | None:
    match = STAR_ITEM_RE.match(remove_line_comments(remove_leading_comment_lines(item)).strip())
    if not match:
        return None
    requested_alias = match.group("alias")
    select_pos = scanner_find_keyword(current_query, "select", 0, depth_required=0)
    from_pos = scanner_find_keyword(current_query, "from", select_pos, depth_required=0)
    if from_pos < 0:
        return None
    source_index = skip_ws_and_comments(current_query, from_pos + len("from"))
    if source_index >= len(current_query):
        return None
    if current_query[source_index] == "(":
        subquery, after = extract_parenthesized(current_query, source_index)
        alias, _ = read_identifier(current_query, after)
        alias = alias.split(".")[-1]
        if requested_alias and alias.lower() != requested_alias.lower():
            return None
        return extract_columns_from_query(subquery, ctes)
    source_name, after = read_identifier(current_query, source_index)
    alias = source_name.split(".")[-1]
    after = skip_ws_and_comments(current_query, after)
    if after < len(current_query):
        next_token_match = re.match(r"[A-Za-z_][A-Za-z0-9_]*", current_query[after:])
        if next_token_match and next_token_match.group(0).lower() not in {
            "where",
            "group",
            "order",
            "join",
            "left",
            "right",
            "inner",
            "full",
            "cross",
            "union",
            "limit",
            "having",
        }:
            alias = next_token_match.group(0)
    if requested_alias and alias.lower() != requested_alias.lower():
        return None
    cte_name = source_name.split(".")[-1].lower()
    if cte_name in ctes:
        return extract_columns_from_query(ctes[cte_name], ctes)
    return None


def extract_columns_from_query(query_text: str, inherited_ctes: dict[str, str] | None = None) -> list[ColumnSpec]:
    inherited_ctes = dict(inherited_ctes or {})
    local_ctes, body = split_ctes(query_text)
    ctes = {**inherited_ctes, **local_ctes}
    select_pos = scanner_find_keyword(body, "select", 0, depth_required=0)
    if select_pos < 0:
        raise ValueError("Top-level SELECT not found")
    from_pos = scanner_find_keyword(body, "from", select_pos, depth_required=0)
    if from_pos < 0:
        raise ValueError("Top-level FROM not found after SELECT")
    select_list = body[select_pos + len("select") : from_pos]
    items = split_select_items(select_list)
    if not items:
        raise ValueError("No SELECT items found")
    parsed_items = [
        ParsedItem(
            raw=item,
            leading_comment=extract_leading_comment(item),
            inline_comment=extract_trailing_comment(item),
        )
        for item in items
    ]
    columns: list[ColumnSpec] = []
    seen: set[str] = set()
    for index, parsed in enumerate(parsed_items, start=1):
        expanded = resolve_star_columns(parsed.raw, body, ctes)
        if expanded is not None:
            for column in expanded:
                key = column.name.lower()
                if key in seen:
                    raise ValueError(f"Duplicate output column name detected: {column.name}")
                seen.add(key)
                columns.append(column)
            continue
        name = derive_column_name(parsed.raw, index)
        key = name.lower()
        if key in seen:
            raise ValueError(f"Duplicate output column name detected: {name}")
        seen.add(key)
        comment = parsed.inline_comment
        if comment is None and parsed.leading_comment is not None:
            prev_has_leading = index > 1 and parsed_items[index - 2].leading_comment is not None
            next_has_leading = index < len(parsed_items) and parsed_items[index].leading_comment is not None
            if prev_has_leading or next_has_leading:
                comment = parsed.leading_comment
        if comment is None and not IDENTIFIER_RE.fullmatch(name):
            comment = sanitize_comment(name)
        columns.append(ColumnSpec(name=name, comment=comment))
    return columns


def extract_select_columns(sql_text: str) -> list[ColumnSpec]:
    body = query_body_from_sql(sql_text)
    return extract_columns_from_query(body)


def extract_table_comment_block(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8-sig")
    matches = list(DECLARATION_PATTERN.finditer(text))
    comments: dict[str, str] = {}
    for match in matches:
        target = strip_quotes(match.group("table")).lower()
        before = text[: match.start()]
        lines = before.splitlines()
        description: str | None = None
        for line in reversed(lines):
            stripped = line.strip()
            if not stripped:
                if description is not None:
                    break
                continue
            if not stripped.startswith("--"):
                if description is not None:
                    break
                continue
            body = stripped[2:].strip()
            if re.match(r"^(create|alter)\s+(view|table)\b", body, re.IGNORECASE):
                continue
            if body:
                description = normalize_table_comment(body)
                break
        if description and target not in comments:
            comments[target] = description
    return comments


def discover_table_comments(source_root: Path) -> dict[str, str]:
    table_comments: dict[str, str] = {}
    for path in sorted(source_root.rglob("*.sql")):
        if path.name.lower().endswith("_gold.sql"):
            continue
        for target, comment in extract_table_comment_block(path).items():
            table_comments.setdefault(target, comment)
    return table_comments


def build_ddl(table: str, table_comment: str | None, columns: list[ColumnSpec]) -> str:
    width = max(len(quote_identifier(column.name)) for column in columns)
    lines = [f"CREATE TABLE IF NOT EXISTS gold.{table.lower()} ("]
    for index, column in enumerate(columns):
        identifier = quote_identifier(column.name)
        line = f"    {identifier.ljust(width)}   STRING"
        if column.comment:
            line += f" COMMENT '{column.comment}'"
        if index < len(columns) - 1:
            line += ","
        lines.append(line)
    lines.append(")")
    effective_comment = sanitize_comment(table_comment or table.lower())
    lines.append(f"COMMENT '{effective_comment}'")
    lines.append("STORED AS PARQUET;")
    return "\n".join(lines) + "\n"


def generate(sql_dir: Path, source_root: Path, output_dir: Path) -> list[str]:
    table_comments = discover_table_comments(source_root)
    generated: list[str] = []
    for sql_path in sorted(sql_dir.glob("*.sql")):
        sql_text = sql_path.read_text(encoding="utf-8-sig")
        columns = extract_select_columns(sql_text)
        table = sql_path.stem.lower()
        ddl = build_ddl(table, table_comments.get(table), columns)
        (output_dir / f"{table}.ddl").write_text(ddl, encoding="utf-8")
        generated.append(table)
    return generated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sql-dir", required=True, type=Path)
    parser.add_argument("--source-root", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    generated = generate(args.sql_dir, args.source_root, args.output_dir)
    print(f"generated={len(generated)}")


if __name__ == "__main__":
    main()
