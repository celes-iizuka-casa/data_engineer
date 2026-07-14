# Local Second Brain Read / Write Policy

## 目的

現在利用者のSecond BrainだけをLocal Private Stateとして利用し、未確定情報・他利用者情報・顧客情報を共有AI社員Coreへ混入させない。

## Root解決と分離

Rootは `personalization_policy.md` の順序（明示指定 → `SECOND_BRAIN_ROOT` → `.local/second_brain.yaml`）で解決する。ハードコードした個人pathやhome directory scanは使わない。

- rootがない: 正常なno-opとして継続する
- rootの所有者が不明: 読み書きしない
- 他利用者のroot: 読み書きしない
- Second Brain内容: Git commit、Telemetry、remote syncを禁止する

## 読み込み

作業開始時に利用可能ならUser-local Second Brainを個人コンテキストとして使う。ただし優先順位は次のとおり。

`Current Explicit Request > Current Evidence > User-local Second Brain > Shared Core > General Knowledge`

矛盾時はCurrent Evidenceを優先する。Second Brainの記述を現在のコード・データ・設定を確認したEvidenceとして扱わない。

## 書き込みGate

次のいずれかを満たす場合だけKnowledge Curatorが書き込み候補を作る。

- Celesまたは現在利用者が明示的に同期を依頼した
- 成果物が`Accepted`で、再利用価値があり、Local rootが確認済み

`Draft`、`In Progress`、`Waiting for Celes Review`、`Verification Pending`は正式知識化しない。`Completed`だけではCanonical GrowthやUniversal Knowledgeへ昇格しない。

## 書き込み手順

1. 現在利用者とLocal rootを確認する。
2. 対象成果物のstatus、Independent Review、Human Gateを確認する。
3. 案件固有情報、Personal preference、Universal candidateを分離する。
4. 機密・個人・顧客・secretを除外する。
5. Project Note / Pattern / ADR / Troubleshooting / source mapを必要最小限で更新する。
6. 同期結果を `output/.../_internal/obsidian_sync_summary.md` に記録する。

既存ノートを無条件上書きせず、競合は利用者判断へ戻す。Second BrainからSkill/Policyを直接更新しない。

## Canonical Growthとの境界

Second BrainはPersonalizationとLocal Knowledgeのsourceであり、Canonical Growth Authorityではない。Universal candidateは `capability_growth_policy.yaml` のEvidence・Before/After Eval・Independent Review・Celes Human Gateを通す。

## 参照

- `ai_team/personalization_policy.md`
- `ai_team/governance/capability_growth_policy.yaml`
- `ai_team/workflows/engineering_knowledge_curation_workflow.md`
