#!/usr/bin/env python3
"""Validate the AI engineering team repository structure and skill contracts."""

from __future__ import annotations

import json
import hashlib
import re
import subprocess
import tempfile
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
    "ai_team/governance/skill_lifecycle_registry.yaml",
    "ai_team/governance/documentation_quality_policy.yaml",
    "ai_team/governance/human_gate.schema.json",
    "ai_team/capability_registry.yaml",
    "ai_team/evidence/execution_evidence.schema.json",
    "ai_team/evidence/new_execution_evidence.py",
    "ai_team/evals/eval_catalog.yaml",
    "ai_team/evals/golden_cases.yaml",
    "ai_team/evals/case_fixtures.yaml",
    "ai_team/evals/run_foundation_evals.py",
    "ai_team/review/risk_based_quality_gates.yaml",
    "ai_team/tests/test_ai_team_foundation.py",
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
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"\bAKIA[A-Z0-9]{16}\b"),
    re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"),
    re.compile(r"\bgh[pousr]_[0-9A-Za-z]{36,255}\b"),
    re.compile(r"\bxox[baprs]-[0-9A-Za-z-]{10,255}\b"),
)
PERSONAL_ABSOLUTE_PATH_PATTERNS = (
    re.compile("/" + "Users" + r"/[A-Za-z0-9._-]+/"),
    re.compile("/" + "home" + r"/[A-Za-z0-9._-]+/"),
    re.compile(r"[A-Za-z]:\\" + "Users" + r"\\[^\\\s]+\\"),
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


def canonical_pattern_matches(relative_path: str, pattern: str) -> bool:
    """Match manifest globs, including files directly under a /**/* root."""
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

    if staged_mode:
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

    ignored_tracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "-ci", "--exclude-standard", "-z"],
        check=False,
        capture_output=True,
    )
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
        if not architecture.get("conflict_resolution", {}).get("current_evidence_overrides_second_brain"):
            validation.fail("Architecture contract must prioritize Current Evidence over Second Brain")
        private_state = set(architecture.get("privacy", {}).get("private_state", []))
        for required_private in ("output/**", "**/_internal/**", ".local/**", "second_brain/**", "evidence/**"):
            if required_private not in private_state:
                validation.fail(f"Architecture privacy boundary missing: {required_private}")
        if len(validation.errors) == architecture_error_count:
            validation.ok("Architecture contract preserves runtime, identity, and authority")

    capability = validate_yaml(validation, "ai_team/capability_registry.yaml")
    if capability is not None:
        entries = capability.get("roles")
        if not isinstance(entries, list):
            validation.fail("Capability registry roles must be a list")
        else:
            ids = [entry.get("id") for entry in entries if isinstance(entry, dict)]
            expected = set(ROLES)
            if len(ids) != len(set(ids)):
                validation.fail("Capability registry contains duplicate role IDs")
            if set(ids) != expected:
                validation.fail(
                    "Capability registry role set mismatch: "
                    f"missing={sorted(expected - set(ids))}, "
                    f"extra={sorted(set(ids) - expected)}"
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
            if set(ids) == expected:
                validation.ok(f"Capability registry covers all {len(expected)} roles")

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
            "DISCOVERED", "PROPOSED", "CANDIDATE", "EVALUATED", "REVIEWED",
            "HUMAN_GATE", "ACTIVE", "DEPRECATED",
        }
        expected_dispositions = {"KEEP", "UPDATE", "MERGE", "SPLIT", "DEPRECATE", "UNKNOWN"}
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
            if candidate_state in {"EVALUATED", "REVIEWED", "HUMAN_GATE", "ACTIVE"}:
                if not isinstance(transition, dict) or set(transition) != expected_transition_fields:
                    validation.fail(f"Skill transition record is incomplete: {entry.get('id')}")
                elif transition.get("candidate_revision") != candidate_revision:
                    validation.fail(f"Skill transition revision mismatch: {entry.get('id')}")
                elif transition.get("to_state") != candidate_state:
                    validation.fail(f"Skill transition state mismatch: {entry.get('id')}")
                elif candidate_state in {"EVALUATED", "REVIEWED", "HUMAN_GATE"}:
                    if transition.get("human_gate_status") != "pending":
                        validation.fail(f"Skill candidate bypassed pending Human Gate: {entry.get('id')}")
                    elif (
                        candidate_state in {"REVIEWED", "HUMAN_GATE"}
                        and transition.get("independent_review_ref") == "pending"
                    ):
                        validation.fail(f"Skill candidate bypassed Independent Review: {entry.get('id')}")
                elif candidate_state == "ACTIVE":
                    if entry.get("state") != "ACTIVE":
                        validation.fail(f"Promoted Skill is not ACTIVE: {entry.get('id')}")
                    elif active_revision != candidate_revision:
                        validation.fail(f"Promoted Skill revision mismatch: {entry.get('id')}")
                    elif transition.get("human_gate_status") != "promoted":
                        validation.fail(f"Promoted Skill lacks Celes approval: {entry.get('id')}")
                    elif transition.get("independent_review_ref") == "pending":
                        validation.fail(f"Promoted Skill lacks Independent Review: {entry.get('id')}")
                    else:
                        promoted_entries.append(entry)
        if promoted_entries:
            decision = lifecycle.get("human_gate_decision")
            required_decision = {
                "id", "decision", "decision_type", "decided_by", "timestamp",
                "independent_review_ref", "release_history_decision",
            }
            if not isinstance(decision, dict) or set(decision) != required_decision:
                validation.fail("Promoted Skills lack a complete Celes Human Gate record")
            elif (
                decision.get("decision") != "PROMOTE"
                or decision.get("decision_type") != "canonical_promotion"
                or decision.get("decided_by") != "Celes"
                or decision.get("independent_review_ref") == "pending"
            ):
                validation.fail("Promoted Skills have an invalid Celes Human Gate record")
            else:
                validation.ok(
                    f"Celes Human Gate records promotion for {len(promoted_entries)} Skills"
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
        if len(human_gate.get("allOf", [])) != 2:
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
    golden = validate_yaml(validation, "ai_team/evals/golden_cases.yaml")
    if golden is not None:
        cases = golden.get("cases")
        required_case_fields = set(
            golden.get("case_contract", {}).get("required_fields", [])
        )
        if not isinstance(cases, list) or len(cases) != 15:
            validation.fail("Engineering Golden Cases must contain 15 scenarios")
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
                if not set(case.get("expected_roles", [])) <= set(ROLES):
                    validation.fail(f"Golden Case {case.get('id')} has unknown Role")
                if not set(case.get("expected_skills", [])) <= set(SKILLS):
                    validation.fail(f"Golden Case {case.get('id')} has unknown Skill")
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
            validation.ok("Engineering Eval architecture has 15 representative cases")

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
            "skill_lifecycle", "second_brain_rules", "runtime_recommendation",
            "model_recommendation", "generated_files", "manual_edits",
        }
        missing_areas = required_ownership_areas - set(ownership)
        for area in sorted(missing_areas):
            validation.fail(f"Canonical ownership area is missing: {area}")
        if ownership.get("generated_files", {}).get("mode") != "none_current":
            validation.fail("Generated-file ownership must declare none_current")
        if ownership.get("manual_edits", {}).get("overwrite_by_deprecated_generator") != "forbidden":
            validation.fail("Protected manual canonical edits may be overwritten")
        ownership_patterns: list[str] = []
        for area, contract in ownership.items():
            if not isinstance(contract, dict):
                validation.fail(f"Canonical ownership entry is invalid: {area}")
                continue
            targets = contract.get("canonical", [])
            if isinstance(targets, str):
                targets = [targets]
            ownership_patterns.extend(targets)
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
        unowned = [
            path
            for path in shared_candidates
            if private_tracked_reason(path) is None
            and not any(canonical_pattern_matches(path, pattern) for pattern in ownership_patterns)
        ]
        for path in unowned:
            validation.fail(f"Shared file has no canonical ownership entry: {path}")
        if not unowned:
            validation.ok("Every tracked or candidate shared file has canonical ownership")

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

    code_patterns = (
        re.compile(r"^\s*(?:from|import)\s+openai\b", re.M),
        re.compile(r"^\s*(?:from|import)\s+anthropic\b", re.M),
        re.compile(r"https://api\.(?:openai|anthropic)\.com", re.I),
    )
    for target in (ROOT / "ai_team").rglob("*.py"):
        if target.name.startswith("test_"):
            continue
        content = target.read_text(encoding="utf-8")
        if any(pattern.search(content) for pattern in code_patterns):
            validation.fail(
                f"Cross-provider invocation code is forbidden: "
                f"{target.relative_to(ROOT).as_posix()}"
            )

    exact_groups: dict[str, list[str]] = {}
    canonical_docs = list((ROOT / "ai_team").glob("*.md"))
    canonical_docs += list((ROOT / "ai_team" / "workflows").glob("*.md"))
    canonical_docs += list((ROOT / "ai_team" / "review").glob("*.md"))
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
        validation.ok("No exact duplicate canonical policy/workflow/review documents")

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

    for role in ROLES:
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
        f"- {len(ROLES)} role documents and required headings",
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
    (ROOT / "output").mkdir(exist_ok=True)
    (ROOT / "output" / "validation_report.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


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
