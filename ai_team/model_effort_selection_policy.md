# Model Effort Selection Policy

## 目的

呼び出し元Runtimeと現在選択済みModelを変更せず、タスクのRiskに応じて必要な推論深度・探索量・検証深度を提案する。

## 原則

- Model/effortの提案はRecommendationでありEnforcementではない。
- AI社員がProvider、Runtime、Modelを切り替えない。
- 具体Model名はRuntimeから`observed`または利用者から`declared`された場合だけ記録する。
- 未確認のModel名・token・costを推測しない。
- RoleごとにModelを固定しない。Task、Risk、blast radius、reversibilityで判断する。

## Effort tier

| Tier | 適用例 | 最低限の作業深度 |
|---|---|---|
| low | typo、整形、単一の可逆な軽微変更 | 対象確認 + focused check |
| medium | 通常実装、限定設計、単発review | 影響確認 + relevant tests |
| high | 複数file、Architecture、Security/Data/Operations | alternatives + specialist lens + regression |
| very_high | 全体基盤、不可逆変更、Critical risk | phase validation + independent specialist review + human gate |

Tierは現在Runtime内の作業深度を表し、Model parameterを変更する命令ではない。

## 判定因子

- production impact
- destructive or irreversible operation
- schema/data loss risk
- authentication/authorization/secrets/PII
- financial or contractual impact
- external dependency uncertainty
- large blast radius
- cross-artifact consistency
- rollback cost

## 工程別の推奨能力

| 工程 | 必要能力 |
|---|---|
| 依頼解析 | long-context comprehension、ambiguity detection、evidence discipline |
| 設計 | architecture reasoning、trade-off、security/reliability |
| 実装 | repository comprehension、precise editing、testing |
| 検証 | adversarial review、regression、specialist checks |
| 文書化 | consistency、traceability、human/AI readability |

## 記録

`output/.../_internal/execution_plan.md` とExecution Evidenceには、現在のruntime/modelについて確認できたEvidenceだけを書く。取得不能な値は`unavailable`とする。

## Human Gate

High/Critical、不可逆操作、Canonical promotionでは、effort推奨だけで進行可否を決めない。`risk_based_quality_gates.yaml` とHuman Gateを適用する。

## 参照

- `ai_team/model_selection_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/review/risk_based_quality_gates.yaml`
- `ai_team/evidence/execution_evidence.schema.json`
