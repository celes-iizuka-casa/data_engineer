---
name: skill-adoption-planning
description: 導入・定着・教育・運用を整理し、作って終わりを防ぐ。 Use when acting as AI Forward Deployed Engineer for 導入計画（準備→試行→本番→並行運用終了） / 定着責任者（顧客側）の特定と合意 / 教育・説明の設計（利用者向け/運用者向け）.
---

# Adoption Planning（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 導入計画（準備→試行→本番→並行運用終了）
- 定着責任者（顧客側）の特定と合意
- 教育・説明の設計（利用者向け/運用者向け）
- 運用ルール初版と旧手順廃止条件

## 責任外
- 監視・アラート・Runbookの技術設計（AI SRE / Platform Engineer）
- 教育の実施・人員確保（顧客側）
- 契約上のサポート範囲の確定（セレス）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. 利用者整理（一次/二次/運用者・態度）を確認する
3. 導入ステップと各完了条件を設計する
4. 定着責任者（顧客側）を特定し合意を取る
5. 旧手順の廃止日・並行運用終了条件を決める
6. 教育・説明（利用者向け/運用者向け）を設計する
7. 運用ルール初版（確定・修正・問い合わせ）を作る
8. フィードバック回収の仕組みを導入初日から動く形にする

## 必須出力
- adoption_plan.md
- rollout_plan.md
- training_notes.md
- operation_notes.md（テンプレート: `templates/adoption_plan_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のAdoption Plan品質チェックに合格すること

## 禁止事項
- 定着責任者未定のまま計画を完了扱いにする
- 旧手順の廃止日を決めずに導入する
- 教育を操作手順の羅列だけで済ませる
- 監視・Runbookの技術設計に踏み込む（SREの領分）

## 完了条件
- adoption_plan.md / rollout_plan.md / training_notes.md / operation_notes.md が作成されている。
- 定着責任者と旧手順廃止条件が合意されている。
- `ai_team/fde/fde_quality_gate.md` のAdoption Plan品質チェックに合格している。
- `risk_based_quality_gates.yaml`でIndependent Reviewがrequiredの場合だけAI Deliverable Quality Reviewerへ引き渡している。

## 参照
- `ai_team/fde/fde_adoption_success_guide.md`
- `templates/adoption_plan_template.md`
- `templates/fde/customer_explanation_template.md`
