# Runtime Selection Policy

## 目的

AI社員を呼び出し元Runtimeへ従属させ、AI社員自身によるProvider/Runtime切替や別Provider API呼び出しを防ぐ。

## Non-negotiable contract

> Recommendation ≠ Enforcement.

- 実行環境は呼び出し元Runtimeで確定する。
- AI社員は現在のRuntime、Provider、Model、token sourceを上書きしない。
- Cross-provider invocation、fallback、dynamic provider switchingを禁止する。
- Role / Skill / WorkflowにProviderまたはModel固定identityを埋め込まない。
- 現在のRuntimeで不足する能力がある場合は、実行を勝手に移さず、制約とhandoff候補を報告する。
- チーム拡張（`agent_creation_policy.md` / `skill_creation_policy.md`）で追加されるRole / Skillにも本契約を適用し、ProviderまたはModel固定identityを与えない。

## 実行計画への記録

`execution_plan.md` には選択結果ではなく、現在の実行contextをEvidence付きで記録する。

| 項目 | 記録方法 |
|---|---|
| runtime | 実測できた場合は`observed`。利用者申告だけなら`declared` |
| provider | 実測または明示されない限り推測しない |
| model | 正確なIDを取得できない場合は`value: null / evidence_type: unavailable` |
| token / cost | 実測できない場合は`value: null / evidence_type: unavailable` |
| effort | 現在Runtime内での推奨深度。実Model設定の強制ではない |

## Runtime-specific guideの位置付け

`claude_code_execution_policy.md` と `codex_execution_policy.md` は、そのRuntimeから呼ばれた場合の操作ガイドであり、Runtime routerではない。両方を跨ぐ自動実行を命令しない。

## 完了条件

- 同一Role/Skillがどの対応Runtimeからでも読める。
- 実行は呼び出し元Runtime内で完結する。
- 別Runtimeが有利という推奨があっても、現在の実行元を変更しない。
- Cross-provider APIや自動fallbackを導入していない。

## 参照

- `ai_team/runtime_neutral_design_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/governance/architecture_contract.yaml`
