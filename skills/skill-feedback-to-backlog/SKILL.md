---
name: skill-feedback-to-backlog
description: 現場フィードバックを分類し、改善Backlogへ変換する。 Use when acting as AI Forward Deployed Engineer for フィードバックの出典付き記録 / 7分類（バグ/仕様変更/改善要望/運用課題/教育課題/データ品質課題/セキュリティ課題） / 優先順位付けの初版（業務影響×頻度×利用者数）.
---

# Feedback to Backlog（FDEサブSkill）

## 実行原則

- 親Skill `skill-forward-deployed-engineer` の工程として動く。
- 事実（実物・数字・出典）と推論・仮定を分離する。未確認は「未確認」と書く。
- 作業前に `profiles/current_user_profile.yaml` を読む（不在時はセレス=専門家エンジニアを仮定し明記）。
- コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

## 守備範囲
- フィードバックの出典付き記録
- 7分類（バグ/仕様変更/改善要望/運用課題/教育課題/データ品質課題/セキュリティ課題）
- 優先順位付けの初版（業務影響×頻度×利用者数）
- improvement_backlog への変換と対応しない理由の記録

## 責任外
- 修正方針の技術判断（AI Tech Lead / 各Engineer）
- 優先順位の最終決定（AI Engineering PMO / セレス）
- バグの再現テスト・回帰テスト（AI QA / Test Automation Engineer）

## Workflow
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. フィードバックを出典（誰が・いつ・どの業務場面）付きで記録する
3. fde_feedback_loop.md の7分類に振り分ける
4. 業務影響×頻度×利用者数で優先順位初版を付ける
5. P0/P1は即時にPMO・該当Roleへエスカレーションする
6. 対応する項目を improvement_backlog.md へ変換する
7. 対応しない項目に理由を記録し、現場へ回答できる状態にする
8. PMO/Tech Lead/QAへ連携し、次サイクルの入力にする

## 必須出力
- feedback_log.md
- feedback_analysis.md
- improvement_backlog.md（テンプレート: `templates/feedback_log_template.md`）

## 品質基準
- `ai_team/fde/fde_quality_gate.md` のFeedback Loop品質チェックに合格すること

## 禁止事項
- 出典なしでフィードバックを記録する
- バグと教育課題を混同して振り分ける
- 対応しない項目を無言で破棄する
- 修正方針の技術判断を単独で確定する

## 参照
- `ai_team/fde/fde_feedback_loop.md`
- `ai_team/workflows/customer_feedback_to_engineering_workflow.md`
- `templates/feedback_log_template.md`
