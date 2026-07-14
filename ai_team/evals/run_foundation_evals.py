#!/usr/bin/env python3
"""Run deterministic foundation checks against a repository snapshot."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

import yaml


EXPECTED_ROLES = 19
EXPECTED_SKILLS = 29
EXPECTED_GOLDEN_CASES = 15
EXPECTED_CASE_IDS = {
    "GC-BACKEND-001", "GC-API-001", "GC-DBMIG-001", "GC-DATA-001",
    "GC-SQL-001", "GC-INFRA-001", "GC-IAC-001", "GC-SEC-001",
    "GC-INC-001", "GC-ARCH-001", "GC-PERF-001", "GC-LEGACY-001",
    "GC-RAG-001", "GC-DIST-001", "GC-DOC-001",
}


def load_yaml(root: Path, relative: str) -> dict:
    target = root / relative
    if not target.is_file():
        raise ValueError("missing")
    value = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root is not a mapping")
    return value


def load_json(root: Path, relative: str) -> dict:
    target = root / relative
    if not target.is_file():
        raise ValueError("missing")
    value = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("root is not an object")
    return value


def architecture(root: Path) -> None:
    data = load_yaml(root, "ai_team/governance/architecture_contract.yaml")
    execution = data.get("execution", {})
    if execution.get("binding") != "caller_runtime":
        raise ValueError("caller runtime binding is absent")
    for key in (
        "runtime_switching", "cross_provider_invocation", "provider_fallback",
        "dynamic_provider_switching",
    ):
        if execution.get(key) != "forbidden":
            raise ValueError(f"execution prohibition is absent: {key}")
    if not data.get("identity", {}).get("provider_neutral"):
        raise ValueError("provider-neutral identity is absent")
    if data.get("knowledge_priority", [])[:3] != [
        "current_explicit_request", "current_evidence", "user_local_second_brain"
    ]:
        raise ValueError("knowledge priority is invalid")


def canonical(root: Path) -> None:
    data = load_yaml(root, "ai_team/governance/canonical_sources.yaml")
    required = {
        "agent_definitions", "skill_metadata", "skill_instructions",
        "skill_documentation", "skill_ui_adapters", "workflows", "policies",
        "governance", "review_contracts", "fde_contracts", "evals",
        "execution_evidence_contracts", "shared_tests", "templates",
        "documentation", "runtime_adapters", "claude_adapter", "generated_files",
        "manual_edits",
    }
    if not required <= set(data.get("ownership", {})):
        raise ValueError("canonical ownership areas are incomplete")
    if data["ownership"]["generated_files"].get("mode") != "none_current":
        raise ValueError("generated file ownership is ambiguous")
    legacy = data.get("legacy_generators", [])
    if len(legacy) < 2 or any(item.get("status") != "deprecated_local_only" for item in legacy):
        raise ValueError("legacy generator ownership is unresolved")


def capabilities(root: Path) -> None:
    data = load_yaml(root, "ai_team/capability_registry.yaml")
    roles = data.get("roles", [])
    if len(roles) != EXPECTED_ROLES:
        raise ValueError(f"expected {EXPECTED_ROLES} roles")
    required = {
        "ownership", "capabilities", "decision_rights", "escalation_conditions",
        "supported_task_types", "unsuitable_task_types", "handoff_rules_ref",
        "done_definition_ref",
    }
    if any(required - set(role) for role in roles):
        raise ValueError("a role lacks required capability fields")


def skill_lifecycle(root: Path) -> None:
    data = load_yaml(root, "ai_team/governance/skill_lifecycle_registry.yaml")
    if len(data.get("skills", [])) != EXPECTED_SKILLS:
        raise ValueError(f"expected {EXPECTED_SKILLS} skills")
    if "UNKNOWN" not in data.get("dispositions", []):
        raise ValueError("insufficient evidence outcome is absent")
    for entry in data.get("skills", []):
        if entry.get("state") not in set(data.get("lifecycle_states", [])):
            raise ValueError(f"invalid Skill state: {entry.get('id')}")
        if entry.get("candidate_state") not in set(data.get("lifecycle_states", [])):
            raise ValueError(f"invalid Skill candidate state: {entry.get('id')}")
        revision = entry.get("candidate_revision", "")
        if not isinstance(revision, str) or not revision.startswith("sha256:"):
            raise ValueError(f"Skill revision is absent: {entry.get('id')}")
    promoted = [
        entry
        for entry in data.get("skills", [])
        if entry.get("candidate_state") == "ACTIVE"
    ]
    if promoted:
        decision = data.get("human_gate_decision", {})
        if (
            not isinstance(decision, dict)
            or decision.get("decision") != "PROMOTE"
            or decision.get("decided_by") != "Celes"
        ):
            raise ValueError("promoted Skills lack Celes Human Gate evidence")
        for entry in promoted:
            if entry.get("active_revision") != entry.get("candidate_revision"):
                raise ValueError(f"promoted revision mismatch: {entry.get('id')}")


def evidence_schema(root: Path) -> None:
    data = load_json(root, "ai_team/evidence/execution_evidence.schema.json")
    required = set(data.get("required", []))
    if not {"execution_context", "skills", "second_brain", "improvement_signals"} <= required:
        raise ValueError("execution evidence schema is incomplete")
    choices = data.get("$defs", {}).get("evidenceType", {}).get("enum", [])
    if "unavailable" not in choices or "inferred" not in choices:
        raise ValueError("evidence types are incomplete")
    if len(data.get("$defs", {}).get("contextString", {}).get("oneOf", [])) != 2:
        raise ValueError("null/unavailable Evidence consistency is absent")


def growth_and_human_gate(root: Path) -> None:
    growth = load_yaml(root, "ai_team/governance/capability_growth_policy.yaml")
    if growth.get("authority") != "celes_environment_only":
        raise ValueError("single authority is absent")
    if growth.get("separation_of_duties", {}).get("improver_may_self_approve") is not False:
        raise ValueError("improver/evaluator separation is absent")
    gate = load_json(root, "ai_team/governance/human_gate.schema.json")
    if gate.get("properties", {}).get("decided_by", {}).get("const") != "Celes":
        raise ValueError("Celes human gate is absent")
    if set(gate.get("properties", {}).get("decision_type", {}).get("enum", [])) != {
        "canonical_promotion", "critical_operation"
    }:
        raise ValueError("human gate decision types are incomplete")


def quality_gates(root: Path) -> None:
    data = load_yaml(root, "ai_team/review/risk_based_quality_gates.yaml")
    if set(data.get("levels", {})) != {"low", "medium", "high", "critical"}:
        raise ValueError("risk levels are incomplete")
    if data["levels"]["critical"].get("human_gate") != "required":
        raise ValueError("critical human gate is absent")


def evals(root: Path) -> None:
    load_yaml(root, "ai_team/evals/eval_catalog.yaml")
    golden = load_yaml(root, "ai_team/evals/golden_cases.yaml")
    cases = golden.get("cases", [])
    if len(cases) != EXPECTED_GOLDEN_CASES:
        raise ValueError(f"expected {EXPECTED_GOLDEN_CASES} golden cases")
    ids = {case.get("id") for case in cases if isinstance(case, dict)}
    if ids != EXPECTED_CASE_IDS:
        raise ValueError("golden case scenario set is incomplete")
    gates = load_yaml(root, "ai_team/review/risk_based_quality_gates.yaml")
    levels = gates.get("levels", {})
    known_gates = {
        gate
        for contract in levels.values()
        for gate in contract.get("gates", [])
    }
    for case in cases:
        risk = case.get("risk")
        if risk not in levels:
            raise ValueError(f"{case.get('id')} has unknown risk")
        required = set(case.get("required_gates", []))
        missing = set(levels[risk].get("gates", [])) - required
        unknown = required - known_gates
        if missing or unknown:
            raise ValueError(
                f"{case.get('id')} gate mismatch: missing={sorted(missing)}, "
                f"unknown={sorted(unknown)}"
            )
        for field in (
            "expected_roles", "expected_skills", "required_evidence",
            "prohibited_actions", "artifact_assertions",
        ):
            if not isinstance(case.get(field), list) or not case[field]:
                raise ValueError(f"{case.get('id')} has no {field}")


def case_result_failures(case: dict, result: dict) -> list[str]:
    checks = {
        "expected_roles": set(case["expected_roles"]) == set(result.get("selected_roles", [])),
        "expected_skills": set(case["expected_skills"]) == set(result.get("selected_skills", [])),
        "required_gates": set(case["required_gates"]) <= set(result.get("executed_gates", [])),
        "required_evidence": set(case["required_evidence"]) <= set(result.get("evidence", [])),
        "artifact_assertions": set(case["artifact_assertions"]) <= set(result.get("artifacts", [])),
        "prohibited_actions": not (
            set(case["prohibited_actions"]) & set(result.get("actions", []))
        ),
    }
    return sorted(name for name, passed in checks.items() if not passed)


def representative_case_results(root: Path) -> None:
    """Execute deterministic contract assertions over representative result fixtures."""
    golden = load_yaml(root, "ai_team/evals/golden_cases.yaml")
    fixtures = load_yaml(root, "ai_team/evals/case_fixtures.yaml")
    cases = {case["id"]: case for case in golden.get("cases", [])}
    results = fixtures.get("results", [])
    represented_risks = set()
    if len(results) < 3:
        raise ValueError("at least three representative result fixtures are required")
    for result in results:
        case_id = result.get("case_id")
        if case_id not in cases:
            raise ValueError(f"unknown fixture case: {case_id}")
        case = cases[case_id]
        represented_risks.add(case["risk"])
        failed = case_result_failures(case, result)
        if failed:
            raise ValueError(f"{case_id} result fixture failed: {failed}")
    if not {"low", "high", "critical"} <= represented_risks:
        raise ValueError("representative fixtures must cover low, high, and critical risk")


def documentation(root: Path) -> None:
    data = load_yaml(root, "ai_team/governance/documentation_quality_policy.yaml")
    if "canonical_source_mismatch" not in data.get("level_2_semantic", {}).get("review_dimensions", []):
        raise ValueError("documentation semantic review is incomplete")


def runtime_contract(root: Path) -> None:
    text = (root / "ai_team/runtime_selection_policy.md").read_text(encoding="utf-8")
    for required in ("呼び出し元Runtime", "Recommendation ≠ Enforcement", "Cross-provider"):
        if required not in text:
            raise ValueError(f"missing runtime contract text: {required}")


def second_brain(root: Path) -> None:
    text = (root / "ai_team/personalization_policy.md").read_text(encoding="utf-8")
    for required in ("Current Explicit Request", "Current Evidence", "User-local Second Brain", "Second Brainが存在しない"):
        if required not in text:
            raise ValueError(f"missing local context contract text: {required}")


def privacy(root: Path) -> None:
    ignore = (root / ".gitignore").read_text(encoding="utf-8")
    for required in ("/.local/", "/evidence/", "/secrets/", "/temp/"):
        if required not in ignore:
            raise ValueError(f"missing ignore boundary: {required}")
    profile = load_yaml(root, "profiles/current_user_profile.yaml")
    if profile.get("profile_kind") != "shared_default":
        raise ValueError("tracked profile is not an anonymous shared default")


def validator_enforcement(root: Path) -> None:
    text = (root / "tools/validate_repository.py").read_text(encoding="utf-8")
    for required in ("validate_git_privacy", "validate_capability_foundation", "validate_documentation_quality"):
        if required not in text:
            raise ValueError(f"validator enforcement is absent: {required}")


CHECKS: list[tuple[str, Callable[[Path], None]]] = [
    ("architecture_contract", architecture),
    ("canonical_ownership", canonical),
    ("capability_registry", capabilities),
    ("skill_lifecycle", skill_lifecycle),
    ("execution_evidence", evidence_schema),
    ("growth_and_human_gate", growth_and_human_gate),
    ("risk_quality_gates", quality_gates),
    ("eval_architecture", evals),
    ("representative_case_results", representative_case_results),
    ("documentation_quality", documentation),
    ("runtime_dependency", runtime_contract),
    ("local_second_brain", second_brain),
    ("privacy_boundary", privacy),
    ("validator_enforcement", validator_enforcement),
]


def run(root: Path) -> dict:
    results = []
    for name, check in CHECKS:
        try:
            check(root)
        except (OSError, ValueError, KeyError, json.JSONDecodeError, yaml.YAMLError) as exc:
            results.append({"id": name, "status": "FAIL", "detail": str(exc)})
        else:
            results.append({"id": name, "status": "PASS", "detail": None})
    passed = sum(item["status"] == "PASS" for item in results)
    return {
        "schema_version": "1.0",
        "root": str(root.resolve()),
        "passed": passed,
        "total": len(results),
        "verdict": "PASS" if passed == len(results) else "FAIL",
        "results": results,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    result = run(args.root)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
