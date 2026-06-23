# Codex Team Execution Guide

## 目的

CodexでもAIエンジニアチームを実行できるようにする。判断基準は `ai_team/runtime_selection_policy.md` / `ai_team/model_effort_selection_policy.md`、実行ルールは `ai_team/codex_execution_policy.md` を参照する。

## 基本思想

- AI社員RoleはMarkdown/YAMLで定義する
- SkillsはCodexでも読める構造にする
- `input/` を起点にする
- `output/` に成果物を出す
- Codex実行時も `_internal/execution_plan.md`（Role選定・実行環境・モデル・工数を統合）を作成する

## 実行フロー

1. `input/` を確認する
2. `README.md` / `ai_team/README.md` を確認する
3. `ai_team/model_effort_selection_policy.md` を確認する
4. `ai_team/runtime_selection_policy.md` を確認する
5. 必要なRole / Skillを読む
6. `output/.../_internal/execution_plan.md` を作る
7. 採用 実行環境/モデル/工数 を output.md 制御ブロックに記す
8. 実作業を行う
9. `output/.../output.md` を作る
10. 必要に応じて検証・task_retrospective を作る（必要性ゲート）
11. Completed / Accepted 後に Knowledge Curator へ渡す

## Codexで優先する作業

- SQL / Python / Terraform / dbt
- API / フロントエンド / バックエンド
- テスト
- 既存ファイル修正 / 差分実装

## Codexで注意する作業（Claude Code併用推奨）

- AI社員チーム全体の思想設計
- Role責務の大規模再定義
- セレスの文体・意図の深い反映
- Obsidian全体構成の大規模改修

## Codex使用モデル

- GPT-5.5 低
- GPT-5.5 中
- GPT-5.5 高
- GPT-5.5 非常に高い

## 完了条件

Codexでも、Claude Codeと同じ input/output 契約でAIエンジニアチームを実行できる。

## 参照

- `ai_team/codex_execution_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `claude_code_team_execution.md`
