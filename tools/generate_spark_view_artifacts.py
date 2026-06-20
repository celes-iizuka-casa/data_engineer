#!/usr/bin/env python3
"""Generate split Spark Iceberg DDL and INSERT SQL from commented View SQL."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, replace
from pathlib import Path


DECLARATION_PATTERN = re.compile(
    r"^[ \t]*(?:--[ \t\ufeff]*)?"
    r"(?P<verb>CREATE|ALTER)\s+(?:OR\s+REPLACE\s+)?"
    r"(?P<object>VIEW|TABLE)\s+(?:IF\s+NOT\s+EXISTS\s+)?"
    r"(?P<schema>`?(?:dx_ve|gold)`?)\.(?P<table>`?[A-Za-z0-9_]+`?)\s+AS\b",
    re.IGNORECASE | re.MULTILINE,
)
INTERNAL_REFERENCE_PATTERN = re.compile(
    r"\bdx_ve\.(?P<table>`?[A-Za-z0-9_]+`?)", re.IGNORECASE
)
GOLD_DEPENDENCY_PATTERN = re.compile(
    r"\b(?:FROM|JOIN)\s+gold\.(?P<table>`?[A-Za-z0-9_]+`?)",
    re.IGNORECASE,
)
JST_CURRENT_TIMESTAMP_PATTERN = re.compile(
    r"\bFROM_UTC_TIMESTAMP\s*\(\s*UTC_TIMESTAMP\s*\(\s*\)\s*,\s*"
    r"(['\"])JST\1\s*\)",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class DeclarationGroup:
    target: str
    start: int
    query_start: int


@dataclass(frozen=True)
class Artifact:
    target: str
    source_path: Path
    query: str
    dependencies: tuple[str, ...] = ()
    dependency_level: int = 0
    runtime_requirements: tuple[str, ...] = ()

    @property
    def filename_stem(self) -> str:
        return self.target.lower()


def _only_metadata_between(text: str) -> bool:
    return not re.search(r"\b(?:SELECT|WITH|FROM|INSERT)\b", text, re.IGNORECASE)


def _group_declarations(text: str, source_path: Path) -> list[DeclarationGroup]:
    matches = list(DECLARATION_PATTERN.finditer(text))
    if not matches:
        raise ValueError(f"No View/Table declaration found: {source_path}")

    groups: list[DeclarationGroup] = []
    last_match_end = -1
    for match in matches:
        target = match.group("table").replace("`", "")
        if (
            groups
            and groups[-1].target.lower() == target.lower()
            and _only_metadata_between(text[last_match_end : match.start()])
        ):
            groups[-1] = replace(groups[-1], query_start=match.end())
        else:
            groups.append(
                DeclarationGroup(
                    target=target,
                    start=match.start(),
                    query_start=match.end(),
                )
            )
        last_match_end = match.end()
    return groups


def _statement_end(text: str) -> int | None:
    quote: str | None = None
    line_comment = False
    block_comment = False
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char in "\r\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote:
            if char == "\\" and quote in {"'", '"'}:
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        if char == ";":
            return index
        index += 1
    if quote or block_comment:
        raise ValueError("Unclosed quote or block comment")
    return None


def _remove_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    return re.sub(r"--[^\r\n]*", " ", text)


def _extract_query(block: str, target: str, source_path: Path) -> str:
    block = block.strip()
    end = _statement_end(block)
    if end is not None:
        trailing = block[end + 1 :]
        trailing_tokens = _remove_comments(trailing).replace(";", "").strip()
        if trailing_tokens:
            raise ValueError(
                f"Multiple SQL statements found in target block: {target} ({source_path})"
            )
        block = block[:end]
    query = block.strip()
    first_token_text = _remove_comments(query).lstrip()
    if not re.match(r"(?:WITH|SELECT)\b", first_token_text, re.IGNORECASE):
        raise ValueError(f"Query does not start with WITH/SELECT: {target} ({source_path})")
    return query


def parse_source_file(path: Path, source_root: Path) -> list[Artifact]:
    text = path.read_text(encoding="utf-8-sig")
    groups = _group_declarations(text, path)
    artifacts: list[Artifact] = []
    for index, group in enumerate(groups):
        block_end = groups[index + 1].start if index + 1 < len(groups) else len(text)
        query = _extract_query(
            text[group.query_start : block_end], group.target, path
        )
        artifacts.append(
            Artifact(
                target=group.target,
                source_path=path.relative_to(source_root),
                query=query,
            )
        )
    return artifacts


def discover_artifacts(source_root: Path) -> list[Artifact]:
    source_paths = sorted(
        path
        for path in source_root.rglob("*.sql")
        if not path.name.lower().endswith("_gold.sql")
    )
    if not source_paths:
        raise ValueError(f"No source SQL files found: {source_root}")

    artifacts = [
        artifact
        for path in source_paths
        for artifact in parse_source_file(path, source_root)
    ]
    targets: dict[str, Path] = {}
    for artifact in artifacts:
        key = artifact.target.lower()
        if key in targets:
            raise ValueError(
                f"Duplicate target across sources: {artifact.target} "
                f"({targets[key]}, {artifact.source_path})"
            )
        targets[key] = artifact.source_path
    return artifacts


def _quote_non_ascii_identifiers(query: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if char == "-" and next_char == "-":
            end = query.find("\n", index)
            if end == -1:
                output.append(query[index:])
                break
            output.append(query[index:end])
            index = end
            continue
        if char == "/" and next_char == "*":
            end = query.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unclosed block comment while quoting identifiers")
            output.append(query[index : end + 2])
            index = end + 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            end = index + 1
            while end < len(query):
                if query[end] == "\\" and quote in {"'", '"'}:
                    end += 2
                    continue
                if query[end] == quote:
                    if end + 1 < len(query) and query[end + 1] == quote:
                        end += 2
                        continue
                    end += 1
                    break
                end += 1
            else:
                raise ValueError("Unclosed quote while quoting identifiers")
            output.append(query[index:end])
            index = end
            continue
        if char.isalnum() or char == "_":
            end = index + 1
            while end < len(query) and (query[end].isalnum() or query[end] == "_"):
                end += 1
            token = query[index:end]
            output.append(f"`{token}`" if any(ord(item) > 127 for item in token) else token)
            index = end
            continue
        output.append(char)
        index += 1
    return "".join(output)


def _normalize_double_quoted_literals(query: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if char == "-" and next_char == "-":
            end = query.find("\n", index)
            if end == -1:
                output.append(query[index:])
                break
            output.append(query[index:end])
            index = end
            continue
        if char == "/" and next_char == "*":
            end = query.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unclosed block comment while normalizing literals")
            output.append(query[index : end + 2])
            index = end + 2
            continue
        if char in {"'", "`"}:
            quote = char
            end = index + 1
            while end < len(query):
                if query[end] == "\\" and quote == "'":
                    end += 2
                    continue
                if query[end] == quote:
                    if end + 1 < len(query) and query[end + 1] == quote:
                        end += 2
                        continue
                    end += 1
                    break
                end += 1
            else:
                raise ValueError("Unclosed quote while normalizing literals")
            output.append(query[index:end])
            index = end
            continue
        if char == '"':
            end = index + 1
            value: list[str] = []
            while end < len(query):
                if query[end] == '"':
                    if end + 1 < len(query) and query[end + 1] == '"':
                        value.append('"')
                        end += 2
                        continue
                    break
                value.append(query[end])
                end += 1
            if end >= len(query):
                raise ValueError("Unclosed double-quoted string literal")
            output.append("'" + "".join(value).replace("'", "''") + "'")
            index = end + 1
            continue
        output.append(char)
        index += 1
    return "".join(output)


def _normalize_single_quoted_aliases(query: str) -> str:
    output: list[str] = []
    index = 0
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if char == "-" and next_char == "-":
            end = query.find("\n", index)
            if end == -1:
                output.append(query[index:])
                break
            output.append(query[index:end])
            index = end
            continue
        if char == "/" and next_char == "*":
            end = query.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unclosed block comment while normalizing aliases")
            output.append(query[index : end + 2])
            index = end + 2
            continue
        if char in {'"', "`", "'"}:
            quote = char
            end = index + 1
            while end < len(query):
                if query[end] == "\\" and quote in {"'", '"'}:
                    end += 2
                    continue
                if query[end] == quote:
                    if end + 1 < len(query) and query[end + 1] == quote:
                        end += 2
                        continue
                    end += 1
                    break
                end += 1
            else:
                raise ValueError("Unclosed quote while normalizing aliases")
            output.append(query[index:end])
            index = end
            continue
        if query[index : index + 2].upper() == "AS":
            before = query[index - 1] if index else " "
            after = query[index + 2] if index + 2 < len(query) else " "
            if not (before.isalnum() or before == "_") and not (
                after.isalnum() or after == "_"
            ):
                whitespace_end = index + 2
                while whitespace_end < len(query) and query[whitespace_end].isspace():
                    whitespace_end += 1
                if whitespace_end < len(query) and query[whitespace_end] == "'":
                    alias_end = whitespace_end + 1
                    alias_chars: list[str] = []
                    while alias_end < len(query):
                        if query[alias_end] == "'":
                            if alias_end + 1 < len(query) and query[alias_end + 1] == "'":
                                alias_chars.append("'")
                                alias_end += 2
                                continue
                            break
                        alias_chars.append(query[alias_end])
                        alias_end += 1
                    if alias_end >= len(query):
                        raise ValueError("Unclosed single-quoted alias")
                    alias = "".join(alias_chars).replace("`", "``")
                    output.append(query[index:whitespace_end])
                    output.append(f"`{alias}`")
                    index = alias_end + 1
                    continue
        output.append(char)
        index += 1
    return "".join(output)


def _normalize_values_column_aliases(query: str) -> str:
    """Move a VALUES column alias to Spark's derived-table alias clause."""
    pattern = re.compile(
        r"\bVALUES\s*\(\s*"
        r"\(\s*(?P<first>[^()]*)\s+AS\s+"
        r"(?P<column>[A-Za-z_][A-Za-z0-9_]*)\s*\)"
        r"(?P<rest>(?:\s*,\s*\([^()]*\))*)\s*\)"
        r"(?P<between>\s*)\)\s*(?:AS\s+)?"
        r"(?P<alias>[A-Za-z_][A-Za-z0-9_]*)",
        re.IGNORECASE,
    )

    def replace_values(match: re.Match[str]) -> str:
        return (
            f"VALUES ({match.group('first').strip()}){match.group('rest')}"
            f"{match.group('between')}) AS {match.group('alias')}"
            f"({match.group('column')})"
        )

    return pattern.sub(replace_values, query)


