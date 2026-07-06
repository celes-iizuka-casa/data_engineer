# 【セット表紙】運用保守案件（OPS）ドキュメントセット

> `document_map.md` のOPS列・maintenance差分表に基づく。新規開発を伴わない、既存システムの保守契約案件向け。

## この種別に該当する案件

- 該当する: 既存システムの保守・運用契約（新規開発を含まない）
- 該当しない: 新規開発を伴う → 該当する開発種別セットを使用し、本セットは運用移管以降のみ併用

## 体制

- 主担当Role: SRE / Platform Engineer

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | 保守体制・連絡窓口を明記 |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ◎ | 引き継ぎ時点の既知課題を棚卸しする |
| 3 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ○ | 障害件数・応答時間等の保守KPI |
| 4 | 要件 | 要件定義書 | `../../requirements_template.md` | ○ | 保守範囲の技術要件のみ簡潔に |
| 5 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ○ | 引き継ぎ時点の構成を正として記録 |
| 6 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ○ | 保守担当者のアクセス手順 |
| 7 | 運用 | 保守範囲定義書 | `../maintenance/maintenance_scope_definition_template.md` | ◎ | 「どこまでやるか」の齟齬が契約トラブルの最大要因 |
| 8 | 運用 | 定期作業計画書 | `../maintenance/periodic_work_plan_template.md` | ◎ | パッチ・証明書・バックアップ検証の漏れを防ぐ |
| 9 | 運用 | キャパシティ計画書 | `../maintenance/capacity_plan_template.md` | ○ | リソース枯渇は予兆段階で捕まえるのが最安 |
| 10 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 11 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | — |
| 12 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ◎ | 契約上のSLAと技術上のSLOを対応付ける |
| 13 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |
| 14 | 運用 | 障害対応・ポストモーテム | `../common/incident_postmortem_template.md` | ◎ | — |

## 種別固有の注意事項

保守開始時は「保守範囲定義書」を顧客と最初に合意してから他文書に着手する（範囲未合意のまま作業を始めると契約外作業の線引きができなくなる）。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
