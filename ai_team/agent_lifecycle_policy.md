# Agent Lifecycle Policy

## 目的

AI社員Roleの追加・更新・非推奨化・削除を管理する。正本は `ai_team/governance/ai_employee_lifecycle_registry.yaml`（Role）と `ai_team/governance/skill_lifecycle_registry.yaml`（Skill）。本書はその運用ルールをまとめた実務ガイド。

## Agent Status

運用上の呼び名と、governance登録簿の正式stateの対応:

| 運用ステータス | 正式state（登録簿） | 意味 |
|---|---|---|
| proposed | DISCOVERED / PROPOSED / CANDIDATE / HUMAN_GATE | 提案〜承認待ち。実務投入しない |
| experimental | EVALUATED / INDEPENDENTLY_REVIEWED | 評価・独立レビュー中。限定的な試行のみ |
| active | ACTIVE | 正式運用中（Celes Human Gate承認済み） |
| deprecated | DEPRECATED | 非推奨。新規依頼に割り当てない |
| retired | DEPRECATED（登録簿上は維持） | 退役。定義は履歴として保持し、削除しない |

## Human Gate証跡ルール（CREATE系、2026-08-04 セレス追認）

セレスの明示指示がある場合、その指示原文をHuman Gate承認証跡として扱ってよい（Human Gateの省略ではない）。ただし、CREATE系の変更では次を必ず保存する。

- 指示原文
- 追加理由
- Capability Gap判定
- 追加対象Role / Skill
- 影響範囲
- Rollback可能性
- decision_history

`Celes-HG-20260802-CAPABILITY-ARCHITECT-CREATE` / `Celes-HG-20260802-CAPABILITY-SKILLS-CREATE` は有効な承認証跡として追認済み（追認指示原文: `input/Celes/依頼/20260804_capability_gap_acceptance.md`）。decision_history / promotion_historyは「subject_id + subject_revisionごとに一意なPROMOTE記録」を要求する（`tools/validate_repository.py` の `missing_unique_decision_history` 検査）ため、実体（Role/Skill定義）が変わらない今回のような追認では、既存のCREATE記録に対して重複するPROMOTEエントリを新規追加しない。追認内容そのものは本節のルール反映と `output/.../output.md` / `acceptance_update_report.md` で記録する。

## Accepted（output.md上のステータス）について

`Accepted` は `output.md` の統合報告レベルのステータスであり、本登録簿の正式state（DISCOVERED〜ACTIVE〜DEPRECATED）とは別軸である。すでにACTIVEなRole / Skillに対してセレスが要対応事項を追認した場合、登録簿のstate・decision_history・promotion_historyは変更しない（decision_historyはsubject_id + subject_revisionごとに一意なPROMOTE記録のみを許すため、実体変更を伴わない追認で重複エントリを追加することはできない）。追認内容は本ポリシーのルール反映と `output.md` のステータス更新（Completed→Accepted）・要対応項目の解消記録で表現する。登録簿への新規エントリが必要なのは、Role/Skill定義の実体変更（UPDATE等でrevisionが変わる場合）のみである。

## 新規追加

1. `capability_gap_policy.md` でAgent Gapを確定する
2. `agent_creation_policy.md` のCREATE基準7項目を証跡化する
3. Role定義・Skill一式・登録内容を作成する（disposition: CREATE）
4. before/after eval（Foundation evals）・独立レビュー・Celes Human Gateを通す
5. decision_historyにPROMOTE記録を残し、ACTIVEにする

同一タスク内でCREATE〜promotedまでを一括登録する場合（セレスの明示指示があるときのみ許容）は、次の全てを満たすまで作業を完了扱い（Completed）にしない: (1) `independent_review_ref` の参照先レビュー報告書が実在する、(2) `before_after_eval_ref` の評価記録が実在する、(3) レビューVerdictがREWORK_REQUIRED / BLOCKEDの場合は指摘を解消し再判定を得ている。満たせない場合はcandidate_stateをHUMAN_GATE以前へ戻す。登録簿への確定記録（ACTIVE / promoted）より先に、参照される証跡ファイルを実在させることを原則とする。

