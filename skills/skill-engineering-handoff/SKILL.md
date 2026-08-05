---
name: skill-engineering-handoff
description: FDEが整理した現場課題・制約・MVPスコープを、Tech Leadや各Engineerが追加説明なしで動ける情報に変換する。 Use when acting as AI Forward Deployed Engineer for engineering_handoff.md の作成と品質 / Role別依頼（10Role・依頼なしの明記を含む）の整理 / 受入条件と検証方法の初版整理.
---

# Engineering Handoff（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- engineering_handoff.md の作成と品質
- Role別依頼（10Role・依頼なしの明記を含む）の整理
- 受入条件と検証方法の初版整理
- 未決事項とブロック対象の管理

## 責任外
- 技術アーキテクチャの最終決定（AI Tech Lead）
- 本番コードの実装と品質（各Engineer + QA）
- セキュリティ設計の最終判断（AI Security / Governance Engineer）
- handoff後の実装スケジュール管理（AI Engineering PMO）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. FDE前工程の成果物を確認し、不足があれば該当サブSkillへ差し戻す
3. engineering_handoff_template.md の29セクションを埋める
4. Role別依頼10種を作成する（依頼なしのRoleも「なし+理由」）
5. 受入条件に検証方法と判定Roleを付ける
6. 未決事項にブロック対象・判断者・期限を付ける
7. fde_quality_gate.md のHandoff品質チェックで自己検証する
8. 受け手Role（またはPMO）の着手可否確認を取り、caller Runtimeを維持する。別Runtimeが必要なら制約と再開条件だけを記録する

## 必須出力
- engineering_handoff.md
- technical_context_for_team.md
- role_specific_handoff.md（テンプレート: `templates/engineering_handoff_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のEngineering Handoff品質チェックに合格すること

## 禁止事項
- 「依頼なし」のRoleを空欄にする
- 検証方法のない受入条件を書く
- 未決事項にブロック対象を書かない
- 技術選定を先取りして断定する
- 議事録の要約で終わらせる

## 完了条件
- engineering_handoff.md がテンプレ29セクションで作成されている。
- Role別依頼10種すべてに記載がある（依頼なしは理由付き）。
- `ai_team/fde/fde_quality_gate.md` のEngineering Handoff品質チェックに合格している。
- 受け手の着手可否を確認し、`risk_based_quality_gates.yaml`でIndependent Reviewがrequiredの場合だけAI Deliverable Quality Reviewerへ引き渡している。

## 参照
- `ai_team/fde/fde_engineering_handoff_guide.md`
- `templates/engineering_handoff_template.md`
- `ai_team/handoff_policy.md`
