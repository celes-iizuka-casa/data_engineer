#!/usr/bin/env python3
"""Validate the AI engineering team repository structure and skill contracts."""

from __future__ import annotations

import subprocess
from pathlib import Path

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
]

TEMPLATES = [
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
        validation.fail(f"Official skill validator not found: {SKILL_VALIDATOR}")

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
                    "Quality Reviewer" in str(item) for item in done_definition
                ):
                    validation.fail(
                        f"Final review missing from done_definition in "
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
            "Decisions Required from Ceres",
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

    current_review = ROOT / "output/quality_review_report.md"
    if current_review.is_file():
        content = current_review.read_text(encoding="utf-8")
        if "**最終判定**:" not in content:
            validation.fail("Current quality review has no final verdict")
        if "Pending execution" in content:
            validation.fail("Current quality review contains pending validation")
    else:
        validation.ok("Current quality review is optional in clean clones")
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