レビューで差し戻し（REWORK_REQUIRED / BLOCKED）が出た場合の再判定は、同一の `quality_review_report.md` への追記（再判定セクション）として記録し、登録簿の `independent_review_ref` は常にその報告書（最新判定を含む）を指す。decision_historyへ追記するのはCelesの決定（PROMOTE / REJECT / REWORK / ROLLBACK）のみで、レビュアー判定そのものは決定として記録しない。

P1差分に限定した再レビュー（全体を再レビューせず、指摘差分のみを再検証する方式）は、次をすべて満たす場合にのみ許容する（2026-08-04 セレス追認）:
- P1原因が局所的である
- 修正対象が明確である
- 設計全体に波及しない
- Specialist Reviewが通っている
- 差分レビュー範囲が記録されている
- 未レビュー範囲が明記されている

## 更新

- Role定義・capability entry・共通契約のいずれかを変更するとrevisionが変わるため、候補（candidate_revision + transition）として登録し、同じゲート（eval・独立レビュー・Human Gate）を通す（disposition: UPDATE / MERGE / SPLIT）。
- 登録なしの canonical変更はvalidatorが検出して失敗させる。

## 非推奨化

- DEPRECATEもHuman Gateを要する（disposition: DEPRECATE、candidate_state: DEPRECATED）。
- 「使われていない」だけでは非推奨化の根拠にならない（no_usage_is_not_deprecation_evidence）。品質・重複・境界の証跡を添える。
- 非推奨化したRoleの依頼は、後継Roleへの割当先を `role_scope_matrix.md` に明記する。

## 削除

- 定義ファイルと登録簿エントリの物理削除は行わない（decision_historyはappend-only、mutation / deletion禁止）。
- 退役はDEPRECATED状態の維持と `agent_registry.md` 上の「retired」表示で表現する。

## ローカル層（User-local Capability Layer）の扱い

本書のライフサイクル管理は**共有層のRole / Skillだけ**を対象とする。`.local/capability/` に置いたローカル層のRole / Skillは、両lifecycle registryに載せない。

- ローカル層の状態は登録簿の正式state（DISCOVERED〜DEPRECATED）とは別軸で、`.local/capability/local_decision_log.md` に記録する。
- decision_history / promotion_history のappend-only契約、subject_revisionごとの一意なPROMOTE記録の要求、sha256 revisionの計算は、ローカル層には適用しない。
- ローカル層のRole / Skillは削除してよい（共有層の物理削除禁止ルールの対象外）。削除の事実は `local_decision_log.md` に残す。
- ローカル層のRole / Skillを共有層へ昇格させる場合に限り、本書のCREATE系ルールとHuman Gate証跡ルールが適用される。経路は `local_capability_layer_policy.md` を参照する。

## Agent乱立防止

- 新Role追加は最後の手段（`capability_gap_policy.md` の優先順位ラダー）。
- 同一conflict group内のRole / Skillは重複説明（overlap_review）を必須とする。
- 四半期ごと、または5件以上のRole / Skill追加が発生した時点で、重複・未使用・境界曖昧の点検を行う。

## 定期レビュー

- `review_metrics.md` の蓄積（3件以上の同種タスク）を入力に、Role / Skillの実効性を点検する。
- 点検結果はeffectiveness（not_evaluated / baseline_pending / evaluated）の更新候補として扱い、根拠のない数値スコアは付けない。
- 点検で見つかった改善はUPDATE候補としてガバナンスを通す。

## 完了条件

- すべての共有層Role / Skillが登録簿に存在し、stateとdispositionが実体と一致している（ローカル層は対象外）。
- ACTIVEなRole / SkillにはCeles Human Gate記録（baseline importを除く）がある。
- `python3 tools/validate_repository.py` と Foundation evals がPASSしている。

## 参照

- `ai_team/governance/ai_employee_lifecycle_registry.yaml`
- `ai_team/governance/skill_lifecycle_registry.yaml`
- `ai_team/governance/capability_growth_policy.yaml`
- `ai_team/local_capability_layer_policy.md`
- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_quality_gate.md`
