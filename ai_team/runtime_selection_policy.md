# Runtime Selection Policy

## 目的

Claude Code と Codex のどちらで作業を実行するかを判断する。AIエンジニアチームは Claude Code 専用にせず、両方で実行可能（runtime-neutral）に保つ。

## 基本方針

- AI社員チームの構築・設計・改善は Claude Code を優先する
- リポジトリ内のコード実装・差分修正は Codex を優先する
- 設計と実装が両方ある場合は併用する
- 実行環境の選択理由を記録する（`_internal/execution_plan.md`）
- どちらでも実行できるように、Role / Skills は runtime-neutral に保つ（`runtime_neutral_design_policy.md`）

## Claude Codeを優先する条件

- Role / Skills / Workflow の設計
- AI社員チームの構築・改善・再設計
- 複数Roleの責務整理
- FDE / PMO / Knowledge Curator などの役割設計
- 複雑な方針検討 / プロンプト設計
- 顧客課題整理 / MVPスコープ設計
- 大規模な仕様整理 / 長文ドキュメント群の整合性確認
- 戦略・設計・構想寄りの作業
- セレスの意図を深く読み取る必要がある作業
- 第二の脳の構成設計

推奨:

```yaml
runtime: Claude Code
model:
  default: Opus4.8
  effort: 高
  escalation: [特大, Max, Ultracode]
```

## Codexを優先する条件

- リポジトリ内の実装 / 既存コードの差分修正
- Python / SQL / DDL / Terraform / dbt model 修正
- API / バックエンド / フロントエンド実装
- テストコード作成
- ファイル横断の機械的修正
- 実行可能な成果物の作成
- コードレビュー

推奨:

```yaml
runtime: Codex
model: GPT-5.5
effort:
  default: 高
  escalation: [非常に高い]
```

## 併用する条件

以下は Claude Code（計画・設計）と Codex（実装）を併用する。

- 設計から実装まである作業
- AI社員チームのRole設計と実装ファイル更新の両方を含む作業
- 複雑なデータ基盤構築
- RAG / LLMアプリの商用化設計と実装
- 複数SQLの一括修正方針と実装
- Terraform moduleの設計と実装
- 大きめのWebアプリ / 業務アプリ開発

推奨分担:

```yaml
planning_and_design:
  runtime: Claude Code
  model: Opus4.8
  effort: 高
implementation:
  runtime: Codex
  model: GPT-5.5
  effort: 高
verification:
  runtime: [Claude Code, Codex]
  model: { claude_code: Opus4.8, codex: GPT-5.5 }
  effort: { claude_code: 中, codex: 高 }
```

## 判断の優先順位（迷ったとき）

1. 成果物がコード/SQL/IaC/dbt/テストか → Codex 優先
2. 成果物がRole/Skill/Workflow/方針/長文設計か → Claude Code 優先
3. 両方含む → 併用（設計=Claude Code、実装=Codex）
4. どちらとも言えない軽量作業 → どちらでも可。コスト最小（Claude Code: Haiku / Codex: 低）

## 実行環境の出力形式

選択結果と理由は必ず `output/.../_internal/execution_plan.md`（`templates/execution_plan_template.md`）に記録し、採用した実行環境を output.md 制御ブロックの「実行環境」欄に表示する。

## 参照

- `ai_team/model_effort_selection_policy.md`
- `ai_team/claude_code_execution_policy.md`
- `ai_team/codex_execution_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
- `templates/execution_plan_template.md`
- `claude_code_team_execution.md`
- `codex_team_execution.md`