def _matching_parenthesis(text: str, opening: int) -> int:
    depth = 0
    quote: str | None = None
    line_comment = False
    block_comment = False
    index = opening
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char in "\r\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote:
            if char == "\\" and quote in {"'", '"'}:
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    raise ValueError("Unclosed function parenthesis")


def _split_function_arguments(text: str) -> list[str]:
    arguments: list[str] = []
    start = 0
    depth = 0
    quote: str | None = None
    line_comment = False
    block_comment = False
    index = 0
    while index < len(text):
        char = text[index]
        next_char = text[index + 1] if index + 1 < len(text) else ""
        if line_comment:
            if char in "\r\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote:
            if char == "\\" and quote in {"'", '"'}:
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
        elif char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
        elif char == "," and depth == 0:
            arguments.append(text[start:index].strip())
            start = index + 1
        index += 1
    arguments.append(text[start:].strip())
    return arguments


def _spark_function_replacement(name: str, arguments: list[str]) -> str | None:
    normalized = name.lower()
    expected = {
        "days_add": 2,
        "from_timestamp": 2,
        "hours_add": 2,
        "isnottrue": 1,
        "minutes_add": 2,
        "months_add": 2,
        "months_sub": 2,
        "nullifzero": 1,
    }
    if normalized in expected and len(arguments) != expected[normalized]:
        raise ValueError(
            f"Unexpected argument count for {name}: {len(arguments)}"
        )
    if normalized == "days_add":
        return f"date_add({arguments[0]}, {arguments[1]})"
    if normalized == "from_timestamp":
        return f"date_format({arguments[0]}, {arguments[1]})"
    if normalized == "hours_add":
        return (
            f"(CAST({arguments[0]} AS TIMESTAMP) + "
            f"INTERVAL {arguments[1]} HOURS)"
        )
    if normalized == "isnottrue":
        return f"(NOT coalesce({arguments[0]}, false))"
    if normalized == "minutes_add":
        return f"({arguments[0]} + INTERVAL {arguments[1]} MINUTES)"
    if normalized == "months_add":
        return f"add_months({arguments[0]}, {arguments[1]})"
    if normalized == "months_sub":
        return f"add_months({arguments[0]}, -({arguments[1]}))"
    if normalized == "nullifzero":
        return f"nullif({arguments[0]}, 0)"
    if normalized == "group_concat":
        if len(arguments) not in {1, 2}:
            raise ValueError(
                f"Unexpected argument count for {name}: {len(arguments)}"
            )
        expression = arguments[0]
        if re.match(r"(?is)^\s*(?:ALL|DISTINCT)\b", expression):
            raise ValueError("GROUP_CONCAT ALL/DISTINCT requires explicit review")
        separator = arguments[1] if len(arguments) == 2 else "', '"
        return (
            f"CASE WHEN count({expression}) = 0 THEN NULL "
            f"ELSE concat_ws({separator}, collect_list({expression})) END"
        )
    if normalized == "utc_timestamp":
        raise ValueError("UTC_TIMESTAMP must be wrapped by FROM_UTC_TIMESTAMP(..., 'JST')")
    return None


