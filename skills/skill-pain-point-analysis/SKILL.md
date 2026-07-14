---
name: skill-pain-point-analysis
description: 表面的な要望と本質的な課題を分け、解くべき課題を特定する。 Use when acting as AI Forward Deployed Engineer for 痛みの一覧化（発生箇所・頻度・業務影響の定量化） / 根本原因仮説（なぜ掘り）の作成と裏づけ状況の管理 / problem_statement（解くべき課題1文）の作成.
---

# Pain Point Analysis（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 痛みの一覧化（発生箇所・頻度・業務影響の定量化）
- 根本原因仮説（なぜ掘り）の作成と裏づけ状況の管理
- problem_statement（解くべき課題1文）の作成
- 要望と課題の対応表（MVP/将来/対応しないの振り分け材料）

## 責任外
- 解決手段の確定（skill-solution-framing以降）
- 技術的原因の深掘り調査（AI Tech Lead / 各Engineer）
- 要件の最終化（PM起用時はAI Product Manager）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. 要望を原文のまま一覧化する
3. 痛みを発生箇所・頻度・業務影響付きで一覧化する
4. 「なぜ」を2段以上掘り、根本原因仮説を作る
5. 仮説の裏づけ状況（確認済み/未検証）を分ける
6. problem_statement を1文で作り、裏づけ事実を添える
7. 要望と課題の対応表を作り、解かない課題に理由を付ける
8. skill-solution-framing / skill-mvp-scoping へ渡す

## 必須出力
- pain_point_analysis.md
- root_cause_hypothesis.md
- problem_statement.md（テンプレート: `templates/fde/pain_point_analysis_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のDiscovery品質チェック（本質課題）に合格すること

## 禁止事項
- 要望をそのまま課題として扱う
- 裏づけのない根本原因を断定する
- 課題を複数のまま優先を付けずに次工程へ渡す
- 技術原因の調査に踏み込み実装領域を侵食する

## 参照
- `ai_team/fde/fde_discovery_checklist.md`
- `templates/fde/pain_point_analysis_template.md`
- `templates/fde/fde_template_index.md`
