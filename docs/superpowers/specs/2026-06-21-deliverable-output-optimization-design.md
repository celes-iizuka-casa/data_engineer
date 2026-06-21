# 提出物の出力最適化 設計書

- 日付: 2026-06-21
- 対象: AIエンジニアチーム（`ai_team/`）の成果物出力
- 方式: A案（階層出力＋必要性ゲート / 入力テンプレなし）

## 背景・課題

1依頼に対し `input_to_output_workflow.md` が最大12個前後のファイル（work_plan, model_recommendation, questions, iteration_plan, sample_output_for_review, 本成果物, quality_review_request, quality_review_report, execution_summary, task_retrospective, feedback_analysis, obsidian_sync_summary）を生成する。本命の成果物がプロセス文書に埋もれ、「量が多すぎて読むのが大変」状態になっている。

セレスの要望:
- 選ばれたAI社員（Role）の **必要最低限の成果物** だけを受け取りたい
- デフォルトで渡すのは **①チームとしての結論サマリー ＋ ②選ばれたRoleの本成果物** の2つ
- 本成果物は **関連セクションだけ**（該当なしの見出しは出さない）
- **不要なものは裏でも作らない**（「全部作って隠す」ではなく「必要なものだけ作る」）
- 依頼時の **入力フォーマット化はしない**（使いづらいため）

重要な前提: 独立した品質レビュー・自己レビュー禁止・反復作業ゲートといったガバナンスの **判定そのものは残す**。軽量化のために品質ゲートを捨てるのではなく、出力を軽く・条件付きにする。

既存ポリシーの確認結果: model_selection / iteration / obsidian / retrospective は **既に条件付きトリガーを持っている**（例: model_selection_policy は「各タスクで必要に応じて」）。主因は「ポリシー上は条件付きなのに workflow が標準ステップとして毎回ファイル化している」ズレ。本設計はこのズレを正す。

## 設計

### 1. 出力モデル（3階層 + フォルダ構造）

成果物を「ユーザーが読む層」と「チームが使う層」に物理分離する。

| 階層 | 中身 | 生成条件 |
|---|---|---|
| **A. 常に渡す（ユーザー向け）** | `deliverable_summary.md`（結論サマリー）＋ 選ばれたRoleの本成果物 | 毎回 |
| **B. 条件付き（トリガー時のみ）** | model_recommendation / iteration_plan＋sample / quality_review_report / task_retrospective / obsidian_sync_summary | 各ポリシーのトリガーを満たした時だけ |
| **C. 要求時のみ** | work_plan / quality_review_request / execution_summary（10項目詳細）/ questions（全文） | セレスが明示要求した時、または内部参照用 |

フォルダ構造:
```
output/<client>/<YYYYMMDD>/<task-name>/
├── deliverable_summary.md      ← まずこれだけ読めばいい（常時）
├── <deliverable>.md            ← Roleの本成果物・関連セクションのみ（常時）
└── _internal/                  ← B/C層。普段は開かない
    ├── quality_review_report.md   (トリガー時)
    ├── model_recommendation.md    (トリガー時)
    └── ...
```

`_internal/` への隔離により、フォルダを開いた瞬間に「読むべき2ファイル」だけが見える。

### 2. 結論サマリー（`deliverable_summary.md`）の固定フォーマット

新しい「司令塔」。10項目の `execution_summary` は要求時のみのC層に降格し、代わりにこの短い1枚を常時の標準にする。

```md
# <タスク名> — 結論サマリー

- 依頼の理解: <1〜2行。チームが何を頼まれたと解釈したか＝読み違い検知用>
- 担当: <選ばれたRole> / モード: <Opinion|Design|Implementation|Verification>
- 結論: <数行。一番言いたいこと>
- 品質判定: <PASS | PASS_WITH_CONDITIONS | REWORK_REQUIRED | BLOCKED | レビュー対象外>
- 要対応（セレスへ）: <ブロッキング質問・承認待ち・判断が要る点。無ければ「なし」>
- 次アクション: <チーム側 / セレス側>
- 本成果物: ./<deliverable>.md
- 参考(必要時): ./_internal/...
```

設計の肝は **「要対応」行**。品質レビューやquestionsを `_internal/` に隠しても、要対応がここに必ず集約されるため、「要対応: なし」を見れば安心して詳細を読み飛ばせ、何かあれば1行で気づける。隠すことで安全性が落ちない。

### 3. 必要性ゲート（トリガー表）

各成果物に「作る条件」を明示し、満たさなければ作らない（裏でも作らない）。既存ポリシーの条件をそのまま使い、無いものだけ新設する。

| 成果物 | 作る条件（これを満たした時だけ） | 満たさない時 |
|---|---|---|
| **deliverable_summary** | 常に | — |
| **Roleの本成果物** | 常に | — |
| **work_plan** | 3工程以上 or 明示的な除外スコープが要る依頼 | 作らない（サマリーの「次アクション」で代替） |
| **model_recommendation** | 2工程以上で必要能力が変わる or 高リスク/セキュリティ工程を含む | 作らない |
| **iteration_plan + sample** | `iteration_confirmation_policy` の繰り返し判定に該当（対象3件以上 等） | 作らない |
| **quality_review_report** | Design/Implementation/Verification で「顧客提出物・再利用物・本番/破壊的/セキュリティ影響」のいずれか | 作らない＝サマリーに「レビュー対象外」と明記 |
| **questions（独立ファイル）** | 未確認事項が実在する場合のみ | 作らない（空ファイルを作らない。少数ならサマリー「要対応」に直書き） |
| **task_retrospective** | `Completed/Accepted` かつ軽量依頼でない | 作らない |
| **obsidian_sync_summary** | `obsidian_write_policy` のトリガー かつ 顧客/再利用価値あり | 作らない |
| **execution_summary（10項目詳細）** | セレスが明示要求 or 大型案件で詳細記録が要る時 | 作らない（サマリーで代替） |

