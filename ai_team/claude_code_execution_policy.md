# Claude Code Execution Policy

## 目的

Claude Code でAIエンジニアチームを実行する際の実行ルールを定義する。手順ガイドは `claude_code_team_execution.md`、判断基準は `runtime_selection_policy.md` / `model_effort_selection_policy.md` を参照する。

## Claude Codeで優先する作業

- AI社員チーム構築 / Role・Skills設計 / Workflow設計
- FDE / PMO / Knowledge Curator などの役割設計
- プロンプト設計 / 大規模な方針整理
- 顧客課題整理 / MVPスコープ設計
- 長文ドキュメント群の整合性確認
- 第二の脳の構成設計

## 使用モデルと工数

| モデル | 工数 | 主な用途 |
|---|---|---|
| Opus4.8 | 高 | 設計・方針・チーム改良の標準 |
| Opus4.8 | 特大 | 複数Role/Skill影響・広範囲差分・全体整合性重視 |
| Opus4.8 | Max | 複数Workflow横断の大規模改修・設計実装検証混在 |
| Opus4.8 | Ultracode | チーム自体の大規模再設計・最重要（常用しない・理由明記） |
| Sonnet4.6 | 中 | 通常ドキュメント・小〜中設計整理 |
| Sonnet4.6 | 高 / Max | 大きめだがコスト配慮したい作業 |
| Haiku4.5 | （指定なし） | 軽量タスク・要約・整形 |

## 実行原則

- 既存構成を壊さない（追記・差分優先、見出し・スキーマ維持）
- 不明な外部仕様を断定しない（公式資料または実データで確認）
- 破壊的変更には理由・影響範囲・移行・ロールバックを付ける
- 作業前に `_internal/execution_plan.md` を作る（model/effort/runtime と理由）
- 高工数（特大/Max/Ultracode）はセレス確認点を作る
- runtime-neutral を維持し、Claude Code 固有機能を Role/Skill 定義の前提にしない

## Codexと併用すべき場合

- 実装がある場合
- リポジトリ内コード修正がある場合
- SQL / Python / Terraform / dbt を直接修正する場合
- 大量ファイルの差分修正がある場合

この場合、Claude Codeで設計し、実装をCodexへ渡す（`runtime_selection_policy.md` の併用条件）。

## 完了条件

Claude Codeで設計し、必要に応じてCodexへ実装を渡せる。input/output契約は Codex と共通。

## 参照

- `claude_code_team_execution.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/codex_execution_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
