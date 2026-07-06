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

## 2. テンプレートの書式（既存45本と同一様式）

既存 `templates/` 直下45本（requirements / architecture / api_design / db_design / runbook 等）はすべて「英語タイトル＋番号付き見出しのみ」の簡潔な骨格で、メタ説明文や必須/任意タグを本文中に持たない。`templates/development/` 配下の新規テンプレートもこれに合わせる（engineering guardrails「既存成果物と整合させる」に基づく判断。Phase 1時点の初版はメタヘッダ＋Why行＋必須/任意タグを本文に埋め込む重い様式にしていたが、既存45本と様式が食い違うため本改訂で揃えた）。

- タイトルは `# <Title>`（英語）。技術系（設計・運用・API等）は英語見出し、業務・企画系は既存の `mvp_scope_template.md` 等に倣い日本語見出し可
- 見出しは `## N. <Section>` の番号付き。構造化データはテーブル化する（既存テンプレの列構成に倣う）
- 文書ごとの版数・承認状態・作成者は本文に埋め込まず、`requirements_template.md` 同様に必要な文書のみ `## Document Control` セクション（Owner / Reviewers / Status / Last updated）を持たせる。全文書一律の必須ヘッダにはしない
- 各文書の**必須/任意・理由**は本文に書かず `document_map.md`（種別×工程マトリクス）と種別セット表紙（`sets/<type>.md`）に集約する。理由を知りたい記入者はそちらを参照する（本文が長くなりすぎるのを防ぎ、既存テンプレの簡潔さを保つため）

## 3. セクション規約

- 【必須】/【任意】タグや `Why:` 説明行は本文セクション見出しには付けない（§2の理由による集約方針）。例外は `sets/` 配下のセット表紙のみ（表紙は既存に対応物がない新しい文書種別のため、判断根拠を載せる独自様式を許容する）
- 記入例が必要な箇所は `例:` プレフィックスで実データと区別する
- 任意項目を省略した場合の記録は、テンプレート本文ではなく案件の `output.md`（要対応・補足欄）に残す

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
- `tools/validate_repository.py` が本ディレクトリの構成を契約としてロックしている: (1) document_map.md・各セット表紙内のバッククォート参照パスが実在すること、(2) 本ディレクトリ配下の全 `*_template.md` が document_map.md またはいずれかのセット表紙から参照されていること、(3) 各セット表紙が document_map.md の対象種別表に載っていること。違反すると `python3 tools/validate_repository.py` が失敗する
