# Review Metrics

## 目的
レビュー結果を蓄積し、どのAI社員・Skill・成果物で同じ問題が繰り返されるかを特定して、Skill、テンプレート、品質ゲートを改善する。

## 記録単位
タスクごとに `templates/review_metrics_template.md` を使い、Producerロール、リスク、判定、重大度別指摘、再作業回数、レビュー時間、利用者確認回数、承認後に発見された不具合を記録する。

## 主要指標
| 指標 | 目的 | 注意 |
|---|---|---|
| Escaped P0 / P1 | 重大な見逃しを減らす | 最重要。0を目標とする |
| Reopened finding rate | 修正の実効性を確認する | 解決済み判定の甘さを検出 |
| Repeated finding themes | Skillやテンプレートの構造欠陥を発見する | 個人責任ではなく仕組みを直す |
| Rework cycles | 初回成果物の準備度を測る | 複雑度・リスクで補正する |
| Review lead time | 運用可能なレビュー速度を測る | 短さだけを最適化しない |
| User clarification count | セレスへの説明の明瞭さを測る | 質問ゼロ自体を目的にしない |

## 改善ループ
1. 3件以上の同種タスクを蓄積する。
2. P1 / P2の反復テーマを集計する。
3. Producer Skill、成果物テンプレート、検証スクリプトのどこで予防するか決める。
4. 修正後3件で再発率を確認する。
5. 閾値やレビュー深度を調整する。

## 進行中の点検

- **Capability Architect / Gap判定精度**（2026-08-04 セレス追認）: `capability_architect` によるGap判定・Skill選定の実効性は `not_evaluated`。初回実運用3件（新規領域の依頼で `input_to_output_workflow.md` 手順4のCapability Gap判定を実施したタスク）を本ページの記録単位で蓄積し、上記「改善ループ」に投入して精度を点検する。3件到達まではeffectivenessを`not_evaluated`のまま維持し、根拠のない数値化は行わない。
- **セレス環境における実験的追加のゲート迂回点検**（2026-08-05）: `local_capability_layer_policy.md` の副作用2（セレス環境は`.local/`を使わず、実験的な追加も常に共有層のCREATE基準7項目・Before/After Eval・独立レビュー・Celes Human Gateを通す）が、儀式コストの圧力でゲートの形骸化（証跡の水増し・簡略化）を招いていないかを定期点検する。四半期ごと、または5件以上のRole / Skill追加が発生した時点で、`decision_history` / `promotion_history` の該当PROMOTE記録を読み、証跡refが具体的か（`local-evidence:` / `local-review:` が実在ファイルを指しているか）を確認する。

## 禁止
- 合格率だけでAI社員を評価しない。
- 指摘件数を減らすために重大度を下げない。
- リスクやタスク難易度を無視してロールを順位付けしない。
- 顧客名、個人情報、秘密情報をメトリクスへ記録しない。
