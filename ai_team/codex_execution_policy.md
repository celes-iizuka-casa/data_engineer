# Codex Execution Policy

## 目的

Codexから呼び出された場合に、AI社員チームをそのCodex実行環境内で安全に動かす。

## 実行原則

- 現在のCodex Runtime、選択済みModel、token sourceを使う。
- AI社員側からClaude APIや別Providerへ切り替えない。
- Role/Skill/Workflow本体へCodex固有identityを埋め込まない。
- Current Request、Current Evidence、User-local Second Brain、Shared Coreの優先順位を守る。
- Repository変更は差分優先で、Riskに応じてテスト・独立レビュー・Human Gateを適用する。

## Model / effort

利用可能な具体Model名をAI社員が推測・固定しない。現在Runtime内で必要能力とeffort tierを推奨できるが、実Model設定を上書きしない。

## Handoff

他Runtimeが有利と判断しても自動移行しない。未完了事項、必要能力、Evidence、再開条件をhandoff候補として報告し、現在の実行は現在Runtime内で扱う。

## 参照

- `codex_team_execution.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
