#!/usr/bin/env python3
"""Validate a local-private documentation semantic review record."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

import yaml


REQUIRED_FIELDS = {
    "schema_version",
    "review_id",
    "timestamp",
    "reviewer",
    "independent",
    "trigger",
    "changed_paths",
    "review_targets",
    "dimensions",
    "findings",
    "verdict",
    "unknowns",
}
FINDING_FIELDS = {
    "id", "severity", "target", "dimension", "finding", "evidence",
    "required_action",
}
DIMENSIONS = {
    "accuracy", "completeness", "freshness", "contradiction", "duplication",
    "discoverability", "ai_readability", "human_readability",
    "implementation_alignment", "maintainability",
    "canonical_source_mismatch", "stale_path", "broken_link",
    "role_skill_mismatch", "stale_model_recommendation",
    "responsibility_clarity", "fragmentation",
    "cross_document_consistency",
}
TRIGGERS = {
    "changed_policy_or_workflow", "deterministic_drift_signal",
    "high_risk_change", "independent_reviewer_request",
}
VERDICTS = {
    "PASS", "PASS_WITH_NON_BLOCKING_FINDINGS", "REWORK_REQUIRED", "BLOCKED",
    "UNKNOWN",
}


def valid_timestamp(value: object) -> bool:
    """Require a real RFC-3339 timestamp with an explicit timezone."""
    if not isinstance(value, str) or not re.fullmatch(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:\d{2})",
        value,
    ):
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def record_failures(record: object) -> list[str]:
    """Return deterministic contract failures for one semantic review record."""
    if not isinstance(record, dict):
        return ["record_not_mapping"]
    failures: list[str] = []
    if set(record) != REQUIRED_FIELDS:
        failures.append("top_level_fields")
    if record.get("schema_version") != "1.0":
        failures.append("schema_version")
    if not isinstance(record.get("review_id"), str) or not record.get("review_id"):
        failures.append("review_id")
    if not isinstance(record.get("reviewer"), str) or not record.get("reviewer"):
        failures.append("reviewer")
    if record.get("independent") is not True:
        failures.append("independence")
    if record.get("trigger") not in TRIGGERS:
        failures.append("trigger")
    if not valid_timestamp(record.get("timestamp")):
        failures.append("timestamp")
    for field in ("changed_paths", "review_targets", "dimensions"):
        value = record.get(field)
        if (
            not isinstance(value, list)
            or not value
            or any(not isinstance(item, str) or not item for item in value)
        ):
            failures.append(field)
        elif len(value) != len(set(value)):
            failures.append(field)
    raw_dimensions = record.get("dimensions")
    dimensions = (
        set(raw_dimensions)
        if isinstance(raw_dimensions, list)
        and all(isinstance(item, str) for item in raw_dimensions)
        else set()
    )
    if not dimensions <= DIMENSIONS:
        failures.append("unknown_dimension")
    findings = record.get("findings")
    if not isinstance(findings, list):
        failures.append("findings")
        findings = []
    severities: list[str] = []
    for finding in findings:
        if not isinstance(finding, dict) or set(finding) != FINDING_FIELDS:
            failures.append("finding_fields")
            continue
        severity = finding.get("severity")
        severities.append(str(severity))
        if severity not in {"P0", "P1", "P2", "P3"}:
            failures.append("finding_severity")
        if finding.get("dimension") not in DIMENSIONS:
            failures.append("finding_dimension")
        for field in FINDING_FIELDS - {"severity"}:
            if not isinstance(finding.get(field), str) or not finding.get(field):
                failures.append(f"finding_{field}")
    unknowns = record.get("unknowns")
    if not isinstance(unknowns, list) or any(
        not isinstance(item, str) or not item for item in unknowns
    ):
        failures.append("unknowns")
        unknowns = []
    verdict = record.get("verdict")
    if verdict not in VERDICTS:
        failures.append("verdict")
    if {"P0", "P1"} & set(severities) and verdict not in {
        "REWORK_REQUIRED", "BLOCKED",
    }:
        failures.append("blocking_finding_verdict")
    if verdict == "PASS" and (findings or unknowns):
        failures.append("pass_with_findings_or_unknowns")
    if verdict == "PASS_WITH_NON_BLOCKING_FINDINGS" and (
        not findings or not set(severities) <= {"P2", "P3"}
    ):
        failures.append("non_blocking_verdict_mismatch")
    if verdict == "UNKNOWN" and not unknowns:
        failures.append("unknown_verdict_without_unknowns")
    return sorted(set(failures))


def load_record(path: Path) -> object:
    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("record", type=Path)
    args = parser.parse_args()
    try:
        record = load_record(args.record)
        failures = record_failures(record)
    except (OSError, ValueError, json.JSONDecodeError, yaml.YAMLError) as exc:
        failures = [f"load_error:{exc}"]
    result = {
        "record": str(args.record),
        "verdict": "PASS" if not failures else "FAIL",
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
