# Definition of Done

## 完了条件
- 依頼タイプが分類されている。
- 担当Roleと連携Roleが明記されている。
- Professional Modeに合った成果物がある。
- 実務で使える粒度になっている。
- 非プロフェッショナルな感想、一般論、無根拠な同意が除去されている。
- リスク、代案、未確認事項、次アクションがある。
- 必要な検証が実施され、未検証項目が明記されている。
- `risk_based_quality_gates.yaml`で独立レビュー対象の場合、Quality Reviewerの最終判定がPASSまたはPASS_WITH_CONDITIONSである。
- 実施したレビューがREWORK_REQUIREDまたはBLOCKEDの場合は完了扱いにしない。
- 繰り返し作業の場合、`iteration_confirmation_policy.md` に従い代表例確認ゲートを通過している。
- 軽量依頼でなくCompleted/Acceptedの場合、`output/.../_internal/task_retrospective.md` が作成されている。
- `obsidian_write_policy.md` のトリガーを満たした場合、Knowledge Curatorによる整理が完了または予定されている。
- Canonical promotionはBefore/After Eval、Independent Review、Celes Human Gate recordが揃うまで実施しない。
