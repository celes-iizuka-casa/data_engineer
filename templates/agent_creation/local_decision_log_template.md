# Local Capability Decision Log

<!-- 配置先: .local/capability/local_decision_log.md -->
<!-- ローカル層のRole / Skillの追加・変更・削除・昇格提案の判断記録。 -->
<!-- 共有層の decision_history / promotion_history とは別物で、append-only契約や -->
<!-- subject_revisionごとの一意なPROMOTE記録の要求は適用されない。 -->
<!-- Gateは現在の利用者自身。記入規約は ai_team/local_capability_layer_policy.md を参照する。 -->

## この環境について

- 環境判定: （正本環境 / 派生環境）
- 判定日: YYYY-MM-DD
- 確認した内容: （origin URLの正規化後の値と宣言値の一致有無、push権限の実測結果。確認できなかった項目は `unavailable`）

## 記録

### YYYY-MM-DD — （追加 / 変更 / 削除 / 昇格提案）: `local_<name>` または `skill-local-<name>`

- 追加日: YYYY-MM-DD
- 対象: （Role ID / Skill ID とファイルパス）
- 追加理由: （どの依頼で何が必要になったか）
- Capability Gap判定: （No / Skill / Role Scope / Workflow / Template / Quality Gate / Agent。判定根拠となった参照先も書く）
- 既存で足りなかった理由: （どの正本Role / Skillを実読して、何が不足していたか。名前の印象ではなく定義本文を根拠にする）
- 影響範囲: （このローカル追加が影響する依頼種別・成果物）
- Rollback手順: （削除する場合の手順。共有層に触れていないことの確認方法を含める）
- 独立レビュー: （実施 / 未実施。Risk Medium以上では推奨。未実施なら理由）
- Risk判定: （Low / Medium / High / Critical。`ai_team/review/risk_based_quality_gates.yaml` に照らす）

### YYYY-MM-DD — 昇格提案の結果: `local_<name>`

- 提案ファイル: `.local/capability/promotion/<file>.md`
- 結果: （PROMOTE / REJECT / 保留）
- REJECTの場合の理由: （記録する。同一提案を根拠なく再提出しないため）
- PROMOTEの場合の後処理: （ローカル定義を削除し `git pull` して二重定義を解消したか）

## 注意

- ローカル層は `tools/validate_repository.py` の検査対象外である。契約違反は検出されないが、成果物の品質として現れる。初回利用前に、共有層と同じ見出し契約・キー契約に準拠しているか自己点検する。
- ローカル層のRole / Skillを使って作った成果物にも、`risk_based_quality_gates.yaml` の判定を通常どおり適用する。
- raw evidence（顧客情報・個人属性を含む生の記録）はここに置かない。`.local/evidence` または `output/` を使う。
