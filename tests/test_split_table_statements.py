import tempfile
import unittest
from pathlib import Path

from tools.split_table_statements import (
    DDL_START,
    INSERT_START,
    _write_statements,
    split_statements,
)


class SplitTableStatementsTest(unittest.TestCase):
    def test_ddl_ignores_semicolons_in_literals_and_comments(self) -> None:
        source = """CREATE TABLE IF NOT EXISTS gold.First AS
SELECT ';' AS value /* ; */ -- ;
LIMIT 0;
-- metadata for the next table
CREATE TABLE IF NOT EXISTS gold.SECOND AS
SELECT 2
LIMIT 0;
"""

        statements = split_statements(source, DDL_START)

        self.assertEqual(["first", "second"], [item.filename_stem for item in statements])
        self.assertTrue(all(item.terminated for item in statements))
        self.assertNotIn("metadata", statements[0].sql)

    def test_insert_accepts_unterminated_final_statement(self) -> None:
        source = """INSERT OVERWRITE TABLE gold.first
SELECT 1;
INSERT OVERWRITE TABLE gold.second
SELECT 2
-- disabled predicate;
"""

        statements = split_statements(source, INSERT_START)

        self.assertEqual(2, len(statements))
        self.assertTrue(statements[0].terminated)
        self.assertFalse(statements[1].terminated)
        self.assertIn("-- disabled predicate;", statements[1].sql)

    def test_marker_block_preserves_cte_before_insert(self) -> None:
        source = """-- generated file
-- [001/001] level=0 target=gold.Sample
-- Gold dependencies: none
-- Source file: sample.sql

WITH source AS (
    SELECT 1 AS id
)
INSERT OVERWRITE TABLE gold.Sample
SELECT id FROM source -- terminator is commented out;
"""

        statements = split_statements(source, INSERT_START)

        self.assertEqual(1, len(statements))
        self.assertTrue(statements[0].sql.startswith("WITH source AS"))
        self.assertIn("INSERT OVERWRITE TABLE gold.Sample", statements[0].sql)
        self.assertFalse(statements[0].terminated)

    def test_rejects_unterminated_non_final_statement(self) -> None:
        source = """INSERT OVERWRITE TABLE gold.first
SELECT 1
INSERT OVERWRITE TABLE gold.second
SELECT 2;
"""

        with self.assertRaisesRegex(ValueError, "not terminated"):
            split_statements(source, INSERT_START)

    def test_rejects_case_insensitive_filename_collision(self) -> None:
        source = """CREATE TABLE IF NOT EXISTS gold.TableA AS SELECT 1;
CREATE TABLE IF NOT EXISTS gold.tablea AS SELECT 2;
"""

        with self.assertRaisesRegex(ValueError, "Duplicate output filename"):
            split_statements(source, DDL_START)

    def test_writer_adds_real_terminator_to_unterminated_statement(self) -> None:
        source = """INSERT OVERWRITE TABLE gold.sample
SELECT 1 -- source terminator is commented out;
"""
        statements = split_statements(source, INSERT_START)

        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory)
            _write_statements(statements, output_dir, ".sql")
            output = (output_dir / "sample.sql").read_text(encoding="utf-8")

        self.assertTrue(output.endswith("\n;\n"))


if __name__ == "__main__":
    unittest.main()
