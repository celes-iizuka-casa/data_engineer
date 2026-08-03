# Project Skills

各Skillは対応Roleの専門職能として動く。全Skillは4つのProfessional Modeを持ち、プロフェッショナルではない感想、一般論、無根拠な同意を出力しない。

## 共通モード
- Professional Opinion Mode
- Professional Design Mode
- Professional Implementation Mode
- Professional Verification Mode

## Skill一覧
- `skill-engineering-pmo`: AI Engineering PMO
- `skill-forward-deployed-engineer`: AI Forward Deployed Engineer
- `skill-deliverable-quality-reviewer`: AI Deliverable Quality Reviewer
- `skill-engineering-knowledge-curator`: AI Engineering Knowledge Curator
- `skill-tech-lead`: AI Tech Lead
- `skill-fullstack-engineer`: AI Fullstack Engineer
- `skill-frontend-engineer`: AI Frontend Engineer
- `skill-backend-engineer`: AI Backend Engineer
- `skill-data-engineer`: AI Data Engineer
- `skill-data-platform-engineer`: AI Data Platform Engineer
- `skill-cloud-infrastructure-engineer`: AI Cloud / Infrastructure Engineer
- `skill-sre-platform-engineer`: AI SRE / Platform Engineer
- `skill-security-governance-engineer`: AI Security / Governance Engineer
- `skill-qa-test-automation-engineer`: AI QA / Test Automation Engineer
- `skill-llm-application-engineer`: AI / LLM Application Engineer
- `skill-devex-agent-workflow-engineer`: AI DevEx / Agent Workflow Engineer
- `skill-integration-engineer`: AI Integration Engineer
- `skill-product-manager`: AI Product Manager
- `skill-ml-engineer`: AI ML Engineer
- `skill-capability-gap-analysis`: AI Capability Architect

## Capability Architect Skill一覧

AI Capability Architect が使うチーム能力設計の職能群。依頼に対するGap判定を起点に、必要な場合のみCreation系を起動する（`ai_team/capability_gap_policy.md` の優先順位ラダー参照）。

- `skill-capability-gap-analysis`: 依頼→必要Capability抽出→既存Role / Skill対応可否→Gap分類
- `skill-agent-creation`: Agent Gap確定時のみ、新AI社員Roleを統治手順（CREATE基準 + Celes Human Gate）で追加
- `skill-skill-creation`: Skill Gap確定時のみ、既存Roleへ新Skillを契約準拠で追加
- `skill-agent-registry-management`: `agent_registry.md` / `capability_matrix.md` / `role_skill_map.md` を正本と整合維持

## FDEサブSkill一覧

`skill-forward-deployed-engineer` を親Skillとするサブ職能。工程単位で起動する（`ai_team/fde/fde_operating_model.md` の基本フロー参照）。

- `skill-field-discovery`: Discovery（背景・要望・制約・成功条件の整理）
- `skill-business-flow-mapping`: 現状/To-Be業務フローとギャップ
- `skill-stakeholder-mapping`: 利用者・意思決定者・運用者の整理
- `skill-pain-point-analysis`: 表面要望と本質課題の分離
- `skill-mvp-scoping`: MVPスコープの切り出し
- `skill-solution-framing`: 解決方針への変換
- `skill-engineering-handoff`: 実装チームへの引き継ぎ
- `skill-adoption-planning`: 導入・定着計画
- `skill-success-metrics-design`: 成功指標・効果測定の設計
- `skill-feedback-to-backlog`: フィードバックのBacklog化
