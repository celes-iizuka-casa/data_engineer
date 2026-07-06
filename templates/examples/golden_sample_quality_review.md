# 【見本】Quality Review Report（採点済み・全15次元記入）

> ゴールデンサンプル（見本）。`golden_sample_output.md`（Opinionモード）をレビューした想定の記入例。採点アンカー・必須次元・スコア→判定の変換規則は `ai_team/review/quality_scoring_rubric.md` に従っている。実レポートでも Scorecard は15行すべてを記入する（N/A は理由必須。証跡不足の次元は 0 のまま残す）。

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

## 3. Quality Scorecard（全15次元・スコア理由付き）

Opinionモードの必須次元（Purpose / Factual accuracy / Cross-artifact consistency / Documentation and handover / Technical correctness）はすべて採点済み。0（not reviewed）のまま残る次元はない。

| Dimension | Score | Evidence | Key issue |
|---|---:|---|---|
| Purpose and requirement fit | 4 | 依頼の理解が制御ブロックに明記され、Opinion要求に対して実装を先走っていない | - |
| Factual accuracy and evidence | 4 | Athena対応状況を公式ドキュメントで確認し、仮定（営業要件）を仮定と明記 | - |
| Technical correctness and architecture | 4 | Iceberg採用理由・段階移行案が既存構成（Glue Catalog/S3）と整合し、撤退条件まで技術根拠付き | - |
| Cross-artifact consistency and traceability | 3 | 用語・テーブル名が入力DDLと一致。結論→根拠（ログ・公式Doc）を追跡できる | P3: 要件IDは要件定義工程で付与 |
| Implementation readiness | N/A | Opinionモードで実装物がない。着手粒度はDesign工程の採点対象（理由記載） | - |
| Test coverage and reproducibility | N/A | Opinionモードのため検証実施は対象外（理由記載） | - |
| Data quality and data contract | 3 | 差分キー・訂正データの扱いに言及。粒度の確定は設計工程の扱いで妥当 | P3: 粒度はDesign時に確定 |
| Security, privacy, and governance | N/A | 移行方式の意見であり認証認可・秘密情報・公開範囲の変更を伴わない。アクセス制御はDesign工程で採点（理由記載） | - |
| Reliability, operations, and recovery | 3 | コンパクション等の運用負荷と段階移行の撤退条件（ロールバック相当）に言及 | P3: 監視項目の具体化はDesign時 |
| Performance and scalability | N/A | 性能検証の対象成果物がない。クエリ性能への影響はDesign時のベンチマークで採点（理由記載） | - |
| Cost and commercial viability | 3 | コンパクション怠慢時のコスト増リスクを明示 | P3: 削減効果の概算数値は未算出 |
| Usability and accessibility | 4 | 結論先行・採用条件/不採用条件が明確で、セレスがそのまま顧客判断に使える | - |
| Maintainability and reuse | 3 | 判断基準が汎用化されており他案件のAthena→Iceberg判断に再利用できる | P3: 再利用時の前提条件を1行追記余地 |
| Documentation and handover | 3 | 仮定・未確認事項・次工程（Design）への引き継ぎ事項が残っている | - |
| LLM safety and evaluation, if applicable | N/A | LLMアプリ成果物ではない（理由記載） | - |

平均 3.4 / 4.0（採点10次元、N/A除外。最低: Cost 3 ほか同点あり）

## 4. Findings

| ID | Severity | Area | Finding | Required action | Owner | Due |
|---|---|---|---|---|---|---|
| F-1 | P3 | Cost | 移行後のコスト削減効果が概算されていない | Design時にS3書き込み量の概算を追加 | AI Data Engineer | Design着手時 |

## 9. Final Verdict Rationale

採点済み10次元がすべて3以上で、P0/P1/P2の指摘なし。必須次元に0（not reviewed）は残っていない（N/A 5次元はいずれも構造的な対象外で理由記載済み）。`quality_scoring_rubric.md` の変換規則「採点済み全次元が3以上、かつ P0/P1/P2 なし」に従い PASS。
