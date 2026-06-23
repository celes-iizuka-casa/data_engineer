# Claude Code Team Execution Guide

## 目的

Claude CodeでAIエンジニアチームを実行するためのガイド。判断基準は `ai_team/runtime_selection_policy.md` / `ai_team/model_effort_selection_policy.md`、実行ルールは `ai_team/claude_code_execution_policy.md` を参照する。

## Claude Codeで優先する作業

- AI社員チーム構築
- Role / Skills設計
- Workflow設計
- FDE設計
- Knowledge Curator設計
- プロンプト設計
- 大規模な方針整理
- 顧客課題整理
- MVPスコープ設計

## 実行フロー

1. `input/` を確認する
2. `README.md` / `ai_team/README.md` を確認する
3. `ai_team/model_effort_selection_policy.md` を確認する
4. `ai_team/runtime_selection_policy.md` を確認する
5. 必要なRole / Skillを読む
6. `output/.../_internal/execution_plan.md` を作る（Role選定・実行環境・モデル・工数・理由を統合）
7. 採用 実行環境/モデル/工数 を output.md 制御ブロックに記す
8. 実作業を行う
9. `output/.../output.md` を作る（制御ブロック＋本成果物）
10. 必要に応じて検証・task_retrospective を作る（必要性ゲート）
11. Completed / Accepted 後に Knowledge Curator へ渡す

## 使用モデル

- Opus4.8: 低 / 中 / 高 / 特大 / Max / Ultracode
- Sonnet4.6: 低 / 中 / 高 / Max
- Haiku4.5

## Codexと併用すべき場合

- 実装がある場合
- リポジトリ内コード修正がある場合
- SQL / Python / Terraform / dbt を直接修正する場合
- 大量ファイルの差分修正がある場合

## 完了条件

Claude Codeで設計し、必要に応じてCodexへ実装を渡せる。Codexと同じ input/output 契約で動作する。

## 参照

- `ai_team/claude_code_execution_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `codex_team_execution.md`
