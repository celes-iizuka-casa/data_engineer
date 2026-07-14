---
name: skill-stakeholder-mapping
description: 利用者、意思決定者、運用者、情シス、開発者などの関係者を整理する。 Use when acting as AI Forward Deployed Engineer for 関係者一覧の整理（役割・関心事・判断権限・接点） / 利用者・意思決定者・運用者の分離 / 意思決定構造（誰が何を判断するか）の整理.
---

# Stakeholder Mapping（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 関係者一覧の整理（役割・関心事・判断権限・接点）
- 利用者・意思決定者・運用者の分離
- 意思決定構造（誰が何を判断するか）の整理
- 定着責任者候補の特定

## 責任外
- 契約・単価の対顧客調整（セレス）
- 顧客組織内の人事・政治判断
- 要件の最終化（PM起用時はAI Product Manager）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. input・Discovery成果物から関係者情報を抽出する
3. 利用者・意思決定者・運用者・データ提供者・情シスを分離する
4. 判断権限と関心事を関係者ごとに整理する
5. 意思決定構造（判断事項×判断者×時期）を整理する
6. 定着責任者候補を特定する
7. 未確認の関係者を discovery_questions.md に残す

## 必須出力
- stakeholder_map.md
- user_roles.md
- decision_structure.md（テンプレート: `templates/stakeholder_map_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のDiscovery品質チェック（関係者分離）に合格すること

## 禁止事項
- 役職名だけで実務者を特定した気になる
- 定着責任者を未定のまま導入計画工程へ進める
- 顧客組織内の調整をFDEが代行・断定する

## 参照
- `ai_team/fde/fde_discovery_checklist.md`
- `templates/stakeholder_map_template.md`
- `templates/fde/fde_template_index.md`
