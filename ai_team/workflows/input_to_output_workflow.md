# Input to Output Workflow

## 目的
`input/` の依頼を、Professional Modeに分類し、専門Roleの成果物と品質レビューへつなげる。

## 手順

1. **input確認**: 入力ファイル、既存output、制約を確認する。
2. **依頼内容解析**: `request_mode_policy.md` に従い Opinion / Design / Implementation / Verification を判定する。背景・意図・制約を含めて解析する。
3. **作業工程分解**: 依頼を実行可能な工程に分解し、`output/work_plan.md` と `output/questions.md` を更新する。
4. **作業工程ごとのモデル提案**: `ai_team/model_selection_policy.md` に従い、工程ごとに最適なモデルタイプを提案する。`output/model_recommendation.md` を作成する（フォーマット: `templates/model_selection_template.md`）。
5. **Role選定**: `role_scope_matrix.md` に従い担当Roleと連携Roleを選ぶ。
6. **繰り返し作業か判定**: `ai_team/iteration_confirmation_policy.md` の判定条件に照らし、繰り返し作業かどうかを確認する。
7. **繰り返し作業なら代表例を先に作成**: 繰り返し作業に該当する場合、全件対応せず代表例1件を作成し、`output/iteration_plan.md` と `output/sample_output_for_review.md` を作成する。ステータスを `Waiting for Celes Review` にする。
8. **セレス確認が必要なら確認待ちにする**: 代表例・方針・体裁についてセレスの確認を得るまで全件展開しない。
9. **承認後に全件展開**: セレス承認後、ステータスを `Expanding` にして全件展開する。
10. **実装・設計・検証**: 担当RoleがProfessional Modeに応じた成果物を作る。`professional_only_policy.md` に従い、感想・一般論・無根拠な同意を除去する。責任外の論点は `handoff_policy.md` に従い渡す。QA / Security / SRE / Tech Leadの該当レビューを受ける。Quality Reviewerが最終判定する。
11. **execution_summary作成**: `output/execution_summary.md` を作成・更新し、ステータスを `Completed` にする。
12. **task_retrospective作成**: `ai_team/retrospective_policy.md` に従い `output/task_retrospective.md` を作成する（フォーマット: `templates/task_retrospective_template.md`）。
13. **必要に応じてfeedback_analysis作成**: セレスからのフィードバックがある場合、`ai_team/feedback_optimization_policy.md` に従い `output/feedback_analysis.md` を作成する。
14. **作業完了後にKnowledge Curatorが第二の脳へ整理**: `ai_team/obsidian_write_policy.md` のトリガーを満たした場合のみ、AI Engineering Knowledge Curatorが整理を実施する。Draft・確認待ち状態では整理しない。
15. **obsidian_sync_summary作成**: Knowledge Curator が `output/obsidian_sync_summary.md` を作成し、ステータスを `Obsidian Synced` にする。

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
- task_retrospective が作成されている。
- 第二の脳への書き込みは `obsidian_write_policy.md` のトリガーを満たした後にのみ実施されている。

## 成果物
- `output/work_plan.md`
- `output/model_recommendation.md`
- `output/iteration_plan.md`（繰り返し作業時）
- `output/sample_output_for_review.md`（繰り返し作業時）
- Professional Mode別成果物
- `output/quality_review_request.md`
- `output/quality_review_report.md`
- `output/execution_summary.md`
- `output/task_retrospective.md`
- `output/feedback_analysis.md`（フィードバックあり時）
- `output/team_improvement_proposal.md`（改善提案あり時）
- `output/obsidian_sync_summary.md`

## 参照

- `ai_team/model_selection_policy.md`
- `ai_team/iteration_confirmation_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/feedback_optimization_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/professional_only_policy.md`
- `ai_team/handoff_policy.md`
- `ai_team/request_mode_policy.md`
- `ai_team/role_scope_matrix.md`
