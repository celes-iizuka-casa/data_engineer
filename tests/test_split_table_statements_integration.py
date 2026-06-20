import os
import re
import tempfile
import unittest
from pathlib import Path

from tools.split_table_statements import (
    DDL_START,
    INSERT_START,
    _write_statements,
    split_statements,
)


DDL_SOURCE = os.environ.get("BLUE_CRYSTAL_DDL_SOURCE")
INSERT_SOURCE = os.environ.get("BLUE_CRYSTAL_INSERT_SOURCE")
SOURCE_MARKER = re.compile(
    r"^-- \[(?P<number>\d{3})/(?P<total>\d{3})\].*target=(?P<target>\S+)[ \t]*$",
    re.MULTILINE,
)
DDL_DECLARATION = re.compile(
    r"^[ \t]*CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+gold\.([A-Za-z0-9_]+)\s+AS\b",
    re.IGNORECASE | re.MULTILINE,
)
INSERT_DECLARATION = re.compile(
    r"^[ \t]*INSERT\s+OVERWRITE\s+TABLE\s+gold\.([A-Za-z0-9_]+)(?=\s|$)",
    re.IGNORECASE | re.MULTILINE,
)


@unittest.skipUnless(
    DDL_SOURCE and INSERT_SOURCE,
    "Set BLUE_CRYSTAL_DDL_SOURCE and BLUE_CRYSTAL_INSERT_SOURCE to run integration tests",
)
class BlueCrystalSplitIntegrationTest(unittest.TestCase):
    def test_real_sources_split_without_loss_or_duplicate(self) -> None:
        ddl_source = Path(DDL_SOURCE).read_text(encoding="utf-8")
        insert_source = Path(INSERT_SOURCE).read_text(encoding="utf-8")
        ddl_statements = split_statements(ddl_source, DDL_START)
        insert_statements = split_statements(insert_source, INSERT_START)
        expected_ddl = self._extract_source_blocks(ddl_source)
        expected_insert = self._extract_source_blocks(insert_source)
        expected_count = int(os.environ.get("BLUE_CRYSTAL_EXPECTED_COUNT", "99"))
        expected_cte_count = int(os.environ.get("BLUE_CRYSTAL_EXPECTED_CTE_COUNT", "15"))
        expected_unterminated = int(
            os.environ.get("BLUE_CRYSTAL_EXPECTED_UNTERMINATED_COUNT", "9")
        )

        self.assertEqual(expected_count, len(ddl_statements))
        self.assertEqual(expected_count, len(insert_statements))
        self.assertEqual(expected_count, len(expected_ddl))
        self.assertEqual(expected_count, len(expected_insert))
        self.assertEqual(
            [item.filename_stem for item in ddl_statements],
            [item.filename_stem for item in insert_statements],
        )
        self.assertEqual(
            expected_cte_count,
            sum(bool(re.match(r"WITH\b", item.sql.lstrip(), re.IGNORECASE)) for item in insert_statements),
        )
        self.assertEqual(
            expected_unterminated,
            sum(not item.terminated for item in insert_statements),
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_output = root / "ddl"
            insert_output = root / "sql"
            _write_statements(ddl_statements, ddl_output, ".ddl")
            _write_statements(insert_statements, insert_output, ".sql")

            ddl_files = sorted(ddl_output.glob("*.ddl"))
            insert_files = sorted(insert_output.glob("*.sql"))
            self.assertEqual(expected_count, len(ddl_files))
            self.assertEqual(expected_count, len(insert_files))
            self.assertEqual(
                {path.stem for path in ddl_files},
                {path.stem for path in insert_files},
            )
            self._assert_outputs(ddl_files, expected_ddl, DDL_DECLARATION, 0)
            self._assert_outputs(
                insert_files,
                expected_insert,
                INSERT_DECLARATION,
                expected_unterminated,
            )

    def _extract_source_blocks(self, source: str) -> dict[str, str]:
        markers = list(SOURCE_MARKER.finditer(source))
        blocks: dict[str, str] = {}
        for index, marker in enumerate(markers):
            block_end = markers[index + 1].start() if index + 1 < len(markers) else len(source)
            block = source[marker.end() : block_end]
            offset = 0
            for line in block.splitlines(keepends=True):
                if line.strip() and not line.lstrip().startswith("--"):
                    break
                offset += len(line)
            target = marker.group("target").replace("`", "").rsplit(".", 1)[-1]
            blocks[target.lower()] = block[offset:].strip() + "\n"
        return blocks

    def _assert_outputs(
        self,
        files: list[Path],
        expected_blocks: dict[str, str],
        declaration_pattern: re.Pattern[str],
        expected_normalized_count: int,
    ) -> None:
        normalized_count = 0
        for path in files:
            sql = path.read_text(encoding="utf-8")
            declarations = list(declaration_pattern.finditer(sql))
            self.assertEqual(1, len(declarations), path)
            target = declarations[0].group(1)
            self.assertEqual(path.stem, target.lower(), path)
            expected = expected_blocks[path.stem]
            if sql != expected:
                self.assertEqual(expected.rstrip() + "\n;\n", sql, path)
                normalized_count += 1
            self.assertTrue(sql.rstrip().endswith(";"), path)
        self.assertEqual(expected_normalized_count, normalized_count)
