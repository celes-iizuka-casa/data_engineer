#!/usr/bin/env python3
"""Split generated Gold DDL and INSERT scripts into one file per table."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Pattern


DDL_START = re.compile(
    r"^[ \t]*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+"
    r"(?P<target>(?:`?[^`.\s]+`?\.)?`?[^`\s]+`?)\s+AS\b",
    re.IGNORECASE | re.MULTILINE,
)
INSERT_START = re.compile(
    r"^[ \t]*INSERT\s+OVERWRITE\s+TABLE\s+"
    r"(?P<target>(?:`?[^`.\s]+`?\.)?`?[^`\s]+`?)(?=\s|$)",
    re.IGNORECASE | re.MULTILINE,
)
BLOCK_MARKER = re.compile(
    r"^-- \[(?P<number>\d{3})/(?P<total>\d{3})\].*\btarget=(?P<target>\S+)[ \t]*$",
    re.MULTILINE,
)


@dataclass(frozen=True)
class Statement:
    target: str
    filename_stem: str
    sql: str
    terminated: bool


def _filename_stem(target: str) -> str:
    table_name = target.replace("`", "").rsplit(".", 1)[-1]
    if not re.fullmatch(r"[A-Za-z0-9_]+", table_name):
        raise ValueError(f"Unsupported table name for output filename: {target}")
    return table_name.lower()


def _statement_end(text: str, start: int, limit: int) -> int | None:
    quote: str | None = None
    line_comment = False
    block_comment = False
    index = start

    while index < limit:
        char = text[index]
        next_char = text[index + 1] if index + 1 < limit else ""

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
            return index + 1
        index += 1

    if quote:
        raise ValueError(f"Unclosed {quote} quote near offset {start}")
    if block_comment:
        raise ValueError(f"Unclosed block comment near offset {start}")
    return None


def _sql_start_after_metadata(block: str) -> int:
    offset = 0
    for line in block.splitlines(keepends=True):
        stripped = line.strip()
        if stripped and not line.lstrip().startswith("--"):
            return offset
        offset += len(line)
    raise ValueError("Generated block contains no SQL")


def _split_marker_blocks(
    text: str, start_pattern: Pattern[str], markers: list[re.Match[str]]
) -> list[Statement]:
    statements: list[Statement] = []
    seen_stems: set[str] = set()
    expected_total = int(markers[0].group("total"))
    if expected_total != len(markers):
        raise ValueError(
            f"Marker count mismatch: header={expected_total}, actual={len(markers)}"
        )

    for position, marker in enumerate(markers):
        expected_number = position + 1
        actual_number = int(marker.group("number"))
        if actual_number != expected_number:
            raise ValueError(
                f"Marker sequence mismatch: expected={expected_number}, actual={actual_number}"
            )

        block_end = markers[position + 1].start() if position + 1 < len(markers) else len(text)
        block = text[marker.end() : block_end]
        declaration = start_pattern.search(block)
        if declaration is None:
            raise ValueError(f"No target declaration in marker block {actual_number}")

        marker_target = marker.group("target").replace("`", "")
        declared_target = declaration.group("target").replace("`", "")
        if marker_target.lower() != declared_target.lower():
            raise ValueError(
                f"Marker/declaration target mismatch: {marker_target} != {declared_target}"
            )

        stem = _filename_stem(marker_target)
        if stem in seen_stems:
            raise ValueError(f"Duplicate output filename after normalization: {stem}")
        seen_stems.add(stem)

        sql_start = _sql_start_after_metadata(block)
        sql = block[sql_start:].strip() + "\n"
        end = _statement_end(sql, 0, len(sql))
        statements.append(
            Statement(
                target=marker_target,
                filename_stem=stem,
                sql=sql,
                terminated=end is not None,
            )
        )
    return statements


def split_statements(text: str, start_pattern: Pattern[str]) -> list[Statement]:
    markers = list(BLOCK_MARKER.finditer(text))
    if markers:
        return _split_marker_blocks(text, start_pattern, markers)

    matches = list(start_pattern.finditer(text))
    if not matches:
        raise ValueError("No target statements found")

    statements: list[Statement] = []
    seen_stems: set[str] = set()
    for position, match in enumerate(matches):
        limit = matches[position + 1].start() if position + 1 < len(matches) else len(text)
        end = _statement_end(text, match.start(), limit)
        if end is None and position + 1 < len(matches):
            target = match.group("target")
            raise ValueError(f"Statement is not terminated before the next target: {target}")

        target = match.group("target").replace("`", "")
        stem = _filename_stem(target)
        if stem in seen_stems:
            raise ValueError(f"Duplicate output filename after normalization: {stem}")
        seen_stems.add(stem)

        statement_end = end if end is not None else limit
        sql = text[match.start() : statement_end].strip() + "\n"
        statements.append(
            Statement(
                target=target,
                filename_stem=stem,
                sql=sql,
                terminated=end is not None,
            )
        )
    return statements


def _write_statements(
    statements: list[Statement], output_dir: Path, extension: str
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for statement in statements:
        destination = output_dir / f"{statement.filename_stem}{extension}"
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        sql = statement.sql
        if not statement.terminated:
            sql = sql.rstrip() + "\n;\n"
        temporary.write_text(sql, encoding="utf-8")
        temporary.replace(destination)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ddl-source", type=Path, required=True)
    parser.add_argument("--insert-source", type=Path, required=True)
    parser.add_argument("--ddl-output-dir", type=Path, required=True)
    parser.add_argument("--insert-output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    ddl_statements = split_statements(
        args.ddl_source.read_text(encoding="utf-8"), DDL_START
    )
    insert_statements = split_statements(
        args.insert_source.read_text(encoding="utf-8"), INSERT_START
    )

    ddl_stems = [statement.filename_stem for statement in ddl_statements]
    insert_stems = [statement.filename_stem for statement in insert_statements]
    if ddl_stems != insert_stems:
        raise ValueError("DDL and INSERT target order does not match")

    _write_statements(ddl_statements, args.ddl_output_dir, ".ddl")
    _write_statements(insert_statements, args.insert_output_dir, ".sql")

    print(
        json.dumps(
            {
                "ddl_files": len(ddl_statements),
                "insert_files": len(insert_statements),
                "ddl_unterminated": [
                    statement.target
                    for statement in ddl_statements
                    if not statement.terminated
                ],
                "insert_unterminated": [
                    statement.target
                    for statement in insert_statements
                    if not statement.terminated
                ],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
