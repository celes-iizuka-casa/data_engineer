# Runtime Neutral Design Policy

## 目的

AI社員のIdentity、Role、Capability、Quality StandardをProvider/Modelから分離し、呼び出し元Runtimeで同じ共有Coreを利用できるようにする。

## Shared Coreに含めるもの

- Identity / Role / Responsibilities / Decision Rights
- Capability / Evidence / Done Definition
- Skills / Workflows / Quality Gates
- Collaboration / Review / Handoff / Evaluation criteria

## Runtime adapterに分離するもの

- Runtime固有toolの呼び方
- UI metadataやprovider adapter（例: `agents/openai.yaml`）
- 現在利用可能なModelの表示
- sandbox、権限、approvalの具体操作

Runtime adapterはIdentity Authorityを持たない。

## 禁止事項

- Role/Skillを特定Provider用社員として定義する
- Role/Skillへ具体Modelを固定する
- AI社員が別Runtime/APIへ自動fallbackする
- Recommendationを実行強制として扱う
- Runtime固有tool名を共有Role/Skillの必須前提にする

## 共通interface

- `input/`: Local Private task input
- `output/<client>/<date>/<task>/output.md`: Local Private deliverable
- `_internal/`: Local Private plan/evidence/review
- `ai_team/`, `skills/`, `templates/`: Shared Core

## 完了条件

同じRole/Skill/Workflowが対応Runtimeから読め、実行元を変更せず、同じEvidence/Review/Output contractで完了できる。

## 参照

- `ai_team/runtime_selection_policy.md`
- `ai_team/governance/architecture_contract.yaml`
- `ai_team/evidence/execution_evidence.schema.json`
