# Claude Code Team Execution Guide

## Contract

このガイドはClaude CodeからAI社員チームを呼び出した場合だけ使う。別Runtimeを選択・起動するrouterではない。

## 実行フロー

1. `input/`、既存`output/`、Current Evidenceを確認する。
2. `personalization_policy.md`で現在利用者のLocal contextを任意読込する。
3. Task/Risk/Capabilityを分類し、必要最小限のRoleとSkillを選ぶ。新規領域で既存Role / Skillに不足がある場合は `ai_team/capability_gap_policy.md` に従いAI Capability ArchitectがGap判定を行う（新Role追加はCeles Human Gate必須）。
4. 現在のClaude Code Runtimeを`observed`または`declared`として記録し、Model ID不明時は`unavailable`とする。
5. 現在Runtime内で実装・検証する。別Provider APIを呼ばない。
6. Risk-based reviewとHuman Gateを適用し、`output.md`へ結果を統合する。
7. Canonical promotionはIndependent ReviewとCeles Human Gate後に別途行う。

## 参照

- `ai_team/claude_code_execution_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/workflows/input_to_output_workflow.md`
