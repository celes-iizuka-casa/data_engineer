# Input to Output Workflow

## 目的
`input/` の依頼を、Professional Modeに分類し、専門Roleの成果物と品質レビューへつなげる。

## 手順

1. **input確認**: 入力ファイル、既存output、制約を確認する。あわせて `profiles/current_user_profile.yaml` を読む（`personalization_policy.md`。不在時はセレス=専門家エンジニアを仮定し成果物に明記）。
2. **依頼内容解析**: `request_mode_policy.md` に従い Opinion / Design / Implementation / Verification を判定する。背景・意図・制約、`@role`/`@mode`/`@light`/`@full` タグ（`output_optimization_policy.md`）を解析する。
3. **軽量依頼か判定**: `output_optimization_policy.md` の軽量依頼定義に照らす。軽量なら A層の2ファイルのみを目標にし、B/C層は原則スキップする。
4. **Role選定・実行環境/モデル/工数判定**: `role_scope_matrix.md` に従い担当Roleと連携Roleを選ぶ。続けて各工程の実行環境（Claude Code / Codex / 併用）・モデル・工数を `runtime_selection_policy.md` と `model_effort_selection_policy.md` で判定する。採用結果は output.md 制御ブロックに表示する。
5. **FDE要否判定**: 顧客相談・現場ヒアリングメモがある、業務課題が曖昧、MVPスコープ切り出しや業務フロー整理・導入定着観点が必要、RAG/AI Agent/データ基盤/業務アプリの現場適用——のいずれかに該当する場合は `ai_team/fde/fde_operating_model.md` の起動条件でAI FDEを起動し、`field_discovery_to_solution_workflow.md` に接続する。単純なSQL修正・明確なバグ修正・typo等では必須にしない。
6. **（条件付き）work_plan**: 3工程以上 or 明示的除外スコープが要る場合のみ `output/.../_internal/work_plan.md` を作る。
7. **（条件付き）execution_plan**: 2工程以上で実行環境/モデル/工数が変わる、または高リスク・セキュリティ・大規模改修・複数ファイル一括展開の場合のみ `output/.../_internal/execution_plan.md`（`templates/execution_plan_template.md`）に Role選定・実行環境・モデル・工数・理由を統合記録する。軽量依頼では作らず output.md 制御ブロックの記載で足りる（旧 `model_recommendation` はこれに統合）。
8. **（条件付き）繰り返し作業**: `iteration_confirmation_policy.md` に該当する場合のみ代表例を先に作り、`_internal/iteration_plan.md` と `_internal/sample_output_for_review.md` を作る。ステータス `Waiting for Celes Review`。承認後 `Expanding` で全件展開。
9. **実装・設計・検証**: 担当RoleがProfessional Modeに応じた本成果物を作る。`professional_only_policy.md` と `output_optimization_policy.md` のセクション間引き（関連セクションのみ＋必須核＋条件付き必須）に従う。責任外は `handoff_policy.md` で渡す。
10. **（条件付き）品質レビュー**: 必要性ゲートを満たす場合（顧客提出物・再利用物・本番/破壊的/セキュリティ影響）のみ、Quality Reviewerが `_internal/quality_review_report.md` を作る。満たさない場合はサマリーの品質判定を「レビュー対象外」にする。自己レビューを独立レビュー扱いにしない。
11. **output.md作成（常時）**: `templates/output_template.md` で `output/.../output.md` を作る。複数Roleが関与した場合はDeliverable Optimizer（PMO）が各Role成果物を統合・編集する。制御ブロック（依頼の理解・担当Role/モード・出力モード・ステータス・品質判定・要対応）を先頭に置き、§1〜§5の構成で仕上げる。ステータスを `Completed` にする（`deliverable_optimization_policy.md` 参照）。
12. **（条件付き）task_retrospective**: `Completed/Accepted` かつ軽量依頼でない場合のみ `_internal/task_retrospective.md` を作る（`retrospective_policy.md`）。
13. **（条件付き）feedback_analysis**: セレスのフィードバックがある場合のみ `_internal/feedback_analysis.md` を作る（`feedback_optimization_policy.md`）。
14. **（条件付き）Obsidian整理**: `obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理し、`_internal/obsidian_sync_summary.md` を作る。ステータス `Obsidian Synced`。
15. **（要求時のみ）execution_summary**: セレスが明示要求 or 大型案件の場合のみ `_internal/execution_summary.md`（10項目）を作る。

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
| `Completed` | 作業完了 |
| `Accepted` | セレス承認済み |
| `Obsidian Synced` | 第二の脳への整理完了 |

## 品質ゲート
- 依頼タイプに合う成果物がある。
- Roleの守備範囲と責任外が明確。
- 工程ごとのモデル提案がある。
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

条件付き / 要求時（`output/.../_internal/` 配下）:
- `execution_plan.md`（実行環境・モデル・工数・Role選定の統合記録）
- `work_plan.md` / `model_recommendation.md` / `iteration_plan.md` ＋ `sample_output_for_review.md`
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
- `ai_team/fde/fde_operating_model.md`
