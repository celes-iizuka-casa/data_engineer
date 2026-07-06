# 【セット表紙】Webコンテンツ開発（WEB）ドキュメントセット

> `../document_map.md` のWEB列・web_content差分表に基づく。

## この種別に該当する案件

- 該当する: コーポレートサイト・LP・オウンドメディア等のコンテンツ中心Web開発
- 該当しない: 会員機能・決済等システム性が強い → `application_development.md`

## 体制

- 主担当Role: Frontend Engineer / Product Manager

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ○ | — |
| 3 | 企画 | MVPスコープ | `../../mvp_scope_template.md` | ○ | — |
| 4 | 企画 | ステークホルダーマップ | `../../stakeholder_map_template.md` | ○ | — |
| 5 | 企画 | 成功指標定義 | `../../success_metrics_template.md` | ○ | コンバージョン・PV等の測定指標を先に決める |
| 6 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 7 | 設計 | 基本設計書 | `../../basic_design_template.md` | ○ | — |
| 8 | 設計 | サイト構成・IA設計書 | `../web_content/site_structure_ia_design_template.md` | ◎ | 情報設計の失敗はコンテンツ量産後では直せない |
| 9 | 設計 | コンテンツ設計書 | `../web_content/content_design_template.md` | ◎ | 品質基準を事前合意しないと修正が無限ループする |
| 10 | 設計 | SEO・計測設計書 | `../web_content/seo_measurement_design_template.md` | ○ | 公開後の後付けはローンチ時データが欠損する |
| 11 | 設計 | インフラ・環境構成設計書 | `../common/infrastructure_design_template.md` | ○ | — |
| 12 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ○ | — |
| 13 | 実装 | 開発標準・規約 | `../common/development_standards_template.md` | ○ | — |
| 14 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ○ | — |
| 15 | テスト | テスト計画書 | `../../test_plan_template.md` | ○ | — |
| 16 | テスト | テスト仕様書・ケース | `../common/test_specification_template.md` | ○ | — |
| 17 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 18 | 移行 | 公開前チェックリスト | `../web_content/prelaunch_checklist_template.md` | ◎ | 公開は不可逆イベント。リンク切れ・OGP・a11yの最終関門 |
| 19 | 運用 | CMS運用ガイド | `../web_content/cms_operation_guide_template.md` | ○ | 引き渡し後に顧客が自走できるかを決める |
| 20 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ○ | — |
| 21 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ○ | — |

## 種別固有の注意事項

公開前チェックリストはリリース直前ではなく設計完了直後に一度仮チェックし、抜け漏れを早期発見する。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
