# 【セット表紙】システム開発（SY）ドキュメントセット

> `document_map.md` のSY列・system_app差分表に基づく。

## この種別に該当する案件

- 該当する: 業務システム・基幹システムの新規開発・改修
- 該当しない: 顧客/一般ユーザー向けアプリの新規開発 → `application_development.md`、API連携のみ → `integration.md`

## 体制

- 主担当Role: Backend Engineer / Tech Lead
- 関与Role: QA / Test Automation Engineer

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ◎ | — |
| 3 | 企画 | MVPスコープ | `../../mvp_scope_template.md` | ○ | — |
| 4 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | — |
| 5 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ○ | — |
| 6 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 7 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | — |
| 8 | 要件 | 業務フロー定義書 | `../common/business_flow_template.md` | ◎ | 業務システムは現行業務との整合が最重要 |
| 9 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | — |
| 10 | 設計 | 基本設計書 | `../../basic_design_template.md` | ◎ | — |
| 11 | 設計 | 詳細設計書 | `../../detailed_design_template.md` | ○ | — |
| 12 | 設計 | 画面設計書 | `../system_app/screen_design_template.md` | ◎（UI有時） | 顧客との認識齟齬が最も出やすい成果物 |
| 13 | 設計 | 帳票設計書 | `../system_app/report_design_template.md` | ○（該当時） | 法務・経理都合で後から変えにくい |
| 14 | 設計 | 状態遷移・シーケンス設計書 | `../system_app/state_sequence_design_template.md` | ○ | 複雑な業務状態・非同期処理はここで潰す |
| 15 | 設計 | API設計書 | `../../api_design_template.md` | ○ | — |
| 16 | 設計 | DB設計書 | `../../db_design_template.md` | ◎ | — |
| 17 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 18 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ◎ | — |
| 19 | 設計 | バッチ・ジョブ設計書 | `../common/batch_job_design_template.md` | ○ | — |
| 20 | 設計 | 外部インターフェース設計書 | `../common/external_interface_design_template.md` | ○ | — |
| 21 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 22 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ◎ | — |
| 23 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | — |
| 24 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 25 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 26 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 27 | 移行 | データ移行計画書 | `../common/data_migration_plan_template.md` | ○ | — |
| 28 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 29 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | — |
| 30 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 31 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ○ | — |
| 32 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ○ | — |

## 種別固有の注意事項

UIを持たないバッチ主体システムでは画面設計書を省略できる（省略記録に理由を残す）。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
