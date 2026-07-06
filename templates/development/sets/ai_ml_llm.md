# 【セット表紙】AI/ML・LLMアプリ開発（AI）ドキュメントセット

> `../document_map.md` のAI列・ai_ml_llm差分表に基づく。AIエージェント開発もここに含む。

## この種別に該当する案件

- 該当する: 機械学習モデル・LLMアプリケーション・AIエージェントの開発
- 該当しない: 既存API呼び出しのみで独自モデル・評価が不要 → `integration.md`

## 体制

- 主担当Role: ML Engineer / LLM Application Engineer
- 関与Role: Security & Governance Engineer（ガードレール設計時）

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ○ | — |
| 3 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | — |
| 4 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ◎ | 評価指標なしのモデル開発は「良くなった気がする」で終わる |
| 5 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 6 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | — |
| 7 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | — |
| 8 | 設計 | 基本設計書 | `../../basic_design_template.md` | ◎ | — |
| 9 | 設計 | 実験・評価設計書 | `../ai_ml_llm/experiment_evaluation_design_template.md` | ◎ | Go/No-go基準を事前定義する |
| 10 | 設計 | データセット仕様書 | `../ai_ml_llm/dataset_specification_template.md` | ◎ | 学習・評価データの出所と前処理は再現性そのもの |
| 11 | 設計 | モデルカード | `../ai_ml_llm/model_card_template.md` | ○ | 制約・限界を顧客に引き継ぐ標準形式 |
| 12 | 設計 | LLMガードレール・評価設計書 | `../ai_ml_llm/llm_guardrail_evaluation_design_template.md` | ◎（LLM時） | 有害出力・プロンプトインジェクション対策は本番必須 |
| 13 | 設計 | プロンプト設計書 | `../ai_ml_llm/prompt_design_template.md` | △ | プロンプトが資産化する案件（エージェント等）で版管理 |
| 14 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 15 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ◎ | GPU/推論コストを含める |
| 16 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 17 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ◎ | — |
| 18 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | — |
| 19 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 20 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 21 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 22 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 23 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | モデル劣化（ドリフト）検知を含める |
| 24 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 25 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ○ | — |
| 26 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ○ | 有害出力発生時のインシデント対応も含める |

## 種別固有の注意事項

LLMを使う案件ではLLMガードレール・評価設計書を実験・評価設計書と切り離さず同時に作る（評価基準に安全性評価を含めないと本番投入後に安全性の穴が見つかる）。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
