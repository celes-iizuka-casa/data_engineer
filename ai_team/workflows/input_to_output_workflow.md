# Input to Output Workflow

## 目的
`input/` の依頼を、Professional Modeに分類し、専門Roleの成果物と品質レビューへつなげる。

## 手順

1. **input / context確認**: 入力ファイル、既存output、制約を確認する。`personalization_policy.md` に従い Current Explicit Request > Current Evidence > User-local Second Brain > Shared Core の順で読み、`.local/user_profile.yaml` がなければ匿名shared defaultを使う。個人属性は推測しない。`.local/capability/local_capability_registry.yaml` が存在する場合は、利用可能なRole / Skillの一覧として正本3ビューと併せて読む（無ければ正常なno-op）。
2. **依頼内容解析**: `request_mode_policy.md` に従い Opinion / Design / Implementation / Verification を判定する。背景・意図・制約、`@role`/`@mode`/`@light`/`@full` タグ（`output_optimization_policy.md`）を解析する。
3. **軽量依頼か判定**: `output_optimization_policy.md` の軽量依頼定義に照らす。軽量なら A層の`output.md` 1ファイルのみを目標にし、B/C層は原則スキップする。
4. **（新規領域のみ）Capability Gap判定**: 依頼から必要Capabilityを抽出し、`agent_registry.md`・`capability_matrix.md`・`role_skill_map.md` を確認して既存Role / Skillで対応可能か判定する。判定は `capability_gap_policy.md` のGap分類（No / Skill / Role Scope / Workflow / Template / Quality Gate / Agent）と優先順位ラダーに従い、AI Capability Architect（`skill-capability-gap-analysis`）が `capability_gap_analysis.md` に記録する。追加が必要な場合は、書き込む前に `local_capability_layer_policy.md` で追加先レイヤ（共有層 / ローカル層）を決める。派生環境（正本環境と判定できない環境）では常にローカル層 `.local/capability/` へ追加し、`ai_team/**`・`skills/**`・`templates/**`・`tools/validate_repository.py` には書かない。共有層へ追加する場合のみ、Skill Gapは `skill_creation_policy.md`、Agent Gapは `agent_creation_policy.md`（CREATE基準 + Celes Human Gate）で解消し、Registry / Matrix / Map・ライフサイクル登録簿の更新まで行ってから実作業に入る。既知の依頼タイプ・軽量依頼ではこのステップをスキップしてよい。
5. **Role選定・実行context記録**: Task / Risk / Capabilityから必要最小限のRoleとSkillを選ぶ。呼び出し元Runtimeを変更せず、確認できたruntime/model Evidenceと推奨effortを `runtime_selection_policy.md` と `model_effort_selection_policy.md` に従って記録する。別Provider/Runtimeを自動起動しない。
6. **FDE要否判定**: 顧客相談・現場ヒアリングメモがある、業務課題が曖昧、MVPスコープ切り出しや業務フロー整理・導入定着観点が必要、RAG/AI Agent/データ基盤/業務アプリの現場適用——のいずれかに該当する場合は `ai_team/fde/fde_operating_model.md` の起動条件でAI FDEを起動し、`field_discovery_to_solution_workflow.md` に接続する。単純なSQL修正・明確なバグ修正・typo等では必須にしない。
7. **（条件付き）work_plan**: 3工程以上 or 明示的除外スコープが要る場合のみ `output/.../_internal/work_plan.md` を作る。
8. **（条件付き）execution_plan**: 高リスク・セキュリティ・大規模改修・複数工程/複数ファイルの場合のみ `output/.../_internal/execution_plan.md` にRole、caller runtime、Evidence type、推奨effort、理由を記録する。取得不能値は`unavailable`とする。軽量依頼ではoutput.md制御ブロックで足りる。
9. **（条件付き）繰り返し作業**: `iteration_confirmation_policy.md` に該当する場合のみ代表例を先に作り、`_internal/iteration_plan.md` と `_internal/sample_output_for_review.md` を作る。ステータス `Waiting for Celes Review`。承認後 `Expanding` で全件展開。
10. **実装・設計・検証**: 担当RoleがProfessional Modeに応じた本成果物を作る。`professional_only_policy.md` と `output_optimization_policy.md` のセクション間引き（関連セクションのみ＋必須核＋条件付き必須）に従う。責任外は `handoff_policy.md` で渡す。
11. **（Risk-based）品質レビュー**: `review/risk_based_quality_gates.yaml` を正本とし、Medium以上はIndependent Quality Review、High/Criticalは必要なSpecialist Reviewを実施する。顧客提出物・再利用物はRiskがLowでも追加レビュー対象にできる。必須Gateがない場合だけ「レビュー対象外」とし、自己レビューを独立レビュー扱いにしない。
12. **output.md作成（常時）**: `templates/output_template.md` で `output/.../output.md` を作る。複数Roleが関与した場合はDeliverable Optimizer（PMO）が各Role成果物を統合・編集する。制御ブロック（依頼の理解・担当Role/モード・出力モード・ステータス・品質判定・要対応）を先頭に置き、§1〜§5の構成で仕上げる。必須GateがPASSし作業が完了した時だけ`Completed`、レビュー待ちは`Waiting for Celes Review`、`REWORK_REQUIRED`は`Rework Required`、`BLOCKED`は`Blocked`とする。`Accepted`はCelesだけが決める。
13. **（条件付き）task_retrospective**: `Completed/Accepted` かつ軽量依頼でない場合のみ `_internal/task_retrospective.md` を作る（`retrospective_policy.md`）。
14. **（条件付き）feedback_analysis**: セレスのフィードバックがある場合のみ `_internal/feedback_analysis.md` を作る（`feedback_optimization_policy.md`）。
15. **（条件付き）Local Second Brain整理**: `obsidian_write_policy.md` の明示依頼またはAccepted gateを満たし、現在利用者のrootが確認できた場合だけKnowledge Curatorが整理する。Universal/Canonical Growthへ自動昇格しない。
16. **（要求時のみ）execution_summary**: セレスが明示要求 or 大型案件の場合のみ `_internal/execution_summary.md`（10項目）を作る。

