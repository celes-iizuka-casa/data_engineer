import os
import re
import tempfile
import unittest
from pathlib import Path

from tools.convert_ctas_ddl_to_iceberg import convert_directory


DDL_SOURCE_DIR = os.environ.get("BLUE_CRYSTAL_DDL_DIR")
INSERT_SOURCE_DIR = os.environ.get("BLUE_CRYSTAL_INSERT_DIR")
QUERY_PATTERN = re.compile(
    r"CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+"
    r"(?:`?[^`.\s]+`?\.)?`?[^`\s]+`?.*?\bAS\b\s*(?P<query>.*)$",
    re.IGNORECASE | re.DOTALL,
)


@unittest.skipUnless(
    DDL_SOURCE_DIR and INSERT_SOURCE_DIR,
    "Set BLUE_CRYSTAL_DDL_DIR and BLUE_CRYSTAL_INSERT_DIR to run integration tests",
)
class ConvertCtasDdlToIcebergIntegrationTest(unittest.TestCase):
    def test_converts_all_real_ddl_files_to_iceberg(self) -> None:
        expected_count = int(os.environ.get("BLUE_CRYSTAL_EXPECTED_COUNT", "99"))
        with tempfile.TemporaryDirectory() as directory:
            output_dir = Path(directory) / "ddl"
            result = convert_directory(
                Path(DDL_SOURCE_DIR), Path(INSERT_SOURCE_DIR), output_dir
            )
            outputs = sorted(output_dir.glob("*.ddl"))
            source_files = {
                path.stem.lower(): path
                for path in Path(DDL_SOURCE_DIR).glob("*.ddl")
            }

            self.assertEqual(expected_count, result["ddl_files"])
            self.assertEqual(expected_count, len(outputs))
            self.assertEqual(0, result["partitioned_tables"])
            for output in outputs:
                sql = output.read_text(encoding="utf-8")
                source_sql = source_files[output.stem].read_text(encoding="utf-8")
                source_match = QUERY_PATTERN.search(source_sql)
                output_match = QUERY_PATTERN.search(sql)
                self.assertIsNotNone(source_match, output)
                self.assertIsNotNone(output_match, output)
                self.assertEqual(
                    source_match.group("query").strip(),
                    output_match.group("query").strip(),
                    output,
                )
                self.assertEqual(
                    1, len(re.findall(r"(?im)^USING[ \t]+iceberg[ \t]*$", sql)), output
                )
                self.assertEqual(1, sql.count("'write.format.default' = 'parquet'"), output)
                self.assertEqual(
                    1,
                    sql.count("'write.parquet.compression-codec' = 'snappy'"),
                    output,
                )
                self.assertNotRegex(sql, r"(?i)PARTITIONED\s+BY")
                self.assertRegex(sql, r"(?im)^AS[ \t]*$")
                self.assertRegex(sql, r"(?im)^[ \t]*(?:WITH|SELECT)\b")
                self.assertRegex(sql, r"(?is)LIMIT\s+0\s*;\s*$")
