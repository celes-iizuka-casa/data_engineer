# 【セット表紙】データ基盤開発（DP）ドキュメントセット

> `../document_map.md` のDP列・DP差分表に基づく。実体テンプレートは複製せず参照する。

## この種別に該当する案件

- 該当する: 分析・AI等の利活用を目的にデータを収集・蓄積・整備する案件（利活用が未確定でも可）
- 該当しない: 利活用が「分析」と確定している → `analytics_platform.md`

## 体制

- 主担当Role: Data Engineer / Data Platform Engineer
- 関与Role: Security & Governance Engineer（データガバナンス設計時）

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | データ提供元部門を体制図に含める（提供停止が全工程を止める） |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ◎ | 既存データソースの棚卸しを最優先（後工程設計の前提になる） |
| 3 | 企画 | MVPスコープ | `../../mvp_scope_template.md` | ○ | 初期は対象データソース1〜2本に絞る判断を明記 |
| 4 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | データ提供者・将来の利用予定部門を必ず含める |
| 5 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ○ | 利活用未確定時はKPIでなく基盤の可用性・鮮度を指標にする |
| 6 | 企画 | データ利活用仮説シート | `../data_platform/data_utilization_hypothesis_template.md` | ◎（利活用未確定時） | 想定ユースケースと将来転用のための設計判断を記録 |
| 7 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | データ要件（鮮度・粒度・保持期間）を機能要件と分けて記載 |
| 8 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | データ量増加時のスケーラビリティを明記 |
| 9 | 要件 | 業務フロー定義書 | `../common/business_flow_template.md` | ○ | データ発生源の業務プロセスを可視化 |
| 10 | 設計 | データアーキテクチャ設計書 | `../data_platform/data_architecture_design_template.md` | ◎ | レイヤー構成（raw/staging/mart）と技術選定根拠 |
| 11 | 設計 | データモデル・データディクショナリ | `../data_platform/data_model_dictionary_template.md` | ◎ | 項目定義の曖昧さを残さない |
| 12 | 設計 | データフロー・リネージ定義書 | `../data_platform/data_lineage_template.md` | ◎ | 障害調査・影響分析の基礎 |
| 13 | 設計 | データガバナンス・権限設計書 | `../data_platform/data_governance_access_design_template.md` | ◎ | PII分類とアクセス制御を設計段階で確定 |
| 14 | 設計 | データカタログ・メタデータ管理定義 | `../data_platform/data_catalog_metadata_template.md` | ○ | 将来の利活用者が発見できる設計にする |
| 15 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | システム全体構成との整合を確認 |
| 16 | 設計 | 基本設計書 | `../../basic_design_template.md` | ◎ | — |
| 17 | 設計 | データパイプライン設計 | `../../data_pipeline_design_template.md` | ◎ | Source Contract・CDC戦略・再実行性を定義 |
| 18 | 設計 | データ品質ルール | `../../data_quality_rules_template.md` | ◎ | 閾値・重大度・隔離処理を定義 |
| 19 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 20 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ◎ | — |
| 21 | 設計 | バッチ・ジョブ設計書 | `../common/batch_job_design_template.md` | ◎ | 冪等性・バックフィル手順を必ず定義 |
| 22 | 設計 | 外部インターフェース設計書 | `../common/external_interface_design_template.md` | ○ | — |
| 23 | 設計 | DB設計書 | `../../db_design_template.md` | ○ | 運用系メタストア等がある場合のみ |
| 24 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 25 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ◎ | — |
| 26 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | — |
| 27 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 28 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 29 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 30 | 移行 | データ移行計画書 | `../common/data_migration_plan_template.md` | ○ | 既存データの移し替えがある場合は必須 |
| 31 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 32 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | データ鮮度・パイプライン失敗の監視を明記 |
| 33 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 34 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ○ | — |
| 35 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ○ | — |

## 種別固有の注意事項

利活用未確定時は `../document_map.md` の「利活用未確定データ基盤の分岐規則」に従い、データ利活用仮説シートを必須化し、指標・KPI定義書は作らない。利活用が「分析」に確定した時点で `analytics_platform.md` へ移行し、仮説シートの内容をKPI定義書へ昇格する。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
