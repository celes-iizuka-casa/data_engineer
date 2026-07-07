#!/usr/bin/env python3
"""Validate the AI engineering team repository structure and skill contracts."""

from __future__ import annotations

import re
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
    validate_yaml(validation, "profiles/current_user_profile.yaml")


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
