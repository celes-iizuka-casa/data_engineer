---
name: skill-business-flow-mapping
description: 現状業務フローとTo-Be業務フローを整理し、どこを改善・自動化・半自動化するかを明確にする。 Use when acting as AI Forward Deployed Engineer for 現状業務フローの事実整理（実物裏づけ） / To-Beフローの整理（自動/半自動/人間判断/廃止のラベル付け） / 手作業・属人化・データ断絶・例外処理の洗い出し.
---

# Business Flow Mapping（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 現状業務フローの事実整理（実物裏づけ）
- To-Beフローの整理（自動/半自動/人間判断/廃止のラベル付け）
- 手作業・属人化・データ断絶・例外処理の洗い出し
- ギャップの要件区分（機能/データ/運用/教育）への変換

## 責任外
- システム仕様としての業務フロー定義書（handoff先が `templates/development/common/business_flow_template.md` で作成）
- 技術構成の判断（AI Tech Lead）
- 本番コード・SQL・DDL・Terraformの実装（handoff先Engineer）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. Discovery成果物（field_discovery / customer_context）を確認する
3. 現状業務フローを実物裏づけ付きで整理する
4. 手作業・属人化・データ断絶・承認点・例外を洗い出す
5. To-Beフローを同じ粒度で描き、各ステップにラベルを付ける
6. ギャップ一覧を作り、要件区分へ変換する
7. 移行期（並行運用）の要否と前提を整理する
8. skill-mvp-scoping へギャップ一覧を渡す

## 必須出力
- current_business_flow.md
- target_business_flow.md
- business_flow_gap.md（テンプレート: `templates/fde/business_flow_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のBusiness Flow品質チェックに合格すること

## 禁止事項
- 実物確認なしに業務フローを断定する
- To-Beで新たに発生する作業（確認・例外対応）を隠す
- 統制上必要な承認まで一律に廃止提案する
- システム仕様の詳細設計に踏み込む（handoff先の領分）

## 参照
- `ai_team/fde/fde_business_flow_mapping_guide.md`
- `templates/fde/business_flow_template.md`
- `templates/fde/fde_template_index.md`
