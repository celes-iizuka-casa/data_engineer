# 開発ドキュメント標準構成定義

> `templates/development/` 配下の全テンプレートが従う共通規約。テンプレート作成者（Phase 2/3）と記入者（各Role）の両方が対象。

## 1. 配置と命名

```
templates/development/
├── document_map.md                  # 全体索引（種別×工程）
├── development_doc_standards.md     # 本書
├── sets/                            # 種別ごとのセット表紙（フルセット目次）
│   ├── set_cover_template.md        # セット表紙の型
│   └── <type>.md                    # 種別別（Phase 3）
├── common/                          # 共通コア（全種別で使う工程別文書）
└── <type>/                          # 種別差分（data_platform / analytics_platform / system_app /
                                     #   web_content / ai_ml_llm / integration / cloud_infra /
                                     #   maintenance / poc / management）
```

- ファイル名は英語 snake_case + `_template.md`。文書の中身は日本語
- 既存 `templates/` 直下の45本は移動しない（validator契約・既存参照を壊さないため）。開発文書として流用するもの（requirements / basic_design 等）は document_map から相対パスで参照する

## 2. 共通メタヘッダ（全テンプレート冒頭・必須）

```markdown
- 案件 / 顧客: <client> / <project>
- 文書名 / 版数: <本文書名> / v0.1
- 作成日 / 最終更新: YYYY-MM-DD / YYYY-MM-DD
- 作成Role / レビュー: <role> / <未レビュー | reviewer名>
- ステータス: Draft | In Review | Approved | Deprecated
- 関連文書: <要件定義書 v1.0 / REQ-xxx 等>
```

理由: 版・承認状態・トレース先が文書に無いと、複数文書間の整合（engineering guardrails）を機械的に確認できない。

## 3. セクション規約

- 各セクション見出しに **【必須】/【任意】** を明記する
- 各セクション見出しの直下に記入ガイドを1行置く: `> Why: この項目が必要な理由` — 記入者（AI社員）はこの理由ごとセレス・顧客に提示できる。顧客提出時に Why 行を残すか削るかは提出先で判断（内部文書は残す）
- 【任意】セクションを省略した場合は、文書末尾の「省略記録」に理由を1行残す（判断のトレースを残すため。無言の省略は禁止）
- 記入例が必要な箇所は `例:` プレフィックスで実データと区別する

## 4. 整合規則（engineering guardrails 準拠）

- 用語は要件定義書の用語定義に従う。同じ概念に別名を作らない
- 要件は要件ID（REQ-xxx）で振り、設計・テスト文書は必ず要件IDへトレースする
- データ粒度・API契約・画面項目は既存成果物と一致させる。変える場合は変更管理記録に理由・影響範囲・移行を残す
- 未確認の外部仕様を断定しない。確認元（公式ドキュメント・実データ）を文書内に記す

## 5. MVPでも省略しない領域

最小構成を選んでも次は省略不可（該当セクションを空にする場合は「省略記録」で理由必須）:
認証認可・秘密管理 / 監視 / 再実行性（リラン・ロールバック） / テスト

## 6. 品質接続

- 文書提出前に `ai_team/review/quality_scoring_rubric.md` のモード別必須次元を自己チェックする
- 顧客提出・本番・破壊的変更・セキュリティ影響のいずれかに該当する文書は quality-reviewer の独立レビューを通す（`ai_team/output_optimization_policy.md` のゲート表）

## 7. テンプレート自体の変更管理

- テンプレート追加・変更時は `document_map.md` と該当セット表紙を同時更新する
- Phase 4 以降、`tools/validate_repository.py` が本ディレクトリの構成（document_map と実ファイルの整合）を契約としてロックする予定