def _replace_jst_current_timestamp(query: str) -> tuple[str, int]:
    output: list[str] = []
    replacements = 0
    index = 0
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if char == "-" and next_char == "-":
            end = query.find("\n", index)
            if end == -1:
                output.append(query[index:])
                break
            output.append(query[index:end])
            index = end
            continue
        if char == "/" and next_char == "*":
            end = query.find("*/", index + 2)
            if end == -1:
                raise ValueError("Unclosed block comment while rewriting JST timestamp")
            output.append(query[index : end + 2])
            index = end + 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            end = index + 1
            while end < len(query):
                if query[end] == "\\" and quote in {"'", '"'}:
                    end += 2
                    continue
                if query[end] == quote:
                    if end + 1 < len(query) and query[end + 1] == quote:
                        end += 2
                        continue
                    end += 1
                    break
                end += 1
            else:
                raise ValueError("Unclosed quote while rewriting JST timestamp")
            output.append(query[index:end])
            index = end
            continue
        match = JST_CURRENT_TIMESTAMP_PATTERN.match(query, index)
        if match:
            output.append("current_timestamp()")
            replacements += 1
            index = match.end()
            continue
        output.append(char)
        index += 1
    return "".join(output), replacements


def _rewrite_spark_functions(query: str) -> tuple[str, tuple[str, ...]]:
    query, jst_replacements = _replace_jst_current_timestamp(query)

    def rewrite(text: str) -> str:
        output: list[str] = []
        index = 0
        while index < len(text):
            char = text[index]
            next_char = text[index + 1] if index + 1 < len(text) else ""
            if char == "-" and next_char == "-":
                end = text.find("\n", index)
                if end == -1:
                    output.append(text[index:])
                    break
                output.append(text[index:end])
                index = end
                continue
            if char == "/" and next_char == "*":
                end = text.find("*/", index + 2)
                if end == -1:
                    raise ValueError("Unclosed block comment while rewriting functions")
                output.append(text[index : end + 2])
                index = end + 2
                continue
            if char in {"'", '"', "`"}:
                quote = char
                end = index + 1
                while end < len(text):
                    if text[end] == "\\" and quote in {"'", '"'}:
                        end += 2
                        continue
                    if text[end] == quote:
                        if end + 1 < len(text) and text[end + 1] == quote:
                            end += 2
                            continue
                        end += 1
                        break
                    end += 1
                else:
                    raise ValueError("Unclosed quote while rewriting functions")
                output.append(text[index:end])
                index = end
                continue
            if char.isalpha() or char == "_":
                name_end = index + 1
                while name_end < len(text) and (
                    text[name_end].isalnum() or text[name_end] == "_"
                ):
                    name_end += 1
                opening = name_end
                while opening < len(text) and text[opening].isspace():
                    opening += 1
                if opening < len(text) and text[opening] == "(":
                    closing = _matching_parenthesis(text, opening)
                    inner = rewrite(text[opening + 1 : closing])
                    arguments = _split_function_arguments(inner)
                    replacement = _spark_function_replacement(
                        text[index:name_end], arguments
                    )
                    if replacement is not None:
                        output.append(replacement)
                    else:
                        output.append(text[index : opening + 1])
                        output.append(inner)
                        output.append(")")
                    index = closing + 1
                    continue
            output.append(char)
            index += 1
        return "".join(output)

    requirements = ["Spark SQL 3.3+"]
    if jst_replacements:
        requirements.append("spark.sql.session.timeZone=Asia/Tokyo")
    return rewrite(query), tuple(requirements)


