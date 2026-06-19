# Input to Output Workflow

## 目的
`input/` の依頼を、Professional Modeに分類し、専門Roleの成果物と品質レビューへつなげる。

## 手順
1. 入力ファイル、既存output、制約を確認する。
2. `request_mode_policy.md` に従い Opinion / Design / Implementation / Verification を判定する。
3. `role_scope_matrix.md` に従い担当Roleと連携Roleを選ぶ。
4. PMOが `output/work_plan.md` と `output/questions.md` を更新する。
5. 担当RoleがProfessional Modeに応じた成果物を作る。
6. `professional_only_policy.md` に従い、感想、一般論、無根拠な同意を除去する。
7. 責任外の論点は `handoff_policy.md` に従い渡す。
8. QA / Security / SRE / Tech Leadの該当レビューを受ける。
9. Quality Reviewerが最終判定する。
10. Knowledge Curatorが再利用価値のある成果物を第二の脳へ反映する。

## 品質ゲート
- 依頼タイプに合う成果物がある。
- Roleの守備範囲と責任外が明確。
- 仮定、未確認事項、リスク、代案、次アクションがある。
- 非プロフェッショナルな感想、一般論、無根拠な同意が残っていない。
- 検証結果と未検証項目が明記されている。

## 成果物
- `work_plan.md`
- Professional Mode別成果物
- `quality_review_request.md`
- `quality_review_report.md`
- `execution_summary.md`
- `obsidian_sync_summary.md`
