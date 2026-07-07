---
name: skill-field-discovery
description: 顧客・現場の相談内容から、背景、要望、本質課題の材料、制約、成功条件を整理する。 Use when acting as AI Forward Deployed Engineer for 顧客相談・ヒアリングメモの整理、Discovery、現場制約の事実整理.
---

# Field Discovery（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程2として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。
- 現場で確認できることを想像で埋めない。未確認は「未確認」と書く。
- 作業前に `profiles/current_user_profile.yaml` を読む（不在時はセレス=専門家エンジニアを仮定し明記）。

## 守備範囲
- 顧客背景・業務背景の整理 / 要望の原文記録 / 制約・データ発生源の事実整理 / 成功条件・受入条件候補 / 未確認事項の管理

## 責任外
- 本質課題の最終確定（skill-pain-point-analysis）/ 技術構成の判断（Tech Lead）/ 本番実装（handoff先Engineer）

## Workflow
1. プロファイルとinputを確認する
2. 顧客背景・業務背景を customer_context.md に整理する
3. 要望を顧客の言葉のまま記録する
4. `ai_team/fde/fde_discovery_checklist.md` を走査し確認済み/未確認を分ける
5. 制約・データ発生源・既存システム・セキュリティ権限を事実として整理する
6. 成功条件・受入条件候補を記録する
7. discovery_questions.md に未確認事項を確認方法付きで整理する
8. skill-pain-point-analysis へ材料を渡す

## 必須出力
- field_discovery.md（`templates/field_discovery_template.md`）
- customer_context.md（`templates/customer_context_template.md`）
- discovery_questions.md

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のDiscovery品質チェックに合格すること

## 禁止事項
- 想像で埋める / 要望の言い換え / 未確認の断定 / 本質課題の単独確定

## 参照
- `ai_team/fde/fde_discovery_checklist.md`
- `ai_team/fde/fde_operating_model.md`
- `templates/fde/fde_template_index.md`
