import tempfile
import unittest
from pathlib import Path

from tools.convert_ctas_ddl_to_iceberg import (
    convert_directory,
    parse_source_pair,
    render_iceberg_ddl,
)


class ConvertCtasDdlToIcebergTest(unittest.TestCase):
    def test_renders_explicit_iceberg_provider_and_properties(self) -> None:
        ddl = """CREATE TABLE IF NOT EXISTS gold.sample AS
SELECT source.id, ';' AS marker
FROM bronze.source
LIMIT 0;
"""
        insert = """INSERT OVERWRITE TABLE gold.sample
SELECT source.id, ';' AS marker
FROM bronze.source;
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_path = root / "sample.ddl"
            insert_path = root / "sample.sql"
            ddl_path.write_text(ddl, encoding="utf-8")
            insert_path.write_text(insert, encoding="utf-8")
            output = render_iceberg_ddl(parse_source_pair(ddl_path, insert_path))

        self.assertIn("CREATE TABLE IF NOT EXISTS gold.sample\n", output)
        self.assertIn("active Spark catalog supports Iceberg", output)
        self.assertIn("USING iceberg\n", output)
        self.assertIn("'write.format.default' = 'parquet'", output)
        self.assertIn("'write.parquet.compression-codec' = 'snappy'", output)
        self.assertIn("AS\nSELECT source.id", output)
        self.assertTrue(output.rstrip().endswith("LIMIT 0;"))
        self.assertNotIn("PARTITIONED BY", output)

    def test_preserves_cte_before_insert(self) -> None:
        ddl = """CREATE TABLE IF NOT EXISTS gold.sample AS
WITH source AS (
    SELECT 1 AS id
)
SELECT id FROM source
LIMIT 0;
"""
        insert = """WITH source AS (
    SELECT 1 AS id
)
INSERT OVERWRITE TABLE gold.sample
SELECT id FROM source;
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_path = root / "sample.ddl"
            insert_path = root / "sample.sql"
            ddl_path.write_text(ddl, encoding="utf-8")
            insert_path.write_text(insert, encoding="utf-8")
            pair = parse_source_pair(ddl_path, insert_path)

        self.assertTrue(pair.ddl_query.startswith("WITH source AS"))
        self.assertIn("SELECT id FROM source", pair.ddl_query)

    def test_rejects_query_mismatch(self) -> None:
        ddl = "CREATE TABLE IF NOT EXISTS gold.sample AS SELECT 1 AS id\nLIMIT 0;\n"
        insert = "INSERT OVERWRITE TABLE gold.sample\nSELECT 2 AS id;\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_path = root / "sample.ddl"
            insert_path = root / "sample.sql"
            ddl_path.write_text(ddl, encoding="utf-8")
            insert_path.write_text(insert, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "query mismatch"):
                parse_source_pair(ddl_path, insert_path)

    def test_conversion_is_idempotent_for_rendered_iceberg_ddl(self) -> None:
        ddl = """CREATE TABLE IF NOT EXISTS gold.sample AS
SELECT 1 AS id
LIMIT 0;
"""
        insert = """INSERT OVERWRITE TABLE gold.sample
SELECT 1 AS id;
"""
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_path = root / "sample.ddl"
            insert_path = root / "sample.sql"
            ddl_path.write_text(ddl, encoding="utf-8")
            insert_path.write_text(insert, encoding="utf-8")
            first = render_iceberg_ddl(parse_source_pair(ddl_path, insert_path))
            ddl_path.write_text(first, encoding="utf-8")
            second = render_iceberg_ddl(parse_source_pair(ddl_path, insert_path))

        self.assertEqual(first, second)

    def test_directory_conversion_rejects_missing_insert(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_dir = root / "ddl"
            sql_dir = root / "sql"
            output_dir = root / "output"
            ddl_dir.mkdir()
            sql_dir.mkdir()
            (ddl_dir / "sample.ddl").write_text(
                "CREATE TABLE IF NOT EXISTS gold.sample AS SELECT 1\nLIMIT 0;\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "file set mismatch"):
                convert_directory(ddl_dir, sql_dir, output_dir)

    def test_rejects_source_ddl_without_limit_zero(self) -> None:
        ddl = "CREATE TABLE IF NOT EXISTS gold.sample AS SELECT 1 AS id;\n"
        insert = "INSERT OVERWRITE TABLE gold.sample\nSELECT 1 AS id;\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_path = root / "sample.ddl"
            insert_path = root / "sample.sql"
            ddl_path.write_text(ddl, encoding="utf-8")
            insert_path.write_text(insert, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "must end with LIMIT 0"):
                parse_source_pair(ddl_path, insert_path)

    def test_directory_conversion_rejects_stale_output_ddl(self) -> None:
        ddl = "CREATE TABLE IF NOT EXISTS gold.sample AS SELECT 1 AS id\nLIMIT 0;\n"
        insert = "INSERT OVERWRITE TABLE gold.sample\nSELECT 1 AS id;\n"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_dir = root / "ddl"
            sql_dir = root / "sql"
            output_dir = root / "output"
            ddl_dir.mkdir()
            sql_dir.mkdir()
            output_dir.mkdir()
            (ddl_dir / "sample.ddl").write_text(ddl, encoding="utf-8")
            (sql_dir / "sample.sql").write_text(insert, encoding="utf-8")
            (output_dir / "stale.ddl").write_text("stale", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "Stale DDL files"):
                convert_directory(ddl_dir, sql_dir, output_dir)


if __name__ == "__main__":
    unittest.main()
