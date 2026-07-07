# 【FDE索引】Forward Deployed Engineer ドキュメントセット

> FDE案件はこの1枚から入る。FDEが使う全テンプレートを工程順に索引する（実体テンプレートは複製せず参照する。既存テンプレは `templates/` 直下が正）。
> 方法論は `../../ai_team/fde/` の各ガイド、品質基準は `../../ai_team/fde/fde_quality_gate.md` を参照。

## 工程順テンプレート一覧

| # | 工程 | 成果物 | テンプレート | 担当サブSkill | 記入観点 |
|---|---|---|---|---|---|
| 1 | Discovery | 顧客コンテキスト | `../customer_context_template.md` | skill-field-discovery | 相談のきっかけと過去の類似取り組みを必ず確認 |
| 2 | Discovery | Field Discovery | `../field_discovery_template.md` | skill-field-discovery | 未確認項目は「未確認」と明示（想像で埋めない） |
| 3 | Discovery | 関係者マップ | `../stakeholder_map_template.md` | skill-stakeholder-mapping | 利用者・意思決定者・運用者を実名/実部門で分離 |
| 4 | Discovery | 痛点分析 | `pain_point_analysis_template.md` | skill-pain-point-analysis | 表面要望と本質課題を分け、裏づけ事実を付ける |
| 5 | 業務整理 | 業務フロー（現状/To-Be/ギャップ） | `business_flow_template.md` | skill-business-flow-mapping | To-Beの各ステップに自動/半自動/人間判断/廃止ラベル |
| 6 | スコープ | MVPスコープ | `../mvp_scope_template.md` | skill-mvp-scoping | 検証仮説を1つに絞る。最低ライン4種を省略しない |
| 7 | 方針 | ソリューション方針 | `solution_framing_template.md` | skill-solution-framing | 技術選定を断定しない（候補+制約+推奨まで） |
| 8 | 引き継ぎ | Engineering Handoff | `../engineering_handoff_template.md` | skill-engineering-handoff | Role別依頼10種。依頼なしも「なし+理由」を書く |
| 9 | 導入 | 導入・定着計画 | `../adoption_plan_template.md` | skill-adoption-planning | 定着責任者と旧手順廃止日を必ず決める |
| 10 | 導入 | 成功指標 | `../success_metrics_template.md` | skill-success-metrics-design | ベースラインなしの指標は測れない |
| 11 | 導入 | 顧客向け説明 | `customer_explanation_template.md` | 親Skill（Personalization適用） | 読み手タイプに応じて技術詳細を業務語へ変換 |
| 12 | 改善 | フィードバックログ | `../feedback_log_template.md` | skill-feedback-to-backlog | 出典付き記録。バグ/仕様変更/教育課題を混同しない |
| 13 | 改善 | フィードバック分析 | `../feedback_analysis_template.md` | skill-feedback-to-backlog | Backlog項目に対応先Roleと受入条件の種を付ける |

## 記載規則

- 行の順序 = FDE基本フロー（`../../ai_team/fde/fde_operating_model.md`）の推奨順。案件により省略可（省略理由を成果物に残す）
- 既存テンプレ（`../`参照の8本）はvalidator契約により `templates/` 直下が正。本索引から参照のみ行い、複製しない
- 記入観点の詳細は `../../ai_team/fde/` の各ガイドに集約（テンプレ本文には書かない — 既存45テンプレの様式維持）

## 開発ドキュメント体系との使い分け

- 本索引のテンプレは**FDE（発見・変換）フェーズ**の成果物。handoff後の開発フェーズは `../development/document_map.md` と種別セット表紙を使う
- `business_flow_template.md`（本ディレクトリ・FDE版）は「どこを変えるか」を決める現場整理用。`../development/common/business_flow_template.md`（開発版）はシステム仕様として書く業務フロー定義書。**FDE版で整理→開発版へ昇格**の順で使う
- mvp_scope / stakeholder_map / success_metrics は両体系で共通（同一ファイルを参照）

## 参照

- `../../ai_team/fde/fde_operating_model.md`（基本フロー・起動条件）
- `../../ai_team/fde/fde_quality_gate.md`（成果物別品質チェック）
- `../../ai_team/personalization_policy.md`（出し分け規則）
