---
name: skill-mvp-scoping
description: 最小で価値が出るMVPスコープを切り出し、やること・やらないこと・将来拡張を整理する。 Use when acting as AI Forward Deployed Engineer for 検証仮説の絞り込み（1つ） / MVP/非スコープ/将来拡張の3区分の明文化 / セキュリティ・運用・データ品質・テストの最低ラインの計画組み込み.
---

# MVP Scoping（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `ai_team/personalization_policy.md` とprofile解決順を確認する（Local profile不在時は匿名shared defaultを使い、個人属性を推測しない）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 検証仮説の絞り込み（1つ）
- MVP/非スコープ/将来拡張の3区分の明文化
- セキュリティ・運用・データ品質・テストの最低ラインの計画組み込み
- 初期リリース範囲と並行運用の整理

## 責任外
- 技術的実現可能性の最終判断（AI Tech Lead）
- 要件の最終化・優先順位の確定（PM起用時はAI Product Manager）
- 見積り・契約スコープの確定（セレス）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. problem_statement とギャップ一覧を確認する
3. 検証仮説を1つに絞る（絞れない場合は優先を付けて分割）
4. 要望・変更点を価値×頻度×影響×難度で分類する
5. MVP/非スコープ/将来拡張の3区分を理由付きで作る
6. 非機能の最低ライン（fde_mvp_scoping_guide.md）を計画に組み込む
7. 初期リリース範囲・並行運用・旧手順廃止条件を整理する
8. Tech Leadへ実現性確認を依頼し、mvp_scoping_workflow.md のゲートを通す

## 必須出力
- mvp_scope.md
- non_scope.md
- release_scope.md
- future_extension.md（テンプレート: `templates/mvp_scope_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のMVP Scope品質チェックに合格すること

## 禁止事項
- 検証仮説が複数のままMVPを切る
- 非機能の最低ラインを削って速度を出す
- 非スコープを口頭合意のまま文書化しない
- 技術的実現可能性を単独で断定する

## 参照
- `ai_team/fde/fde_mvp_scoping_guide.md`
- `ai_team/workflows/mvp_scoping_workflow.md`
- `templates/mvp_scope_template.md`
