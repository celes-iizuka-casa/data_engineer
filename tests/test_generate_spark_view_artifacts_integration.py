import os
import re
import tempfile
import unittest
from pathlib import Path

from tools.generate_spark_view_artifacts import (
    _assign_dependencies,
    discover_artifacts,
    generate_artifacts,
)


SOURCE_DIR = os.environ.get("BLUE_CRYSTAL_VIEW_SOURCE_DIR")


@unittest.skipUnless(
    SOURCE_DIR,
    "Set BLUE_CRYSTAL_VIEW_SOURCE_DIR to run integration tests",
)
class GenerateSparkViewArtifactsIntegrationTest(unittest.TestCase):
    @staticmethod
    def _normalize_query(query: str) -> str:
        query = re.sub(r"\n[ \t]*\n+", "\n", query.strip())
        return "\n".join(line.lstrip() for line in query.splitlines())

    def test_generates_all_expected_spark_artifacts(self) -> None:
        expected = int(os.environ.get("BLUE_CRYSTAL_EXPECTED_TARGETS", "115"))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            ddl_dir = root / "ddl"
            sql_dir = root / "sql"
            result = generate_artifacts(Path(SOURCE_DIR), ddl_dir, sql_dir)
            parsed = _assign_dependencies(discover_artifacts(Path(SOURCE_DIR)))
            expected_queries = {
                artifact.filename_stem: artifact.query for artifact in parsed
            }
            ddl_files = sorted(ddl_dir.glob("*.ddl"))
            sql_files = sorted(sql_dir.glob("*.sql"))

            self.assertEqual(47, result["source_sql_files"])
            self.assertEqual(expected, result["targets"])
            self.assertEqual(expected, len(ddl_files))
            self.assertEqual(expected, len(sql_files))
            self.assertEqual(
                {path.stem for path in ddl_files},
                {path.stem for path in sql_files},
            )
            for ddl in ddl_files:
                text = ddl.read_text(encoding="utf-8")
                self.assertNotRegex(
                    text,
                    r"(?i)\b(?:days_add|from_timestamp|group_concat|hours_add|"
                    r"isnottrue|minutes_add|months_add|months_sub|nullifzero|"
                    r"utc_timestamp)\s*\(",
                )
                self.assertEqual(1, len(re.findall(r"(?im)^USING iceberg$", text)), ddl)
                self.assertRegex(text, r"(?is)LIMIT\s+0\s*;\s*$")
                self.assertNotRegex(text, r"(?im)^\s*(?:DROP|ALTER|INSERT)\b")
                query_match = re.search(
                    r"(?ms)^AS[ \t]*\r?\n(?P<query>.*)\r?\nLIMIT\s+0\s*;\s*$",
                    text,
                )
                self.assertIsNotNone(query_match, ddl)
                self.assertEqual(
                    self._normalize_query(expected_queries[ddl.stem]),
                    self._normalize_query(query_match.group("query")),
                    ddl,
                )
            for sql in sql_files:
                text = sql.read_text(encoding="utf-8")
                self.assertNotRegex(
                    text,
                    r"(?i)\b(?:days_add|from_timestamp|group_concat|hours_add|"
                    r"isnottrue|minutes_add|months_add|months_sub|nullifzero|"
                    r"utc_timestamp)\s*\(",
                )
                self.assertEqual(
                    1,
                    len(re.findall(r"(?im)^[ \t]*INSERT OVERWRITE TABLE gold\.", text)),
                    sql,
                )
                self.assertNotRegex(text, r"(?im)^\s*(?:DROP|CREATE|ALTER)\b")
                self.assertTrue(text.rstrip().endswith(";"), sql)
                body = text.split("\n\n", 1)[1]
                body = re.sub(
                    r"(?im)^[ \t]*INSERT OVERWRITE TABLE gold\.[A-Za-z0-9_]+[ \t]*\r?\n?",
                    "",
                    body,
                    count=1,
                )
                body = re.sub(r"(?:\r?\n)[ \t]*;[ \t]*\Z", "", body.rstrip())
                self.assertEqual(
                    self._normalize_query(expected_queries[sql.stem]),
                    self._normalize_query(body),
                    sql,
                )


if __name__ == "__main__":
    unittest.main()
