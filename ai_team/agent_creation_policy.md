# Agent Creation Policy

## 目的

不足能力がある場合に、新しいAI社員Roleを追加するかどうかを判断する。判断の担当RoleはAI Capability Architect（`skills/skill-agent-creation`）。

## 基本方針

- 新Role追加は最後の手段
- まず既存Role / Skillで対応できるか確認する（`capability_gap_policy.md` の優先順位ラダー）
- Skill追加で済むならRoleは増やさない
- 既存Roleの責任境界を壊す場合のみ新Roleを検討する
- 再利用性のないRoleは作らない
- 一度きりのタスク専用Roleは作らない
- 追加するRoleには明確な守備範囲を持たせる

## 新Roleを追加してよい条件

`ai_team/governance/ai_employee_lifecycle_registry.yaml` のCREATE基準7項目と同一。全て証跡付きで満たすこと。

- 能力ギャップの証跡がある（evidenced_responsibility_or_capability_gap）
- 既存Roleの更新では解決できない（existing_role_update_cannot_resolve）
- 既存Roleの統合・分割では解決できない（merge_or_split_cannot_resolve）
- 複数回再利用される価値がある（recurring_reuse_value）
- 責任境界が明確である（clear_responsibility_boundary）
- 評価可能な契約（成果物・完了条件・Quality Gate）を定義できる（evaluable_contract）
- 既存Roleとの重複が説明されている（overlap_explained）

## 新Roleを追加してはいけない条件

- 既存Roleのサブタスクにすぎない
- Skill追加で対応できる
- テンプレート追加で対応できる
- 一度きりの特殊作業である
- 責任範囲が曖昧
- 既存Roleとほぼ重複する（特にPMO / Tech Lead / FDE / Data Engineer等との重複に注意）
- 完了条件を定義できない

## 判定フロー

1. 依頼内容を解析する
2. 必要能力を抽出する
3. `capability_matrix.md` を確認する
4. `agent_registry.md` を確認する
5. 既存Roleで対応可能か判定する（定義本文の実読）
6. 既存Skillで対応可能か判定する
7. Skill追加でよいか判定する
8. 既存Role更新でよいか判定する
9. 新Roleが必要か判定する（CREATE基準7項目）
10. 新Role追加理由を記録する（`new_agent_proposal.md` / `new_agent_creation_report.md`）

## 承認とHuman Gate（共有層へ追加する場合）

本節は共有層への追加にのみ適用する。ローカル層（`.local/capability/`）への追加は現在の利用者自身が判断でき、記録先は `local_decision_log.md` になる。

- 新Roleの正式化（ACTIVE）は、常にCelesのHuman Gate記録（`ai_team/governance/human_gate.schema.json` 準拠、`ai_employee_lifecycle_registry.yaml` のdecision_history）を必要とする。
- セレスが依頼文で新Role追加を明示指示した場合は、その指示自体をHuman Gate記録のevidenceとして即時記録してよい（Gateの省略ではなく、承認の記録方法の違い）。事後にROLLBACK経路で差し戻せる。
- 「確認不要で進めて」は無制限には適用しない。適用範囲はA案（2026-08-04 セレス追認、正本）で確定する。

  **確認不要で進めてよい条件（すべて満たす場合のみ）:**
  - 依頼文で対象Role / Skill / Capabilityが明示されている
  - 既存RoleのSkill追加または軽微拡張である
  - 既存Workflowへの影響が限定的
  - Rollback可能である
  - Agent Registry / Capability Matrix / Role Skill Mapへ記録される
  - `output/execution_summary.md` に判断理由が残る

  **セレス確認を必須にする条件（いずれか該当する場合）:**
  - 新しいAI社員Roleを追加する
  - 既存Roleの責任境界を変更する
  - 複数Workflowに影響する
  - Governance / Human Gate / Lifecycleに影響する
  - Model / Effort Selectionの標準ルールに影響する
  - チーム全体構成に影響する
  - 既存Roleとの責任重複リスクがある

  新Role追加は上記いずれの条件下でも「セレス確認必須」に該当するため、実質的に確認不要での新Role追加はない（Skill追加・軽微拡張のみが確認不要の対象）。
