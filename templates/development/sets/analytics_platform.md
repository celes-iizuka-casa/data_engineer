# 【セット表紙】データ分析基盤開発（AP）ドキュメントセット

> DPセットを継承した上で分析特化文書を追加する。`document_map.md` のAP列・AP差分表に基づく。

## この種別に該当する案件

- 該当する: 利活用が「分析」と確定しているデータ基盤・分析基盤構築案件
- 該当しない: 利活用が未確定 → `data_platform.md`

## 体制

- 主担当Role: Data Engineer / ML Engineer
- 関与Role: Product Manager（指標定義のビジネス合意）

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ◎ | — |
| 3 | 企画 | MVPスコープ | `../../mvp_scope_template.md` | ○ | — |
| 4 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | 指標を実際に使う意思決定者を含める |
| 5 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ◎ | 分析対象指標の初期候補を記載 |
| 6 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 7 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | — |
| 8 | 要件 | 業務フロー定義書 | `../common/business_flow_template.md` | ○ | — |
| 9 | 要件 | 指標・KPI定義書 | `../analytics_platform/kpi_definition_template.md` | ◎ | 集計条件の定義揺れ（例:「売上」の範囲）を防ぐ |
| 10 | 設計 | データアーキテクチャ設計書 | `../data_platform/data_architecture_design_template.md` | ◎ | DPセット継承 |
| 11 | 設計 | データモデル・データディクショナリ | `../data_platform/data_model_dictionary_template.md` | ◎ | — |
| 12 | 設計 | データフロー・リネージ定義書 | `../data_platform/data_lineage_template.md` | ◎ | — |
| 13 | 設計 | データガバナンス・権限設計書 | `../data_platform/data_governance_access_design_template.md` | ◎ | — |
| 14 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | — |
| 15 | 設計 | 基本設計書 | `../../basic_design_template.md` | ◎ | — |
| 16 | 設計 | データパイプライン設計 | `../../data_pipeline_design_template.md` | ◎ | — |
| 17 | 設計 | データ品質ルール | `../../data_quality_rules_template.md` | ◎ | — |
| 18 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 19 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ◎ | — |
| 20 | 設計 | バッチ・ジョブ設計書 | `../common/batch_job_design_template.md` | ◎ | — |
| 21 | 設計 | ディメンショナルモデル設計書 | `../analytics_platform/dimensional_model_design_template.md` | ○ | クエリ性能・一貫性はモデル設計で決まる |
| 22 | 設計 | データマート設計書 | `../analytics_platform/data_mart_design_template.md` | ○ | 利用部門別マートの乱立を防ぐ |
| 23 | 設計 | DB設計書 | `../../db_design_template.md` | ○ | 運用系メタストア等がある場合のみ |
| 24 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 25 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ◎ | — |
| 26 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | — |
| 27 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 28 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 29 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 30 | 移行 | データ移行計画書 | `../common/data_migration_plan_template.md` | ○ | — |
| 31 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 32 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | — |
| 33 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 34 | 運用 | BIダッシュボード設計書 | `../analytics_platform/bi_dashboard_design_template.md` | ○ | 誰の何の意思決定に使うかを明記しないと放置される |
| 35 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ○ | — |
| 36 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ○ | — |

## 種別固有の注意事項

指標定義（KPI定義書）はダッシュボード設計より先に確定する。指標定義が固まる前にダッシュボードを作ると、後戻りで全ダッシュボードの再修正が発生する。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