def _redirect_internal_references(
    query: str, generated_targets: set[str]
) -> str:
    def replace_reference(match: re.Match[str]) -> str:
        table = match.group("table").replace("`", "")
        if table.lower() in generated_targets:
            return f"gold.{table}"
        return match.group(0)

    return INTERNAL_REFERENCE_PATTERN.sub(replace_reference, query)


def _assign_dependencies(artifacts: list[Artifact]) -> list[Artifact]:
    targets = {artifact.target.lower() for artifact in artifacts}
    rewritten: dict[str, Artifact] = {}
    for artifact in artifacts:
        query = _normalize_double_quoted_literals(artifact.query)
        query = _normalize_single_quoted_aliases(query)
        query = _normalize_values_column_aliases(query)
        query, runtime_requirements = _rewrite_spark_functions(query)
        query = _quote_non_ascii_identifiers(query)
        query = _redirect_internal_references(query, targets)
        dependencies = sorted(
            {
                match.group("table").replace("`", "").lower()
                for match in GOLD_DEPENDENCY_PATTERN.finditer(query)
                if match.group("table").replace("`", "").lower()
                in targets - {artifact.target.lower()}
            }
        )
        rewritten[artifact.target.lower()] = replace(
            artifact,
            query=query,
            dependencies=tuple(dependencies),
            runtime_requirements=runtime_requirements,
        )

    unresolved = set(rewritten)
    levels: dict[str, int] = {}
    while unresolved:
        ready = sorted(
            target
            for target in unresolved
            if set(rewritten[target].dependencies) <= set(levels)
        )
        if not ready:
            cycle = {target: rewritten[target].dependencies for target in sorted(unresolved)}
            raise ValueError(f"Internal Gold dependency cycle detected: {cycle}")
        for target in ready:
            dependencies = rewritten[target].dependencies
            levels[target] = (
                0 if not dependencies else max(levels[item] for item in dependencies) + 1
            )
            unresolved.remove(target)

    return [
        replace(rewritten[artifact.target.lower()], dependency_level=levels[artifact.target.lower()])
        for artifact in artifacts
    ]


