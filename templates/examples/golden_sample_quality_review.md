# 【見本】Quality Review Report（採点済み）

> ゴールデンサンプル（見本）。`golden_sample_output.md` をレビューした想定の記入例。採点アンカーとスコア→判定の変換規則は `ai_team/review/quality_scoring_rubric.md` に従っている。

## 1. セレス向け結論
- **最終判定**: PASS
- **一言で言うと**: 事実と仮定が分離され、段階移行の判断根拠と撤退条件まで揃っている。顧客にそのまま出せる。
- **今すぐ対応が必要なこと**: なし
- **セレスの判断が必要なこと**: なし

## 2. Review Scope
- Reviewed artifacts: golden_sample_output.md
- Evidence checked: 引用されたジョブログ・AWS公式ドキュメントの記載箇所
- Excluded or unverified areas: 営業側ヒアリング前提の訂正データ要件（成果物内で仮定と明示済み）
- Reviewer independence: 作成Role（AI Data Engineer）とは別のReviewerが実施

## 3. Quality Scorecard（抜粋・スコア理由付き）

| Dimension | Score | Evidence | Key issue |
|---|---:|---|---|
| Purpose and requirement fit | 4 | 依頼の理解が制御ブロックに明記され、Opinion要求に対して実装を先走っていない | - |
| Factual accuracy and evidence | 4 | Athena対応状況を公式ドキュメントで確認し、仮定（営業要件）を仮定と明記 | - |
| Data quality and data contract | 3 | 差分キー・訂正データの扱いに言及。粒度の確定は設計工程の扱いで妥当 | P3: 粒度はDesign時に確定 |
| Cost and commercial viability | 3 | コンパクション怠慢時のコスト増リスクを明示 | P3: 削減効果の概算数値は未算出 |
| Test coverage and reproducibility | N/A | Opinionモードのため検証実施は対象外（理由記載） | - |

平均 3.4 / 4.0（採点10次元、N/A除外。最低: Cost 3）

## 4. Findings

| ID | Severity | Area | Finding | Required action | Owner | Due |
|---|---|---|---|---|---|---|
| F-1 | P3 | Cost | 移行後のコスト削減効果が概算されていない | Design時にS3書き込み量の概算を追加 | AI Data Engineer | Design着手時 |

## 9. Final Verdict Rationale

採点済み全次元が3以上で、P0/P1/P2の指摘なし。`quality_scoring_rubric.md` の変換規則に従い PASS。
