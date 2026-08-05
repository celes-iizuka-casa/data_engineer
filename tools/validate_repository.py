#!/usr/bin/env python3
"""Validate the AI engineering team repository structure and skill contracts."""

from __future__ import annotations

import json
import hashlib
import os
import re
import subprocess
import tempfile
import unicodedata
from datetime import datetime
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_VALIDATOR = (
    Path.home()
    / ".codex"
    / "skills"
    / ".system"
    / "skill-creator"
    / "scripts"
    / "quick_validate.py"
)

SKILLS = [
    "skill-engineering-pmo",
    "skill-forward-deployed-engineer",
    "skill-deliverable-quality-reviewer",
    "skill-engineering-knowledge-curator",
    "skill-tech-lead",
    "skill-fullstack-engineer",
    "skill-frontend-engineer",
    "skill-backend-engineer",
    "skill-data-engineer",
    "skill-data-platform-engineer",
    "skill-cloud-infrastructure-engineer",
    "skill-sre-platform-engineer",
    "skill-security-governance-engineer",
    "skill-qa-test-automation-engineer",
    "skill-llm-application-engineer",
    "skill-devex-agent-workflow-engineer",
    "skill-integration-engineer",
    "skill-product-manager",
    "skill-ml-engineer",
    # FDE sub-skills (parent: skill-forward-deployed-engineer)
    "skill-field-discovery",
    "skill-business-flow-mapping",
    "skill-stakeholder-mapping",
    "skill-pain-point-analysis",
    "skill-mvp-scoping",
    "skill-solution-framing",
    "skill-engineering-handoff",
    "skill-adoption-planning",
    "skill-success-metrics-design",
    "skill-feedback-to-backlog",
    # Capability Architect skills (role: capability_architect)
    "skill-capability-gap-analysis",
    "skill-agent-creation",
    "skill-skill-creation",
    "skill-agent-registry-management",
]

ROLES = [
    "engineering_pmo",
    "forward_deployed_engineer",
    "deliverable_quality_reviewer",
    "engineering_knowledge_curator",
    "tech_lead",
    "fullstack_engineer",
    "frontend_engineer",
    "backend_engineer",
    "data_engineer",
    "data_platform_engineer",
    "cloud_infrastructure_engineer",
    "sre_platform_engineer",
    "security_governance_engineer",
    "qa_test_automation_engineer",
    "llm_application_engineer",
    "devex_agent_workflow_engineer",
    "integration_engineer",
    "product_manager",
    "ml_engineer",
]

ROLE_LIFECYCLE_BASELINE_HEAD = (
    "437bfe2dabea28f08aa9750a6a8b848af20374f0"
)
ROLE_LIFECYCLE_BASELINE_REVISIONS = {
    "engineering_pmo": "sha256:e58fedbde14b1a9d63469a819ef800f831a4e7cd1a906e507eeadcd343e7f2d1",
    "forward_deployed_engineer": "sha256:07ff5ac100f509808f90fa3d323e28f31883e4159e2578e5ce6d4325fe67cc13",
    "deliverable_quality_reviewer": "sha256:87204887afa10f08711dadd212e17d8a57485276c608167fad6dd1d250957e73",
    "engineering_knowledge_curator": "sha256:1301c3ce95d8cc79ec79474018d06a8cd5bc88633bc82f3f1f845071bd9e02b5",
    "tech_lead": "sha256:f162824f3619304b13a2593ccee429dc3a065e350900b483a4912caae3a45ed4",
    "fullstack_engineer": "sha256:e4d8cd9566832c5d2c6c0d598e8358af1165a4d5a53be080d33bcca8d5e12c04",
    "frontend_engineer": "sha256:737050c76d62f1ea093610cccaa26498151bcc8fd3cb747dc8924b8f47a7fb5d",
    "backend_engineer": "sha256:325ca9d0cf27b395284f1ed692eda40ec6e087905c20981ebd35548928983d08",
    "data_engineer": "sha256:6d1c00265718f48fab4af486475d2a86b0ae780212bc4f44c130f68d990d7f17",
    "data_platform_engineer": "sha256:c539cc686435b20b399d321a10874b43e1448217b3162efa465b7bc8e1c5ac64",
    "cloud_infrastructure_engineer": "sha256:017620ce9b6a0398938cace9e8ec1fc84934421b1178807e759de8b75b7e8f05",
    "sre_platform_engineer": "sha256:19070aba9bc7d552802d7f66ed21c9749b77ab88e4ec9926402a5ef0945d45cb",
    "security_governance_engineer": "sha256:80592d0da855c1057923bbfd74f88f29159e055933629bc8b2205e4ffdee1589",
    "qa_test_automation_engineer": "sha256:1dd2fcf40ae5c3a9b4e2f4ee64564947573bffb6d38d8987be5290e08b34ac1b",
    "llm_application_engineer": "sha256:c509a44110ce9afce4a57a896ff43d09328dceda1d4202ddcca457aa35f75df5",
    "devex_agent_workflow_engineer": "sha256:78055b42962e5b51cee46f238d88f626c7d05308e92077496ccf9ac0ac8ec73b",
    "integration_engineer": "sha256:f4ce12bedb95d4933b5d7770c2e1138cea0cfbe00d7a1a3e6816768bb60acef6",
    "product_manager": "sha256:957537844b892afa31e1dd31970039b630b48d1f0ec250f00c9f289d5328fa08",
    "ml_engineer": "sha256:a18eb23a4d874a0f8dffc992684e01da4f601e1b10b945bb84aa6559d66d09ed",
}
ROLE_TRANSITION_FIELDS = {
    "from_state",
    "from_revision",
    "to_state",
    "candidate_revision",
    "evidence_refs",
    "before_after_eval_ref",
    "independent_review_ref",
    "human_gate_status",
    "celes_human_gate_ref",
}
ROLE_CREATE_REQUIREMENTS = {
    "evidenced_responsibility_or_capability_gap",
    "existing_role_update_cannot_resolve",
    "merge_or_split_cannot_resolve",
    "recurring_reuse_value",
    "clear_responsibility_boundary",
    "evaluable_contract",
    "overlap_explained",
}

WORKFLOWS = [
    "input_to_output_workflow.md",
    "field_discovery_to_solution_workflow.md",
    "customer_feedback_to_engineering_workflow.md",
    "mvp_scoping_workflow.md",
    "requirements_to_design_workflow.md",
    "design_to_implementation_workflow.md",
    "implementation_to_test_workflow.md",
    "data_platform_workflow.md",
    "rag_llm_workflow.md",
    "incident_response_workflow.md",
    "deliverable_quality_review_workflow.md",
    "engineering_knowledge_curation_workflow.md",
    "risk_based_team_formation_workflow.md",
    "capability_growth_workflow.md",
]

FOUNDATION_FILES = [
    "ai_team/governance/architecture_contract.yaml",
    "ai_team/governance/canonical_sources.yaml",
    "ai_team/governance/capability_growth_policy.yaml",
    "ai_team/governance/ai_employee_lifecycle_registry.yaml",
    "ai_team/governance/skill_lifecycle_registry.yaml",
    "ai_team/governance/documentation_quality_policy.yaml",
    "ai_team/governance/human_gate.schema.json",
    "ai_team/capability_registry.yaml",
    "ai_team/evidence/execution_evidence.schema.json",
    "ai_team/evidence/new_execution_evidence.py",
    "ai_team/evals/eval_catalog.yaml",
    "ai_team/evals/golden_cases.yaml",
    "ai_team/evals/case_fixtures.yaml",
    "ai_team/evals/agent_skill_fixtures.yaml",
    "ai_team/evals/skill_eval_bindings.yaml",
    "ai_team/evals/documentation_semantic_review.schema.json",
    "ai_team/evals/validate_documentation_semantic_review.py",
    "ai_team/evals/select_documentation_review_targets.py",
    "ai_team/evals/run_foundation_evals.py",
    "ai_team/review/risk_based_quality_gates.yaml",
    "ai_team/tests/test_ai_team_foundation.py",
]

# Shared Core roots as declared in architecture_contract.yaml. Pinned here so a
# silent edit to the contract (e.g. dropping tools/validate_repository.py) fails
# instead of shipping a contract that disagrees with the policy documents.
SHARED_CORE_ROOTS = [
    "ai_team/**",
    "skills/**",
    "templates/**",
    "tools/validate_repository.py",
]

