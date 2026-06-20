#!/usr/bin/env python3
"""Convert split Spark CTAS DDL files into explicit Iceberg CTAS DDL files."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


CTAS_PATTERN = re.compile(
    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+"
    r"(?P<target>(?:`?[^`.\s]+`?\.)?`?[^`\s]+`?)"
    r"(?P<options>.*?)\bAS\b\s*(?P<query>.*)$",
    re.IGNORECASE | re.DOTALL,
)
INSERT_PATTERN = re.compile(
    r"^[ \t]*INSERT\s+OVERWRITE\s+TABLE\s+"
    r"(?P<target>(?:`?[^`.\s]+`?\.)?`?[^`\s]+`?)(?=\s|$)[ \t]*(?:\r?\n)?",
    re.IGNORECASE | re.MULTILINE,
)
LIMIT_ZERO_PATTERN = re.compile(
    r"(?:\r?\n)[ \t]*LIMIT[ \t]+0[ \t]*;[ \t]*\Z", re.IGNORECASE
)


@dataclass(frozen=True)
class SourcePair:
    filename_stem: str
    target: str
    ddl_query: str
    insert_query: str


def _table_name(target: str) -> str:
    return target.replace("`", "").rsplit(".", 1)[-1]


def _strip_insert_terminator(sql: str) -> str:
    stripped = sql.rstrip()
    stripped = re.sub(r"(?:\r?\n)[ \t]*;[ \t]*\Z", "", stripped)
    stripped = stripped.rstrip()
    if stripped.endswith(";"):
        stripped = stripped[:-1].rstrip()
    return stripped


def _normalize_query(sql: str) -> str:
    sql = sql.replace("\r\n", "\n").strip()
    sql = re.sub(r"\n[ \t]*\n+", "\n", sql)
    return "\n".join(line.lstrip() for line in sql.splitlines())


def parse_source_pair(ddl_path: Path, insert_path: Path) -> SourcePair:
    ddl = ddl_path.read_text(encoding="utf-8")
    insert = insert_path.read_text(encoding="utf-8")
    ddl_match = CTAS_PATTERN.search(ddl)
    if ddl_match is None:
        raise ValueError(f"Unsupported source DDL structure: {ddl_path}")
    options = ddl_match.group("options").strip()
    if options and not re.search(r"(?im)^USING[ \t]+iceberg[ \t]*$", options):
        raise ValueError(f"Existing DDL is not an Iceberg CTAS: {ddl_path}")
    insert_match = INSERT_PATTERN.search(insert)
    if insert_match is None:
        raise ValueError(f"INSERT OVERWRITE declaration not found: {insert_path}")

    ddl_target = ddl_match.group("target").replace("`", "")
    insert_target = insert_match.group("target").replace("`", "")
    if ddl_target.lower() != insert_target.lower():
        raise ValueError(
            f"DDL/INSERT target mismatch: {ddl_target} != {insert_target}"
        )

    stem = ddl_path.stem.lower()
    if _table_name(ddl_target).lower() != stem or insert_path.stem.lower() != stem:
        raise ValueError(f"Filename/target mismatch: {ddl_path.name}, {ddl_target}")

    ddl_query_with_limit = ddl_match.group("query").rstrip()
    if LIMIT_ZERO_PATTERN.search(ddl_query_with_limit) is None:
        raise ValueError(f"Source DDL must end with LIMIT 0;: {ddl_path}")
    ddl_query = LIMIT_ZERO_PATTERN.sub("", ddl_query_with_limit).strip()
    insert_without_declaration = (
        insert[: insert_match.start()] + insert[insert_match.end() :]
    )
    insert_query = _strip_insert_terminator(insert_without_declaration).strip()
    if _normalize_query(ddl_query) != _normalize_query(insert_query):
        raise ValueError(f"DDL/INSERT query mismatch: {stem}")

    return SourcePair(
        filename_stem=stem,
        target=ddl_target,
        ddl_query=ddl_match.group("query").strip(),
        insert_query=insert_query,
    )


def render_iceberg_ddl(source: SourcePair) -> str:
    return (
        "-- Spark 3 Iceberg CTAS. The SELECT is limited to zero rows to create only the schema.\n"
        "-- IMPORTANT: IF NOT EXISTS does not convert an existing non-Iceberg table.\n\n"
        "-- Assumption: the active Spark catalog supports Iceberg and resolves the gold schema.\n\n"
        f"CREATE TABLE IF NOT EXISTS {source.target}\n"
        "USING iceberg\n"
        "TBLPROPERTIES (\n"
        "    'write.format.default' = 'parquet'\n"
        "    , 'write.parquet.compression-codec' = 'snappy'\n"
        ")\n"
        "AS\n"
        f"{source.ddl_query.rstrip()}\n"
    )


def convert_directory(
    ddl_source_dir: Path, insert_source_dir: Path, output_dir: Path
) -> dict[str, object]:
    ddl_paths = sorted(ddl_source_dir.glob("*.ddl"), key=lambda path: path.name.lower())
    if not ddl_paths:
        raise ValueError(f"No DDL files found: {ddl_source_dir}")

    insert_paths = {path.stem.lower(): path for path in insert_source_dir.glob("*.sql")}
    ddl_stems = {path.stem.lower() for path in ddl_paths}
    if ddl_stems != set(insert_paths):
        missing_sql = sorted(ddl_stems - set(insert_paths))
        extra_sql = sorted(set(insert_paths) - ddl_stems)
        raise ValueError(
            f"DDL/INSERT file set mismatch: missing_sql={missing_sql}, extra_sql={extra_sql}"
        )

    pairs = [
        parse_source_pair(path, insert_paths[path.stem.lower()]) for path in ddl_paths
    ]
    output_dir.mkdir(parents=True, exist_ok=True)
    existing_stems = {path.stem.lower() for path in output_dir.glob("*.ddl")}
    stale_stems = sorted(existing_stems - ddl_stems)
    if stale_stems:
        raise ValueError(f"Stale DDL files exist in output directory: {stale_stems}")
    for pair in pairs:
        destination = output_dir / f"{pair.filename_stem}.ddl"
        temporary = destination.with_suffix(".ddl.tmp")
        temporary.write_text(render_iceberg_ddl(pair), encoding="utf-8")
        temporary.replace(destination)

    written_stems = {path.stem.lower() for path in output_dir.glob("*.ddl")}
    if written_stems != ddl_stems:
        raise ValueError("Generated DDL file set does not match source DDL file set")

    return {
        "ddl_files": len(pairs),
        "iceberg_provider": "iceberg",
        "partitioned_tables": 0,
        "source_query_matches": len(pairs),
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ddl-source-dir", type=Path, required=True)
    parser.add_argument("--insert-source-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    result = convert_directory(
        args.ddl_source_dir, args.insert_source_dir, args.output_dir
    )
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
