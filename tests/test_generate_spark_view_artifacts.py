import tempfile
import unittest
from pathlib import Path

from tools.generate_spark_view_artifacts import (
    _assign_dependencies,
    _normalize_double_quoted_literals,
    _normalize_single_quoted_aliases,
    _normalize_values_column_aliases,
    _quote_non_ascii_identifiers,
    _replace_jst_current_timestamp,
    _rewrite_spark_functions,
    parse_source_file,
    render_ddl,
    render_insert_sql,
)


class GenerateSparkViewArtifactsTest(unittest.TestCase):
    def _parse(self, source: str, name: str = "source.sql"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / name
            path.write_text(source, encoding="utf-8")
            return parse_source_file(path, root)

    def test_collapses_adjacent_create_and_alter_declarations(self) -> None:
        artifacts = self._parse(
            """-- CREATE VIEW dx_ve.Sample AS
-- ALTER VIEW dx_ve.Sample AS
SELECT 1 AS id;
"""
        )

        self.assertEqual(1, len(artifacts))
        self.assertEqual("Sample", artifacts[0].target)
        self.assertEqual("SELECT 1 AS id", artifacts[0].query)

    def test_parses_active_create_table_exception(self) -> None:
        artifacts = self._parse(
            """DROP TABLE IF EXISTS gold.sample;
CREATE TABLE gold.sample AS
SELECT 1 AS id;
"""
        )

        self.assertEqual("sample", artifacts[0].target)
        self.assertEqual("SELECT 1 AS id", artifacts[0].query)

    def test_preserves_semicolons_in_comments_and_literals(self) -> None:
        artifacts = self._parse(
            """-- ALTER VIEW dx_ve.sample AS
SELECT ';' AS marker -- comment;
;
"""
        )

        self.assertIn("SELECT ';' AS marker -- comment;", artifacts[0].query)

    def test_allows_redundant_standalone_terminators(self) -> None:
        artifacts = self._parse(
            """-- ALTER VIEW dx_ve.sample AS
SELECT 1 AS id; -- first terminator
;
"""
        )

        self.assertEqual("SELECT 1 AS id", artifacts[0].query)

    def test_redirects_internal_references_and_assigns_levels(self) -> None:
        artifacts = self._parse(
            """-- ALTER VIEW dx_ve.base AS
SELECT 1 AS id;
-- ALTER VIEW dx_ve.child AS
SELECT id FROM dx_ve.base;
"""
        )
        assigned = _assign_dependencies(artifacts)

        self.assertEqual(0, assigned[0].dependency_level)
        self.assertEqual(1, assigned[1].dependency_level)
        self.assertIn("FROM gold.base", assigned[1].query)

    def test_quotes_only_unquoted_non_ascii_identifiers(self) -> None:
        query = "SELECT value AS 日本語, `既存名`, '文字列', \"二重引用\" -- コメント日本語\nFROM source"

        quoted = _quote_non_ascii_identifiers(query)

        self.assertIn("AS `日本語`", quoted)
        self.assertIn("`既存名`", quoted)
        self.assertIn("'文字列'", quoted)
        self.assertIn("\"二重引用\"", quoted)
        self.assertIn("-- コメント日本語", quoted)

    def test_normalizes_single_quoted_aliases_only(self) -> None:
        query = "SELECT 'value AS ''text''' AS 'alias', value AS '日本語' -- AS 'comment'"

        normalized = _normalize_single_quoted_aliases(query)

        self.assertIn("'value AS ''text'''", normalized)
        self.assertIn("AS `alias`", normalized)
        self.assertIn("AS `日本語`", normalized)
        self.assertIn("-- AS 'comment'", normalized)

    def test_normalizes_double_quoted_string_literals_only(self) -> None:
        query = 'SELECT "先週", "O\'Brien" -- "comment"\n, \'"unchanged"\''

        normalized = _normalize_double_quoted_literals(query)

        self.assertEqual(
            "SELECT '先週', 'O''Brien' -- \"comment\"\n, '\"unchanged\"'",
            normalized,
        )

    def test_moves_values_column_alias_to_derived_table(self) -> None:
        query = "SELECT i FROM (VALUES((0 AS i),(1),(2))) dd"

        normalized = _normalize_values_column_aliases(query)

        self.assertEqual("SELECT i FROM (VALUES (0),(1),(2)) AS dd(i)", normalized)

    def test_rewrites_impala_functions_for_spark(self) -> None:
        query = """SELECT
FROM_TIMESTAMP(HOURS_ADD(CONCAT('1970-01-01 ', tm), 2), 'HH:mm:ss'),
DAYS_ADD(dd, 1), MINUTES_ADD(ts, 30), MONTHS_ADD(dd, 6), MONTHS_SUB(dd, 4),
GROUP_CONCAT(CONCAT(code, ',', name), ';'), GROUP_CONCAT(name),
ISNOTTRUE(status IN ('00', '01'))
NULLIFZERO(amount)
FROM source
WHERE dd = CAST(FROM_UTC_TIMESTAMP(UTC_TIMESTAMP(), 'JST') AS DATE)
"""

        rewritten, requirements = _rewrite_spark_functions(query)

        self.assertIn(
            "date_format((CAST(CONCAT('1970-01-01 ', tm) AS TIMESTAMP) + INTERVAL 2 HOURS), 'HH:mm:ss')",
            rewritten,
        )
        self.assertIn("date_add(dd, 1)", rewritten)
        self.assertIn("(ts + INTERVAL 30 MINUTES)", rewritten)
        self.assertIn("add_months(dd, 6)", rewritten)
        self.assertIn("add_months(dd, -(4))", rewritten)
        self.assertIn(
            "CASE WHEN count(CONCAT(code, ',', name)) = 0 THEN NULL "
            "ELSE concat_ws(';', collect_list(CONCAT(code, ',', name))) END",
            rewritten,
        )
        self.assertIn(
            "CASE WHEN count(name) = 0 THEN NULL "
            "ELSE concat_ws(', ', collect_list(name)) END",
            rewritten,
        )
        self.assertIn("(NOT coalesce(status IN ('00', '01'), false))", rewritten)
        self.assertIn("nullif(amount, 0)", rewritten)
        self.assertIn("CAST(current_timestamp() AS DATE)", rewritten)
        self.assertEqual(
            ("Spark SQL 3.3+", "spark.sql.session.timeZone=Asia/Tokyo"),
            requirements,
        )

    def test_does_not_rewrite_functions_in_literals_or_comments(self) -> None:
        query = "SELECT 'GROUP_CONCAT(x)', value -- MONTHS_SUB(dd, 1)"

        rewritten, requirements = _rewrite_spark_functions(query)

        self.assertEqual(query, rewritten)
        self.assertEqual(("Spark SQL 3.3+",), requirements)

    def test_rewrites_jst_current_timestamp_only_in_sql_code(self) -> None:
        expression = "FROM_UTC_TIMESTAMP(UTC_TIMESTAMP(), 'JST')"
        query = f"SELECT {expression}, '{expression}' -- {expression}"

        rewritten, count = _replace_jst_current_timestamp(query)

        self.assertEqual(1, count)
        self.assertEqual(
            f"SELECT current_timestamp(), '{expression}' -- {expression}",
            rewritten,
        )

    def test_renders_cte_before_insert(self) -> None:
        artifact = _assign_dependencies(
            self._parse(
                """-- ALTER VIEW dx_ve.sample AS
WITH source AS (SELECT 1 AS id)
SELECT id FROM source;
"""
            )
        )[0]
        sql = render_insert_sql(artifact)

        self.assertLess(sql.index("WITH source"), sql.index("INSERT OVERWRITE"))
        self.assertLess(sql.index("INSERT OVERWRITE"), sql.rindex("SELECT id"))

    def test_renders_iceberg_ddl_with_limit_zero(self) -> None:
        artifact = _assign_dependencies(
            self._parse("-- ALTER VIEW dx_ve.sample AS\nSELECT 1 AS id;\n")
        )[0]
        ddl = render_ddl(artifact)

        self.assertIn("CREATE TABLE IF NOT EXISTS gold.sample", ddl)
        self.assertIn("USING iceberg", ddl)
        self.assertIn("'write.format.default' = 'parquet'", ddl)
        self.assertTrue(ddl.rstrip().endswith("LIMIT 0;"))


if __name__ == "__main__":
    unittest.main()
