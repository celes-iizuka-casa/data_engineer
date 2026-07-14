# Quality Gate

## 必須ゲート
- 要件と成果物が対応している。
- Professional Modeに合っている。
- Roleの守備範囲に合っている。
- Professional Only Policyに合っており、感想、一般論、無根拠な同意がない。
- 仮定と未確認事項が明記されている。
- セキュリティ、運用、テスト、データ品質の該当観点がある。
- Quality Reviewerへレビュー依頼できる証跡がある。
- 繰り返し作業の場合、代表例確認ゲートを通過している。
- 呼び出し元Runtimeを変更せず、実測できないmodel/token/costを`unavailable`としている。
- 軽量依頼でなくCompleted/Acceptedの場合、`output/.../_internal/task_retrospective.md` が作成されている。
- 第二の脳への書き込みは `obsidian_write_policy.md` のトリガーを満たした後にのみ実施されている。
- 品質レビュー実施時は `quality_scoring_rubric.md` の採点アンカーと変換規則に従っている。
- FDE成果物（Discovery / 業務フロー / MVP / Handoff / 導入定着 / 指標 / フィードバック）は `../fde/fde_quality_gate.md` の成果物別チェックを併用している。
- Risk別レビュー深度は `risk_based_quality_gates.yaml` と一致している。
- Canonical promotionにはBefore/After Eval、Independent Review、Celes Human Gate recordがある。

## 参照
- `../professional_only_policy.md`
- `quality_scoring_rubric.md`
- `professional_quality_gate.md`
- `definition_of_done.md`
- `review_policy.md`
- `../fde/fde_quality_gate.md`
