# Deliverable Optimization Policy

## 目的

AI社員チームの思考量を減らすことではない。**ユーザーに渡す提出物を最適化すること**が目的。チーム内部では必要に応じて計画・レビュー・モデル選定・反省・Obsidian同期判断を行ってよい。ただし、それらを毎回ユーザー向けの標準成果物として出さない。

**担当: AI Engineering PMO**（既存守備範囲「成果物管理・output構成整理」の延長としてDeliverable Optimizerの帽子を被る）

## Deliverable Optimizerの責務

Deliverable Optimizerは**単なる要約係でなく、成果物設計者**として機能する。

- 依頼内容に応じて最終成果物の形式・粒度を決める
- ユーザーが読む順番を設計する（結論を必ず先頭に）
- 内部成果物と外部成果物を分離する
- Role別成果物を統合し、`output.md` 1本に編集する
- 長文が必要な場合と不要な場合を判断する
- 「今読むべき情報」と「必要になったら読む情報」を分ける
- 不要な内部ファイル生成を抑制する

## ユーザー向けデフォルト成果物

**1依頼 = 原則 `output.md` 1ファイル**

```
output/<client>/<YYYYMMDD>/<task-name>/
├── output.md                  # ユーザーが読む成果物（常時・必須）
└── _internal/                 # 内部用（条件付き・普段は開かない）
    ├── work_plan.md
    ├── quality_review_report.md
    └── ...
```

## `output.md` の構成

```markdown
# <成果物タイトル>

- 依頼の理解: <1〜2行。読み違い検知用>
- 担当Role / モード: <Role> / <Opinion|Design|Implementation|Verification>
- 出力モード: <quick|standard|detailed|implementation|review|handoff|obsidian>
- ステータス: <Draft|In Progress|Completed|Accepted|...>
- 品質判定: <PASS|PASS_WITH_CONDITIONS|REWORK_REQUIRED|BLOCKED|レビュー対象外>
- 要対応（セレスへ）: <ブロッキング質問・承認待ち。無ければ「なし」>

## 1. 結論サマリー
## 2. 今回の判断
## 3. 本成果物
## 4. 確認事項     ← 必要時のみ。不要なら省略
## 5. 次アクション
## 補足            ← 必要時のみ。「詳細は _internal/ 配下。通常確認不要」
```

**ルール:**
- 不要セクションは機械的に出さず省略する
- 「該当なし」とも書かない
- §3が大きなコード/SQL/設計の場合のみ長文を許可する
- 先頭ブロック＋§1を必ず冒頭に置き、結論を後ろに回さない
- 制御ブロック（依頼の理解〜要対応）は旧 deliverable_summary.md の制御項目を吸収したもの

## 出力モード（自動判定）

ユーザーに選ばせない。依頼文から自動判定し、output.md 先頭ブロックに記載する。

| モード | 用途 | 出力方針 | 自動判定トリガー例 |
|---|---|---|---|
| quick | 軽い相談・方向性確認 | 短く結論中心 | 一行相談、軽微依頼 |
| standard | 通常依頼（デフォルト） | 結論サマリー＋本成果物 | 明示語なし |
| detailed | 設計・分析・比較 | 必要な詳細を含む | 「詳しく」 |
| implementation | コード・設定・実装 | 実装物中心 | 「実装レベルで」「コードで」 |
| review | レビュー・添削 | 指摘・修正案中心 | 「レビューして」「添削して」 |
| handoff | 他AI・人間へ渡す | 再利用可能形式 | 「Claude Codeに渡す」「引き継ぎ」 |
| obsidian | 第二の脳保存 | Markdown整理 | 「Obsidianに残す」「第二の脳」 |

## 複数Role成果物の統合ルール

複数のAI社員・Roleが選ばれた場合でも、Role別成果物をそのまま全量ユーザーに渡さない。

**禁止（悪い例）:**
```text
pmo_deliverable.md
engineer_deliverable.md
reviewer_deliverable.md
```

**推奨（良い例）:**
```text
output.md                  ← Optimizerが統合・編集した最終版
_internal/pmo_notes.md     ← 要求時のみ確認可
_internal/engineer_notes.md
```

**統合ルール:**
- Role別出力は内部材料扱いにする
- 意見が割れた場合は §1結論サマリーに論点だけ出す
- 各Roleの全文ログは要求時のみ `_internal/<role>_notes.md` で確認可
- 「誰が何を担当したか」は必要な場合のみ簡潔に記載する

## 長文に関するルール

長文を完全に禁止しない。必要な長文は許可する。

- 標準出力で不要な長文を出さない
- チーム内部の作業ログをそのまま出さない
- 詳細は必要なセクションだけに閉じ込める
- 結論を必ず先頭に置く
- 補足・詳細・内部ログは §補足 または `_internal/` に格納する
- **本成果物（§3）そのものが長文である場合のみ、長文を許可する**

重要なのは「短くすること」ではなく、**読む順番と情報の濃淡を設計すること**。

## 参照

- `ai_team/output_optimization_policy.md` — 3階層ゲート・必要性ゲート
- `ai_team/professional_response_templates.md` — モード別必須核
- `templates/output_template.md` — output.md の雛形
- `.claude/agents/deliverable-optimizer.md` — Optimizerの独立subagent定義