## ステータス管理

| ステータス | 意味 |
|---|---|
| `Draft` | 初期案・仮案 |
| `In Progress` | 作業中 |
| `Waiting for Celes Review` | 代表例や方針についてセレス確認待ち |
| `Waiting for Approval` | 全件展開前の承認待ち |
| `Approved` | セレス確認済み |
| `Expanding` | 全件展開中 |
| `Verification Pending` | 検証待ち |
| `Rework Required` | P0/P1または必須修正が残り再作業中 |
| `Blocked` | 必須Evidence・権限・外部状態がなく停止 |
| `Completed` | 作業完了 |
| `Accepted` | セレス承認済み |
| `Obsidian Synced` | 第二の脳への整理完了 |

## 品質ゲート
- 依頼タイプに合う成果物がある。
- Roleの守備範囲と責任外が明確。
- 新規領域の依頼では、Capability Gap判定と対応（割当 / Skill追加 / Role追加）が記録されている。
- Role / Skillを追加した場合、`agent_quality_gate.md` を通過し、Registry / Matrix / Map・ライフサイクル登録簿が更新されている。
- 呼び出し元Runtimeを変更せず、確認可能な実行contextとEvidence typeが記録されている。
- 繰り返し作業の場合、代表例確認ゲートを通過している。
- 仮定、未確認事項、リスク、代案、次アクションがある。
- 非プロフェッショナルな感想、一般論、無根拠な同意が残っていない。
- 検証結果と未検証項目が明記されている。
- task_retrospective が作成されている（軽量依頼は除く）。
- 第二の脳への書き込みは `obsidian_write_policy.md` のトリガーを満たした後にのみ実施されている。
- 軽量依頼では A層の `output.md` 1ファイルのみが出力されている。
- B/C層の成果物は必要性ゲートを満たしたものだけが `_internal/` 配下に置かれている。
- 本成果物に該当なしの見出しが残っていない（必須核と条件付き必須は除く）。
- output.md 先頭ブロックの「要対応」に、ブロッキング質問・承認待ち・要判断が集約されている。

## 成果物

常時（タスクフォルダ直下）:
- `output/.../output.md`（制御ブロック＋本成果物を統合した1ファイル）

条件付き / 要求時（タスクフォルダ直下）:
- `capability_gap_analysis.md` / `agent_need_assessment.md` / `new_agent_proposal.md` / `new_agent_creation_report.md` / `new_skill_creation_report.md`（Capability Gap判定・チーム拡張が発生した場合のみ）

条件付き / 要求時（`output/.../_internal/` 配下）:
- `execution_plan.md`（実行環境・モデル・工数・Role選定の統合記録）
- `work_plan.md` / `iteration_plan.md` ＋ `sample_output_for_review.md`
- `quality_review_request.md` / `quality_review_report.md`
- `task_retrospective.md` / `feedback_analysis.md` / `team_improvement_proposal.md`
- `obsidian_sync_summary.md` / `execution_summary.md` / `questions.md`

## 参照

- `ai_team/output_optimization_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
- `ai_team/iteration_confirmation_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/feedback_optimization_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/professional_only_policy.md`
- `ai_team/handoff_policy.md`
- `ai_team/request_mode_policy.md`
- `ai_team/role_scope_matrix.md`
- `ai_team/personalization_policy.md`
- `ai_team/capability_gap_policy.md`
- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_registry.md`
- `ai_team/capability_matrix.md`
- `ai_team/role_skill_map.md`
- `ai_team/review/risk_based_quality_gates.yaml`
- `ai_team/fde/fde_operating_model.md`
