# Data Migration Plan

## 1. Purpose, Scope, and Exclusions

## 2. Owners and Decision Rights

| Decision / Action | Responsible | Accountable | Consulted | Evidence |
|---|---|---|---|---|

- Migration orchestration / acceptance: wave、Gate、rehearsal、cutover/rollback、最終Evidenceの統制
- Data-plane implementation: bulk/delta/CDC、変換・照合SQL、データ品質、backfill/replayの実装
- 上記2責務の担当Role、境界、handoff acceptanceを表に明記する。

## 3. Migration Inventory and Dependencies

| Asset | Asset Type | Grain / Key or Execution Unit | Volume / Change Rate | Upstream / Downstream | Data Class | Compatibility Disposition | Owner | Wave |
|---|---|---|---|---|---|---|---|---|

Asset Type must cover applicable tables/files/streams as well as views, materialized views, UDFs/procedures, jobs, grants, masking/row policies, integrations/connections, secret references, orchestration, and BI semantic models. Each non-data asset needs a target mapping, rebuild/replace/retire decision, dependency owner, and validation evidence.

## 4. Source and Target Contract

| Source Object / Field | Target Object / Field | Source Type | Target Type | Precision / Scale / Collation / Constraint / Nullability | Transformation | Timezone / Delete / History Semantics | Compatibility Disposition | Validation Evidence |
|---|---|---|---|---|---|---|---|---|

Compatibility Disposition: preserve / translate / emulate / rebuild / accepted difference / retire. Accepted differences require an owner, downstream impact, acceptance criterion, and approval evidence.

## 5. Strategy and State Transitions

- Strategy: Big Bang / Phased / Parallel Run / Bulk + Delta or CDC
- States: inventory → mapped → bulk-loaded → delta-synced → reconciled → cutover-ready → cut over / rolled back → verified
- Checkpoint and restart boundary:
- Dual-write or source-of-truth rule:
- Authoritative write start point and target-only write detection:
- Post-write return path: verified reverse CDC / replay / dual-write, or rollback prohibited and forward-fix required:
- Immutable baseline / manifest location, revision, hash, and retention:

## 6. Wave and Dependency Plan

| Wave | Objects | Entry Criteria | Exit Criteria | Rollback Unit | Dependencies |
|---|---|---|---|---|---|

## 7. Data Volume, Performance, Capacity, and Cost

| Measure | Baseline | Target / Limit | Rehearsal Result | Evidence | Owner |
|---|---|---|---|---|---|

Target infrastructure readiness must separately cover connectivity/network/DNS or private endpoints, IAM/service identities, quota, compute/storage/catalog capacity, secret distribution, monitoring access, and an accountable Cloud owner. 未検証項目はopen gateとし、Plan-readyをCutover-readyと表現しない。

## 8. Bulk, Delta / CDC, and Freeze Plan

- Bulk extraction watermark:
- Delta capture start and ordering:
- Duplicate, delete, late-arrival, and schema-change handling:
- Freeze start/end and exception process:

## 9. Quantitative Reconciliation

| Check | Gate Class | Grain / Scope | As-of Watermark | Query / Contract Version | Normalization | Expected | Threshold / Exact Rule | Actual | Evidence | Difference Handling / Exception Expiry | Approver |
|---|---|---|---|---|---|---|---|---|---|---|---|

Minimum checks: counts, distinct keys, key aggregates, nulls, deletes, history, time boundaries, access-control parity, and full-coverage value reconciliation. Source and target must use the same immutable baseline or as-of watermark; serialization, timezone, decimal, NULL, and delete normalization must be versioned.

Hard gates use exact/zero-difference rules by default for key completeness/uniqueness, missing or extra deletes, referential integrity newly introduced by migration, access-control/masking parity, unauthorized exposure, and unresolved CDC gaps. Soft tolerance is allowed only for an explicitly justified measure such as approved rounding; record rationale, impact, exception owner, expiry, remediation, and Human Gate approval. A generic non-zero threshold must not weaken a hard gate.

For lossless mappings, compare every in-scope row/value using a deterministic canonical row hash aggregated by partition, or an equivalent full column comparison; preserve mismatch keys for drill-down without exposing sensitive values. Sampling is supplementary diagnostics and never substitutes for full-coverage acceptance. For approved transformations, use a contract-specific full-coverage invariant or deterministic expected-output check, with the transformation version and owner recorded.

## 10. Rehearsal and Failure Recovery

| Scenario | Injection / Procedure | Expected Recovery | Actual | RTO / RPO | Evidence |
|---|---|---|---|---|---|

## 11. Cutover Runbook and Go / No-Go

| Time | Action | Responsible | Precondition | Evidence | Decision / Rollback Point |
|---|---|---|---|---|---|

## 12. Rollback / Forward-fix Plan

- Trigger and decision owner:
- Before authoritative target writes: source route restoration and verification procedure:
- After target-only writes: reverse CDC / replay / dual-write proof, ordering/idempotency, and latest common watermark:
- If the return path is unverified: write freeze, incident ownership, and forward-fix procedure; do not label source retention as rollback readiness:
- Target recovery point and maximum execution time:
- Source/target restoration and write-routing procedure:
- Allowed data loss / RPO and explicit approval:
- Full reconciliation after rollback or forward-fix:

## 13. Security, Audit, and Data Retention

| Control | Data / Principal Scope | Expected | Test Procedure | Actual | Evidence | Owner / Approver |
|---|---|---|---|---|---|---|

Minimum controls: data classification, least-privilege IAM, row/column/masking parity, encryption, secret handling, audit logging, log redaction, residency, retention/deletion, legal hold, and emergency access. 未検証または未承認のaccess-control差分はGo/No-Goの停止条件とする。

## 14. Stakeholder Sign-off Points

| Gate | Required Evidence | Acceptance Criteria | Accountable Owner | Reviewer | Decision / Timestamp |
|---|---|---|---|---|---|

At minimum: data contract/baseline、bulk + delta reconciliation、Security / Privacy parity、performance / capacity / cost、rollback drill、cutover Go/No-Go、post-cutover acceptance、source decommissionを分離して承認する。

## 15. Post-migration Verification and Monitoring

| Check / SLI | Baseline | SLO / Threshold | Observation Window | Alert / Stop Condition | Owner | Evidence |
|---|---|---|---|---|---|---|

## 16. Assumptions, Open Issues, and Residual Risks
