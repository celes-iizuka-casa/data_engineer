# Runtime Neutral Design Policy

## 目的

AIエンジニアチームの Role / Skills / Workflows を、Claude Code でも Codex でも実行できる runtime-neutral な構成に保つための設計原則を定義する。特定の実行環境に閉じたチームにしない。

## 原則

- Role定義に Claude Code 固有機能（特定のツール名・UI・サブエージェント機構など）を前提として書かない
- Skillsは Markdown / YAML ベースで定義する（実行環境に依存しない記述）
- `input/` を起点、`output/` を成果物出力先とする共通インターフェースにする
- 実行環境依存の内容は runtime policy（`runtime_selection_policy.md` / `claude_code_execution_policy.md` / `codex_execution_policy.md`）に分離する
- Claude Code用とCodex用の実行ガイドを分ける（`claude_code_team_execution.md` / `codex_team_execution.md`）
- 成果物のファイル構成は共通化する（output.md ＋ `_internal/`）
- 作業結果は `output/` に集約する
- 第二の脳への書き込みルールは共通化する（`obsidian_write_policy.md`）

## 守ること

- 新規 Role / Skill / Workflow / Template を作るときは、両 runtime で読める記述か確認する
- 実行環境固有の手順は本体に書かず、対応する execution policy / team execution guide に書く
- モデル名・工数は runtime policy で扱い、Role/Skill本体には初期推奨のみ書く

## やってはいけないこと

- Codexで実行できないRole / Skills構造にする
- Codexが読むべきガイドを作らない
- 実行環境固有の前提をRole/Skill本体に埋め込む

## 完了条件

同一の input/output 契約で、Claude Code / Codex の双方が Role / Skill / Workflow を読んで実行できる。

## 参照

- `ai_team/runtime_selection_policy.md`
- `ai_team/claude_code_execution_policy.md`
- `ai_team/codex_execution_policy.md`
- `claude_code_team_execution.md`
- `codex_team_execution.md`
- `ai_team/obsidian_write_policy.md`
