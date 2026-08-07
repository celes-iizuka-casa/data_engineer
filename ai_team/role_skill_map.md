# Role Skill Map

## 目的

各AI社員RoleがどのSkillを使えるかを明確にする。

## 正本と本書の関係

- primary skillの正本は `ai_team/capability_registry.yaml` の各role entry、Skillの実体は `skills/index.yaml`。本書はRole→Skillの逆引きview。
- 本書は配布される共有層のRole / Skillだけを載せる。利用者ローカルで追加した分は `.local/capability/local_capability_registry.yaml` にあり、依頼受付時は本書と併せて読む（`ai_team/local_capability_layer_policy.md`）。

## Role x Skill Map

| Role | Primary Skills | Optional Skills | Related Skills | Notes |
|---|---|---|---|---|
| AI Engineering PMO | skill-engineering-pmo | — | skill-deliverable-quality-reviewer / skill-capability-gap-analysis | 成果物統合（Deliverable Optimizer）を兼務 |
| AI Capability Architect | skill-capability-gap-analysis | skill-agent-creation / skill-skill-creation / skill-agent-registry-management | skill-engineering-pmo / skill-devex-agent-workflow-engineer | Gap判定→必要時のみCreation Skillを起動 |
| AI Forward Deployed Engineer | skill-forward-deployed-engineer | skill-field-discovery / skill-business-flow-mapping / skill-stakeholder-mapping / skill-pain-point-analysis / skill-mvp-scoping / skill-solution-framing / skill-engineering-handoff / skill-adoption-planning / skill-success-metrics-design / skill-feedback-to-backlog | skill-product-manager | サブSkillは工程に応じて選択 |
| AI Deliverable Quality Reviewer | skill-deliverable-quality-reviewer | — | 全Role Skill（レビュー対象理解のため参照） | 自作成果物はレビューしない |
| AI Engineering Knowledge Curator | skill-engineering-knowledge-curator | — | skill-deliverable-quality-reviewer | obsidian_write_policyのゲート充足時のみ起動 |
| AI Tech Lead | skill-tech-lead | — | skill-cloud-infrastructure-engineer / skill-sre-platform-engineer | — |
| AI Fullstack Engineer | skill-fullstack-engineer | — | skill-frontend-engineer / skill-backend-engineer | — |
| AI Frontend Engineer | skill-frontend-engineer | — | skill-fullstack-engineer | — |
| AI Backend Engineer | skill-backend-engineer | — | skill-fullstack-engineer / skill-integration-engineer | — |
| AI Data Engineer | skill-data-engineer | — | skill-data-platform-engineer / skill-qa-test-automation-engineer | — |
| AI Data Platform Engineer | skill-data-platform-engineer | skill-data-platform-migration | skill-data-engineer / skill-cloud-infrastructure-engineer | 移行Skillはinventory・wave・照合・cutover/rollbackを担当 |
| AI Cloud / Infrastructure Engineer | skill-cloud-infrastructure-engineer | — | skill-sre-platform-engineer / skill-security-governance-engineer | — |
| AI SRE / Platform Engineer | skill-sre-platform-engineer | — | skill-cloud-infrastructure-engineer / skill-qa-test-automation-engineer | — |
| AI Security / Governance Engineer | skill-security-governance-engineer | — | skill-cloud-infrastructure-engineer / skill-backend-engineer | — |
| AI QA / Test Automation Engineer | skill-qa-test-automation-engineer | — | 全実装系Skill | — |
| AI / LLM Application Engineer | skill-llm-application-engineer | — | skill-ml-engineer / skill-data-engineer | — |
| AI DevEx / Agent Workflow Engineer | skill-devex-agent-workflow-engineer | — | skill-capability-gap-analysis / skill-skill-creation | validator・Skill契約の技術実装を支援 |
| AI Integration Engineer | skill-integration-engineer | — | skill-backend-engineer / skill-security-governance-engineer | — |
| AI Product Manager | skill-product-manager | — | skill-forward-deployed-engineer / skill-engineering-pmo | — |
| AI ML Engineer | skill-ml-engineer | — | skill-llm-application-engineer / skill-data-engineer | — |

## Skill追加時の更新ルール

- `ai_team/skill_creation_policy.md` に従い、追加と同時に本書・`capability_matrix.md`・`agent_registry.md`・`skills/index.yaml`・`skill_lifecycle_registry.yaml`・`skill_eval_bindings.yaml` を更新する。
- 追加Skillは必ずいずれかのRoleのPrimaryまたはOptionalに紐づける（宙に浮いたSkillを作らない）。

## Role追加時の更新ルール

- `ai_team/agent_creation_policy.md` に従い、追加と同時に本書へ行を追加し、primary skillを `capability_registry.yaml` と一致させる。
- 既存Roleとの Related関係（連携・境界）をNotesに1行で残す。

## 更新履歴

| 日付 | 内容 | 根拠 |
|---|---|---|
| 2026-08-02 | 初版作成。20Role×33Skillの対応を登録 | セレス指示（Capability Gap / Agent Creation機構の追加依頼） |
| 2026-08-07 | AI Data Platform EngineerのOptional Skill候補として`skill-data-platform-migration`を追加（20Role×34Skill） | CelesのSkill実装指示。Lifecycleは独立レビュー済み/HUMAN_GATE pending、ACTIVE未昇格 |