- 明示指示がない場合は `new_agent_proposal.md` を作成し、セレスの判断を待つ（ステータス: Waiting for Celes Review）。
- 指示ベースでGateを記録する場合、承認根拠となるセレス指示原文をリポジトリへ保存し（保存先: `input/Celes/依頼/` または当該タスクの `_internal/`）、`celes-instruction:<日付>-<件名>` 参照から辿れる状態にすることを必須とする。
- 同一タスク内でACTIVEまで登録する場合は、独立レビュー報告書とBefore/After評価記録が実在するまで完了扱いにしない（`agent_lifecycle_policy.md` の順序ルール参照）。

## 追加先レイヤ

追加に着手する前に、追加先が共有層かローカル層かを `local_capability_layer_policy.md` の基準で決める。**派生環境（正本環境と判定できない環境）では共有層へ追加できない。** 派生環境で新Roleが必要になった場合は、以下の「共有層へ追加する場合」の手順を実行せず、「ローカル層へ追加する場合」だけを実行する。

## Agent追加時に必ず更新するもの（共有層へ追加する場合）

以下はセレス環境で正本へ追加する場合の手順である。派生環境では実行しない。

- `ai_team/capability_registry.yaml`（role entry）
- `ai_team/governance/ai_employee_lifecycle_registry.yaml`（CREATE candidate + transition + decision_history）
- `ai_team/roles/<new_role>.md` と `skills/skill-<new-role>/` 一式
- `ai_team/agent_registry.md` / `ai_team/capability_matrix.md` / `ai_team/role_skill_map.md`
- `ai_team/team_overview.md` / `ai_team/role_scope_matrix.md`
- `ai_team/agent_registry.md` のデフォルトモデル / デフォルト工数列（非拘束の推奨。`model_effort_selection_policy.md` 本体は新しいリスク区分が生じる場合のみ更新する）
- `ai_team/evals/golden_cases.yaml`（新RoleをカバーするGolden Case）と `skill_eval_bindings.yaml`
- `tools/validate_repository.py` のSKILLSリスト（新primary Skillがある場合）
- `README.md` / `CLAUDE.md` / `AGENTS.md` / `claude_code_team_execution.md` / `codex_team_execution.md` のRole数・一覧記述

## Agent追加時に必ず更新するもの（ローカル層へ追加する場合）

派生環境、およびセレス環境での個人的・実験的な追加はこちらを使う。共有層のファイルには一切触れない。

- `.local/capability/roles/local_<name>.md`（共有層と同じ見出し契約に準拠させる）
- `.local/capability/skills/skill-local-<name>/` 一式（必要な場合。4面ファイル契約に準拠させる）
- `.local/capability/local_capability_registry.yaml`（Role / Skillの一覧と守備範囲）
- `.local/capability/local_decision_log.md`（追加日・追加理由・Capability Gap判定・既存で足りない理由・影響範囲・Rollback手順）

Celes Human Gate、両lifecycle registryへの登録、`SKILLS` 定数・`index.yaml`・eval bindings・Golden Caseの更新は**いずれも不要**である。ローカル層は共有層のライフサイクル登録簿に載らない。

## 完了条件

**共有層へ追加した場合:**

- CREATE基準7項目の証跡が `ai_employee_lifecycle_registry.yaml` のcreate_criteriaに記録されている。
- Celes Human Gate記録（gate_id・timestamp・evidence_refs）が存在する。
- `python3 tools/validate_repository.py`・Foundationテスト・Foundation evalsがPASSしている。
- `agent_quality_gate.md` の新Agent追加チェックを全て通過している。
- 追加理由と判断ログが `new_agent_creation_report.md` に残っている。

**ローカル層へ追加した場合:**

- 追加先をローカル層と判定した根拠（正本環境か派生環境か、何を確認したか）が記録されている。
- 共有層のファイルに差分が出ていない（`git status` で確認する）。
- `local_capability_registry.yaml` と `local_decision_log.md` の両方に記録がある。
- 成果物の実行記録に、ローカル層のRole / Skillを使った事実が書かれている。

## 参照

- `ai_team/capability_gap_policy.md`
- `ai_team/local_capability_layer_policy.md`
- `ai_team/agent_lifecycle_policy.md`
- `ai_team/agent_quality_gate.md`
- `ai_team/governance/ai_employee_lifecycle_registry.yaml`
- `ai_team/governance/capability_growth_policy.yaml`
