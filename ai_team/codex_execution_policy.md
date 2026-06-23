# Codex Execution Policy

## 目的

CodexでAIエンジニアチームを実行する際の実行ルールを定義する。手順ガイドは `codex_team_execution.md`、判断基準は `runtime_selection_policy.md` / `model_effort_selection_policy.md` を参照する。AIエンジニアチームを Claude Code 専用にしないための実体ポリシー。

## Codexで優先する作業

- SQL / Python / DDL / Terraform / dbt model
- API / バックエンド / フロントエンド実装
- テストコード作成
- 既存ファイルの差分修正
- ファイル横断の機械的修正
- リポジトリ内の実装・コードレビュー

## Codexで注意する作業（Claude Code併用推奨）

- AI社員チーム全体の思想設計
- Role責務の大規模再定義
- セレスの文体・意図の深い反映
- Obsidian全体構成の大規模改修

## 使用モデルと工数

| モデル | 工数 | 主な用途 |
|---|---|---|
| GPT-5.5 | 低 | 軽量タスク・整形・単純修正 |
| GPT-5.5 | 中 | 通常実装・単発SQL/Python修正・軽めレビュー |
| GPT-5.5 | 高 | 設計込み実装・既存コード読解修正・Sec/運用/テスト観点（標準） |
| GPT-5.5 | 非常に高い | 複数ファイル横断・既存コード/SQL/Terraform/dbt深読み改修・高リスク（常用しない・理由明記） |

## 実行原則

- input/ を起点にし、output/ に成果物を出す（Claude Codeと共通のinput/output契約）
- Role/SkillはMarkdown/YAMLとして読む（Claude Code固有機能を前提にしない）
- 作業前に `_internal/execution_plan.md` を作る（model/effort/runtime と理由）
- 既存構成を壊さない（差分修正優先）
- 破壊的変更には理由・影響範囲・移行・ロールバックを付ける
- 高工数（非常に高い）はセレス確認点を作る
- 繰り返し作業は代表例確認フローと組み合わせる

## 完了条件

Codexでも、Claude Codeと同じinput/output契約でAIエンジニアチームを実行でき、`_internal/execution_plan.md` と output.md を生成できる。

## 参照

- `codex_team_execution.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/claude_code_execution_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
