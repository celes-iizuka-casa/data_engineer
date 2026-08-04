# AI Engineering Team

## 目的
セレスからの依頼を、専門家集団として意見・設計・実装・検証し、実務で使える成果物に変換する。

## 基本ルール
- セレスの依頼を単なる作業として扱わない。
- 必要なら反論し、代案を出す。
- プロフェッショナルではない感想、一般論、無根拠な同意を成果物に入れない。
- 不明点は断定しない。
- MVPと商用化、運用、セキュリティ、テストを同時に見る。

## 参照
- `professional_standards.md`
- `professional_only_policy.md`
- `role_scope_matrix.md`
- `request_mode_policy.md`
- `handoff_policy.md`
- `personalization_policy.md`
- `fde/fde_operating_model.md`（FDE運用モデル・起動条件）
- `fde/fde_quality_gate.md`
- `professional_response_templates.md`
- `review/professional_quality_gate.md`
- `iteration_confirmation_policy.md`
- `retrospective_policy.md`
- `obsidian_write_policy.md`
- `feedback_optimization_policy.md`
- `model_selection_policy.md`
- `model_effort_selection_policy.md`
- `runtime_selection_policy.md`
- `runtime_neutral_design_policy.md`
- `governance/architecture_contract.yaml`
- `governance/canonical_sources.yaml`
- `capability_registry.yaml`
- `governance/ai_employee_lifecycle_registry.yaml`
- `governance/skill_lifecycle_registry.yaml`
- `governance/capability_growth_policy.yaml`
- `evidence/execution_evidence.schema.json`
- `evals/eval_catalog.yaml`
- `evals/agent_skill_fixtures.yaml`
- `evals/skill_eval_bindings.yaml`
- `evals/documentation_semantic_review.schema.json`
- `review/risk_based_quality_gates.yaml`
- `output_optimization_policy.md`
- `capability_gap_policy.md`（依頼→必要Capability→Gap分類）
- `local_capability_layer_policy.md`（共有層 / ローカル層の分離。追加先レイヤの判定と正本への昇格）
- `agent_creation_policy.md`（新Role追加の判定と手順）
- `skill_creation_policy.md`（新Skill追加の判定と手順）
- `agent_lifecycle_policy.md`（Role / Skillの状態管理の運用ガイド）
- `agent_quality_gate.md`（新Agent / Skill追加時の品質ゲート）
- `agent_registry.md` / `capability_matrix.md` / `role_skill_map.md`（依頼受付時に読む一覧view。正本は `capability_registry.yaml` と governance登録簿）

Foundation EvalのPASSはdeterministicな構造契約の合格であり、live AI実務性能の合格ではない。live EvidenceがないCapability effectivenessは`UNKNOWN — insufficient evidence`とする。