PRIVATE_TOP_LEVEL = {
    "output",
    ".local",
    "second_brain",
    "evidence",
    "secrets",
    "secret",
    "credentials",
    "tokens",
    "temp",
    "tmp",
    "projects",
    "clients",
    "customers",
    "customer",
    "client",
    "sources",
    "source",
    "raw",
    "private",
    "feedback",
    "raw_evidence",
    "private_feedback",
    "raw_feedback",
    "raw_reviewer_findings",
    "raw_retrospectives",
}
PRIVATE_TRACKED_ALLOWLIST = {"input/README.md"}
PRIVATE_SHARED_EVIDENCE_ALLOWLIST = {
    "ai_team/evidence/execution_evidence.schema.json",
    "ai_team/evidence/new_execution_evidence.py",
}
PRIVATE_EXACT_PATHS = {
    ".claude/settings.local.json",
    ".claude/.needs_validation",
}
PRIVATE_PATH_COMPONENTS = {
    ".local",
    "second_brain",
    "secrets",
    "secret",
    "credentials",
    "credential",
    "tokens",
    "token",
    "temp",
    "tmp",
    ".ssh",
    ".aws",
    ".gnupg",
    "raw_evidence",
    "private_feedback",
    "raw_feedback",
    "raw_reviewer_findings",
    "raw_retrospectives",
}
SECRET_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".crt", ".cer"}
REQUIRED_IGNORE_RULES = {
    "/input/*",
    "!/input/README.md",
    "/output/*",
    "/second_brain/",
    "/.local/",
    "/**/_internal/",
    "/evidence/",
    "/ai_team/evidence/*",
    "!/ai_team/evidence/execution_evidence.schema.json",
    "!/ai_team/evidence/new_execution_evidence.py",
    "/secrets/",
    "/secret/",
    "/credentials/",
    "/tokens/",
    "/temp/",
    "/projects/",
    "/clients/",
    "/client/",
    "/customers/",
    "/customer/",
    "/sources/",
    "/source/",
    "/raw/",
    "/private/",
    "/feedback/",
    "/raw_evidence/",
    "/private_feedback/",
    "/raw_feedback/",
    "/raw_reviewer_findings/",
    "/raw_retrospectives/",
    "/.ssh/",
    "/.aws/",
    "/.gnupg/",
    "/**/.local/",
    "/**/second_brain/",
    "/**/secrets/",
    "/**/secret/",
    "/**/credentials/",
    "/**/tokens/",
    "/**/temp/",
    "/**/evidence/*",
    "/**/raw_evidence/",
    "/**/private_feedback/",
    "/**/raw_feedback/",
    "/**/raw_reviewer_findings/",
    "/**/raw_retrospectives/",
    "/.claude/settings.local.json",
    "/.claude/.needs_validation",
}
ALLOWED_GITIGNORE_NEGATIONS = {
    "!/input/README.md",
    "!/tools/validate_repository.py",
    "!/ai_team/evidence/execution_evidence.schema.json",
    "!/ai_team/evidence/new_execution_evidence.py",
}
PRIVATE_GITIGNORE_SENTINELS = {
    "input/example-client/request.md",
    "output/example-client/output.md",
    "projects/example-client/request.md",
    "clients/example-client/request.md",
    "client/example-client/request.md",
    "customers/example-client/request.md",
    "customer/example-client/request.md",
    "sources/example-client/source.txt",
    "source/example-client/source.txt",
    "raw/evidence.json",
    "private/feedback.md",
    "feedback/review.md",
    "raw_evidence/run.yaml",
    "private_feedback/review.md",
    "raw_feedback/comment.md",
    "raw_reviewer_findings/finding.md",
    "raw_retrospectives/task.md",
    ".local/evidence/run.yaml",
    "evidence/run.yaml",
    "ai_team/evidence/customer-run.yaml",
    "secrets/key.txt",
    "secret/key.txt",
    "credentials/account.json",
    "tokens/access.txt",
    "temp/work.txt",
    "second_brain/private.md",
    "nested/_internal/review.md",
    "nested/.local/state.yaml",
    "nested/second_brain/private.md",
    "nested/evidence/run.yaml",
    "nested/raw_evidence/run.yaml",
    "nested/private_feedback/review.md",
    "nested/raw_feedback/comment.md",
    "nested/raw_reviewer_findings/finding.md",
    "nested/raw_retrospectives/task.md",
    "nested/secrets/key.txt",
    "nested/credentials/account.json",
    "nested/tokens/access.txt",
    "nested/temp/work.txt",
    ".claude/settings.local.json",
    ".claude/.needs_validation",
    ".ssh/id_rsa",
    ".aws/credentials",
    ".gnupg/private-keys-v1.d/key",
}
SHARED_GITIGNORE_SENTINELS = {
    "input/README.md",
    "tools/validate_repository.py",
    "ai_team/evidence/execution_evidence.schema.json",
    "ai_team/evidence/new_execution_evidence.py",
}
ANONYMOUS_INPUT_README_SHA256 = (
    "955bc0f273b9c36bd148f01998102dbf44c2e2559c5c8461919029c3a22ad64b"
)
SECRET_CONTENT_PATTERNS = (
    re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\bASIA[A-Z0-9]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\bgh[pousr]_[0-9A-Za-z]{36,255}\b"),
    re.compile(r"\bgithub_pat_[0-9A-Za-z_]{20,255}\b"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,255}\b"),
    re.compile(r"\bsk-proj-[0-9A-Za-z_-]{20,255}\b"),
    re.compile(r"\bsk-ant-[0-9A-Za-z_-]{20,255}\b"),
    re.compile(r"\bsk-(?!proj-|ant-)[0-9A-Za-z_-]{20,255}\b"),
)
PERSONAL_ABSOLUTE_PATH_PATTERNS = (
    re.compile("/" + "Users" + r"/[A-Za-z0-9._-]+/"),
    re.compile("/" + "home" + r"/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\" + "Users" + r"\\[^\\\s]+\\"),
)
PRIVATE_README_INPUT_EXAMPLE_PATTERN = re.compile(
    r"\binput/(?!example-client/|<client>/|README\.md\b)[^\s`/]+/"
)

TEMPLATES = [
    "output_template.md",
    "deliverable_summary_template.md",
    "execution_plan_template.md",
    "model_selection_template.md",
    "iteration_plan_template.md",
    "iteration_sample_review_template.md",
    "feedback_analysis_template.md",
    "task_retrospective_template.md",
    "team_improvement_proposal_template.md",
    "requirements_template.md",
    "field_discovery_template.md",
    "customer_context_template.md",
    "stakeholder_map_template.md",
    "mvp_scope_template.md",
    "engineering_handoff_template.md",
    "adoption_plan_template.md",
    "success_metrics_template.md",
    "feedback_log_template.md",
    "basic_design_template.md",
    "detailed_design_template.md",
    "architecture_template.md",
    "api_design_template.md",
    "db_design_template.md",
    "data_pipeline_design_template.md",
    "data_quality_rules_template.md",
    "test_plan_template.md",
    "runbook_template.md",
    "handover_template.md",
    "execution_summary_template.md",
    "quality_review_request_template.md",
    "quality_review_report_template.md",
    "finding_register_template.md",
    "review_metrics_template.md",
    "obsidian_project_note_template.md",
    "obsidian_architecture_note_template.md",
    "obsidian_decision_log_template.md",
    "obsidian_troubleshooting_template.md",
    "obsidian_learning_note_template.md",
    "obsidian_source_map_template.md",
    "professional_opinion_template.md",
    "professional_design_template.md",
    "professional_implementation_template.md",
    "professional_verification_template.md",
    "role_handoff_template.md",
    "gap_analysis_template.md",
    "fde/fde_template_index.md",
    "fde/business_flow_template.md",
    "fde/pain_point_analysis_template.md",
    "fde/solution_framing_template.md",
    "fde/customer_explanation_template.md",
    "examples/golden_sample_output.md",
    "examples/golden_sample_quality_review.md",
    "agent_creation/capability_gap_analysis_template.md",
    "agent_creation/agent_need_assessment_template.md",
    "agent_creation/new_agent_proposal_template.md",
    "agent_creation/new_agent_definition_template.md",
    "agent_creation/new_skill_definition_template.md",
    "agent_creation/agent_registry_entry_template.md",
    "agent_creation/capability_matrix_entry_template.md",
    "agent_creation/local_capability_registry_template.yaml",
    "agent_creation/local_decision_log_template.md",
]

ROLE_HEADINGS = [
    "## 概要",
    "## 目的",
    "## 守備範囲",
    "## 主な責務",
    "## 得意な課題",
    "## 入力",
    "## 出力",
    "## 責任を持つ成果物",
    "## 責任を持たない領域",
    "## 他Roleへ渡す条件",
    "## 判断基準",
    "## Professional Opinion Modeでの観点",
    "## Professional Design Modeでの観点",
    "## Professional Implementation Modeでの観点",
    "## Professional Verification Modeでの観点",
    "## 他ロールとの連携",
    "## 成果物例",
    "## レビュー観点",
    "## Professional Only Policy",
    "## 非プロフェッショナルな出力",
    "## セレスへの返答スタイル",
    "## 禁止事項",
    "## 品質基準",
    "## 完了条件",
    "## セレスをどう補完するか",
    "## 判断事例",
    "## エスカレーション基準",
]

README_HEADINGS = [
    "## Skill名",
    "## 対応Role",
    "## 目的",
    "## 守備範囲",
    "## 責任を持つ成果物",
    "## 責任を持たない領域",
    "## 使用タイミング",
    "## 入力",
    "## 出力",
    "## Professional Opinion Mode",
    "## Professional Design Mode",
    "## Professional Implementation Mode",
    "## Professional Verification Mode",
    "## 実行手順",
    "## 判断基準",
    "## レビュー観点",
    "## Professional Only Policy",
    "## 非プロフェッショナルな出力",
    "## 他Skillとの連携",
    "## 不明点がある場合の対応",
    "## セレスへの返答スタイル",
    "## 禁止事項",
    "## 完了条件",
    "## 実務プレイブック",
]

YAML_KEYS = {
    "name",
    "legacy_id",
    "role",
    "purpose",
    "scope",
    "when_to_use",
    "inputs",
    "outputs",
    "modes",
    "steps",
    "decision_criteria",
    "review_points",
    "collaboration",
    "professional_only_policy",
    "non_professional_outputs",
    "uncertainty_handling",
    "response_style_for_celes",
    "deliverables",
    "done_definition",
    "prohibited_actions",
}


class Validation:
    def __init__(self) -> None:
        self.checks: list[str] = []
        self.errors: list[str] = []

    def ok(self, message: str) -> None:
        self.checks.append(message)

    def fail(self, message: str) -> None:
        self.errors.append(message)

    def require_file(self, relative_path: str) -> Path | None:
        target = ROOT / relative_path
        if not target.is_file():
            self.fail(f"Missing file: {relative_path}")
            return None
        if target.stat().st_size == 0:
            self.fail(f"Empty file: {relative_path}")
            return None
        self.ok(f"File exists: {relative_path}")
        return target


def validate_yaml(validation: Validation, relative_path: str) -> dict | None:
    target = validation.require_file(relative_path)
    if target is None:
        return None
    try:
        value = yaml.safe_load(target.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        validation.fail(f"Invalid YAML: {relative_path}: {exc}")
        return None
    if not isinstance(value, dict):
        validation.fail(f"YAML root is not a mapping: {relative_path}")
        return None
    validation.ok(f"YAML parses: {relative_path}")
    return value


def validate_json(validation: Validation, relative_path: str) -> dict | None:
    target = validation.require_file(relative_path)
    if target is None:
        return None
    try:
        value = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        validation.fail(f"Invalid JSON: {relative_path}: {exc}")
        return None
    if not isinstance(value, dict):
        validation.fail(f"JSON root is not an object: {relative_path}")
        return None
    validation.ok(f"JSON parses: {relative_path}")
    return value


def private_tracked_reason(relative_path: str) -> str | None:
    """Return a safe reason when a Git-tracked path crosses a privacy boundary."""
    normalized = relative_path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    normalized = normalized.lstrip("/")
    if normalized in PRIVATE_TRACKED_ALLOWLIST:
        return None
    if normalized in PRIVATE_EXACT_PATHS:
        return "local runtime state"

    parts = tuple(part for part in normalized.split("/") if part)
    if not parts:
        return None
    if parts[:2] == ("ai_team", "evidence"):
        if normalized in PRIVATE_SHARED_EVIDENCE_ALLOWLIST:
            return None
        return "raw evidence in shared schema directory"
    if parts[0] == "input":
        return "private task input"
    if parts[0] in PRIVATE_TOP_LEVEL:
        return "local private state"
    if "_internal" in parts:
        return "internal task artifact"
    if any(part.lower() in PRIVATE_PATH_COMPONENTS for part in parts):
        return "nested local private state"
    if "evidence" in (part.lower() for part in parts):
        return "raw local evidence"

    basename = parts[-1].lower()
    if basename == ".env" or basename.startswith(".env."):
        return "environment secret"
    if basename in {"id_rsa", "id_rsa.pub"}:
        return "credential material"
    if Path(basename).suffix in SECRET_SUFFIXES:
        return "credential or certificate material"
    if re.match(r"^(credentials?|secrets?|tokens?)(\.|$)", basename):
        return "credential-like filename"
    return None


def git_tracked_files(root: Path = ROOT) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-z"],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "git ls-files failed")
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def git_untracked_files(root: Path = ROOT) -> list[str]:
    """Return untracked, non-ignored candidate shared files."""
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard", "-z"],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "git ls-files --others failed")
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def git_staged_files(root: Path = ROOT) -> list[str]:
    """Return paths whose Git-index content differs from HEAD."""
    result = subprocess.run(
        [
            "git", "-C", str(root), "diff", "--cached", "--name-only", "-z",
        ],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or "git diff --cached failed")
    return [
        item.decode("utf-8", errors="surrogateescape")
        for item in result.stdout.split(b"\0")
        if item
    ]


def git_index_blob(relative_path: str, root: Path = ROOT) -> bytes:
    """Read exactly what a commit would take from the current Git index."""
    result = subprocess.run(
        ["git", "-C", str(root), "show", f":{relative_path}"],
        check=False,
        capture_output=True,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(detail or f"cannot read index blob: {relative_path}")
    return result.stdout


def gitignore_effective_ignored_paths(raw: bytes) -> set[str]:
    """Evaluate privacy sentinels with Git itself against supplied ignore bytes."""
    sentinels = sorted(PRIVATE_GITIGNORE_SENTINELS | SHARED_GITIGNORE_SENTINELS)
    with tempfile.TemporaryDirectory(prefix="ai-team-ignore-check-") as directory:
        temporary_root = Path(directory)
        (temporary_root / ".gitignore").write_bytes(raw)
        initialized = subprocess.run(
            ["git", "-C", str(temporary_root), "init", "-q"],
            check=False,
            capture_output=True,
        )
        if initialized.returncode:
            detail = initialized.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(detail or "temporary git init failed")
        checked = subprocess.run(
            [
                "git", "-C", str(temporary_root), "check-ignore", "--no-index",
                "-z", "--stdin",
            ],
            input=("\0".join(sentinels) + "\0").encode("utf-8"),
            check=False,
            capture_output=True,
        )
        if checked.returncode not in {0, 1}:
            detail = checked.stderr.decode("utf-8", errors="replace").strip()
            raise RuntimeError(detail or "git check-ignore failed")
        return {
            item.decode("utf-8", errors="surrogateescape")
            for item in checked.stdout.split(b"\0")
            if item
        }


def validate_cross_provider_code(
    validation: Validation, root: Path = ROOT
) -> None:
    """Scan both worktree candidates and Git-index blobs for provider calls."""
    code_suffixes = {
        ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".sh", ".zsh",
        ".json",
    }
    code_patterns = (
        re.compile(r"^\s*(?:from|import)\s+(?:openai|anthropic)\b", re.M),
        re.compile(
            r"(?:from\s+|require\s*\(|import\s*\()"
            r"[\"'](?:openai|@anthropic-ai/sdk)[\"']"
        ),
        re.compile(r"https://api\.(?:openai|anthropic)\.com", re.I),
        re.compile(r"^\s*(?:exec\s+)?(?:claude|codex)(?:\s|$)", re.M),
        re.compile(
            r"subprocess\.(?:run|Popen|call|check_call|check_output)\s*\(\s*"
            r"\[\s*[\"'](?:claude|codex)[\"']"
        ),
        re.compile(
            r"(?:spawn|execFile|execSync|exec|system)\s*\(\s*"
            r"[\"'](?:claude|codex)(?:[\"']|\s)"
        ),
    )
    try:
        tracked = set(git_tracked_files(root))
        untracked = set(git_untracked_files(root))
    except (OSError, RuntimeError) as exc:
        validation.fail(
            f"Cannot enumerate shared code for provider scan (fail closed): {exc}"
        )
        return

    def is_shared_code(relative: str) -> bool:
        return (
            private_tracked_reason(relative) is None
            and Path(relative).suffix.lower() in code_suffixes
        )

    violations: list[tuple[str, str]] = []
    for relative in sorted(tracked):
        if not is_shared_code(relative):
            continue
        try:
            content = git_index_blob(relative, root).decode("utf-8")
        except (OSError, RuntimeError, UnicodeDecodeError) as exc:
            validation.fail(
                f"Cannot inspect Git-index provider code {relative} "
                f"(fail closed): {exc}"
            )
            continue
        if any(pattern.search(content) for pattern in code_patterns):
            violations.append(("Git index", relative))
    for relative in sorted(tracked | untracked):
        if not is_shared_code(relative):
            continue
        target = root / relative
        if not target.is_file():
            continue
        try:
            content = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            validation.fail(
                f"Cannot inspect worktree provider code {relative} "
                f"(fail closed): {exc}"
            )
            continue
        if any(pattern.search(content) for pattern in code_patterns):
            violations.append(("working tree", relative))
    for source, relative in violations:
        validation.fail(
            f"Cross-provider invocation code is forbidden in {source}: {relative}"
        )
    if not violations:
        validation.ok(
            "Cross-provider invocation is absent from Git index and worktree code"
        )


def canonical_pattern_matches(relative_path: str, pattern: str) -> bool:
    """Match manifest globs, including files directly under a /**/* root."""
    if "/" not in pattern:
        return relative_path == pattern
    if pattern.endswith("/**/*"):
        prefix = pattern[:-5].rstrip("/")
        return relative_path.startswith(prefix + "/")
    return PurePosixPath(relative_path).match(pattern)


def skill_content_revision(skill_id: str, root: Path = ROOT) -> str | None:
    """Derive the Skill revision from the three canonical Skill surfaces."""
    base = root / "skills" / skill_id
    relative_files = ("skill.yaml", "SKILL.md", "agents/openai.yaml")
    targets = [base / relative for relative in relative_files]
    if not all(target.is_file() for target in targets):
        return None
    digest = hashlib.sha256()
    for relative, target in zip(relative_files, targets):
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(target.read_bytes())
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def configured_role_ids(root: Path = ROOT) -> list[str]:
    """Read the current canonical Role IDs, retaining the baseline minimum."""
    target = root / "ai_team" / "capability_registry.yaml"
    try:
        data = yaml.safe_load(target.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return list(ROLES)
    entries = data.get("roles", []) if isinstance(data, dict) else []
    ids = [
        str(entry.get("id"))
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    ]
    return ids if ids else list(ROLES)


def skill_head_revision(skill_id: str, root: Path = ROOT) -> str | None:
    """Derive the active Skill revision from the canonical committed HEAD."""
    digest = hashlib.sha256()
    for relative in ("skill.yaml", "SKILL.md", "agents/openai.yaml"):
        path = f"skills/{skill_id}/{relative}"
        result = subprocess.run(
            ["git", "-C", str(root), "show", f"HEAD:{path}"],
            check=False,
            capture_output=True,
        )
        if result.returncode:
            return None
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        digest.update(result.stdout)
        digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def role_content_revision(role_id: str, root: Path = ROOT) -> str | None:
    """Derive a Role revision from shared contract, identity, and capability."""
    capability_path = root / "ai_team" / "capability_registry.yaml"
    role_path = root / "ai_team" / "roles" / f"{role_id}.md"
    if not capability_path.is_file() or not role_path.is_file():
        return None
    try:
        capability = yaml.safe_load(capability_path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError):
        return None
    entries = capability.get("roles", []) if isinstance(capability, dict) else []
    entry = next(
        (
            item
            for item in entries
            if isinstance(item, dict) and item.get("id") == role_id
        ),
        None,
    )
    if entry is None:
        return None
    digest = hashlib.sha256()
    digest.update(b"common_contract\0")
    digest.update(
        yaml.safe_dump(
            capability.get("common_contract", {}),
            allow_unicode=True,
            sort_keys=True,
        ).encode("utf-8")
    )
    digest.update(b"\0")
    digest.update(b"role_document\0")
    digest.update(role_path.read_bytes())
    digest.update(b"\0capability_entry\0")
    digest.update(
        yaml.safe_dump(
            entry,
            allow_unicode=True,
            sort_keys=True,
        ).encode("utf-8")
    )
    digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def role_git_revision(
    role_id: str, revision: str, root: Path = ROOT
) -> str | None:
    """Derive a Role revision from a canonical Git revision."""
    role_result = subprocess.run(
        [
            "git", "-C", str(root), "show",
            f"{revision}:ai_team/roles/{role_id}.md",
        ],
        check=False,
        capture_output=True,
    )
    capability_result = subprocess.run(
        [
            "git", "-C", str(root), "show",
            f"{revision}:ai_team/capability_registry.yaml",
        ],
        check=False,
        capture_output=True,
    )
    if role_result.returncode or capability_result.returncode:
        return None
    try:
        capability = yaml.safe_load(capability_result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError):
        return None
    entries = capability.get("roles", []) if isinstance(capability, dict) else []
    entry = next(
        (
            item
            for item in entries
            if isinstance(item, dict) and item.get("id") == role_id
        ),
        None,
    )
    if entry is None:
        return None
    digest = hashlib.sha256()
    digest.update(b"common_contract\0")
    digest.update(
        yaml.safe_dump(
            capability.get("common_contract", {}),
            allow_unicode=True,
            sort_keys=True,
        ).encode("utf-8")
    )
    digest.update(b"\0")
    digest.update(b"role_document\0")
    digest.update(role_result.stdout)
    digest.update(b"\0capability_entry\0")
    digest.update(
        yaml.safe_dump(
            entry,
            allow_unicode=True,
            sort_keys=True,
        ).encode("utf-8")
    )
    digest.update(b"\0")
    return f"sha256:{digest.hexdigest()}"


def role_head_revision(role_id: str, root: Path = ROOT) -> str | None:
    """Derive the active Role revision from the canonical committed HEAD."""
    return role_git_revision(role_id, "HEAD", root)


def non_pending_reference(value: object) -> bool:
    """Return true only for an evidence reference that is not a placeholder."""
    if not isinstance(value, str):
        return False
    normalized = value.strip()
    return bool(normalized) and normalized.casefold() not in {
        "pending", "tbd", "todo", "unknown", "unavailable", "n/a", "na",
        "none", "null",
    }


def valid_reference_list(value: object) -> bool:
    """Require a non-empty list of concrete, non-placeholder references."""
    return (
        isinstance(value, list)
        and bool(value)
        and all(non_pending_reference(item) for item in value)
    )


def valid_decision_timestamp(value: object) -> bool:
    """Require a real ISO-8601 timestamp with an explicit timezone."""
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


def role_candidate_registration_failures(
    entry: dict,
    current_revision: str | None,
    head_revision: str | None,
    previous_entry: dict | None = None,
) -> list[str]:
    """Require every canonical Role revision change to be a registered candidate."""
    candidate_revision = entry.get("candidate_revision")
    failures: list[str] = []
    if current_revision != head_revision and candidate_revision != current_revision:
        failures.append("unregistered_canonical_change")
    previous_active_revision = (
        previous_entry.get("active_revision")
        if previous_entry is not None
        else None
    )
    canonical_changed_from_previous = (
        current_revision is not None
        and current_revision != previous_active_revision
    )
    if canonical_changed_from_previous and candidate_revision != current_revision:
        failures.append("unregistered_canonical_change")
    if candidate_revision is not None and current_revision == head_revision:
        candidate_state = entry.get("candidate_state")
        final_candidate = candidate_state in {"ACTIVE", "DEPRECATED"}
        progressed_candidate = (
            previous_entry is not None
            and previous_entry.get("candidate_revision") == candidate_revision
        )
        governed_state_change = (
            previous_entry is not None
            and previous_entry.get("state") != candidate_state
        )
        governed_create = (
            previous_entry is None and entry.get("disposition") == "CREATE"
        )
        content_changed_from_previous = canonical_changed_from_previous
        if not final_candidate or not (
            progressed_candidate
            or governed_state_change
            or governed_create
            or content_changed_from_previous
        ):
            failures.append("candidate_without_revision_change")
    return sorted(set(failures))


def role_allowed_dispositions(established_revision: str | None) -> set[str]:
    """Allow CREATE only until a Role has an established governed revision.

    ``established_revision`` is the Role's last governed revision: the frozen
    baseline for Roles present at ``ROLE_LIFECYCLE_BASELINE_HEAD``, otherwise
    the ``active_revision`` of its committed lifecycle entry. Keying this on
    ``ROLE_LIFECYCLE_BASELINE_REVISIONS`` alone would lock every Role created
    after the baseline into CREATE forever, which no ``from_revision`` value
    can satisfy: CREATE requires ``from_revision: null`` while the historical
    continuity check requires the prior ``active_revision``.
    """
    if established_revision is None:
        return {"CREATE", "UNKNOWN"}
    return {"UPDATE", "MERGE", "SPLIT", "DEPRECATE", "UNKNOWN"}


def role_create_criteria_failures(entry: dict) -> list[str]:
    """Require evidence for every strict CREATE criterion and nowhere else."""
    criteria = entry.get("create_criteria")
    if entry.get("disposition") != "CREATE":
        return [] if criteria in (None, {}) else ["criteria_on_non_create"]
    if not isinstance(criteria, dict) or set(criteria) != ROLE_CREATE_REQUIREMENTS:
        return ["incomplete_create_criteria"]
    if not all(non_pending_reference(reference) for reference in criteria.values()):
        return ["placeholder_create_evidence"]
    return []


def role_registry_state_failures(
    entry: dict, previous_entry: dict | None
) -> list[str]:
    """Prevent direct Role activation/deprecation outside a final candidate."""
    if previous_entry is None:
        return []
    candidate_state = entry.get("candidate_state")
    transition = entry.get("transition")
    final_candidate = (
        entry.get("candidate_revision") is not None
        and candidate_state in {"ACTIVE", "DEPRECATED"}
        and isinstance(transition, dict)
        and transition.get("human_gate_status") in {"promoted", "rolled_back"}
    )
    failures: list[str] = []
    if not final_candidate and entry.get("state") != previous_entry.get("state"):
        failures.append("unregistered_state_change")
    if entry.get("candidate_revision") is not None and isinstance(
        transition, dict
    ):
        previous_transition = previous_entry.get("transition")
        if (
            previous_entry.get("candidate_revision")
            == entry.get("candidate_revision")
            and isinstance(previous_transition, dict)
        ):
            expected_from_state = previous_transition.get("from_state")
        else:
            expected_from_state = previous_entry.get("state")
        if transition.get("from_state") != expected_from_state:
            failures.append("from_state_history_mismatch")
    return sorted(failures)


def ai_employee_transition_failures(
    entry: dict, decision_history: list[dict]
) -> list[str]:
    """Validate the state-specific Role candidate and Celes decision contract."""
    role_id = str(entry.get("id", ""))
    candidate_revision = entry.get("candidate_revision")
    candidate_state = entry.get("candidate_state")
    transition = entry.get("transition")
    failures: list[str] = []
    if candidate_revision is None:
        if transition not in (None, {}):
            failures.append("transition_without_candidate")
        return failures
    allowed_candidate_states = {
        "DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED",
        "INDEPENDENTLY_REVIEWED", "HUMAN_GATE", "ACTIVE", "DEPRECATED",
    }
    if candidate_state not in allowed_candidate_states:
        failures.append("invalid_candidate_state")
    if not isinstance(transition, dict) or set(transition) != ROLE_TRANSITION_FIELDS:
        failures.append("incomplete_transition")
        return failures
    if transition.get("from_state") not in allowed_candidate_states:
        failures.append("invalid_from_state")
    if (
        candidate_state not in {"ACTIVE", "DEPRECATED"}
        and transition.get("from_state") != entry.get("state")
    ):
        failures.append("from_state_mismatch")
    if transition.get("to_state") != candidate_state:
        failures.append("to_state_mismatch")
    from_revision = transition.get("from_revision")
    if from_revision is not None and (
        not isinstance(from_revision, str)
        or not re.fullmatch(r"sha256:[0-9a-f]{64}", from_revision)
    ):
        failures.append("invalid_from_revision")
    if (
        candidate_state not in {"ACTIVE", "DEPRECATED"}
        and entry.get("active_revision") != from_revision
    ):
        failures.append("from_revision_mismatch")
    if transition.get("candidate_revision") != candidate_revision:
        failures.append("candidate_revision_mismatch")
    if (
        entry.get("disposition") in {"UPDATE", "MERGE", "SPLIT"}
        and from_revision == candidate_revision
    ):
        failures.append("noop_candidate_revision")
    if entry.get("disposition") == "CREATE" and from_revision is not None:
        failures.append("create_from_revision_must_be_null")
    if not valid_reference_list(transition.get("evidence_refs")):
        failures.append("missing_evidence_refs")
    gate_status = transition.get("human_gate_status")
    before_after_ref = transition.get("before_after_eval_ref")
    independent_ref = transition.get("independent_review_ref")
    celes_ref = transition.get("celes_human_gate_ref")
    pending_states = {
        "DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED",
        "INDEPENDENTLY_REVIEWED",
    }
    if candidate_state in pending_states:
        if gate_status != "pending":
            failures.append("human_gate_not_pending")
        if celes_ref != "pending":
            failures.append("premature_celes_gate_ref")
    if candidate_state in {"DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED"}:
        if independent_ref != "pending":
            failures.append("premature_independent_review")
    if candidate_state in {
        "EVALUATED", "INDEPENDENTLY_REVIEWED", "HUMAN_GATE", "ACTIVE",
        "DEPRECATED",
    } and not non_pending_reference(before_after_ref):
        failures.append("missing_before_after_eval")
    if candidate_state in {
        "INDEPENDENTLY_REVIEWED", "HUMAN_GATE", "ACTIVE", "DEPRECATED",
    } and not non_pending_reference(independent_ref):
        failures.append("missing_independent_review")
    decision_by_status = {
        "promoted": "PROMOTE",
        "rejected": "REJECT",
        "rework": "REWORK",
        "rolled_back": "ROLLBACK",
    }
    if candidate_state == "HUMAN_GATE" and gate_status not in {
        "pending", "rejected", "rework",
    }:
        failures.append("invalid_human_gate_outcome")
    if candidate_state in {"ACTIVE", "DEPRECATED"}:
        if gate_status not in {"promoted", "rolled_back"}:
            failures.append("missing_human_promotion")
        if entry.get("state") != candidate_state:
            failures.append("final_role_state_mismatch")
        if entry.get("active_revision") != candidate_revision:
            failures.append("promoted_revision_mismatch")
    if gate_status in decision_by_status:
        if not non_pending_reference(celes_ref):
            failures.append("missing_celes_gate_ref")
        expected_decision = decision_by_status[gate_status]
        matching_decisions = [
            decision
            for decision in decision_history
            if isinstance(decision, dict)
            and decision.get("subject_id") == role_id
            and decision.get("subject_revision") == candidate_revision
            and decision.get("decision") == expected_decision
        ]
        if len(matching_decisions) != 1:
            failures.append("missing_unique_decision_history")
        else:
            decision = matching_decisions[0]
            if decision.get("gate_id") != celes_ref:
                failures.append("celes_gate_ref_mismatch")
            if decision.get("from_revision") != from_revision:
                failures.append("decision_from_revision_mismatch")
            if decision.get("target_state") != candidate_state:
                failures.append("decision_target_state_mismatch")
            if decision.get("disposition") != entry.get("disposition"):
                failures.append("decision_disposition_mismatch")
            if decision.get("before_after_eval_ref") != before_after_ref:
                failures.append("decision_before_after_mismatch")
            if decision.get("independent_review_ref") != independent_ref:
                failures.append("decision_review_mismatch")
            if set(decision.get("evidence_refs", [])) != set(
                transition.get("evidence_refs", [])
            ):
                failures.append("decision_evidence_mismatch")
            if expected_decision == "ROLLBACK":
                if decision.get("rollback_revision") != candidate_revision:
                    failures.append("rollback_revision_mismatch")
                if decision.get("promoted_revision") != from_revision:
                    failures.append("rollback_source_mismatch")
                if decision.get("celes_decision") != "ROLLBACK":
                    failures.append("rollback_celes_decision_mismatch")
                if not any(
                    isinstance(source, dict)
                    and source.get("subject_id") == role_id
                    and source.get("subject_revision") == from_revision
                    and source.get("decision") == "PROMOTE"
                    for source in decision_history
                ):
                    failures.append("rollback_source_not_promoted")
    elif candidate_state == "HUMAN_GATE" and gate_status == "pending":
        if celes_ref != "pending":
            failures.append("premature_celes_gate_ref")
    elif candidate_state in {"ACTIVE", "DEPRECATED"}:
        failures.append("missing_unique_decision_history")
    return sorted(set(failures))


def historical_role_decision_records(root: Path = ROOT) -> list[dict]:
    """Read every decision record previously committed on reachable history."""
    path = "ai_team/governance/ai_employee_lifecycle_registry.yaml"
    history = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%H", "--", path],
        check=False,
        capture_output=True,
        text=True,
    )
    if history.returncode:
        raise RuntimeError(history.stderr.strip() or "git log failed")
    records: list[dict] = []
    for revision in (line.strip() for line in history.stdout.splitlines()):
        if not revision:
            continue
        content = subprocess.run(
            ["git", "-C", str(root), "show", f"{revision}:{path}"],
            check=False,
            capture_output=True,
        )
        if content.returncode:
            continue
        try:
            data = yaml.safe_load(content.stdout.decode("utf-8"))
        except (UnicodeDecodeError, yaml.YAMLError):
            continue
        if not isinstance(data, dict):
            continue
        for record in data.get("decision_history", []):
            if isinstance(record, dict):
                records.append(record)
    return records


def role_lifecycle_entries_at_git_ref(
    revision: str = "HEAD", root: Path = ROOT
) -> dict[str, dict]:
    """Load committed Role lifecycle entries; an absent first-version file is empty."""
    path = "ai_team/governance/ai_employee_lifecycle_registry.yaml"
    content = subprocess.run(
        ["git", "-C", str(root), "show", f"{revision}:{path}"],
        check=False,
        capture_output=True,
    )
    if content.returncode:
        return {}
    try:
        data = yaml.safe_load(content.stdout.decode("utf-8"))
    except (UnicodeDecodeError, yaml.YAMLError):
        return {}
    entries = data.get("roles", []) if isinstance(data, dict) else []
    return {
        str(entry.get("id")): entry
        for entry in entries
        if isinstance(entry, dict) and entry.get("id")
    }


def role_lifecycle_previous_entries(root: Path = ROOT) -> dict[str, dict]:
    """Load the path-aware Role registry state immediately before the candidate."""
    relative = "ai_team/governance/ai_employee_lifecycle_registry.yaml"
    target = root / relative
    try:
        worktree_bytes = target.read_bytes()
    except OSError:
        return {}
    head = subprocess.run(
        ["git", "-C", str(root), "show", f"HEAD:{relative}"],
        check=False,
        capture_output=True,
    )
    if head.returncode:
        return {}
    if worktree_bytes != head.stdout:
        return role_lifecycle_entries_at_git_ref("HEAD", root)
    history = subprocess.run(
        ["git", "-C", str(root), "log", "--format=%H", "--", relative],
        check=False,
        capture_output=True,
        text=True,
    )
    if history.returncode:
        return {}
    revisions = [
        revision.strip()
        for revision in history.stdout.splitlines()
        if revision.strip()
    ]
    if len(revisions) < 2:
        return {}
    return role_lifecycle_entries_at_git_ref(revisions[1], root)


def missing_historical_decisions(
    current: list[dict], historical: list[dict]
) -> list[dict]:
    """Return committed decision records removed or mutated by the candidate."""
    current_fingerprints = {
        json.dumps(record, ensure_ascii=False, sort_keys=True, default=str)
        for record in current
        if isinstance(record, dict)
    }
    missing: list[dict] = []
    for record in historical:
        fingerprint = json.dumps(
            record, ensure_ascii=False, sort_keys=True, default=str
        )
        if fingerprint not in current_fingerprints:
            missing.append(record)
    return missing


def validate_git_privacy(validation: Validation, root: Path = ROOT) -> None:
    """Fail closed when tracked files cross the Local Privacy Boundary."""
    try:
        staged = set(git_staged_files(root))
    except (OSError, RuntimeError) as exc:
        validation.fail(f"Cannot verify staged privacy state (fail closed): {exc}")
        staged = set()
    staged_mode = bool(staged)

    ignore_file = root / ".gitignore"
    ignore_sources: list[tuple[str, bytes]] = []
    if not ignore_file.is_file():
        validation.fail("Missing .gitignore for Local Privacy Boundary")
    else:
        try:
            ignore_sources.append(("working tree", ignore_file.read_bytes()))
        except OSError as exc:
            validation.fail(f"Cannot inspect working-tree .gitignore: {exc}")
    if staged_mode:
        try:
            ignore_sources.append(("Git index", git_index_blob(".gitignore", root)))
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot inspect Git-index .gitignore: {exc}")
    for source, raw in ignore_sources:
        try:
            lines = raw.decode("utf-8").splitlines()
        except UnicodeDecodeError as exc:
            validation.fail(f"Cannot decode {source} .gitignore: {exc}")
            continue
        rules = set(lines)
        missing = sorted(REQUIRED_IGNORE_RULES - rules)
        for rule in missing:
            validation.fail(f"Missing privacy ignore rule in {source}: {rule}")
        if not missing:
            validation.ok(f"Required Local Privacy Boundary ignore rules exist in {source}")
        unsafe_negations = sorted(
            line.strip()
            for line in lines
            if line.strip().startswith("!")
            and line.strip() not in ALLOWED_GITIGNORE_NEGATIONS
        )
        for rule in unsafe_negations:
            validation.fail(f"Unsafe .gitignore negation in {source}: {rule}")
        try:
            effective_ignored = gitignore_effective_ignored_paths(raw)
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot evaluate {source} .gitignore semantics: {exc}")
            continue
        exposed = sorted(PRIVATE_GITIGNORE_SENTINELS - effective_ignored)
        hidden_shared = sorted(SHARED_GITIGNORE_SENTINELS & effective_ignored)
        for path in exposed:
            validation.fail(f"{source} .gitignore exposes private sentinel: {path}")
        for path in hidden_shared:
            validation.fail(f"{source} .gitignore hides canonical shared file: {path}")
        if not exposed and not hidden_shared and not unsafe_negations:
            validation.ok(f"{source} .gitignore effective privacy semantics pass")

    try:
        tracked = git_tracked_files(root)
    except (OSError, RuntimeError) as exc:
        validation.fail(f"Cannot verify tracked private paths (fail closed): {exc}")
        return

    violations = [
        (path, reason)
        for path in tracked
        if (reason := private_tracked_reason(path)) is not None
    ]
    for path, reason in violations:
        validation.fail(f"Tracked private path ({reason}): {path}")
    if not violations:
        validation.ok("No forbidden private path is Git tracked")

    try:
        untracked = git_untracked_files(root)
    except (OSError, RuntimeError) as exc:
        validation.fail(f"Cannot inspect untracked shared candidates: {exc}")
        untracked = []

    untracked_violations = [
        (path, reason)
        for path in untracked
        if (reason := private_tracked_reason(path)) is not None
    ]
    for path, reason in untracked_violations:
        validation.fail(f"Untracked private candidate ({reason}): {path}")
    if not untracked_violations:
        validation.ok("No untracked private path is exposed as a shared candidate")

    secret_hits: list[tuple[str, str]] = []
    for relative_path in tracked:
        try:
            raw = git_index_blob(relative_path, root)
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot inspect Git index blob {relative_path}: {exc}")
            continue
        if len(raw) > 1_000_000:
            continue
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(content) for pattern in SECRET_CONTENT_PATTERNS):
            secret_hits.append(("Git index", relative_path))

    worktree_candidates = sorted(set(tracked) | set(untracked))
    personal_path_hits: list[tuple[str, str]] = []
    for relative_path in worktree_candidates:
        target = root / relative_path
        if not target.is_file() or target.stat().st_size > 1_000_000:
            continue
        try:
            content = target.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if any(pattern.search(content) for pattern in SECRET_CONTENT_PATTERNS):
            secret_hits.append(("working tree", relative_path))
        if any(pattern.search(content) for pattern in PERSONAL_ABSOLUTE_PATH_PATTERNS):
            personal_path_hits.append(("working tree", relative_path))

    for relative_path in tracked:
        try:
            raw = git_index_blob(relative_path, root)
            if len(raw) > 1_000_000:
                continue
            content = raw.decode("utf-8")
        except (OSError, RuntimeError, UnicodeDecodeError):
            continue
        if any(pattern.search(content) for pattern in PERSONAL_ABSOLUTE_PATH_PATTERNS):
            personal_path_hits.append(("Git index", relative_path))

    for source, path in sorted(set(secret_hits)):
        validation.fail(
            f"{source} file contains a high-confidence secret signature: {path}"
        )
    if not secret_hits:
        validation.ok("No high-confidence secret signature found in Git index or shared candidates")

    for source, path in sorted(set(personal_path_hits)):
        validation.fail(f"{source} shared file contains a personal absolute path: {path}")
    if not personal_path_hits:
        validation.ok("No personal absolute path found in shared candidate files")

    readme_sources: list[tuple[str, bytes]] = []
    readme_path = root / "README.md"
    if readme_path.is_file():
        readme_sources.append(("working tree", readme_path.read_bytes()))
    if "README.md" in tracked:
        try:
            readme_sources.append(("Git index", git_index_blob("README.md", root)))
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot inspect Git-index README.md: {exc}")
    private_readme_examples = []
    for source, raw in readme_sources:
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            validation.fail(f"Cannot decode {source} README.md")
            continue
        if PRIVATE_README_INPUT_EXAMPLE_PATTERN.search(content):
            private_readme_examples.append(source)
    for source in private_readme_examples:
        validation.fail(
            f"{source} README.md contains a non-anonymous input path example"
        )
    if not private_readme_examples:
        validation.ok("README input path examples are anonymous")

    ignored_tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-ci", "--exclude-standard", "-z"],
        check=False,
        capture_output=True,
    )
    paths: list[str] = []
    if ignored_tracked.returncode:
        validation.fail("Cannot verify tracked files that are now ignored")
    else:
        paths = [
            item.decode("utf-8", errors="surrogateescape")
            for item in ignored_tracked.stdout.split(b"\0")
            if item
        ]
        for path in paths:
            validation.fail(f"Tracked file is covered by .gitignore: {path}")
    if not paths:
        validation.ok("No tracked file is accidentally covered by .gitignore")

    if os.name == "posix":
        permission_violations: list[str] = []
        for base_name in ("input", "output"):
            base = root / base_name
            if not base.exists():
                continue
            for target in base.rglob("*"):
                relative = target.relative_to(root).as_posix()
                if relative == "input/README.md":
                    continue
                if target.is_symlink():
                    permission_violations.append(f"symlink:{relative}")
                    continue
                try:
                    mode = target.stat().st_mode & 0o777
                except OSError as exc:
                    permission_violations.append(f"unreadable:{relative}:{exc}")
                    continue
                if mode & 0o077:
                    permission_violations.append(f"mode={mode:04o}:{relative}")
        for item in permission_violations:
            validation.fail(
                f"Local private state permission is too broad: {item} "
                f"(fix: chmod 700 for directories / 600 for files under "
                f"input/ and output/, e.g. "
                f"`find input output -type d -exec chmod 700 {{}} +; "
                f"find input output -type f -exec chmod 600 {{}} +`)"
            )
        if not permission_violations:
            validation.ok("Local input/output private state has owner-only permissions")

    input_readme = root / "input" / "README.md"
    input_sources: list[tuple[str, bytes]] = []
    if not input_readme.is_file():
        validation.fail("Missing anonymous input/README.md shared scaffold")
    else:
        try:
            input_sources.append(("working tree", input_readme.read_bytes()))
        except OSError as exc:
            validation.fail(f"Cannot inspect working-tree input/README.md: {exc}")
    if staged_mode:
        try:
            input_sources.append(
                ("Git index", git_index_blob("input/README.md", root))
            )
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot inspect Git-index input/README.md: {exc}")
    for source, raw in input_sources:
        digest = hashlib.sha256(raw).hexdigest()
        if digest != ANONYMOUS_INPUT_README_SHA256:
            validation.fail(
                f"{source} input/README.md is not the canonical anonymous "
                "privacy-safe scaffold"
            )
        else:
            validation.ok(
                f"{source} input/README.md matches the canonical anonymous scaffold"
            )

    if staged_mode and "profiles/current_user_profile.yaml" in tracked:
        try:
            staged_profile = yaml.safe_load(
                git_index_blob("profiles/current_user_profile.yaml", root).decode("utf-8")
            )
        except (OSError, RuntimeError, UnicodeDecodeError, yaml.YAMLError) as exc:
            validation.fail(f"Cannot inspect effective shared profile: {exc}")
        else:
            expected_user = {
                "name": None,
                "user_type": "unspecified",
                "technical_level": "unspecified",
                "decision_scope": "request_owner_decides",
            }
            if (
                not isinstance(staged_profile, dict)
                or staged_profile.get("profile_kind") != "shared_default"
                or staged_profile.get("user") != expected_user
            ):
                validation.fail("Git index shared profile contains personal attributes")


def validate_headings(
    validation: Validation, relative_path: str, headings: list[str]
) -> None:
    target = validation.require_file(relative_path)
    if target is None:
        return
    content = target.read_text(encoding="utf-8")
    for heading in headings:
        if heading not in content:
            validation.fail(f"Missing heading in {relative_path}: {heading}")
    if "TODO" in content:
        validation.fail(f"TODO placeholder remains: {relative_path}")
    validation.ok(f"Required headings present: {relative_path}")


MARKDOWN_LIST_ITEM = re.compile(r"^(?:\d+\.|[-*+])\s+(.*)")


def extract_markdown_list_section(content: str, heading: str) -> list[str] | None:
    """Return top-level bullet/numbered items directly under an H2 `heading`.

    Returns None (not an empty list) when the heading is absent, so callers
    can distinguish "section intentionally omitted" from "section present
    but empty."

    Only top-level items count. Indented child bullets belong to their parent
    item, and anything inside a fenced code block is sample text rather than a
    real list item -- counting either would make the caller's item-by-item
    comparison against skill.yaml wrong. The fence check also runs before the
    `## ` terminator so a heading quoted inside a fence cannot cut the section
    short.
    """
    lines = content.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == f"## {heading}":
            start = index + 1
            break
    if start is None:
        return None
    items: list[str] = []
    in_fence = False
    for line in lines[start:]:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            break
        if line[:1].isspace():
            continue
        match = MARKDOWN_LIST_ITEM.match(line.strip())
        if match:
            items.append(match.group(1).strip())
    return items


def normalize_skill_item(text: str) -> str:
    """Reduce a SKILL.md / skill.yaml list item to its comparable core.

    The two faces legitimately differ in presentation: SKILL.md decorates
    paths with backticks and full `ai_team/` prefixes and bolds key phrases,
    while skill.yaml writes bare filenames followed by `参照`. Neither
    difference changes what the item means, so both are normalized away before
    comparison. The wording itself survives, so a reordered or substituted
    item still reads as different.
    """
    value = unicodedata.normalize("NFKC", text)
    value = value.replace("`", "").replace("*", "")
    value = re.sub(r"ai_team/(?:[\w\-]+/)*([\w\-]+\.(?:md|yaml))", r"\1", value)
    value = re.sub(r"参照\)", ")", value)
    value = re.sub(r"参照$", "", value)
    value = re.sub(r"[（）()、,。\.:：/]", "", value)
    return re.sub(r"\s+", "", value)


def skill_item_matches(md_item: str, yaml_item: str) -> bool:
    """Whether a SKILL.md item and a skill.yaml item state the same thing.

    Containment, not equality: either face may carry detail the other omits
    (SKILL.md adds a template path, skill.yaml adds a layer-condition prefix),
    and that is additive rather than contradictory. But neither may say
    something absent from the other -- which is what catches reordering.

    Containment is used instead of a text-similarity threshold because no
    threshold separates the two classes. Measured across all 33 Skills, real
    drift scored 0.079-0.39 and benign decoration 0.39-0.99: they overlap, so
    any cutoff would either miss real drift or fail correct Skills.
    """
    left = normalize_skill_item(md_item)
    right = normalize_skill_item(yaml_item)
    return left in right or right in left


# SKILL.md heading -> skill.yaml list key that must stay in sync. A missing
# heading is skipped rather than failed (extract_markdown_list_section returns
# None); only a present-but-mismatched count fails.
#
# KNOWN GAP (2026-08-05 independent review, P2-1): the 10 lightweight FDE
# sub-Skills have no `## 完了条件`, and their `## 品質基準` carries only 1 item
# (a pointer to fde_quality_gate.md) against 4 in `done_definition`. The other
# three -- template conformance, unconfirmed-item tracking, and handoff to the
# Quality Reviewer when risk_based_quality_gates requires it -- appear nowhere
# in those SKILL.md files. This is the same "declared but not read at runtime"
# risk this check was added to close, still open for those 10. Tracked in
# ai_team/review/review_metrics.md; do not read the skip above as "handled."
SKILL_MD_YAML_LIST_PAIRS = [
    ("Workflow", "steps"),
    ("必須出力", "outputs"),
    ("禁止事項", "prohibited_actions"),
    ("完了条件", "done_definition"),
]

# (skill_id, yaml_key) pairs exempt from the drift check above: these
# `outputs` lists were already Human-Gate-approved and PROMOTEd in the Local
# Capability Layer governance cycle (2026-08-04), and intentionally
# consolidate SKILL.md's per-layer bullets into fewer prefixed entries.
# Editing them now would change skill_content_revision() and invalidate the
# promoted registry's recorded content hash (see decision_history in
# ai_team/governance/skill_lifecycle_registry.yaml) -- out of scope here.
SKILL_MD_YAML_LIST_DRIFT_EXCEPTIONS = {
    ("skill-agent-creation", "outputs"),
    ("skill-skill-creation", "outputs"),
}


def validate_skills(validation: Validation) -> None:
    if not SKILL_VALIDATOR.is_file():
        # Optional local dependency: skip (do not fail) so the validator
        # stays runnable on machines without the Codex skill-creator install.
        print(
            f"WARN: official skill validator not found ({SKILL_VALIDATOR}); "
            "skipping per-skill official validation"
        )

    for skill in SKILLS:
        base = f"skills/{skill}"
        validate_headings(validation, f"{base}/README.md", README_HEADINGS)

        data = validate_yaml(validation, f"{base}/skill.yaml")
        if data is not None:
            missing = sorted(YAML_KEYS - set(data))
            if missing:
                validation.fail(
                    f"Missing keys in {base}/skill.yaml: {', '.join(missing)}"
                )
            scope = data.get("scope")
            if not isinstance(scope, dict):
                validation.fail(f"Missing scope mapping in {base}/skill.yaml")
            else:
                for key in ["owns", "does_not_own", "handoff_to"]:
                    if not isinstance(scope.get(key), list) or not scope.get(key):
                        validation.fail(
                            f"Missing scope.{key} list in {base}/skill.yaml"
                        )
            modes = data.get("modes")
            if not isinstance(modes, dict):
                validation.fail(f"Missing modes mapping in {base}/skill.yaml")
            else:
                for key in [
                    "professional_opinion",
                    "professional_design",
                    "professional_implementation",
                    "professional_verification",
                ]:
                    mode = modes.get(key)
                    if not isinstance(mode, dict):
                        validation.fail(
                            f"Missing mode {key} in {base}/skill.yaml"
                        )
                        continue
                    for required_key in ["description", "outputs", "review_points"]:
                        if required_key not in mode:
                            validation.fail(
                                f"Missing {key}.{required_key} in "
                                f"{base}/skill.yaml"
                            )
            if data.get("name") != skill:
                validation.fail(
                    f"Skill name mismatch in {base}/skill.yaml: {data.get('name')}"
                )
            professional_only_policy = data.get("professional_only_policy")
            if (
                not isinstance(professional_only_policy, list)
                or not professional_only_policy
            ):
                validation.fail(
                    f"Missing professional_only_policy list in {base}/skill.yaml"
                )
            non_professional_outputs = data.get("non_professional_outputs")
            if (
                not isinstance(non_professional_outputs, list)
                or not non_professional_outputs
                or not any("根拠" in str(item) for item in non_professional_outputs)
            ):
                validation.fail(
                    f"Missing non_professional_outputs list in {base}/skill.yaml"
                )
            expected_legacy_id = skill.replace("-", "_")
            if data.get("legacy_id") != expected_legacy_id:
                validation.fail(
                    f"Legacy ID mismatch in {base}/skill.yaml: "
                    f"{data.get('legacy_id')}"
                )
            collaboration = data.get("collaboration", [])
            done_definition = data.get("done_definition", [])
            if skill == "skill-engineering-knowledge-curator":
                if "AI Deliverable Quality Reviewer" not in collaboration:
                    validation.fail(
                        f"Final reviewer missing from collaboration in "
                        f"{base}/skill.yaml"
                    )
                if not any(
                    "obsidian_sync_summary.md" in str(item)
                    for item in done_definition
                ):
                    validation.fail(
                        f"Obsidian sync summary missing from done_definition in "
                        f"{base}/skill.yaml"
                    )
            elif skill != "skill-deliverable-quality-reviewer":
                if "AI Deliverable Quality Reviewer" not in collaboration:
                    validation.fail(
                        f"Final reviewer missing from collaboration in "
                        f"{base}/skill.yaml"
                    )
                if not any(
                    "risk_based_quality_gates" in str(item)
                    and "required" in str(item)
                    and "Quality Reviewer" in str(item)
                    for item in done_definition
                ):
                    validation.fail(
                        f"Risk-conditional final review missing from done_definition in "
                        f"{base}/skill.yaml"
                    )
            else:
                expected_verdicts = {
                    "PASS",
                    "PASS_WITH_CONDITIONS",
                    "REWORK_REQUIRED",
                    "BLOCKED",
                }
                if set(data.get("verdicts", [])) != expected_verdicts:
                    validation.fail(
                        f"Invalid verdicts in {base}/skill.yaml"
                    )

        openai_data = validate_yaml(validation, f"{base}/agents/openai.yaml")
        if openai_data is not None:
            interface = openai_data.get("interface")
            if not isinstance(interface, dict):
                validation.fail(f"Missing interface in {base}/agents/openai.yaml")
            else:
                short_description = interface.get("short_description", "")
                if not isinstance(short_description, str) or not (
                    25 <= len(short_description) <= 64
                ):
                    validation.fail(
                        f"Invalid short_description length in "
                        f"{base}/agents/openai.yaml"
                    )
                default_prompt = interface.get("default_prompt", "")
                if (
                    not isinstance(default_prompt, str)
                    or f"${skill}" not in default_prompt
                ):
                    validation.fail(
                        f"default_prompt must reference ${skill} in "
                        f"{base}/agents/openai.yaml"
                    )

        skill_md = validation.require_file(f"{base}/SKILL.md")
        if skill_md is not None:
            content = skill_md.read_text(encoding="utf-8")
            if "TODO" in content:
                validation.fail(f"TODO placeholder remains: {base}/SKILL.md")
            if len(content.splitlines()) > 500:
                validation.fail(f"SKILL.md exceeds 500 lines: {base}/SKILL.md")
            if data is not None:
                for heading, yaml_key in SKILL_MD_YAML_LIST_PAIRS:
                    if (skill, yaml_key) in SKILL_MD_YAML_LIST_DRIFT_EXCEPTIONS:
                        continue
                    md_items = extract_markdown_list_section(content, heading)
                    if md_items is None:
                        continue
                    yaml_items = data.get(yaml_key, [])
                    if not isinstance(yaml_items, list):
                        # len() on a bare string would silently count
                        # characters and compare them against an item count.
                        validation.fail(
                            f"skill.yaml {yaml_key} must be a list: "
                            f"{base}/skill.yaml has "
                            f"{type(yaml_items).__name__}"
                        )
                        continue
                    if len(md_items) != len(yaml_items):
                        validation.fail(
                            f"SKILL.md/skill.yaml drift in {base}: "
                            f"## {heading} has {len(md_items)} item(s) but "
                            f"skill.yaml {yaml_key} has {len(yaml_items)} item(s)"
                        )

        if SKILL_VALIDATOR.is_file():
            result = subprocess.run(
                ["python3", str(SKILL_VALIDATOR), str(ROOT / base)],
                check=False,
                capture_output=True,
                text=True,
            )
            if result.returncode:
                detail = (result.stdout + result.stderr).strip()
                validation.fail(f"Official validator failed for {skill}: {detail}")
            else:
                validation.ok(f"Official validator passed: {skill}")


DEV_TEMPLATES_DIR = "templates/development"
DEV_TEMPLATE_LINK = re.compile(r"`([^`\s]+\.md)`")
DEV_MATRIX_TYPES = ["DP", "AP", "SY", "APP", "WEB", "AI", "INT", "INF", "OPS", "POC"]
DEV_TYPE_COVERS = {
    "DP": "data_platform.md",
    "AP": "analytics_platform.md",
    "SY": "system_development.md",
    "APP": "application_development.md",
    "WEB": "web_content.md",
    "AI": "ai_ml_llm.md",
    "INT": "integration.md",
    "INF": "cloud_infrastructure.md",
    "OPS": "maintenance.md",
    "POC": "poc.md",
}


def validate_development_templates(validation: Validation) -> None:
    """Lock document_map.md and the actual template files to each other.

    Contract: every backtick .md reference in document_map.md and the set
    covers must resolve to a real file, and every template file under
    templates/development/ must be indexed by document_map.md or a set cover.
    """
    base = ROOT / DEV_TEMPLATES_DIR
    doc_map = validation.require_file(f"{DEV_TEMPLATES_DIR}/document_map.md")
    validation.require_file(f"{DEV_TEMPLATES_DIR}/development_doc_standards.md")
    validation.require_file(f"{DEV_TEMPLATES_DIR}/sets/set_cover_template.md")
    if doc_map is None:
        return

    def check_links(source: Path, relative_to: Path, label: str) -> None:
        broken = [
            link
            for link in DEV_TEMPLATE_LINK.findall(
                source.read_text(encoding="utf-8")
            )
            if not (relative_to / link).resolve().is_file()
        ]
        for link in broken:
            validation.fail(f"Broken template reference in {label}: {link}")
        if not broken:
            validation.ok(f"Template references resolve: {label}")

    check_links(doc_map, base, f"{DEV_TEMPLATES_DIR}/document_map.md")

    index_text = doc_map.read_text(encoding="utf-8")
    sets_dir = base / "sets"
    for cover in sorted(sets_dir.glob("*.md")):
        if cover.name == "set_cover_template.md":
            continue
        if f"sets/{cover.name}" not in index_text:
            validation.fail(
                f"Set cover not listed in document_map.md: sets/{cover.name}"
            )
        else:
            validation.ok(f"Set cover indexed in document_map.md: {cover.name}")
        check_links(cover, sets_dir, f"{DEV_TEMPLATES_DIR}/sets/{cover.name}")
        index_text += cover.read_text(encoding="utf-8")

    for template_file in sorted(base.rglob("*_template.md")):
        rel = template_file.relative_to(base).as_posix()
        if rel == "sets/set_cover_template.md":
            continue
        if template_file.name not in index_text:
            validation.fail(
                "Template not indexed by document_map.md or a set cover: "
                f"{DEV_TEMPLATES_DIR}/{rel}"
            )
        else:
            validation.ok(f"Development template indexed: {rel}")

    # Matrix <-> set cover consistency: every ◎ document per type must be
    # listed in that type's set cover, and any listed mark must match the
    # matrix (document_map.md is the source of truth).
    matrix: dict[Path, dict[str, str]] = {}
    for line in doc_map.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 + len(DEV_MATRIX_TYPES):
            continue
        link = DEV_TEMPLATE_LINK.search(cells[2])
        if link is None:
            continue
        matrix[(base / link.group(1)).resolve()] = {
            type_id: cells[4 + idx][:1]
            for idx, type_id in enumerate(DEV_MATRIX_TYPES)
        }
    if len(matrix) < 20:
        validation.fail(
            f"document_map.md matrix parse found only {len(matrix)} rows"
        )
    else:
        validation.ok(f"document_map.md matrix parsed: {len(matrix)} rows")

    for type_id, cover_name in DEV_TYPE_COVERS.items():
        cover_path = sets_dir / cover_name
        if not cover_path.is_file():
            continue  # missing covers are reported by the set-cover loop
        cover_marks: dict[Path, str] = {}
        for line in cover_path.read_text(encoding="utf-8").splitlines():
            if not line.startswith("|"):
                continue
            cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
            if len(cells) < 6:
                continue
            link = DEV_TEMPLATE_LINK.search(cells[3])
            if link is None:
                continue
            cover_marks[(sets_dir / link.group(1)).resolve()] = (
                cells[4][:1] if cells[4] else ""
            )
        issues = 0
        for target, marks in matrix.items():
            if marks.get(type_id) == "◎" and target not in cover_marks:
                validation.fail(
                    f"Required (◎) document missing from sets/{cover_name}: "
                    f"{target.name} (type {type_id})"
                )
                issues += 1
        for target, mark in cover_marks.items():
            expected = matrix.get(target, {}).get(type_id, "")
            if expected and mark and mark != expected:
                validation.fail(
                    f"Mark mismatch in sets/{cover_name} for {target.name}: "
                    f"cover={mark} document_map={expected}"
                )
                issues += 1
        if not issues:
            validation.ok(
                f"Set cover consistent with document_map matrix: {cover_name}"
            )


FDE_DOCS_DIR = "ai_team/fde"
FDE_DOC_HEADINGS = {
    "fde_operating_model.md": [
        "## FDEとは何か", "## FDEの目的", "## FDEが解く課題", "## FDEの基本フロー",
        "## FDEの起動条件", "## FDEが出す成果物", "## FDEが連携するRole",
        "## FDEがやること", "## FDEがやらないこと", "## FDEの完了条件",
        "## よくある失敗", "## セレス向け運用上の注意", "## 他利用者向け運用上の注意",
    ],
    "fde_scope_boundary.md": [
        "## FDEの守備範囲", "## FDEが責任を持つ成果物", "## FDEが責任を持たない領域",
        "## PMOとの違い", "## Tech Leadとの違い", "## Product Managerとの違い",
        "## Consultantとの違い", "## Solution Architectとの違い",
        "## Customer Successとの違い", "## Data Engineerとの違い",
        "## LLM Application Engineerとの違い", "## 他Roleへ引き継ぐ条件",
        "## 責任境界マトリクス",
    ],
    "fde_discovery_checklist.md": [
        "## 顧客背景", "## 業務背景", "## 表面的な要望", "## 本質課題", "## 利用者",
        "## 意思決定者", "## 運用者", "## 現状業務フロー", "## 現場の痛み",
        "## 手作業・属人化", "## データ発生源", "## 既存システム", "## 既存制約",
        "## セキュリティ・権限", "## 成功条件", "## 受入条件", "## 導入時の懸念",
        "## 未決事項", "## 次に確認すること",
    ],
    "fde_business_flow_mapping_guide.md": [
        "## 目的", "## 現状業務フローの整理方法", "## To-Be業務フローの整理方法",
        "## 業務フローで必ず見る観点", "## 手作業の洗い出し", "## データ断絶の洗い出し",
        "## 承認・確認ポイント", "## 例外処理", "## システム連携ポイント",
        "## 自動化できる箇所", "## 人間判断を残すべき箇所",
        "## 業務フローから要件へ変換する方法",
    ],
    "fde_mvp_scoping_guide.md": [
        "## 目的", "## MVPとは何か", "## MVPに含める条件", "## MVPから外す条件",
        "## PoCでよい条件", "## 商用化前提にすべき条件", "## 初期リリース範囲",
        "## 将来拡張範囲", "## やらないことリスト", "## 技術負債を避ける考え方",
        "## 後回しにしてはいけない非機能要件", "## セキュリティ・運用・品質の最低ライン",
        "## MVPスコープ判断チェックリスト", "## 例",
    ],
    "fde_engineering_handoff_guide.md": [
        "## 目的", "## 引き継ぎが必要なタイミング", "## Tech Leadへ渡す情報",
        "## Backend Engineerへ渡す情報", "## Frontend Engineerへ渡す情報",
        "## Data Engineerへ渡す情報", "## Data Platform Engineerへ渡す情報",
        "## LLM Application Engineerへ渡す情報", "## Integration Engineerへ渡す情報",
        "## Security Engineerへ渡す情報", "## QA Engineerへ渡す情報",
        "## SREへ渡す情報", "## Handoffに含めるべき情報",
        "## Handoffでやってはいけないこと", "## Handoff完了条件",
    ],
    "fde_adoption_success_guide.md": [
        "## 目的", "## 導入計画", "## 利用者整理", "## 利用シーン",
        "## 初回利用までに必要なこと", "## 教育・説明", "## 運用ルール",
        "## 定着リスク", "## 定着のための対策", "## 成功指標", "## 効果測定",
        "## 利用状況の確認", "## 導入後の改善サイクル",
        "## 作って終わりを防ぐチェックリスト",
    ],
    "fde_feedback_loop.md": [
        "## 目的", "## フィードバックの種類", "## バグ", "## 仕様変更", "## 改善要望",
        "## 運用課題", "## 教育課題", "## データ品質課題", "## セキュリティ課題",
        "## 優先順位付け", "## Backlogへの変換方法",
        "## Tech Lead / PMO / QA への連携", "## 次回改善への反映",
        "## Knowledge Curatorへの連携",
    ],
    "fde_quality_gate.md": [
        "## 目的", "## FDE成果物の品質基準", "## Discovery品質チェック",
        "## Business Flow品質チェック", "## MVP Scope品質チェック",
        "## Engineering Handoff品質チェック", "## Adoption Plan品質チェック",
        "## Success Metrics品質チェック", "## Feedback Loop品質チェック",
        "## Personalization反映チェック", "## セキュリティ・運用・データ品質チェック",
        "## 不合格条件", "## 差し戻し条件", "## 完了条件",
    ],
}
FDE_TEMPLATE_HEADINGS = {
    "templates/engineering_handoff_template.md": [
        "## 本質課題", "## 非スコープ", "## 現状業務フロー", "## To-Be業務フロー",
        "## 成功指標", "## Tech Leadへの依頼", "## Backend Engineerへの依頼",
        "## Frontend Engineerへの依頼", "## Data Engineerへの依頼",
        "## Data Platform Engineerへの依頼",
        "## LLM Application Engineerへの依頼",
        "## Integration Engineerへの依頼", "## Security Engineerへの依頼",
        "## QA Engineerへの依頼", "## SREへの依頼",
    ],
    "templates/mvp_scope_template.md": [
        "## 後回しにしてはいけない非機能要件", "## セキュリティ最低ライン",
        "## 運用最低ライン", "## データ品質最低ライン",
    ],
    "templates/field_discovery_template.md": [
        "## データ発生源", "## セキュリティ・権限", "## 成功条件", "## 受入条件",
    ],
}


def validate_fde_documents(validation: Validation) -> None:
    """Lock the FDE operating docs, the personalization files, and the
    strengthened FDE template sections to the approved contract."""
    for name, headings in FDE_DOC_HEADINGS.items():
        validate_headings(validation, f"{FDE_DOCS_DIR}/{name}", headings)
    for path, headings in FDE_TEMPLATE_HEADINGS.items():
        validate_headings(validation, path, headings)
    validation.require_file("ai_team/personalization_policy.md")
    profile = validate_yaml(validation, "profiles/current_user_profile.yaml")
    if profile is not None:
        expected_root_keys = {"schema_version", "profile_kind", "user", "output_preferences"}
        if set(profile) != expected_root_keys:
            validation.fail("Tracked shared profile has unexpected personal fields")
        if profile.get("profile_kind") != "shared_default":
            validation.fail(
                "profiles/current_user_profile.yaml must be an anonymous shared default"
            )
        user = profile.get("user", {})
        expected_user = {
            "name": None,
            "user_type": "unspecified",
            "technical_level": "unspecified",
            "decision_scope": "request_owner_decides",
        }
        if not isinstance(user, dict) or user != expected_user:
            validation.fail("Tracked shared profile must not contain a user name")
        else:
            validation.ok("Tracked profile contains no personal identity")


def validate_capability_foundation(validation: Validation) -> None:
    """Validate the structured capability, lifecycle, evidence, and eval contracts."""
    for relative_path in FOUNDATION_FILES:
        validation.require_file(relative_path)

    architecture = validate_yaml(
        validation, "ai_team/governance/architecture_contract.yaml"
    )
    if architecture is not None:
        architecture_error_count = len(validation.errors)
        if architecture.get("execution", {}).get("binding") != "caller_runtime":
            validation.fail("Architecture contract must bind to caller_runtime")
        for key in (
            "runtime_switching", "cross_provider_invocation", "provider_fallback",
            "dynamic_provider_switching",
        ):
            if architecture.get("execution", {}).get(key) != "forbidden":
                validation.fail(f"Architecture execution contract must forbid: {key}")
        if architecture.get("execution", {}).get("recommendation_is_enforcement") is not False:
            validation.fail("Architecture contract must keep Recommendation separate from Enforcement")
        if not architecture.get("identity", {}).get("provider_neutral"):
            validation.fail("Architecture contract must require provider-neutral identity")
        if set(architecture.get("identity", {}).get("forbidden_bindings", [])) != {
            "provider", "model", "vendor_specific_identity"
        }:
            validation.fail("Architecture identity forbidden bindings are incomplete")
        if architecture.get("knowledge_priority") != [
            "current_explicit_request", "current_evidence", "user_local_second_brain",
            "shared_ai_employee_core", "general_model_knowledge",
        ]:
            validation.fail("Architecture knowledge priority is invalid")
        if architecture.get("growth_authority", {}).get("canonical_authority") != "celes_environment":
            validation.fail("Architecture contract must preserve Celes growth authority")
        if architecture.get("growth_authority", {}).get("other_user_telemetry_collection") != "forbidden":
            validation.fail("Architecture contract must forbid other-user telemetry")
        if architecture.get("growth_authority", {}).get("automatic_remote_sync") != "forbidden":
            validation.fail("Architecture contract must forbid automatic remote sync")
        if architecture.get("growth_authority", {}).get("automatic_git_push") != "forbidden":
            validation.fail("Architecture contract must forbid automatic Git push")
        required_promotion = {"before_after_eval", "independent_review", "celes_human_gate"}
        if set(architecture.get("growth_authority", {}).get("promotion_requires", [])) != required_promotion:
            validation.fail("Architecture promotion requirements are incomplete")
        detection = architecture.get("growth_authority", {}).get(
            "canonical_environment_detection", {}
        )
        if set(detection.get("checks", [])) != {
            "origin_url_matches_canonical_repository",
            "push_permission_confirmed",
        }:
            validation.fail("Canonical environment detection checks are incomplete")
        if detection.get("all_checks_required") is not True:
            validation.fail("Canonical environment detection must require all checks")
        if detection.get("unknown_result") != "derived_environment":
            validation.fail("Canonical environment detection must fail safe to derived")
        if detection.get("push_permission_check_override") != "forbidden":
            validation.fail("Canonical environment push permission check must not be overridable")
        if detection.get("push_permission_is_sufficient_for_shared_core_write") is not False:
            validation.fail("Push permission must not be sufficient for shared core writes")
        # A declared override that widened beyond the origin-URL check would silently
        # reopen the self-declaration bypass these two checks above close.
        if detection.get("explicit_user_declaration_override") != "origin_url_check_only":
            validation.fail(
                "Explicit user declaration must override only the origin URL check"
            )
        if detection.get("shared_core_write_additionally_requires") != "celes_explicit_instruction":
            validation.fail(
                "Shared core writes must additionally require an explicit Celes instruction"
            )
        if (
            detection.get("url_comparison")
            != "strip_scheme_userinfo_and_git_suffix_lowercase_host"
        ):
            validation.fail("Canonical repository URL comparison rule is not declared")
        canonical_repository = architecture.get("growth_authority", {}).get(
            "canonical_repository"
        )
        if not isinstance(canonical_repository, str) or not canonical_repository.strip():
            validation.fail("Canonical repository identifier is not declared")
        layers = architecture.get("capability_layers", {})
        if layers.get("shared_core", {}).get("roots") != SHARED_CORE_ROOTS:
            validation.fail("Shared core roots do not match the declared contract")
        user_local = layers.get("user_local", {})
        if user_local.get("root") != ".local/capability/**":
            validation.fail("User-local capability layer root is not declared")
        if user_local.get("distribution") != "forbidden":
            validation.fail("User-local capability layer must not be distributed")
        if user_local.get("may_override_shared_core") is not False:
            validation.fail("User-local capability layer must not override shared core")
        if user_local.get("absence_behavior") != "continue_without_error":
            validation.fail("Missing user-local capability layer must be a no-op")
        if set(user_local.get("promotion_to_shared_core_requires", [])) != required_promotion:
            validation.fail("User-local promotion requirements must match canonical promotion")
        if layers.get("derived_environment_write_targets") != ["user_local"]:
            validation.fail("Derived environments must write only to the user-local layer")
        if layers.get("shared_core", {}).get("write_authority") != "celes_environment":
            validation.fail("Shared core write authority must remain the Celes environment")
        if not architecture.get("conflict_resolution", {}).get("current_evidence_overrides_second_brain"):
            validation.fail("Architecture contract must prioritize Current Evidence over Second Brain")
        private_state = set(architecture.get("privacy", {}).get("private_state", []))
        for required_private in ("output/**", "**/_internal/**", ".local/**", "second_brain/**", "evidence/**"):
            if required_private not in private_state:
                validation.fail(f"Architecture privacy boundary missing: {required_private}")
        # privacy.shared_state duplicates the shared-core roots for a different
        # purpose (marking them non-private); it must not drift from
        # SHARED_CORE_ROOTS the way shared_core.roots is pinned above.
        shared_state = set(architecture.get("privacy", {}).get("shared_state", []))
        if not set(SHARED_CORE_ROOTS) <= shared_state:
            validation.fail("Architecture privacy shared_state does not match the shared-core roots")
        local_permissions = architecture.get("privacy", {}).get(
            "local_filesystem_permissions", {}
        )
        if local_permissions != {
            "directories": "0700",
            "files": "0600",
            "shared_group_exception": "explicit_user_decision_only",
        }:
            validation.fail("Architecture local private permissions are incomplete")
        if len(validation.errors) == architecture_error_count:
            validation.ok("Architecture contract preserves runtime, identity, and authority")

    capability_role_ids = set(configured_role_ids(ROOT))
    capability = validate_yaml(validation, "ai_team/capability_registry.yaml")
    if capability is not None:
        entries = capability.get("roles")
        if not isinstance(entries, list):
            validation.fail("Capability registry roles must be a list")
        else:
            ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
            expected_minimum = set(ROLES)
            capability_role_ids = set(ids)
            if len(ids) != len(set(ids)):
                validation.fail("Capability registry contains duplicate role IDs")
            if not expected_minimum <= set(ids):
                validation.fail(
                    "Capability registry removed baseline Roles: "
                    f"missing={sorted(expected_minimum - set(ids))}"
                )
            required = {
                "ownership",
                "capabilities",
                "decision_rights",
                "escalation_conditions",
                "supported_task_types",
                "unsuitable_task_types",
                "handoff_rules_ref",
                "done_definition_ref",
            }
            for entry in entries:
                if not isinstance(entry, dict):
                    validation.fail("Capability registry role entry is not a mapping")
                    continue
                missing = required - set(entry)
                if missing:
                    validation.fail(
                        f"Capability role {entry.get('id')} missing: {sorted(missing)}"
                    )
                if entry.get("primary_skill") not in SKILLS:
                    validation.fail(
                        f"Capability role {entry.get('id')} has unknown primary_skill"
                    )
                capabilities = entry.get("capabilities")
                if not isinstance(capabilities, dict) or not capabilities:
                    validation.fail(
                        f"Capability role {entry.get('id')} has no capabilities"
                    )
                else:
                    for name, value in capabilities.items():
                        if not isinstance(value, dict):
                            validation.fail(
                                f"Capability {entry.get('id')}.{name} is not a mapping"
                            )
                            continue
                        if value.get("criticality") not in {"low", "medium", "high"}:
                            validation.fail(
                                f"Invalid capability criticality: {entry.get('id')}.{name}"
                            )
                        if value.get("evaluation") not in {
                            "not_evaluated",
                            "baseline_pending",
                            "evaluated",
                        }:
                            validation.fail(
                                f"Invalid capability evaluation: {entry.get('id')}.{name}"
                            )
                        if "score" in value:
                            validation.fail(
                                f"Unevidenced numeric score field is forbidden: "
                                f"{entry.get('id')}.{name}"
                            )
                for reference_key in (
                    "role_document",
                    "handoff_rules_ref",
                    "done_definition_ref",
                ):
                    reference = str(entry.get(reference_key, "")).split("#", 1)[0]
                    if not reference or not (ROOT / reference).is_file():
                        validation.fail(
                            f"Broken capability registry reference for "
                            f"{entry.get('id')}: {reference_key}={reference}"
                        )
            if expected_minimum <= set(ids):
                validation.ok(
                    f"Capability registry covers {len(set(ids))} Roles "
                    "without removing the baseline set"
                )

    role_lifecycle = validate_yaml(
        validation, "ai_team/governance/ai_employee_lifecycle_registry.yaml"
    )
    if role_lifecycle is not None:
        role_entries = role_lifecycle.get("roles")
        if not isinstance(role_entries, list):
            validation.fail("AI Employee lifecycle roles must be a list")
            role_entries = []
        role_ids = [
            entry.get("id")
            for entry in role_entries
            if isinstance(entry, dict)
        ]
        if len(role_ids) != len(set(role_ids)):
            validation.fail("AI Employee lifecycle contains duplicate Role IDs")
        if set(role_ids) != capability_role_ids:
            validation.fail(
                "AI Employee lifecycle Role set mismatch: "
                f"missing={sorted(capability_role_ids - set(role_ids))}, "
                f"extra={sorted(set(role_ids) - capability_role_ids)}"
            )
        expected_role_states = {
            "DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED",
            "INDEPENDENTLY_REVIEWED", "HUMAN_GATE", "ACTIVE", "DEPRECATED",
        }
        expected_role_dispositions = {
            "CREATE", "KEEP", "UPDATE", "MERGE", "SPLIT", "DEPRECATE",
            "UNKNOWN",
        }
        if set(role_lifecycle.get("lifecycle_states", [])) != expected_role_states:
            validation.fail("AI Employee lifecycle states are invalid")
        if set(role_lifecycle.get("dispositions", [])) != expected_role_dispositions:
            validation.fail("AI Employee lifecycle dispositions are invalid")
        if role_lifecycle.get("revision_strategy", {}).get("algorithm") != "sha256":
            validation.fail("AI Employee revision strategy must be content-addressed")
        create_requirements = set(
            role_lifecycle.get("decision_rules", {}).get("create_requires", [])
        )
        if create_requirements != ROLE_CREATE_REQUIREMENTS:
            validation.fail("AI Employee CREATE decision rules are incomplete")
        candidate_fields = set(
            role_lifecycle.get("candidate_contract", {}).get(
                "required_fields", []
            )
        )
        if candidate_fields != {
            "candidate_revision", "evidence_refs", "transition",
        }:
            validation.fail("AI Employee candidate contract is incomplete")
        transition_fields = set(
            role_lifecycle.get("transition_record_contract", {}).get(
                "required_fields", []
            )
        )
        if transition_fields != ROLE_TRANSITION_FIELDS:
            validation.fail("AI Employee transition record contract is incomplete")
        baseline_import = role_lifecycle.get("baseline_import", {})
        baseline_head = baseline_import.get("repository_head")
        baseline_role_revisions = baseline_import.get("role_revisions")
        if (
            baseline_head != ROLE_LIFECYCLE_BASELINE_HEAD
            or baseline_import.get("immutable") is not True
            or baseline_role_revisions != ROLE_LIFECYCLE_BASELINE_REVISIONS
        ):
            validation.fail("AI Employee baseline import must remain immutable")
        for baseline_role, recorded_revision in (
            ROLE_LIFECYCLE_BASELINE_REVISIONS.items()
        ):
            git_revision = role_git_revision(
                baseline_role, ROLE_LIFECYCLE_BASELINE_HEAD, ROOT
            )
            if git_revision is not None and git_revision != recorded_revision:
                validation.fail(
                    f"AI Employee baseline Git cross-check failed: {baseline_role}"
                )
        decision_contract = role_lifecycle.get("decision_history_contract", {})
        if (
            set(decision_contract.get("decisions", []))
            != {"PROMOTE", "REJECT", "REWORK", "ROLLBACK"}
            or set(decision_contract.get("required_fields", []))
            != {
                "schema_version", "gate_id", "decision_type", "subject_id",
                "from_revision", "subject_revision", "target_state", "disposition",
                "decision", "decided_by",
                "timestamp", "before_after_eval_ref", "independent_review_ref",
                "evidence_refs",
            }
            or set(decision_contract.get("rollback_required_fields", []))
            != {
                "promoted_revision", "rollback_revision", "reason",
                "evidence_refs", "celes_decision",
            }
            or decision_contract.get("persistence")
            != "append_only_across_reachable_git_history"
            or decision_contract.get("mutation_or_deletion") != "forbidden"
        ):
            validation.fail("AI Employee decision history contract is incomplete")
        decision_history = role_lifecycle.get("decision_history")
        if not isinstance(decision_history, list):
            validation.fail("AI Employee decision history must be a list")
            decision_history = []
        required_decision_fields = {
            "schema_version", "gate_id", "decision_type", "subject_id",
            "from_revision", "subject_revision", "target_state", "disposition",
            "decision", "decided_by", "timestamp",
            "before_after_eval_ref", "independent_review_ref", "evidence_refs",
        }
        rollback_decision_fields = {
            "promoted_revision", "rollback_revision", "reason",
            "celes_decision",
        }
        allowed_decision_fields = (
            required_decision_fields | rollback_decision_fields | {"notes"}
        )
        decision_gate_ids: list[object] = []
        for decision in decision_history:
            if (
                not isinstance(decision, dict)
                or not required_decision_fields <= set(decision)
                or set(decision) - allowed_decision_fields
            ):
                validation.fail("AI Employee decision history record is incomplete")
                continue
            decision_gate_ids.append(decision.get("gate_id"))
            if (
                decision.get("schema_version") != "1.1"
                or decision.get("decision_type") != "canonical_promotion"
                or decision.get("decision")
                not in {"PROMOTE", "REJECT", "REWORK", "ROLLBACK"}
                or decision.get("decided_by") != "Celes"
                or decision.get("subject_id") not in capability_role_ids
                or decision.get("target_state") not in expected_role_states
                or decision.get("disposition") not in expected_role_dispositions
                or (
                    decision.get("from_revision") is not None
                    and not re.fullmatch(
                        r"sha256:[0-9a-f]{64}",
                        str(decision.get("from_revision", "")),
                    )
                )
                or not re.fullmatch(
                    r"sha256:[0-9a-f]{64}",
                    str(decision.get("subject_revision", "")),
                )
                or not non_pending_reference(
                    decision.get("before_after_eval_ref")
                )
                or not non_pending_reference(
                    decision.get("independent_review_ref")
                )
                or not non_pending_reference(decision.get("gate_id"))
                or not valid_reference_list(decision.get("evidence_refs"))
                or not valid_decision_timestamp(decision.get("timestamp"))
            ):
                validation.fail("AI Employee decision history record is invalid")
            if decision.get("decision") == "ROLLBACK":
                if (
                    not rollback_decision_fields <= set(decision)
                    or not re.fullmatch(
                        r"sha256:[0-9a-f]{64}",
                        str(decision.get("promoted_revision", "")),
                    )
                    or decision.get("rollback_revision")
                    != decision.get("subject_revision")
                    or decision.get("promoted_revision")
                    == decision.get("rollback_revision")
                    or not non_pending_reference(decision.get("reason"))
                    or decision.get("celes_decision") != "ROLLBACK"
                ):
                    validation.fail(
                        "AI Employee ROLLBACK decision record is invalid"
                    )
            elif rollback_decision_fields & set(decision):
                validation.fail(
                    "Non-ROLLBACK AI Employee decision contains rollback fields"
                )
        if len(decision_gate_ids) != len(set(decision_gate_ids)):
            validation.fail("AI Employee decision history contains duplicate gate IDs")
        try:
            historical_decisions = historical_role_decision_records(ROOT)
        except (OSError, RuntimeError) as exc:
            validation.fail(
                f"Cannot verify append-only AI Employee decision history: {exc}"
            )
            historical_decisions = []
        removed_decisions = missing_historical_decisions(
            decision_history, historical_decisions
        )
        if removed_decisions:
            validation.fail(
                "AI Employee decision history removed or mutated a committed record: "
                f"{[record.get('gate_id') for record in removed_decisions]}"
            )
        required_role_fields = {
            "id", "active_revision", "state", "candidate_revision",
            "candidate_state", "disposition", "effectiveness",
            "decision_rationale", "overlap_review", "evidence_refs",
        }
        committed_role_entries = role_lifecycle_previous_entries(ROOT)
        for entry in role_entries:
            if not isinstance(entry, dict):
                validation.fail("AI Employee lifecycle entry is not a mapping")
                continue
            role_id = str(entry.get("id", ""))
            missing = required_role_fields - set(entry)
            if missing:
                validation.fail(
                    f"AI Employee lifecycle {role_id} missing: {sorted(missing)}"
                )
            if entry.get("state") not in expected_role_states:
                validation.fail(f"Invalid AI Employee lifecycle state: {role_id}")
            if entry.get("disposition") not in expected_role_dispositions:
                validation.fail(f"Invalid AI Employee disposition: {role_id}")
            if entry.get("effectiveness") not in {
                "not_evaluated", "baseline_pending", "evaluated",
            }:
                validation.fail(f"Invalid AI Employee effectiveness: {role_id}")
            if "score" in entry:
                validation.fail(
                    f"Unevidenced AI Employee numeric score is forbidden: {role_id}"
                )
            active_revision = entry.get("active_revision")
            if active_revision is not None and (
                not isinstance(active_revision, str)
                or not re.fullmatch(r"sha256:[0-9a-f]{64}", active_revision)
            ):
                validation.fail(f"Invalid AI Employee active revision: {role_id}")
            candidate_revision = entry.get("candidate_revision")
            candidate_state = entry.get("candidate_state")
            transition = entry.get("transition")
            gate_status = (
                transition.get("human_gate_status")
                if isinstance(transition, dict)
                else None
            )
            is_final_candidate = (
                candidate_state in {"ACTIVE", "DEPRECATED"}
                and gate_status in {"promoted", "rolled_back"}
            )
            baseline_revision = ROLE_LIFECYCLE_BASELINE_REVISIONS.get(role_id)
            head_revision = role_head_revision(role_id, ROOT)
            current_revision = role_content_revision(role_id, ROOT)
            previous_entry = committed_role_entries.get(role_id)
            if previous_entry is None and baseline_revision is not None:
                previous_entry = {
                    "state": "ACTIVE",
                    "disposition": "KEEP",
                    "active_revision": baseline_revision,
                }
            established_revision = (
                previous_entry.get("active_revision")
                if isinstance(previous_entry, dict)
                else None
            )
            for failure in role_registry_state_failures(entry, previous_entry):
                validation.fail(
                    f"AI Employee registry state {failure}: {role_id}"
                )
            expected_from_revision = None
            if previous_entry is not None:
                previous_transition = previous_entry.get("transition")
                if (
                    candidate_revision is not None
                    and previous_entry.get("candidate_revision")
                    == candidate_revision
                    and isinstance(previous_transition, dict)
                ):
                    expected_from_revision = previous_transition.get(
                        "from_revision"
                    )
                else:
                    expected_from_revision = previous_entry.get(
                        "active_revision"
                    )
            for failure in role_candidate_registration_failures(
                entry, current_revision, head_revision, previous_entry
            ):
                validation.fail(
                    f"AI Employee candidate registration {failure}: {role_id}"
                )
            if (
                candidate_revision is not None
                and isinstance(transition, dict)
                and transition.get("from_revision")
                != expected_from_revision
            ):
                validation.fail(
                    f"AI Employee candidate baseline revision mismatch: {role_id}"
                )
            if is_final_candidate:
                expected_active = current_revision
            elif established_revision is None:
                expected_active = (
                    head_revision
                    if candidate_revision is None
                    and entry.get("state") in {"ACTIVE", "DEPRECATED"}
                    else None
                )
            else:
                expected_active = head_revision
            if active_revision != expected_active:
                validation.fail(
                    f"AI Employee active revision drift: {role_id} "
                    f"expected={expected_active} actual={active_revision}"
                )
            if active_revision is not None and (
                baseline_revision is None or active_revision != baseline_revision
            ) and not any(
                isinstance(decision, dict)
                and decision.get("subject_id") == role_id
                and decision.get("subject_revision") == active_revision
                and decision.get("decision") in {"PROMOTE", "ROLLBACK"}
                for decision in decision_history
            ):
                validation.fail(
                    f"AI Employee active revision lacks Celes decision history: {role_id}"
                )
            if (candidate_revision is None) != (candidate_state is None):
                validation.fail(
                    f"AI Employee candidate revision/state must both be null or set: {role_id}"
                )
            for failure in role_create_criteria_failures(entry):
                validation.fail(
                    f"AI Employee CREATE criteria {failure}: {role_id}"
                )
            if candidate_revision is not None:
                if candidate_revision != role_content_revision(role_id, ROOT):
                    validation.fail(f"AI Employee candidate revision drift: {role_id}")
                disposition = entry.get("disposition")
                allowed_dispositions = role_allowed_dispositions(
                    established_revision
                )
                if disposition not in allowed_dispositions:
                    validation.fail(
                        f"AI Employee candidate lacks change disposition: {role_id}"
                    )
                if (
                    disposition == "UNKNOWN"
                    and candidate_state not in {"DISCOVERED", "PROPOSED"}
                ):
                    validation.fail(
                        f"AI Employee UNKNOWN candidate advanced too far: {role_id}"
                    )
                if (
                    candidate_state == "DEPRECATED"
                    and disposition != "DEPRECATE"
                ):
                    validation.fail(
                        f"AI Employee deprecation disposition mismatch: {role_id}"
                    )
                if candidate_state == "ACTIVE" and disposition == "DEPRECATE":
                    validation.fail(
                        f"AI Employee active candidate uses DEPRECATE: {role_id}"
                    )
                for failure in ai_employee_transition_failures(
                    entry, decision_history
                ):
                    validation.fail(
                        f"AI Employee candidate transition {failure}: {role_id}"
                    )
            else:
                if entry.get("state") not in {"ACTIVE", "DEPRECATED"}:
                    validation.fail(
                        f"AI Employee without candidate has non-final state: {role_id}"
                    )
                allowed_without_candidate = (
                    {"DEPRECATE"}
                    if entry.get("state") == "DEPRECATED"
                    else {"KEEP", "UNKNOWN"}
                )
                if entry.get("disposition") not in allowed_without_candidate:
                    validation.fail(
                        f"AI Employee without candidate has invalid disposition: {role_id}"
                    )
                if transition not in (None, {}):
                    validation.fail(
                        f"AI Employee without candidate has a transition: {role_id}"
                    )
                if (
                    baseline_revision is None
                    and entry.get("state") not in {"ACTIVE", "DEPRECATED"}
                ):
                    validation.fail(
                        f"New AI Employee lacks a governed candidate: {role_id}"
                    )
            if not isinstance(entry.get("decision_rationale"), str) or not entry.get("decision_rationale"):
                validation.fail(f"AI Employee decision rationale is absent: {role_id}")
            if not valid_reference_list(entry.get("evidence_refs")):
                validation.fail(f"AI Employee evidence refs are absent: {role_id}")
        if set(role_ids) == capability_role_ids:
            validation.ok(
                f"AI Employee lifecycle covers all {len(capability_role_ids)} Roles"
            )

    index = validate_yaml(validation, "skills/index.yaml")
    index_names: set[str] = set()
    if index is not None:
        entries = index.get("skills")
        if isinstance(entries, list):
            index_names = {
                entry.get("name")
                for entry in entries
                if isinstance(entry, dict) and isinstance(entry.get("name"), str)
            }
        if index_names != set(SKILLS):
            validation.fail(
                "skills/index.yaml set mismatch: "
                f"missing={sorted(set(SKILLS) - index_names)}, "
                f"extra={sorted(index_names - set(SKILLS))}"
            )
        else:
            validation.ok(f"skills/index.yaml covers all {len(SKILLS)} Skills")

    lifecycle = validate_yaml(
        validation, "ai_team/governance/skill_lifecycle_registry.yaml"
    )
    if lifecycle is not None:
        entries = lifecycle.get("skills")
        lifecycle_ids = {
            entry.get("id")
            for entry in entries or []
            if isinstance(entry, dict)
        }
        if lifecycle_ids != set(SKILLS):
            validation.fail("Skill lifecycle registry does not match Skill index")
        if "UNKNOWN" not in lifecycle.get("dispositions", []):
            validation.fail("Skill lifecycle must allow UNKNOWN for insufficient evidence")
        if lifecycle.get("revision_strategy", {}).get("algorithm") != "sha256":
            validation.fail("Skill revision strategy must be content-addressed")
        expected_states = {
            "DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED", "INDEPENDENTLY_REVIEWED",
            "HUMAN_GATE", "ACTIVE", "DEPRECATED",
        }
        expected_dispositions = {
            "CREATE", "KEEP", "UPDATE", "MERGE", "SPLIT", "DEPRECATE", "UNKNOWN",
        }
        if set(lifecycle.get("lifecycle_states", [])) != expected_states:
            validation.fail("Skill lifecycle states are invalid")
        if set(lifecycle.get("dispositions", [])) != expected_dispositions:
            validation.fail("Skill lifecycle dispositions are invalid")
        transition_fields = set(
            lifecycle.get("transition_record_contract", {}).get("required_fields", [])
        )
        expected_transition_fields = {
            "from_state", "to_state", "candidate_revision", "evidence_refs",
            "independent_review_ref", "human_gate_status",
        }
        if transition_fields != expected_transition_fields:
            validation.fail("Skill transition record contract is incomplete")
        promoted_entries: list[dict] = []
        for entry in entries or []:
            if not isinstance(entry, dict):
                validation.fail("Skill lifecycle entry is not a mapping")
                continue
            if entry.get("usage_evidence") != "unavailable":
                validation.fail(
                    f"Baseline usage evidence must not be invented: {entry.get('id')}"
                )
            if entry.get("state") not in expected_states:
                validation.fail(f"Invalid Skill lifecycle state: {entry.get('id')}")
            candidate_state = entry.get("candidate_state")
            if candidate_state not in expected_states:
                validation.fail(f"Invalid Skill candidate state: {entry.get('id')}")
            if entry.get("disposition") not in expected_dispositions:
                validation.fail(f"Invalid Skill disposition: {entry.get('id')}")
            if entry.get("effectiveness") not in {
                "not_evaluated", "baseline_pending", "evaluated"
            }:
                validation.fail(f"Invalid Skill effectiveness: {entry.get('id')}")
            active_revision = entry.get("active_revision")
            candidate_revision = entry.get("candidate_revision")
            if not isinstance(active_revision, str) or not re.fullmatch(r"sha256:[0-9a-f]{64}", active_revision):
                validation.fail(f"Skill active revision is invalid: {entry.get('id')}")
            transition = entry.get("transition")
            if (
                not isinstance(transition, dict)
                or set(transition) != expected_transition_fields
            ):
                validation.fail(
                    f"Skill transition record is incomplete: {entry.get('id')}"
                )
            else:
                if transition.get("from_state") != entry.get("state"):
                    validation.fail(
                        f"Skill transition source mismatch: {entry.get('id')}"
                    )
                if transition.get("to_state") != candidate_state:
                    validation.fail(
                        f"Skill transition state mismatch: {entry.get('id')}"
                    )
                if transition.get("candidate_revision") != candidate_revision:
                    validation.fail(
                        f"Skill transition revision mismatch: {entry.get('id')}"
                    )
                if not valid_reference_list(transition.get("evidence_refs")):
                    validation.fail(
                        f"Skill transition evidence is incomplete: {entry.get('id')}"
                    )
                if (
                    candidate_state != "ACTIVE"
                    and transition.get("human_gate_status") != "pending"
                ):
                    validation.fail(
                        f"Skill candidate bypassed pending Human Gate: {entry.get('id')}"
                    )
            is_promoted = (
                candidate_state == "ACTIVE"
                and isinstance(transition, dict)
                and transition.get("human_gate_status") == "promoted"
            )
            expected_active = (
                skill_content_revision(str(entry.get("id")), ROOT)
                if is_promoted
                else skill_head_revision(str(entry.get("id")), ROOT)
            )
            if active_revision != expected_active:
                validation.fail(
                    f"Skill active revision drift from canonical source: "
                    f"{entry.get('id')} expected={expected_active} "
                    f"actual={active_revision}"
                )
            expected_candidate = skill_content_revision(str(entry.get("id")), ROOT)
            if candidate_revision != expected_candidate:
                validation.fail(
                    f"Skill candidate revision drift: {entry.get('id')} "
                    f"expected={expected_candidate} actual={candidate_revision}"
                )
            if candidate_state in {"EVALUATED", "INDEPENDENTLY_REVIEWED", "HUMAN_GATE", "ACTIVE"}:
                if not isinstance(transition, dict) or set(transition) != expected_transition_fields:
                    validation.fail(f"Skill transition record is incomplete: {entry.get('id')}")
                elif transition.get("candidate_revision") != candidate_revision:
                    validation.fail(f"Skill transition revision mismatch: {entry.get('id')}")
                elif transition.get("to_state") != candidate_state:
                    validation.fail(f"Skill transition state mismatch: {entry.get('id')}")
                elif candidate_state in {"EVALUATED", "INDEPENDENTLY_REVIEWED", "HUMAN_GATE"}:
                    if transition.get("human_gate_status") != "pending":
                        validation.fail(f"Skill candidate bypassed pending Human Gate: {entry.get('id')}")
                    elif (
                        candidate_state in {"INDEPENDENTLY_REVIEWED", "HUMAN_GATE"}
                        and not non_pending_reference(
                            transition.get("independent_review_ref")
                        )
                    ):
                        validation.fail(f"Skill candidate bypassed Independent Review: {entry.get('id')}")
                elif candidate_state == "ACTIVE":
                    if entry.get("state") != "ACTIVE":
                        validation.fail(f"Promoted Skill is not ACTIVE: {entry.get('id')}")
                    elif active_revision != candidate_revision:
                        validation.fail(f"Promoted Skill revision mismatch: {entry.get('id')}")
                    elif transition.get("human_gate_status") != "promoted":
                        validation.fail(f"Promoted Skill lacks Celes approval: {entry.get('id')}")
                    elif not non_pending_reference(
                        transition.get("independent_review_ref")
                    ):
                        validation.fail(f"Promoted Skill lacks Independent Review: {entry.get('id')}")
                    else:
                        promoted_entries.append(entry)
        if promoted_entries:
            decision = lifecycle.get("last_promotion_decision")
            required_decision = {
                "schema_version", "gate_id", "decision", "decision_type",
                "subject_id", "from_revision", "subject_revision", "target_state",
                "disposition", "decided_by", "timestamp",
                "before_after_eval_ref", "independent_review_ref", "evidence_refs",
            }
            allowed_decision = required_decision | {"operation_plan_ref", "notes"}
            if (
                not isinstance(decision, dict)
                or not required_decision <= set(decision)
                or set(decision) - allowed_decision
            ):
                validation.fail("Promoted Skills lack a complete Celes Human Gate record")
            elif (
                decision.get("schema_version") != "1.1"
                or decision.get("decision") != "PROMOTE"
                or decision.get("decision_type") != "canonical_promotion"
                or decision.get("decided_by") != "Celes"
                or not non_pending_reference(
                    decision.get("independent_review_ref")
                )
                or not re.fullmatch(
                    r"sha256:[0-9a-f]{64}", str(decision.get("subject_revision", ""))
                )
                or not non_pending_reference(
                    decision.get("before_after_eval_ref")
                )
                or not non_pending_reference(decision.get("gate_id"))
                or not valid_reference_list(decision.get("evidence_refs"))
            ):
                validation.fail("Promoted Skills have an invalid Celes Human Gate record")
            else:
                validation.ok(
                    f"Celes Human Gate records promotion for {len(promoted_entries)} Skills"
                )
            promotion_history = lifecycle.get("promotion_history")
            if (
                not isinstance(promotion_history, list)
                or not promotion_history
                or promotion_history[-1] != decision
            ):
                validation.fail(
                    "Promoted Skills must retain an append-only promotion history"
                )
            elif len(
                {
                    item.get("gate_id")
                    for item in promotion_history
                    if isinstance(item, dict)
                }
            ) != len(promotion_history):
                validation.fail("Skill promotion history contains duplicate gate IDs")
            else:
                validation.ok("Skill promotion history retains the latest Celes decision")
            candidate_contract = lifecycle.get("candidate", {})
            if (
                candidate_contract.get("effectiveness") != "not_evaluated"
                or candidate_contract.get("improvement_type") != "structural_contract"
                or candidate_contract.get("effectiveness_claim")
                != "UNKNOWN — insufficient live evidence"
            ):
                validation.fail(
                    "Structural Skill promotion must not claim live effectiveness"
                )
        if lifecycle.get("candidate", {}).get("human_gate_status") == "pending":
            if lifecycle.get("current_candidate_decision") is not None:
                validation.fail(
                    "Pending Skill candidate must not inherit a prior Human Gate decision"
                )
        if lifecycle_ids == set(SKILLS):
            validation.ok(f"Skill lifecycle covers all {len(SKILLS)} Skills")

    growth = validate_yaml(
        validation, "ai_team/governance/capability_growth_policy.yaml"
    )
    if growth is not None:
        if growth.get("authority") != "celes_environment_only":
            validation.fail("Capability Growth authority is not Celes-only")
        duties = growth.get("separation_of_duties", {})
        if duties.get("improver_may_self_approve") is not False:
            validation.fail("Improver must not self-approve")
        promotion = growth.get("promotion", {}).get("required", [])
        for required in (
            "baseline_and_candidate_revision",
            "same_eval_contract_before_and_after",
            "independent_review",
            "celes_human_gate_record",
        ):
            if required not in promotion:
                validation.fail(f"Capability Growth promotion missing: {required}")
        local_growth = growth.get("local_growth", {})
        if local_growth.get("root") != ".local/capability":
            validation.fail("Local capability growth root is not declared")
        if local_growth.get("authority") != "current_user":
            validation.fail("Local capability growth authority must be the current user")
        if local_growth.get("git_distribution") != "forbidden":
            validation.fail("Local capability growth must not be Git distributed")
        if local_growth.get("may_override_shared_core") is not False:
            validation.fail("Local capability growth must not override shared core")
        from_local = growth.get("promotion_from_local", {})
        if from_local.get("automatic_promotion") != "forbidden":
            validation.fail("Promotion from the local layer must not be automatic")
        for required in (
            "independent_evidence_without_personal_or_customer_data",
            "independent_review",
            "celes_human_gate_record",
        ):
            if required not in from_local.get("required", []):
                validation.fail(f"Promotion from local layer missing: {required}")
        validation.ok("Capability Growth separation and promotion contract parsed")

    evidence = validate_json(
        validation, "ai_team/evidence/execution_evidence.schema.json"
    )
    if evidence is not None:
        required = set(evidence.get("required", []))
        expected = {
            "task",
            "execution_context",
            "agents",
            "skills",
            "second_brain",
            "result",
            "quality",
            "tests",
            "human_feedback",
            "improvement_signals",
        }
        if not expected <= required:
            validation.fail("Execution Evidence schema misses required sections")
        evidence_types = set(
            evidence.get("$defs", {}).get("evidenceType", {}).get("enum", [])
        )
        if evidence_types != {
            "observed",
            "declared",
            "structural",
            "inferred",
            "unavailable",
        }:
            validation.fail("Execution Evidence types are invalid")
        else:
            validation.ok("Execution Evidence schema distinguishes evidence types")

    human_gate = validate_json(
        validation, "ai_team/governance/human_gate.schema.json"
    )
    if human_gate is not None:
        properties = human_gate.get("properties", {})
        if properties.get("decided_by", {}).get("const") != "Celes":
            validation.fail("Human Gate schema must preserve Celes authority")
        decisions = set(properties.get("decision", {}).get("enum", []))
        if decisions != {"PROMOTE", "REJECT", "REWORK", "ROLLBACK", "APPROVE", "DENY"}:
            validation.fail("Human Gate decisions are incomplete")
        decision_types = set(properties.get("decision_type", {}).get("enum", []))
        if decision_types != {"canonical_promotion", "critical_operation"}:
            validation.fail("Human Gate decision types are incomplete")
        if len(human_gate.get("allOf", [])) != 3:
            validation.fail("Human Gate must constrain promotion and critical operation separately")
        else:
            validation.ok("Human Gate supports auditable promotion and critical-operation decisions")

    gates = validate_yaml(
        validation, "ai_team/review/risk_based_quality_gates.yaml"
    )
    if gates is not None:
        levels = gates.get("levels", {})
        if set(levels) != {"low", "medium", "high", "critical"}:
            validation.fail("Risk-based quality gate levels are incomplete")
        elif levels["critical"].get("human_gate") != "required":
            validation.fail("Critical risk must require Human Gate")
        else:
            validation.ok("Risk-based quality gates cover Low through Critical")

    validate_yaml(validation, "ai_team/evals/eval_catalog.yaml")
    documentation_policy = validate_yaml(
        validation, "ai_team/governance/documentation_quality_policy.yaml"
    )
    semantic_review_schema = validate_json(
        validation, "ai_team/evals/documentation_semantic_review.schema.json"
    )
    if semantic_review_schema is not None:
        required_semantic_fields = {
            "schema_version", "review_id", "timestamp", "reviewer",
            "independent", "trigger", "changed_paths", "review_targets",
            "dimensions", "findings", "verdict", "unknowns",
        }
        if not required_semantic_fields <= set(
            semantic_review_schema.get("required", [])
        ):
            validation.fail("Documentation semantic review schema is incomplete")
        if semantic_review_schema.get("additionalProperties") is not False:
            validation.fail("Documentation semantic review schema is not strict")
        if len(semantic_review_schema.get("allOf", [])) < 4:
            validation.fail(
                "Documentation semantic review verdict constraints are incomplete"
            )
        else:
            validation.ok("Documentation semantic review record contract is strict")
    if documentation_policy is not None:
        semantic_policy = documentation_policy.get("level_2_semantic", {})
        semantic_validator = semantic_policy.get("review_record_validator")
        if (
            not semantic_validator
            or not (ROOT / str(semantic_validator)).is_file()
        ):
            validation.fail("Documentation semantic review validator is absent")
    golden = validate_yaml(validation, "ai_team/evals/golden_cases.yaml")
    if golden is not None:
        cases = golden.get("cases")
        primary_skill_by_role: dict[object, object] = {}
        if isinstance(capability, dict):
            primary_skill_by_role = {
                role.get("id"): role.get("primary_skill")
                for role in capability.get("roles", [])
                if isinstance(role, dict)
            }
        required_case_fields = set(
            golden.get("case_contract", {}).get("required_fields", [])
        )
        if not isinstance(cases, list) or len(cases) < 22:
            validation.fail("Engineering Golden Cases must contain at least 22 scenarios")
        else:
            ids = [case.get("id") for case in cases if isinstance(case, dict)]
            if len(ids) != len(set(ids)):
                validation.fail("Engineering Golden Case IDs must be unique")
            for case in cases:
                if not isinstance(case, dict):
                    validation.fail("Golden Case is not a mapping")
                    continue
                missing = required_case_fields - set(case)
                if missing:
                    validation.fail(
                        f"Golden Case {case.get('id')} missing: {sorted(missing)}"
                    )
                if not set(case.get("expected_roles", [])) <= capability_role_ids:
                    validation.fail(f"Golden Case {case.get('id')} has unknown Role")
                if not set(case.get("expected_skills", [])) <= set(SKILLS):
                    validation.fail(f"Golden Case {case.get('id')} has unknown Skill")
                missing_primary_skills = {
                    primary_skill_by_role.get(role)
                    for role in case.get("expected_roles", [])
                } - set(case.get("expected_skills", []))
                missing_primary_skills.discard(None)
                if missing_primary_skills:
                    validation.fail(
                        f"Golden Case {case.get('id')} omits primary Role Skills: "
                        f"{sorted(missing_primary_skills)}"
                    )
                risk = case.get("risk")
                levels = gates.get("levels", {}) if isinstance(gates, dict) else {}
                if risk not in levels:
                    validation.fail(f"Golden Case {case.get('id')} has unknown risk: {risk}")
                    continue
                known_gates = {
                    gate
                    for contract in levels.values()
                    for gate in contract.get("gates", [])
                }
                case_gates = set(case.get("required_gates", []))
                missing_gates = set(levels[risk].get("gates", [])) - case_gates
                unknown_gates = case_gates - known_gates
                if missing_gates or unknown_gates:
                    validation.fail(
                        f"Golden Case {case.get('id')} gate mismatch: "
                        f"missing={sorted(missing_gates)}, unknown={sorted(unknown_gates)}"
                    )
                for list_field in (
                    "expected_roles", "expected_skills", "required_evidence",
                    "prohibited_actions", "artifact_assertions",
                ):
                    if not isinstance(case.get(list_field), list) or not case[list_field]:
                        validation.fail(
                            f"Golden Case {case.get('id')} has no {list_field}"
                        )
            covered_roles = {
                role
                for case in cases
                if isinstance(case, dict)
                for role in case.get("expected_roles", [])
            }
            missing_role_coverage = capability_role_ids - covered_roles
            if missing_role_coverage:
                validation.fail(
                    "Engineering Golden Cases lack Role coverage: "
                    f"{sorted(missing_role_coverage)}"
                )
            else:
                validation.ok(
                    f"Engineering Eval architecture has {len(cases)} cases "
                    "covering every Role"
                )

    fixtures = validate_yaml(validation, "ai_team/evals/case_fixtures.yaml")
    if fixtures is not None:
        results = fixtures.get("results", [])
        represented_case_ids = {
            result.get("case_id") for result in results if isinstance(result, dict)
        }
        if len(results) < 3 or not represented_case_ids:
            validation.fail("Representative Golden Case result fixtures are incomplete")
        else:
            validation.ok("Representative Golden Case result fixtures are executable")

    agent_skill_fixtures = validate_yaml(
        validation, "ai_team/evals/agent_skill_fixtures.yaml"
    )
    if agent_skill_fixtures is not None:
        expected_agent_dimensions = {
            "role_understanding", "scope_adherence", "capability_application",
            "responsibility_boundary", "handoff_quality", "evidence_discipline",
            "hallucination_resistance", "done_definition_compliance",
            "escalation_quality", "reviewer_selection_quality",
        }
        expected_skill_dimensions = {
            "correct_invocation", "task_improvement", "instruction_adherence",
            "false_positive_avoidance", "overlap_and_conflict", "output_quality",
            "context_efficiency",
        }
        agent_dimensions = set(
            agent_skill_fixtures.get("agent_contract", {}).get(
                "required_dimensions", []
            )
        )
        skill_dimensions = set(
            agent_skill_fixtures.get("skill_contract", {}).get(
                "required_dimensions", []
            )
        )
        if agent_dimensions != expected_agent_dimensions:
            validation.fail("Agent Eval dimensions are incomplete")
        if skill_dimensions != expected_skill_dimensions:
            validation.fail("Skill Eval dimensions are incomplete")
        agent_results = agent_skill_fixtures.get("agent_results", [])
        skill_results = agent_skill_fixtures.get("skill_results", [])
        if len(agent_results) < 3 or len(skill_results) < 4:
            validation.fail("Agent / Skill deterministic result fixtures are incomplete")
        else:
            validation.ok("Agent / Skill deterministic result fixtures are present")

    skill_bindings = validate_yaml(
        validation, "ai_team/evals/skill_eval_bindings.yaml"
    )
    if skill_bindings is not None:
        binding_entries = skill_bindings.get("bindings", [])
        binding_ids = {
            entry.get("skill")
            for entry in binding_entries
            if isinstance(entry, dict)
        }
        if binding_ids != set(SKILLS):
            validation.fail(
                "Skill Eval binding set mismatch: "
                f"missing={sorted(set(SKILLS) - binding_ids)}, "
                f"extra={sorted(binding_ids - set(SKILLS))}"
            )
        required_rubric = set(skill_bindings.get("required_rubric", []))
        expected_binding_rubric = {
            "correct_invocation", "task_improvement", "instruction_adherence",
            "false_positive_avoidance", "overlap_and_conflict",
            "output_quality", "context_efficiency",
        }
        if required_rubric != expected_binding_rubric:
            validation.fail(
                "Skill Eval binding rubric differs from the seven-dimension contract"
            )
        selected_by_case: dict[object, set[object]] = {}
        if isinstance(golden, dict):
            selected_by_case.update(
                {
                    case.get("id"): set(case.get("expected_skills", []))
                    for case in golden.get("cases", [])
                    if isinstance(case, dict)
                }
            )
        if isinstance(agent_skill_fixtures, dict):
            selected_by_case.update(
                {
                    result.get("fixture_id"): set(
                        result.get("expected", {}).get(
                            "selected_skills", []
                        )
                    )
                    for result in agent_skill_fixtures.get(
                        "skill_results", []
                    )
                    if isinstance(result, dict)
                }
            )
        for entry in binding_entries:
            if not isinstance(entry, dict):
                validation.fail("Skill Eval binding is not a mapping")
                continue
            if not entry.get("positive_case") or not entry.get("negative_case"):
                validation.fail(
                    f"Skill Eval binding lacks positive/negative case: "
                    f"{entry.get('skill')}"
                )
            if set(entry.get("rubric", [])) != required_rubric:
                validation.fail(
                    f"Skill Eval binding rubric mismatch: {entry.get('skill')}"
                )
            skill = entry.get("skill")
            positive_case = entry.get("positive_case")
            negative_case = entry.get("negative_case")
            if positive_case not in selected_by_case:
                validation.fail(
                    f"Skill Eval binding has unknown positive case: {skill}"
                )
            elif skill not in selected_by_case[positive_case]:
                validation.fail(
                    f"Skill Eval positive case does not select Skill: {skill}"
                )
            if negative_case not in selected_by_case:
                validation.fail(
                    f"Skill Eval binding has unknown negative case: {skill}"
                )
            elif skill in selected_by_case[negative_case]:
                validation.fail(
                    f"Skill Eval negative case selects Skill: {skill}"
                )
            if positive_case == negative_case:
                validation.fail(
                    f"Skill Eval binding reuses one case as positive and negative: {skill}"
                )
            if not entry.get("conflict_group"):
                validation.fail(
                    f"Skill Eval binding lacks conflict group: {skill}"
                )
        if binding_ids == set(SKILLS):
            validation.ok(f"Skill Eval bindings cover all {len(SKILLS)} Skills")

    canonical = validate_yaml(
        validation, "ai_team/governance/canonical_sources.yaml"
    )
    if canonical is not None:
        ownership = canonical.get("ownership", {})
        required_ownership_areas = {
            "agent_definitions", "skill_metadata", "skill_instructions",
            "skill_documentation", "skill_ui_adapters", "workflows", "policies",
            "governance", "review_contracts", "fde_contracts", "evals",
            "execution_evidence_contracts", "shared_tests", "templates",
            "documentation", "runtime_adapters", "claude_adapter",
            "shared_scaffolds", "repository_validator", "capability_registry",
            "ai_employee_lifecycle", "skill_lifecycle", "second_brain_rules",
            "runtime_recommendation",
            "model_recommendation", "generated_files", "manual_edits",
        }
        missing_areas = required_ownership_areas - set(ownership)
        for area in sorted(missing_areas):
            validation.fail(f"Canonical ownership area is missing: {area}")
        if ownership.get("generated_files", {}).get("mode") != "none_current":
            validation.fail("Generated-file ownership must declare none_current")
        if ownership.get("manual_edits", {}).get("overwrite_by_deprecated_generator") != "forbidden":
            validation.fail("Protected manual canonical edits may be overwritten")
        ownership_contract = canonical.get("ownership_contract", {})
        declared_overlays = set(
            ownership_contract.get("non_owning_overlays", [])
        )
        actual_overlays = {
            area
            for area, contract in ownership.items()
            if isinstance(contract, dict)
            and contract.get("ownership_authority") is False
        }
        if (
            ownership_contract.get("authoritative_match") != "exactly_one"
            or declared_overlays != actual_overlays
        ):
            validation.fail("Canonical exactly-one ownership contract is invalid")
        ownership_patterns_by_area: dict[str, list[str]] = {}
        for area, contract in ownership.items():
            if not isinstance(contract, dict):
                validation.fail(f"Canonical ownership entry is invalid: {area}")
                continue
            targets = contract.get("canonical", [])
            if isinstance(targets, str):
                targets = [targets]
            if contract.get("ownership_authority") is not False:
                ownership_patterns_by_area[area] = list(targets)
            if contract.get("mode") == "provider_adapter" and contract.get("identity_authority") is not False:
                validation.fail(f"Provider adapter must not own AI identity: {area}")
            for target in targets:
                matches = list(ROOT.glob(target)) if "*" in target else [ROOT / target]
                if not matches or not all(item.exists() for item in matches):
                    validation.fail(f"Canonical source target is missing: {area} -> {target}")
                for item in matches:
                    if not item.is_file():
                        continue
                    relative = item.relative_to(ROOT).as_posix()
                    reason = private_tracked_reason(relative)
                    if reason is not None:
                        validation.fail(
                            f"Canonical source crosses privacy boundary ({reason}): {area} -> {relative}"
                        )
        try:
            shared_candidates = sorted(
                set(git_tracked_files(ROOT)) | set(git_untracked_files(ROOT))
            )
        except (OSError, RuntimeError) as exc:
            validation.fail(f"Cannot verify canonical ownership coverage: {exc}")
            shared_candidates = []
        ownership_mismatches: list[tuple[str, list[str]]] = []
        for path in shared_candidates:
            if private_tracked_reason(path) is not None:
                continue
            owners = [
                area
                for area, patterns in ownership_patterns_by_area.items()
                if any(
                    canonical_pattern_matches(path, pattern)
                    for pattern in patterns
                )
            ]
            if len(owners) != 1:
                ownership_mismatches.append((path, owners))
        for path, owners in ownership_mismatches:
            validation.fail(
                f"Shared file must have exactly one canonical owner: "
                f"{path} owners={owners}"
            )
        if not ownership_mismatches:
            validation.ok(
                "Every tracked or candidate shared file has exactly one canonical owner"
            )

        historical_docs = list((ROOT / "docs" / "superpowers").rglob("*.md"))
        missing_markers = [
            item.relative_to(ROOT).as_posix()
            for item in historical_docs
            if "SUPERSEDED / HISTORICAL" not in item.read_text(encoding="utf-8")
        ]
        for path in missing_markers:
            validation.fail(f"Historical documentation lacks superseded marker: {path}")
        if not missing_markers:
            validation.ok("Historical implementation documents are marked superseded")
        try:
            tracked = set(git_tracked_files(ROOT))
        except (OSError, RuntimeError):
            tracked = set()
        for generator in canonical.get("legacy_generators", []):
            if generator.get("status") != "deprecated_local_only":
                validation.fail(f"Legacy generator is not deprecated: {generator.get('path')}")
            if generator.get("path") in tracked:
                validation.fail(f"Deprecated generator must not be tracked: {generator.get('path')}")
        validation.ok("Canonical ownership and deprecated generator contract parsed")


def validate_documentation_quality(validation: Validation) -> None:
    """Apply deterministic drift checks without pretending to do semantic review."""
    knowledge_workflow = ROOT / "ai_team/workflows/engineering_knowledge_curation_workflow.md"
    if knowledge_workflow.is_file():
        knowledge_text = knowledge_workflow.read_text(encoding="utf-8")
        required_gate = (
            "現在利用者が同期を明示した、または成果物がAcceptedかつ"
            "再利用価値ありと判定されている"
        )
        if required_gate not in knowledge_text:
            validation.fail(
                "Knowledge curation workflow lost explicit OR "
                "(Accepted AND reusable) gate"
            )
        else:
            validation.ok("Knowledge curation workflow preserves the reuse gate")

    claude_settings = validate_json(validation, ".claude/settings.json")
    if claude_settings is not None:
        hooks = claude_settings.get("hooks", {})
        post_commands = [
            hook.get("command", "")
            for entry in hooks.get("PostToolUse", [])
            if isinstance(entry, dict)
            for hook in entry.get("hooks", [])
            if isinstance(hook, dict)
        ]
        stop_commands = [
            hook.get("command", "")
            for entry in hooks.get("Stop", [])
            if isinstance(entry, dict)
            for hook in entry.get("hooks", [])
            if isinstance(hook, dict)
        ]
        if not any(".needs_validation" in command for command in post_commands):
            validation.fail("Claude adapter does not mark repository edits for validation")
        if not any(
            "validate_repository.py" in command
            and "exit \"$STATUS\"" in command
            and "|| echo" not in command
            for command in stop_commands
        ):
            validation.fail("Claude validation hook does not fail closed")
        else:
            validation.ok("Claude validation hook propagates validator failures")

    stale_patterns = {
        "output/task_retrospective.md": "use output/.../_internal/task_retrospective.md",
        "output/questions.md": "use output/.../_internal/questions.md",
        "output/obsidian_sync_summary.md": "use output/.../_internal/obsidian_sync_summary.md",
        "output/feedback_analysis.md": "use output/.../_internal/feedback_analysis.md",
        "output/team_improvement_proposal.md": "use output/.../_internal/team_improvement_proposal.md",
        "output/iteration_plan.md": "use output/.../_internal/iteration_plan.md",
        "output/sample_output_for_review.md": "use output/.../_internal/sample_output_for_review.md",
        "output/fde_sample_output_for_review.md": "do not use Local output as shared canonical documentation",
        "model_recommendation.md": "model recommendation is integrated into execution_plan.md",
        "Claude Code→Codex": "caller Runtime must not be switched",
        "実行環境をCodexへ切替": "caller Runtime must not be switched",
        "実行環境/モデル/工数の自動判定": "record execution Evidence and non-binding effort",
        "モデルを使い分ける": "do not change the caller's current Model",
        "セレス=専門家エンジニア": "use anonymous shared default and do not infer personal attributes",
    }
    targets = []
    for base in (
        ROOT / "ai_team", ROOT / "skills", ROOT / ".claude",
        ROOT / "templates", ROOT / "docs",
    ):
        targets.extend(
            path
            for path in base.rglob("*")
            if path.is_file() and path.suffix in {".md", ".yaml", ".yml", ".json"}
        )
    targets.extend(
        ROOT / name
        for name in (
            "README.md",
            "AGENTS.md",
            "CLAUDE.md",
            "claude_code_team_execution.md",
            "codex_team_execution.md",
        )
    )
    for target in targets:
        content = target.read_text(encoding="utf-8")
        relative = target.relative_to(ROOT).as_posix()
        if "SUPERSEDED / HISTORICAL" in content:
            continue
        for pattern, replacement in stale_patterns.items():
            if pattern in content:
                validation.fail(
                    f"Known documentation drift in {relative}: {pattern} ({replacement})"
                )
        for line in content.splitlines():
            if (
                "quality_review_request.mdを用意し、AI Deliverable Quality Reviewerへ引き渡している。" in line
                and "risk_based_quality_gates" not in line
            ):
                validation.fail(
                    f"Unconditional independent-review requirement in {relative}"
                )

    markdown_link = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
    broken_links: list[tuple[str, str]] = []
    for target in (item for item in targets if item.suffix == ".md"):
        content = target.read_text(encoding="utf-8")
        if "SUPERSEDED / HISTORICAL" in content:
            continue
        for raw_link in markdown_link.findall(content):
            link = raw_link.strip().strip("<>").split("#", 1)[0]
            if (
                not link
                or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", link)
                or link.startswith("/")
                or "<" in link
                or ">" in link
            ):
                continue
            candidate = (target.parent / unquote(link)).resolve()
            if not candidate.exists():
                broken_links.append(
                    (target.relative_to(ROOT).as_posix(), raw_link)
                )
    for source, link in broken_links:
        validation.fail(f"Broken Markdown reference in {source}: {link}")
    if not broken_links:
        validation.ok("Markdown references resolve across canonical documentation")

    model_pattern = re.compile(r"\b(?:Opus|Sonnet|Haiku)[0-9]|\bGPT-[0-9]", re.I)
    identity_targets = list((ROOT / "ai_team" / "roles").glob("*.md"))
    identity_targets += list((ROOT / "ai_team" / "workflows").glob("*.md"))
    for skill in SKILLS:
        identity_targets.extend(
            [
                ROOT / "skills" / skill / "SKILL.md",
                ROOT / "skills" / skill / "skill.yaml",
            ]
        )
    for target in identity_targets:
        content = target.read_text(encoding="utf-8")
        if model_pattern.search(content):
            validation.fail(
                "Provider/model fixed identity contamination: "
                f"{target.relative_to(ROOT).as_posix()}"
            )

    validate_cross_provider_code(validation, ROOT)

    exact_groups: dict[str, list[str]] = {}
    try:
        shared_paths = sorted(
            set(git_tracked_files(ROOT)) | set(git_untracked_files(ROOT))
        )
    except (OSError, RuntimeError) as exc:
        validation.fail(
            f"Cannot enumerate canonical Markdown for duplicate scan: {exc}"
        )
        shared_paths = []
    canonical_docs = [
        ROOT / relative
        for relative in shared_paths
        if relative.endswith(".md")
        and private_tracked_reason(relative) is None
        and not relative.startswith("docs/superpowers/")
        and (ROOT / relative).is_file()
    ]
    for target in canonical_docs:
        normalized = "\n".join(
            line.rstrip() for line in target.read_text(encoding="utf-8").splitlines()
        ).strip()
        exact_groups.setdefault(normalized, []).append(
            target.relative_to(ROOT).as_posix()
        )
    duplicates = [paths for paths in exact_groups.values() if len(paths) > 1]
    for paths in duplicates:
        validation.fail(f"Exact duplicate canonical documents: {paths}")
    if not duplicates:
        validation.ok("No exact duplicate shared canonical Markdown documents")

    if not any(
        error.startswith("Known documentation drift")
        or error.startswith("Provider/model fixed identity")
        for error in validation.errors
    ):
        validation.ok("Known stale paths and fixed model identities are absent")


def validate_repository() -> Validation:
    validation = Validation()

    for relative_path in [
        "README.md",
        "AGENTS.md",
        "input/README.md",
        "ai_team/README.md",
        "ai_team/team_overview.md",
        "ai_team/professional_standards.md",
        "ai_team/professional_only_policy.md",
        "ai_team/role_scope_matrix.md",
        "ai_team/request_mode_policy.md",
        "ai_team/handoff_policy.md",
        "ai_team/professional_response_templates.md",
        "ai_team/review/review_policy.md",
        "ai_team/review/quality_gate.md",
        "ai_team/review/professional_quality_gate.md",
        "ai_team/review/definition_of_done.md",
        "ai_team/review/review_matrix.md",
        "ai_team/review/review_metrics.md",
        "ai_team/review/quality_scoring_rubric.md",
        "skills/README.md",
        "skills/index.yaml",
        "requirements-dev.txt",
    ]:
        validation.require_file(relative_path)

    repository_roles = configured_role_ids(ROOT)
    for role in repository_roles:
        validate_headings(
            validation, f"ai_team/roles/{role}.md", ROLE_HEADINGS
        )

    for workflow in WORKFLOWS:
        validation.require_file(f"ai_team/workflows/{workflow}")

    for template in TEMPLATES:
        validation.require_file(f"templates/{template}")

    validate_development_templates(validation)

    validate_fde_documents(validation)

    validate_git_privacy(validation)

    validate_capability_foundation(validation)

    validate_documentation_quality(validation)

    validate_yaml(validation, "skills/index.yaml")
    validate_skills(validation)

    review_report = validation.require_file(
        "templates/quality_review_report_template.md"
    )
    if review_report is not None:
        content = review_report.read_text(encoding="utf-8")
        for required in [
            "セレス向け結論",
            "Quality Scorecard",
            "Findings",
            "Decisions Required from Celes",
            "Final Verdict Rationale",
        ]:
            if required not in content:
                validation.fail(
                    f"Quality report template missing section: {required}"
                )

    policy = validation.require_file("ai_team/review/review_policy.md")
    if policy is not None:
        content = policy.read_text(encoding="utf-8")
        for verdict in [
            "PASS",
            "PASS_WITH_CONDITIONS",
            "REWORK_REQUIRED",
            "BLOCKED",
        ]:
            if verdict not in content:
                validation.fail(f"Review policy missing verdict: {verdict}")

    professional_only = validation.require_file("ai_team/professional_only_policy.md")
    if professional_only is not None:
        content = professional_only.read_text(encoding="utf-8")
        for required in [
            "Professional Only Policy",
            "禁止する出力",
            "差し戻し条件",
            "非プロフェッショナル",
            "無根拠な同意",
        ]:
            if required not in content:
                validation.fail(
                    f"Professional Only Policy missing required text: {required}"
                )

    professional_gate = validation.require_file(
        "ai_team/review/professional_quality_gate.md"
    )
    if professional_gate is not None:
        content = professional_gate.read_text(encoding="utf-8")
        for required in [
            "非プロフェッショナル",
            "無根拠な同意",
            "REWORK_REQUIRED",
        ]:
            if required not in content:
                validation.fail(
                    f"Professional quality gate missing required text: {required}"
                )

    validation.ok("Local output content is intentionally excluded from shared validation")
    return validation


def write_report(validation: Validation) -> None:
    status = "PASS" if not validation.errors else "FAIL"
    lines = [
        "# Validation Report",
        "",
        f"- Status: **{status}**",
        f"- Successful checks: {len(validation.checks)}",
        f"- Errors: {len(validation.errors)}",
        "",
        "## Scope",
        "- Required repository files",
        f"- {len(configured_role_ids(ROOT))} role documents and required headings",
        f"- {len(SKILLS)} Skill README / SKILL.md / skill.yaml / agents/openai.yaml",
        "- Official Codex Skill frontmatter validation",
            f"- {len(WORKFLOWS)} workflows and {len(TEMPLATES)} templates",
            "- Final reviewer collaboration, verdicts, and report contract",
            "- Provider-neutral capability and Skill lifecycle registries",
            "- Execution Evidence, Golden Evals, Human Gate, and Growth contracts",
            "- Local Privacy Boundary and Git-tracked private path protection",
            "- Canonical ownership and deterministic documentation drift checks",
            "",
        ]
    if validation.errors:
        lines.extend(["## Errors", *[f"- {item}" for item in validation.errors], ""])
    lines.extend(
        [
            "## Result",
            (
                "All structural and schema checks passed."
                if not validation.errors
                else "Fix the errors above and rerun `python3 tools/validate_repository.py`."
            ),
        ]
    )
    output_dir = ROOT / "output"
    output_dir.mkdir(mode=0o700, exist_ok=True)
    if os.name == "posix":
        output_dir.chmod(0o700)
    report_path = output_dir / "validation_report.md"
    report_path.write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )
    if os.name == "posix":
        report_path.chmod(0o600)


def main() -> int:
    validation = validate_repository()
    write_report(validation)
    print(
        f"Validation {'passed' if not validation.errors else 'failed'}: "
        f"{len(validation.checks)} checks, {len(validation.errors)} errors"
    )
    for error in validation.errors:
        print(f"ERROR: {error}")
    return 1 if validation.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