def _header(artifact: Artifact) -> str:
    dependencies = (
        ", ".join(f"gold.{item}" for item in artifact.dependencies)
        if artifact.dependencies
        else "none"
    )
    requirements = (
        ", ".join(artifact.runtime_requirements)
        if artifact.runtime_requirements
        else "none"
    )
    return (
        f"-- Source file: {artifact.source_path.as_posix()}\n"
        f"-- Dependency level: {artifact.dependency_level}\n"
        f"-- Internal Gold dependencies: {dependencies}\n"
        f"-- Runtime requirements: {requirements}\n"
    )


def _first_top_level_keyword(query: str) -> tuple[str, int]:
    quote: str | None = None
    line_comment = False
    block_comment = False
    depth = 0
    index = 0
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if line_comment:
            if char in "\r\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote:
            if char == "\\" and quote in {"'", '"'}:
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
            index += 1
            continue
        if char == ")":
            depth -= 1
            index += 1
            continue
        if depth == 0 and (char.isalpha() or char == "_"):
            end = index + 1
            while end < len(query) and (query[end].isalnum() or query[end] == "_"):
                end += 1
            keyword = query[index:end].upper()
            if keyword in {"WITH", "SELECT"}:
                return keyword, index
            index = end
            continue
        index += 1
    raise ValueError("No top-level WITH/SELECT keyword found")