「軽量依頼」の定義（該当したらA層の2つだけ。B/C層は原則全部スキップ）:
- 単一工程で完結
- 顧客提出物でない
- 本番/セキュリティ/破壊的変更を伴わない
- 取り消し可能（リスクが低い）

### 4. 本成果物のセクション間引きルール

基本ルール: テンプレの見出しは「今回中身がある項目だけ」出力。該当なしの見出しはまるごと省略（「該当なし」とも書かない）。

無条件省略で重要観点が静かに消えるのを防ぐため、モード別の必須核だけ残す（短くてOK、空でも一言入れる）:

| モード | 必須核（必ず出す） | 残りは関連時のみ |
|---|---|---|
| Opinion | 結論 / 推奨 / 次アクション | 確認済み事実・仮定・懸念・代案・採用条件… |
| Design | 設計概要 / 推奨アーキテクチャ / リスク / 完了条件 | スコープ・コンポーネント・各種設計・運用… |
| Implementation | 実装方針 / 作成・修正ファイル / 検証手順 | 実行手順・注意点・残課題… |
| Verification | 検証対象 / 検証結果 / 推奨アクション | 観点・重大度・修正案… |

条件付き必須（リスクに応じて必須核に昇格、「該当なし」省略を禁止）:
- 本番/破壊的変更 → **ロールバック**を必須化
- 認証認可・秘密・個人情報・外部公開を伴う → **セキュリティ**を必須化

これでAGENTS.mdの「認証認可・秘密管理・監視・再実行性・テストを省略しない」原則と矛盾せず、平常時は短くなる。

### 5. 入力の扱い（テンプレ化しない）

依頼側に必須フォーマットを課さない。3点で吸収する:

1. **チームが推論する**: 自然文の依頼から role / mode / scope をチーム側が判定（既存 `request_mode_policy` を流用）。
2. **サマリー冒頭で言い返す**: `deliverable_summary` の「依頼の理解」1〜2行でチームの解釈を提示。読み違いを即検知。
3. **任意のワンライナータグ**（使いたい時だけ。必須ではない）:
   - `@role:<name>` … 担当Role指定
   - `@mode:<opinion|design|impl|verify>` … モード指定
   - `@light` … 強制的に軽量（2ファイルのみ）
   - `@full` … 全成果物を出させる（重要案件用）

タグは付けなくても従来通り動く。

## 変更範囲（実装対象）

新規作成（2ファイル）:
- `ai_team/output_optimization_policy.md` — 本設計の単一の正本（3階層・必要性ゲート・軽量依頼定義・セクション間引きルール・入力タグ）
- `templates/deliverable_summary_template.md` — 結論サマリーの固定フォーマット

修正（既存の「毎回作る」記述をゲートに合わせる）:
- `AGENTS.md` — Required Start/Finish の「work_plan / quality_review_request / execution_summary / questions を毎回作る」をゲート参照に変更。出力モデル（A/B/C層・`_internal/`・サマリー先頭）と「関連セクションのみ」を明記
- `ai_team/workflows/input_to_output_workflow.md` — 各ステップをゲート化、deliverable_summaryを常時ステップに、execution_summaryを要求時に降格、成果物リストと品質ゲートを更新
- `ai_team/professional_response_templates.md` — 各モードに「関連セクションのみ＋必須核＋条件付き必須」を追記
- `ai_team/model_selection_policy.md` / `ai_team/retrospective_policy.md` — 「作る条件」を明文化（軽量依頼スキップ）
- `ai_team/README.md` — 新ポリシーへの参照を追加
- iteration / obsidian 系は既にゲート済み。`_internal/` 配置の参照のみ追加

## 検証方法

markdownポリシーのため自動テストは作らない。代表依頼2件で構造を確認する手順を品質ゲートに追加する:
- 軽量依頼1件 → 出力が `deliverable_summary.md` ＋ 本成果物の2ファイルのみであること
- 重量依頼1件 → ゲートを満たした成果物だけが `_internal/` に生成され、サマリーの「要対応」「品質判定」が正しく集約されていること

## 非スコープ

- 既存の出力ファイル（現 `output/` 直下の成果物）の遡及的な再構成
- feedback_optimization / team_improvement の出力様式変更（今回は必要性ゲートの対象外、従来どおり）
- データツール（`tools/`, `tests/`）への変更

## ガバナンス保全（守るべきもの）

- 独立した品質レビューと自己レビュー禁止は維持（出力の有無のみ条件化）
- 反復作業の代表例確認ゲートは維持
- 本番/破壊的変更のロールバック明記、機微情報のセキュリティ明記は条件付き必須として保全
```