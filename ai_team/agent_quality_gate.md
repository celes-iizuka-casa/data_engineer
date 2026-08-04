# Agent Quality Gate

## 目的

新しく追加するAI社員Roleが、既存チームの品質・責任境界・運用ルールを壊さないことを確認する。Skill追加時も該当項目を適用する。

**適用範囲**: 本ゲートは**共有層への追加にのみ適用する**。本ゲートは正本3ビュー・`capability_registry.yaml`・ライフサイクル登録簿・Golden Case・validator PASSを要求するが、ローカル層（`.local/capability/`）への追加はこれらを構造的に持たないため対象外である。ローカル層への追加は `local_capability_layer_policy.md` の完了条件を使う。

## 新Agent追加チェック

- [ ] 既存Roleでは対応できない理由が明記されているか（capability_gap_analysis / agent_need_assessment）
- [ ] Skill追加では足りない理由が明記されているか
- [ ] 守備範囲が明確か（Role定義の27見出し契約準拠）
- [ ] 責任を持たない領域が明確か
- [ ] 既存Roleとの境界が明確か（重複するRoleを名指しで説明）
- [ ] 成果物が明確か
- [ ] Quality Gate（レビュー観点・完了条件）があるか
- [ ] Model / Effort Selectionに反映されているか（`agent_registry.md` の非拘束のデフォルトモデル / 工数列。`model_effort_selection_policy.md` 本体は新しいリスク区分が生じる場合のみ更新）
- [ ] 指示ベースHuman Gateの場合、セレス指示原文が保存され `celes-instruction:` 参照が解決可能か
- [ ] Personalizationに対応しているか（`personalization_policy.md` 準拠の出力調整）
- [ ] Claude Code / Codex両対応になっているか（runtime中立。特定Runtime専用の記述がない）
- [ ] Knowledge Curatorに連携されるか（Accepted後の整理対象が定義されている）
- [ ] `agent_registry.md` に登録されているか
- [ ] `role_skill_map.md` に登録されているか
- [ ] `capability_matrix.md` に登録されているか
- [ ] `capability_registry.yaml` と `ai_employee_lifecycle_registry.yaml`（CREATE基準7項目・Celes Human Gate記録）に登録されているか
- [ ] Golden Case（`ai_team/evals/golden_cases.yaml`）が新Roleをカバーしているか
- [ ] `python3 tools/validate_repository.py`・Foundationテスト・Foundation evalsがPASSしているか

## 新Skill追加チェック

- [ ] 対象Roleの責務内か
- [ ] 既存Skill更新で足りない理由が明記されているか
- [ ] 4面ファイル（README 24見出し / skill.yaml 20キー / SKILL.md / agents/openai.yaml）が契約準拠か
- [ ] `skills/index.yaml`・`skill_lifecycle_registry.yaml`・`skill_eval_bindings.yaml` に登録されているか
- [ ] 既存Skillとの重複・競合が説明されているか（conflict_group）
- [ ] `role_skill_map.md` / `capability_matrix.md` に反映されているか

## 不合格条件

- CREATE基準7項目のいずれかに証跡がない
- 既存Roleとの重複説明がない、または境界が曖昧
- 完了条件・Quality Gateが定義されていない
- validator / Foundationテスト / Foundation evalsのいずれかがFAIL
- 登録簿（capability_registry / lifecycle registries）とview（registry / matrix / map）が不整合
- CelesのHuman Gate記録なしにACTIVE扱いしている

## 差し戻し条件

- 独立レビューでP0 / P1が検出された（REWORK_REQUIRED）
- 追加理由・判断ログが再現不能（誰が・いつ・何を根拠に、が追えない）
- 非プロフェッショナルな出力（無根拠な同意・感想）が定義に混入している

## 完了条件

- 上記チェックが全て通過し、結果が `new_agent_creation_report.md` / `new_skill_creation_report.md` に記録されている。
- 独立レビュー（AI Deliverable Quality Reviewer）のVerdictがPASSまたはPASS_WITH_CONDITIONSで、条件が要対応に記録されている。

## 参照

- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_lifecycle_policy.md`
- `ai_team/review/risk_based_quality_gates.yaml`
- `ai_team/review/professional_quality_gate.md`