def _main_select_position(query: str) -> int:
    first_keyword, first_position = _first_top_level_keyword(query)
    if first_keyword == "SELECT":
        return first_position

    quote: str | None = None
    line_comment = False
    block_comment = False
    depth = 0
    index = first_position + len("WITH")
    while index < len(query):
        char = query[index]
        next_char = query[index + 1] if index + 1 < len(query) else ""
        if line_comment:
            if char in "\r\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 2
            else:
                index += 1
            continue
        if quote:
            if char == "\\" and quote in {"'", '"'}:
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    index += 2
                    continue
                quote = None
            index += 1
            continue
        if char == "-" and next_char == "-":
            line_comment = True
            index += 2
            continue
        if char == "/" and next_char == "*":
            block_comment = True
            index += 2
            continue
        if char in {"'", '"', "`"}:
            quote = char
            index += 1
            continue
        if char == "(":
            depth += 1
            index += 1
            continue
        if char == ")":
            depth -= 1
            index += 1
            continue
        if depth == 0 and query[index : index + 6].upper() == "SELECT":
            before = query[index - 1] if index else " "
            after = query[index + 6] if index + 6 < len(query) else " "
            if not (before.isalnum() or before == "_") and not (
                after.isalnum() or after == "_"
            ):
                return index
        index += 1
    raise ValueError("No main SELECT found after WITH clause")


def render_insert_sql(artifact: Artifact) -> str:
    query = artifact.query.rstrip()
    first_keyword, _ = _first_top_level_keyword(query)
    insert_clause = f"INSERT OVERWRITE TABLE gold.{artifact.target}\n"
    if first_keyword == "WITH":
        position = _main_select_position(query)
        body = query[:position] + insert_clause + query[position:]
    else:
        body = insert_clause + query
    return _header(artifact) + "\n" + body.rstrip() + "\n;\n"


def render_ddl(artifact: Artifact) -> str:
    return (
        _header(artifact)
        + "\n"
        + f"CREATE TABLE IF NOT EXISTS gold.{artifact.target}\n"
        + "USING iceberg\n"
        + "TBLPROPERTIES (\n"
        + "    'write.format.default' = 'parquet'\n"
        + "    , 'write.parquet.compression-codec' = 'snappy'\n"
        + ")\n"
        + "AS\n"
        + artifact.query.rstrip()
        + "\nLIMIT 0;\n"
    )


def generate_artifacts(
    source_root: Path, ddl_output_dir: Path, sql_output_dir: Path
) -> dict[str, object]:
    artifacts = _assign_dependencies(discover_artifacts(source_root))
    expected = {artifact.filename_stem for artifact in artifacts}

    for output_dir, extension in ((ddl_output_dir, ".ddl"), (sql_output_dir, ".sql")):
        output_dir.mkdir(parents=True, exist_ok=True)
        existing = {path.stem.lower() for path in output_dir.glob(f"*{extension}")}
        stale = sorted(existing - expected)
        if stale:
            raise ValueError(f"Stale {extension} files exist: {stale}")

    for artifact in artifacts:
        ddl_path = ddl_output_dir / f"{artifact.filename_stem}.ddl"
        sql_path = sql_output_dir / f"{artifact.filename_stem}.sql"
        ddl_tmp = ddl_path.with_suffix(".ddl.tmp")
        sql_tmp = sql_path.with_suffix(".sql.tmp")
        ddl_tmp.write_text(render_ddl(artifact), encoding="utf-8")
        sql_tmp.write_text(render_insert_sql(artifact), encoding="utf-8")
        ddl_tmp.replace(ddl_path)
        sql_tmp.replace(sql_path)

    ddl_written = {path.stem.lower() for path in ddl_output_dir.glob("*.ddl")}
    sql_written = {path.stem.lower() for path in sql_output_dir.glob("*.sql")}
    if ddl_written != expected or sql_written != expected:
        raise ValueError("Generated DDL/SQL file sets do not match parsed targets")

    return {
        "source_sql_files": len(
            [
                path
                for path in source_root.rglob("*.sql")
                if not path.name.lower().endswith("_gold.sql")
            ]
        ),
        "targets": len(artifacts),
        "ddl_files": len(ddl_written),
        "sql_files": len(sql_written),
        "dependency_edges": sum(len(item.dependencies) for item in artifacts),
        "max_dependency_level": max(item.dependency_level for item in artifacts),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-dir", type=Path, required=True)
    parser.add_argument("--ddl-output-dir", type=Path, required=True)
    parser.add_argument("--sql-output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = generate_artifacts(
        args.source_dir, args.ddl_output_dir, args.sql_output_dir
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
