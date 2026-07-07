---
name: skill-success-metrics-design
description: 導入後の成功条件、効果測定指標、利用状況確認方法を設計する。 Use when acting as AI Forward Deployed Engineer for 成功指標の設計（業務指標を主軸） / ベースライン（導入前実測値）の取得計画 / 測定計画（時期・方法・データ源・担当）.
---

# Success Metrics Design（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `profiles/current_user_profile.yaml` を読む（不在時はセレス=専門家エンジニアを仮定し明記）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- 成功指標の設計（業務指標を主軸）
- ベースライン（導入前実測値）の取得計画
- 測定計画（時期・方法・データ源・担当）
- 利用状況の実測設計

## 責任外
- 指標のビジネス合意の最終化（PM起用時はAI Product Manager / セレス）
- 測定基盤・ログ収集の実装（AI Data Engineer / SRE）
- 効果が出ない場合の投資判断（セレス・顧客）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. mvp_scope の成功条件を測定可能な指標へ変換する
3. 業務指標（主）・利用指標（先行）・技術/品質指標（従）を設計する
4. ベースラインの取得方法と時期を決める（導入前必須）
5. 測定計画（時期・方法・データ源・担当）を作る
6. 利用状況の実測方法（ログ・アクセス）を設計する
7. 効果が出ない場合の判断基準（改善/縮小/撤退）を定義する

## 必須出力
- success_metrics.md
- measurement_plan.md
- usage_metrics.md（テンプレート: `templates/success_metrics_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のSuccess Metrics品質チェックに合格すること

## 禁止事項
- 技術指標のみで成功を定義する
- ベースラインなしで効果を主張する設計にする
- 測定手段のない指標を設定する
- 投資判断・撤退判断を単独で確定する

## 参照
- `ai_team/fde/fde_adoption_success_guide.md`
- `templates/success_metrics_template.md`
- `templates/fde/fde_template_index.md`
