# 【セット表紙】アプリケーション開発（APP）ドキュメントセット

> `document_map.md` のAPP列・system_app差分表に基づく。

## この種別に該当する案件

- 該当する: 顧客/一般ユーザー向けWeb・モバイルアプリケーションの新規開発
- 該当しない: 業務システム・基幹システム → `system_development.md`、コンテンツ中心のサイト → `web_content.md`

## 体制

- 主担当Role: Fullstack Engineer / Frontend Engineer
- 関与Role: Product Manager（UX要件）

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ○ | — |
| 3 | 企画 | MVPスコープ | `../../mvp_scope_template.md` | ○ | — |
| 4 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | — |
| 5 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ○ | — |
| 6 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 7 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | — |
| 8 | 要件 | 業務フロー定義書 | `../common/business_flow_template.md` | ◎ | — |
| 9 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | — |
| 10 | 設計 | 基本設計書 | `../../basic_design_template.md` | ◎ | — |
| 11 | 設計 | 詳細設計書 | `../../detailed_design_template.md` | ○ | — |
| 12 | 設計 | 画面設計書 | `../system_app/screen_design_template.md` | ◎（UI有時） | 顧客との認識齟齬が最も出やすい成果物 |
| 13 | 設計 | 状態遷移・シーケンス設計書 | `../system_app/state_sequence_design_template.md` | ○ | — |
| 14 | 設計 | API設計書 | `../../api_design_template.md` | ○ | — |
| 15 | 設計 | DB設計書 | `../../db_design_template.md` | ◎ | — |
| 16 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 17 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ◎ | — |
| 18 | 設計 | モバイル・ストア公開差分 | `../system_app/mobile_store_release_template.md` | △（モバイル時） | ストア審査・push通知・OS更新追従を別管理 |
| 19 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 20 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ◎ | — |
| 21 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | — |
| 22 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 23 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 24 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 25 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 26 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | — |
| 27 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 28 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ○ | — |
| 29 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ○ | — |

## 種別固有の注意事項

モバイルを含む案件はストア審査期間（数日〜数週間）をリリース計画に織り込む。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
