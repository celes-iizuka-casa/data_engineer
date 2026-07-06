# 【セット表紙】API連携・システム間統合（INT）ドキュメントセット

> `document_map.md` のINT列・integration差分表に基づく。

## この種別に該当する案件

- 該当する: 既存システム間のAPI連携・データ連携構築
- 該当しない: 独自モデル開発を伴う → `ai_ml_llm.md`、クラウド基盤自体の構築 → `cloud_infrastructure.md`

## 体制

- 主担当Role: Integration Engineer

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ◎ | 連携先システムの制約を先に把握する |
| 3 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 4 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | — |
| 5 | 要件 | 業務フロー定義書 | `../common/business_flow_template.md` | ◎ | — |
| 6 | 設計 | IF一覧・連携方式設計書 | `../integration/interface_inventory_design_template.md` | ◎ | 連携全体を台帳化しないと影響分析ができない |
| 7 | 設計 | API設計書 | `../../api_design_template.md` | ◎ | — |
| 8 | 設計 | エラー・リトライ設計書 | `../integration/error_retry_design_template.md` | ◎ | 冪等性・順序保証を事前定義する |
| 9 | 設計 | 外部インターフェース設計書 | `../common/external_interface_design_template.md` | ○ | interface_inventoryの上位互換として利用可 |
| 10 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 11 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ○ | — |
| 12 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 13 | テスト | テスト計画書 | `../../test_plan_template.md` | ◎ | 連携先との結合テスト計画を含める |
| 14 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ◎ | — |
| 15 | テスト | テスト結果報告書 | `../common/test_result_report_template.md` | ◎ | — |
| 16 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | 連携先との同時リリース調整を含める |
| 17 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 18 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ○ | — |
| 19 | 運用 | Runbook | `../../runbook_template.md` | ○ | 連携先障害時の切り分け手順を含める |

## 種別固有の注意事項

連携先が外部企業の場合、テスト・リリースのスケジュールは自社都合だけで決まらない。相手先の検証環境提供時期を要件定義段階で確認する。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
