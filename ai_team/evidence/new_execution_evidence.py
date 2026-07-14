#!/usr/bin/env python3
"""Create local-private execution evidence without guessing unavailable values."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE_TYPES = ("observed", "declared", "structural", "inferred", "unavailable")
SKILL_REVISION_FILES = ("skill.yaml", "SKILL.md", "agents/openai.yaml")
EVIDENCE_TOP_LEVEL_KEYS = {
    "schema_version", "task", "execution_context", "agents", "skills",
    "second_brain", "result", "quality", "tests", "human_feedback",
    "improvement_signals",
}


def skill_revision(skill_id: str, root: Path = ROOT) -> str | None:
    """Return a reproducible digest for the canonical Skill surfaces."""
    base = root / "skills" / skill_id
    targets = [base / relative for relative in SKILL_REVISION_FILES]
    if not all(target.is_file() for target in targets):
        return None
    digest = hashlib.sha256()
    for relative, target in zip(SKILL_REVISION_FILES, targets):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(target.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def shared_candidate_revision(root: Path = ROOT) -> str:
    """Hash all tracked and untracked non-ignored shared working-tree content."""
    result = subprocess.run(
        [
            "git", "-C", str(root), "ls-files", "--cached", "--others",
            "--exclude-standard", "-z",
        ],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ValueError(detail or "cannot enumerate shared candidate files")
    paths = sorted(
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    )
    digest = hashlib.sha256()
    for relative in paths:
        target = root / relative
        digest.update(relative.encode("utf-8", errors="surrogateescape"))
        digest.update(b"\0")
        if target.is_symlink():
            digest.update(b"symlink\0")
            digest.update(os.readlink(target).encode("utf-8", errors="surrogateescape"))
        elif target.is_file():
            executable = bool(target.stat().st_mode & 0o111)
            digest.update(b"executable\0" if executable else b"file\0")
            digest.update(target.read_bytes())
        else:
            digest.update(b"deleted\0")
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def context_value(value: Any, evidence_type: str) -> dict[str, Any]:
    if evidence_type not in EVIDENCE_TYPES:
        raise ValueError(f"unsupported evidence type: {evidence_type}")
    if value is None and evidence_type != "unavailable":
        raise ValueError("null values must use evidence_type=unavailable")
    if value is not None and evidence_type == "unavailable":
        raise ValueError("available values must identify their evidence type")
    return {"value": value, "evidence_type": evidence_type}


def validate_evidence_document(document: dict[str, Any]) -> list[str]:
    """Validate the executable invariants also expressed by the JSON Schema."""
    errors: list[str] = []
    if set(document) != EVIDENCE_TOP_LEVEL_KEYS:
        errors.append("top-level keys do not match the execution evidence contract")
    if document.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")

    task = document.get("task")
    expected_task = {"id", "timestamp", "task_type", "request_mode"}
    if not isinstance(task, dict) or set(task) != expected_task:
        errors.append("task fields are incomplete")
    else:
        for field in ("id", "timestamp", "task_type", "request_mode"):
            if not isinstance(task[field], str) or not task[field].strip():
                errors.append(f"task.{field} must be a non-empty string")
        timestamp = str(task["timestamp"])
        if not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?"
            r"(?:Z|[+-]\d{2}:\d{2})",
            timestamp,
        ):
            errors.append("task.timestamp must be RFC-3339 with timezone")
        else:
            try:
                datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            except ValueError:
                errors.append("task.timestamp must be a valid RFC-3339 date-time")

    context = document.get("execution_context")
    expected_context = {"runtime", "provider", "model", "effort", "token_usage", "cost"}
    if not isinstance(context, dict) or set(context) != expected_context:
        errors.append("execution_context fields are incomplete")
    else:
        for field, entry in context.items():
            if not isinstance(entry, dict) or set(entry) != {"value", "evidence_type"}:
                errors.append(f"execution_context.{field} is malformed")
                continue
            value = entry["value"]
            evidence_type = entry["evidence_type"]
            try:
                context_value(value, evidence_type)
            except ValueError as exc:
                errors.append(f"execution_context.{field}: {exc}")
                continue
            if field in {"token_usage", "cost"}:
                if value is not None and (
                    isinstance(value, bool) or not isinstance(value, (int, float))
                ):
                    errors.append(f"execution_context.{field}.value must be numeric")
                elif value is not None and value < 0:
                    errors.append(
                        f"execution_context.{field}.value must be non-negative"
                    )
            elif value is not None and not isinstance(value, str):
                errors.append(f"execution_context.{field}.value must be a string")
            elif isinstance(value, str) and not value.strip():
                errors.append(f"execution_context.{field}.value must not be empty")

    skills = document.get("skills")
    if not isinstance(skills, list):
        errors.append("skills must be a list")
    else:
        if not skills:
            errors.append("skills must contain at least one Skill")
        skill_ids: list[str] = []
        for entry in skills:
            if not isinstance(entry, dict) or set(entry) != {"id", "revision"}:
                errors.append("every Skill must contain exactly id and revision")
                continue
            skill_id = entry["id"]
            revision = entry["revision"]
            if not isinstance(skill_id, str) or not skill_id.strip():
                errors.append("every Skill must have a non-empty id")
            else:
                skill_ids.append(skill_id)
            if not isinstance(revision, str) or not re.fullmatch(
                r"sha256:[0-9a-f]{64}", revision
            ):
                errors.append("every Skill must have a sha256 revision")
        if len(skill_ids) != len(set(skill_ids)):
            errors.append("Skill ids must be unique")

    agents = document.get("agents")
    if not isinstance(agents, list):
        errors.append("agents must be a list")
    else:
        if not agents:
            errors.append("agents must contain at least one Agent")
        agent_ids: list[str] = []
        for entry in agents:
            if (
                not isinstance(entry, dict)
                or set(entry) != {"id", "role"}
                or any(not isinstance(entry[key], str) or not entry[key].strip() for key in ("id", "role"))
            ):
                errors.append("every Agent must have non-empty id and role")
            else:
                agent_ids.append(entry["id"])
        if len(agent_ids) != len(set(agent_ids)):
            errors.append("Agent ids must be unique")

    second_brain = document.get("second_brain")
    if not isinstance(second_brain, dict) or set(second_brain) != {"available", "used", "source_scope"}:
        errors.append("second_brain fields are incomplete")
    else:
        available = second_brain["available"]
        used = second_brain["used"]
        source_scope = second_brain["source_scope"]
        if (
            available is not None and not isinstance(available, bool)
            or used is not None and not isinstance(used, bool)
            or not isinstance(source_scope, (str, type(None)))
            or isinstance(source_scope, str) and not source_scope.strip()
        ):
            errors.append("second_brain values are invalid")
        elif used is True and (available is not True or source_scope is None):
            errors.append(
                "second_brain.used=true requires available=true and source_scope"
            )
        elif used is None and (available is not None or source_scope is not None):
            errors.append(
                "second_brain.used=null requires unavailable context values"
            )

    result = document.get("result")
    if not isinstance(result, dict) or set(result) != {"status", "verdict"}:
        errors.append("result fields are incomplete")
    else:
        if not isinstance(result["status"], str) or not result["status"].strip():
            errors.append("result.status must be a non-empty string")
        if not isinstance(result["verdict"], (str, type(None))) or (
            isinstance(result["verdict"], str) and not result["verdict"].strip()
        ):
            errors.append("result.verdict must be a non-empty string or null")

    quality = document.get("quality")
    if not isinstance(quality, dict) or set(quality) != {"reviewer", "findings", "score"}:
        errors.append("quality fields are incomplete")
    else:
        reviewer = quality["reviewer"]
        findings = quality["findings"]
        score = quality["score"]
        if not isinstance(reviewer, (str, type(None))) or (
            isinstance(reviewer, str) and not reviewer.strip()
        ):
            errors.append("quality.reviewer must be a non-empty string or null")
        if not isinstance(findings, list) or not all(
            isinstance(item, str) and item.strip() for item in findings
        ):
            errors.append("quality.findings must contain non-empty strings")
        if score is not None and (
            isinstance(score, bool)
            or not isinstance(score, (int, float))
            or not 0 <= score <= 4
        ):
            errors.append("quality.score must be null or a number from 0 to 4")

    tests = document.get("tests")
    if not isinstance(tests, dict) or set(tests) != {"executed", "passed", "evidence"}:
        errors.append("tests fields are incomplete")
    else:
        if not isinstance(tests["executed"], list) or not all(
            isinstance(item, str) and item.strip() for item in tests["executed"]
        ):
            errors.append("tests.executed must contain non-empty strings")
        if not isinstance(tests["evidence"], list) or not all(
            isinstance(item, str) and item.strip() for item in tests["evidence"]
        ):
            errors.append("tests.evidence must contain non-empty strings")
        if tests["passed"] is not None and not isinstance(tests["passed"], bool):
            errors.append("tests.passed must be boolean or null")

    human_feedback = document.get("human_feedback")
    if not isinstance(human_feedback, dict) or set(human_feedback) != {"present"}:
        errors.append("human_feedback fields are incomplete")
    elif not isinstance(human_feedback["present"], bool):
        errors.append("human_feedback.present must be boolean")

    signals = document.get("improvement_signals")
    signal_fields = {"strengths", "weaknesses", "repeated_mistake_candidates"}
    if not isinstance(signals, dict) or set(signals) != signal_fields:
        errors.append("improvement_signals fields are incomplete")
    elif any(
        not isinstance(signals[field], list)
        or not all(isinstance(item, str) and item.strip() for item in signals[field])
        for field in signal_fields
    ):
        errors.append("improvement_signals values are invalid")
    return errors


def private_output_path(path: Path, root: Path = ROOT) -> Path:
    """Reject raw evidence written into shareable repository paths."""
    resolved = path.expanduser().resolve()
    repository = root.resolve()
    try:
        relative = resolved.relative_to(repository)
    except ValueError:
        raise ValueError("raw evidence output must stay inside this repository")
    allowed = (
        bool(relative.parts)
        and (
            relative.parts[0] == "output"
            or relative.parts[:2] == (".local", "evidence")
        )
    )
    if not allowed:
        raise ValueError("raw evidence must be under .local/evidence/ or output/")
    return resolved


def write_private_evidence(target: Path, document: dict[str, Any]) -> None:
    """Create a mode-0600 evidence file without following or overwriting a target."""
    target.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(target, flags, 0o600)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            yaml.safe_dump(document, stream, allow_unicode=True, sort_keys=False)
    except BaseException:
        try:
            target.unlink()
        except OSError:
            pass
        raise


def build_evidence(args: argparse.Namespace, root: Path = ROOT) -> dict[str, Any]:
    skill_entries = []
    for skill_id in args.skill:
        revision = skill_revision(skill_id, root)
        if revision is None:
            raise ValueError(f"unknown or incomplete skill: {skill_id}")
        skill_entries.append({"id": skill_id, "revision": revision})

    return {
        "schema_version": "1.0",
        "task": {
            "id": args.task_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "task_type": args.task_type,
            "request_mode": args.request_mode,
        },
        "execution_context": {
            "runtime": context_value(args.runtime, args.runtime_evidence),
            "provider": context_value(args.provider, args.provider_evidence),
            "model": context_value(args.model, args.model_evidence),
            "effort": context_value(args.effort, args.effort_evidence),
            "token_usage": context_value(args.token_usage, args.token_usage_evidence),
            "cost": context_value(args.cost, args.cost_evidence),
        },
        "agents": [{"id": role, "role": role} for role in args.agent],
        "skills": skill_entries,
        "second_brain": {
            "available": None,
            "used": None,
            "source_scope": None,
        },
        "result": {"status": args.result_status, "verdict": None},
        "quality": {"reviewer": None, "findings": [], "score": None},
        "tests": {"executed": [], "passed": None, "evidence": []},
        "human_feedback": {"present": False},
        "improvement_signals": {
            "strengths": [],
            "weaknesses": [],
            "repeated_mistake_candidates": [],
        },
    }


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(
        description="Create local-private AI team execution evidence"
    )
    value.add_argument("--task-id", required=True)
    value.add_argument("--task-type", required=True)
    value.add_argument("--request-mode", required=True)
    value.add_argument("--output", required=True, type=Path)
    value.add_argument("--agent", action="append", default=[])
    value.add_argument("--skill", action="append", default=[])
    value.add_argument("--result-status", default="in_progress")
    for field in ("runtime", "provider", "model", "effort"):
        value.add_argument(f"--{field}")
        value.add_argument(
            f"--{field}-evidence",
            choices=EVIDENCE_TYPES,
            default="unavailable",
        )
    value.add_argument("--token-usage", type=float)
    value.add_argument(
        "--token-usage-evidence", choices=EVIDENCE_TYPES, default="unavailable"
    )
    value.add_argument("--cost", type=float)
    value.add_argument(
        "--cost-evidence", choices=EVIDENCE_TYPES, default="unavailable"
    )
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        target = private_output_path(args.output)
        evidence = build_evidence(args)
        evidence_errors = validate_evidence_document(evidence)
        if evidence_errors:
            raise ValueError("; ".join(evidence_errors))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    try:
        write_private_evidence(target, evidence)
    except FileExistsError as exc:
        raise SystemExit(f"refusing to overwrite existing evidence: {target}") from exc
    print(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
