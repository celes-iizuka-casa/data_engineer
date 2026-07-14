#!/usr/bin/env python3
"""Run deterministic foundation checks against a repository snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Callable

import yaml


EXPECTED_ROLES = 19
EXPECTED_SKILLS = 29
MINIMUM_GOLDEN_CASES = 22
EXPECTED_CASE_IDS = {
    "GC-BACKEND-001", "GC-API-001", "GC-DBMIG-001", "GC-DATA-001",
    "GC-SQL-001", "GC-INFRA-001", "GC-IAC-001", "GC-SEC-001",
    "GC-INC-001", "GC-ARCH-001", "GC-PERF-001", "GC-LEGACY-001",
    "GC-RAG-001", "GC-DIST-001", "GC-DOC-001", "GC-FRONTEND-001",
    "GC-FULLSTACK-001", "GC-ML-001", "GC-AGENT-001", "GC-DQ-001",
    "GC-FDE-001", "GC-KNOWLEDGE-001",
}
FOUNDATION_CONTRACT_FILES = (
    "ai_team/evals/run_foundation_evals.py",
    "ai_team/evals/eval_catalog.yaml",
    "ai_team/evals/golden_cases.yaml",
    "ai_team/evals/case_fixtures.yaml",
    "ai_team/evals/agent_skill_fixtures.yaml",
    "ai_team/evals/skill_eval_bindings.yaml",
    "ai_team/evals/documentation_semantic_review.schema.json",
    "ai_team/evals/select_documentation_review_targets.py",
    "ai_team/evals/validate_documentation_semantic_review.py",
    "ai_team/governance/documentation_quality_policy.yaml",
    "ai_team/review/risk_based_quality_gates.yaml",
)

DOCUMENTATION_REVIEW_DIMENSIONS = {
    "accuracy", "completeness", "freshness", "stale_path", "contradiction",
    "duplication", "canonical_source_mismatch", "broken_link",
    "role_skill_mismatch", "stale_model_recommendation",
    "responsibility_clarity", "fragmentation",
    "cross_document_consistency", "discoverability", "ai_readability",
    "human_readability", "implementation_alignment", "maintainability",
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


def foundation_contract_revision(root: Path) -> str:
    """Hash every executable Foundation acceptance-contract surface."""
    digest = hashlib.sha256()
    for relative in FOUNDATION_CONTRACT_FILES:
        target = root / relative
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        if target.is_file():
            digest.update(target.read_bytes())
        else:
            digest.update(b"<missing>")
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


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
        "manual_edits", "ai_employee_lifecycle",
    }
    if not required <= set(data.get("ownership", {})):
        raise ValueError("canonical ownership areas are incomplete")
    if data["ownership"]["generated_files"].get("mode") != "none_current":
        raise ValueError("generated file ownership is ambiguous")
    contract = data.get("ownership_contract", {})
    overlays = {
        area
        for area, value in data.get("ownership", {}).items()
        if isinstance(value, dict) and value.get("ownership_authority") is False
    }
    if (
        contract.get("authoritative_match") != "exactly_one"
        or set(contract.get("non_owning_overlays", [])) != overlays
    ):
        raise ValueError("exactly-one canonical ownership is absent")
    legacy = data.get("legacy_generators", [])
    if len(legacy) < 2 or any(item.get("status") != "deprecated_local_only" for item in legacy):
        raise ValueError("legacy generator ownership is unresolved")


def capabilities(root: Path) -> None:
    data = load_yaml(root, "ai_team/capability_registry.yaml")
    roles = data.get("roles", [])
    if len(roles) < EXPECTED_ROLES:
        raise ValueError(f"expected at least {EXPECTED_ROLES} roles")
    if len({role.get("id") for role in roles}) != len(roles):
        raise ValueError("duplicate Role IDs")
    required = {
        "ownership", "capabilities", "decision_rights", "escalation_conditions",
        "supported_task_types", "unsuitable_task_types", "handoff_rules_ref",
        "done_definition_ref",
    }
    if any(required - set(role) for role in roles):
        raise ValueError("a role lacks required capability fields")


def ai_employee_lifecycle(root: Path) -> None:
    capabilities_data = load_yaml(root, "ai_team/capability_registry.yaml")
    data = load_yaml(
        root, "ai_team/governance/ai_employee_lifecycle_registry.yaml"
    )
    role_ids = {role.get("id") for role in capabilities_data.get("roles", [])}
    entries = data.get("roles", [])
    if {entry.get("id") for entry in entries} != role_ids:
        raise ValueError("AI Employee lifecycle does not cover every Role")
    if set(data.get("dispositions", [])) != {
        "CREATE", "KEEP", "UPDATE", "MERGE", "SPLIT", "DEPRECATE",
        "UNKNOWN",
    }:
        raise ValueError("AI Employee disposition set is incomplete")
    if "INDEPENDENTLY_REVIEWED" not in data.get("lifecycle_states", []):
        raise ValueError("AI Employee independent review state is absent")
    states = set(data.get("lifecycle_states", []))
    dispositions = set(data.get("dispositions", []))
    if not isinstance(data.get("decision_history"), list):
        raise ValueError("AI Employee decision history is absent")
    for entry in entries:
        role_id = entry.get("id")
        if entry.get("state") not in states:
            raise ValueError(f"invalid Role state: {role_id}")
        if entry.get("disposition") not in dispositions:
            raise ValueError(f"invalid Role disposition: {role_id}")
        if entry.get("effectiveness") not in {
            "not_evaluated", "baseline_pending", "evaluated",
        }:
            raise ValueError(f"invalid Role effectiveness: {role_id}")
        if "score" in entry:
            raise ValueError(f"Role effectiveness score lacks evidence: {role_id}")
        active_revision = entry.get("active_revision")
        if active_revision is not None and (
            not isinstance(active_revision, str)
            or not active_revision.startswith("sha256:")
        ):
            raise ValueError(f"Role active revision is invalid: {role_id}")
        candidate_revision = entry.get("candidate_revision")
        candidate_state = entry.get("candidate_state")
        if (candidate_revision is None) != (candidate_state is None):
            raise ValueError(f"Role candidate revision/state mismatch: {role_id}")
        if candidate_revision is not None:
            if candidate_state not in states:
                raise ValueError(f"invalid Role candidate state: {role_id}")
            if not isinstance(entry.get("transition"), dict):
                raise ValueError(f"Role candidate transition is absent: {role_id}")
            if entry.get("disposition") == "KEEP":
                raise ValueError(f"Role candidate cannot be KEEP: {role_id}")
        elif entry.get("transition") not in (None, {}):
            raise ValueError(f"Role transition exists without candidate: {role_id}")


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
        decision = data.get("last_promotion_decision", {})
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
    if len(cases) < MINIMUM_GOLDEN_CASES:
        raise ValueError(f"expected at least {MINIMUM_GOLDEN_CASES} golden cases")
    ids = {case.get("id") for case in cases if isinstance(case, dict)}
    if not EXPECTED_CASE_IDS <= ids:
        raise ValueError("golden case scenario set is incomplete")
    capability = load_yaml(root, "ai_team/capability_registry.yaml")
    expected_roles = {role.get("id") for role in capability.get("roles", [])}
    primary_skill_by_role = {
        role.get("id"): role.get("primary_skill")
        for role in capability.get("roles", [])
        if isinstance(role, dict)
    }
    covered_roles = {
        role
        for case in cases
        for role in case.get("expected_roles", [])
    }
    if covered_roles != expected_roles:
        raise ValueError(
            "golden cases do not cover all Roles: "
            f"missing={sorted(expected_roles - covered_roles)}"
        )
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
        missing_primary_skills = {
            primary_skill_by_role.get(role)
            for role in case.get("expected_roles", [])
        } - set(case.get("expected_skills", []))
        missing_primary_skills.discard(None)
        if missing_primary_skills:
            raise ValueError(
                f"{case.get('id')} omits primary Role Skills: "
                f"{sorted(missing_primary_skills)}"
            )


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


def agent_result_failures(result: dict) -> list[str]:
    expected = result.get("expected", {})
    actual = result.get("actual", {})
    checks = {
        "primary_role": expected.get("primary_role") == actual.get("primary_role"),
        "supporting_roles": set(expected.get("supporting_roles", []))
        == set(actual.get("supporting_roles", [])),
        "required_capabilities": set(expected.get("required_capabilities", []))
        <= set(actual.get("applied_capabilities", [])),
        "reviewers": set(expected.get("reviewers", []))
        == set(actual.get("reviewers", [])),
        "required_evidence": set(expected.get("required_evidence", []))
        <= set(actual.get("evidence", [])),
        "required_handoffs": set(expected.get("required_handoffs", []))
        <= set(actual.get("handoffs", [])),
        "done_evidence": set(expected.get("done_evidence", []))
        <= set(actual.get("done_evidence", [])),
        "escalation": expected.get("escalation") == actual.get("escalation"),
        "prohibited_actions": not (
            set(expected.get("prohibited_actions", []))
            & set(actual.get("actions", []))
        ),
        "unsupported_claims": not actual.get("unsupported_claims", []),
    }
    return sorted(name for name, passed in checks.items() if not passed)


def skill_result_failures(result: dict) -> list[str]:
    expected = result.get("expected", {})
    actual = result.get("actual", {})
    selected = set(actual.get("selected_skills", []))
    context_files_loaded = actual.get("context_files_loaded")
    max_context_files = expected.get("max_context_files")
    checks = {
        "selected_skills": set(expected.get("selected_skills", [])) == selected,
        "not_selected_skills": not (
            set(expected.get("not_selected_skills", [])) & selected
        ),
        "loaded_skills": selected == set(actual.get("loaded_skills", [])),
        "required_outputs": set(expected.get("required_outputs", []))
        <= set(actual.get("outputs", [])),
        "improvement_evidence": set(expected.get("improvement_evidence", []))
        <= set(actual.get("improvement_evidence", [])),
        "context_efficiency": type(context_files_loaded) is int
        and context_files_loaded >= 0
        and type(max_context_files) is int
        and max_context_files >= 0
        and context_files_loaded <= max_context_files,
        "instruction_adherence": not actual.get("instruction_violations", []),
        "overlap_and_conflict": not actual.get("conflicts", []),
        "prohibited_actions": not (
            set(expected.get("prohibited_actions", []))
            & set(actual.get("actions", []))
        ),
    }
    return sorted(name for name, passed in checks.items() if not passed)


def skill_binding_failures(
    entry: dict,
    selected_by_case: dict[str, set[str]],
    required_rubric: set[str],
) -> list[str]:
    """Return binding failures, including false positive/negative selection."""
    skill = entry.get("skill")
    positive_case = entry.get("positive_case")
    negative_case = entry.get("negative_case")
    failures: list[str] = []
    if positive_case not in selected_by_case:
        failures.append("unknown_positive_case")
    elif skill not in selected_by_case[positive_case]:
        failures.append("positive_case_does_not_select_skill")
    if negative_case not in selected_by_case:
        failures.append("unknown_negative_case")
    elif skill in selected_by_case[negative_case]:
        failures.append("negative_case_selects_skill")
    if positive_case == negative_case:
        failures.append("same_positive_and_negative_case")
    if set(entry.get("rubric", [])) != required_rubric:
        failures.append("rubric_mismatch")
    if not entry.get("conflict_group"):
        failures.append("missing_conflict_group")
    return sorted(failures)


def agent_skill_results(root: Path) -> None:
    data = load_yaml(root, "ai_team/evals/agent_skill_fixtures.yaml")
    agent_required = set(data.get("agent_contract", {}).get("required_dimensions", []))
    skill_required = set(data.get("skill_contract", {}).get("required_dimensions", []))
    agent_results = data.get("agent_results", [])
    skill_results = data.get("skill_results", [])
    agent_covered = {
        dimension for result in agent_results for dimension in result.get("dimensions", [])
    }
    skill_covered = {
        dimension for result in skill_results for dimension in result.get("dimensions", [])
    }
    if agent_covered != agent_required:
        raise ValueError("Agent Eval dimension coverage is incomplete")
    if skill_covered != skill_required:
        raise ValueError("Skill Eval dimension coverage is incomplete")
    for result in agent_results:
        failed = agent_result_failures(result)
        if failed:
            raise ValueError(f"{result.get('fixture_id')} Agent fixture failed: {failed}")
    for result in skill_results:
        failed = skill_result_failures(result)
        if failed:
            raise ValueError(f"{result.get('fixture_id')} Skill fixture failed: {failed}")

    bindings = load_yaml(root, "ai_team/evals/skill_eval_bindings.yaml")
    lifecycle = load_yaml(root, "ai_team/governance/skill_lifecycle_registry.yaml")
    expected_skills = {entry.get("id") for entry in lifecycle.get("skills", [])}
    binding_entries = bindings.get("bindings", [])
    if {entry.get("skill") for entry in binding_entries} != expected_skills:
        raise ValueError("Skill Eval bindings do not cover every Skill")
    golden_cases = load_yaml(
        root, "ai_team/evals/golden_cases.yaml"
    ).get("cases", [])
    selected_by_case = {
        case.get("id"): set(case.get("expected_skills", []))
        for case in golden_cases
        if isinstance(case, dict)
    }
    selected_by_case.update(
        {
            result.get("fixture_id"): set(
                result.get("expected", {}).get("selected_skills", [])
            )
            for result in skill_results
            if isinstance(result, dict)
        }
    )
    required_rubric = set(bindings.get("required_rubric", []))
    if required_rubric != skill_required:
        raise ValueError("Skill binding rubric differs from Skill Eval contract")
    for entry in binding_entries:
        failed = skill_binding_failures(
            entry, selected_by_case, required_rubric
        )
        if failed:
            raise ValueError(
                f"invalid Skill binding {entry.get('skill')}: {failed}"
            )


def documentation(root: Path) -> None:
    data = load_yaml(root, "ai_team/governance/documentation_quality_policy.yaml")
    semantic = data.get("level_2_semantic", {})
    policy_dimensions = set(semantic.get("review_dimensions", []))
    if policy_dimensions != DOCUMENTATION_REVIEW_DIMENSIONS:
        raise ValueError("documentation semantic review dimensions are incomplete")
    selector = semantic.get("target_selector")
    schema_path = semantic.get("review_record_schema")
    validator_path = semantic.get("review_record_validator")
    if not selector or not (root / selector).is_file():
        raise ValueError("documentation semantic target selector is absent")
    if not schema_path:
        raise ValueError("documentation semantic review schema is absent")
    if not validator_path or not (root / validator_path).is_file():
        raise ValueError("documentation semantic review validator is absent")
    schema = load_json(root, schema_path)
    if schema.get("additionalProperties") is not False:
        raise ValueError("documentation semantic review schema is not strict")
    if len(schema.get("allOf", [])) < 4:
        raise ValueError("documentation semantic verdict constraints are absent")
    schema_dimensions = set(
        schema.get("properties", {})
        .get("dimensions", {})
        .get("items", {})
        .get("enum", [])
    )
    finding_dimensions = set(
        schema.get("properties", {})
        .get("findings", {})
        .get("items", {})
        .get("properties", {})
        .get("dimension", {})
        .get("enum", [])
    )
    catalog_dimensions = set(
        load_yaml(root, "ai_team/evals/eval_catalog.yaml")
        .get("suites", {})
        .get("documentation", {})
        .get("dimensions", [])
    )
    if not (
        schema_dimensions
        == finding_dimensions
        == policy_dimensions
        == catalog_dimensions
    ):
        raise ValueError("documentation semantic dimension contracts diverge")


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
    ("ai_employee_lifecycle", ai_employee_lifecycle),
    ("skill_lifecycle", skill_lifecycle),
    ("execution_evidence", evidence_schema),
    ("growth_and_human_gate", growth_and_human_gate),
    ("risk_quality_gates", quality_gates),
    ("eval_architecture", evals),
    ("representative_case_results", representative_case_results),
    ("agent_skill_results", agent_skill_results),
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
        "verdict_scope": "FOUNDATION_CONTRACT",
        "capability_effectiveness": {
            "status": "UNKNOWN",
            "evidence_type": "unavailable",
            "reason": "Live task effectiveness is not inferred from synthetic contract fixtures.",
        },
        "results": results,
    }


def compare(
    baseline_root: Path,
    candidate_root: Path,
    baseline_revision: str | None = None,
    candidate_revision: str | None = None,
    contract_root: Path | None = None,
) -> dict:
    """Compare snapshots without mislabeling a changed contract as same-contract."""
    baseline = run(baseline_root)
    candidate = run(candidate_root)
    baseline_status = {item["id"]: item["status"] for item in baseline["results"]}
    candidate_status = {item["id"]: item["status"] for item in candidate["results"]}
    regressions = sorted(
        check_id
        for check_id, status in baseline_status.items()
        if status == "PASS" and candidate_status.get(check_id) != "PASS"
    )
    improvements = sorted(
        check_id
        for check_id, status in candidate_status.items()
        if status == "PASS" and baseline_status.get(check_id) != "PASS"
    )
    baseline_contract_revision = foundation_contract_revision(baseline_root)
    candidate_contract_revision = foundation_contract_revision(candidate_root)
    reference_contract_revision = foundation_contract_revision(
        contract_root or candidate_root
    )
    same_contract = (
        baseline_contract_revision == candidate_contract_revision
        and baseline_contract_revision == reference_contract_revision
    )
    comparison_kind = (
        "SAME_CONTRACT_FOUNDATION_REPLAY"
        if same_contract
        else "FOUNDATION_CONTRACT_MIGRATION"
    )
    passed = candidate["verdict"] == "PASS" and not regressions
    if contract_root is not None and not same_contract:
        passed = False
    return {
        "schema_version": "1.0",
        "comparison_scope": "FOUNDATION_CONTRACT",
        "comparison_kind": comparison_kind,
        "contract_revision": reference_contract_revision,
        "contract_revisions": {
            "baseline": baseline_contract_revision,
            "candidate": candidate_contract_revision,
            "reference": reference_contract_revision,
        },
        "same_contract_before_after": same_contract,
        "baseline_revision": baseline_revision,
        "candidate_revision": candidate_revision,
        "baseline": {
            "passed": baseline["passed"],
            "total": baseline["total"],
            "verdict": baseline["verdict"],
        },
        "candidate": {
            "passed": candidate["passed"],
            "total": candidate["total"],
            "verdict": candidate["verdict"],
        },
        "improvements": improvements,
        "regressions": regressions,
        "verdict": "PASS" if passed else "FAIL",
        "capability_effectiveness": {
            "status": "UNKNOWN",
            "evidence_type": "unavailable",
            "reason": (
                "Foundation contract migration does not prove live task effectiveness."
                if not same_contract
                else "Same-contract structural replay does not prove live task effectiveness."
            ),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--baseline-root", type=Path)
    parser.add_argument("--baseline-revision")
    parser.add_argument("--candidate-revision")
    parser.add_argument(
        "--contract-root",
        type=Path,
        help=(
            "Require both snapshots to match this fixed acceptance contract; "
            "mismatch fails closed."
        ),
    )
    args = parser.parse_args()
    result = (
        compare(
            args.baseline_root,
            args.root,
            args.baseline_revision,
            args.candidate_revision,
            args.contract_root,
        )
        if args.baseline_root
        else run(args.root)
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
