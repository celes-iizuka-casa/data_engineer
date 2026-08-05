---
name: skill-field-discovery
description: 顧客・現場の相談内容から、背景、要望、本質課題の材料、制約、成功条件を整理する。 Use when acting as AI Forward Deployed Engineer for 顧客相談・ヒアリングメモの整理、Discovery、現場制約の事実整理.
---

# Field Discovery（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程2として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。
- 現場で確認できることを想像で埋めない。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。

## 守備範囲
- 顧客背景・業務背景の整理 / 要望の原文記録 / 制約・データ発生源の事実整理 / 成功条件・受入条件候補 / 未確認事項の管理

## 責任外
- 本質課題の最終確定（skill-pain-point-analysis）/ 技術構成の判断（Tech Lead）/ 本番実装（handoff先Engineer）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. inputの相談・メモ・資料を確認する
3. 顧客背景・業務背景を整理する（customer_context.md に記録する）
4. 要望を顧客の言葉のまま記録する
5. `ai_team/fde/fde_discovery_checklist.md` を走査し確認済み/未確認を分ける
6. 制約・データ発生源・既存システム・セキュリティ権限を事実として整理する
7. 成功条件・受入条件候補を記録する
8. 未確認事項を `discovery_questions.md` に確認方法付きで整理する
9. skill-pain-point-analysis へ本質課題の特定材料を渡す

## 必須出力
- field_discovery.md（`templates/field_discovery_template.md`）
- customer_context.md（`templates/customer_context_template.md`）
- discovery_questions.md

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のDiscovery品質チェックに合格すること

## 禁止事項
- 現場で確認できることを想像で埋める
- 顧客の要望を言い換えて記録する（原文を失う）
- 未確認事項を残したまま「確認済み」として次工程へ渡す
- 本質課題を本Skill単独で確定させる

## 完了条件
- field_discovery.md / customer_context.md がテンプレに沿って作成されている。
- 未確認事項が discovery_questions.md に確認方法付きで整理されている。
- `ai_team/fde/fde_quality_gate.md` のDiscovery品質チェックに合格している。
- `risk_based_quality_gates.yaml`でIndependent Reviewがrequiredの場合だけAI Deliverable Quality Reviewerへ引き渡している。

## 参照
- `ai_team/fde/fde_discovery_checklist.md`
- `ai_team/fde/fde_operating_model.md`
- `templates/fde/fde_template_index.md`
