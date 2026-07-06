# 【セット表紙】クラウドインフラ構築（INF）ドキュメントセット

> `../document_map.md` のINF列・cloud_infra差分表に基づく。

## この種別に該当する案件

- 該当する: クラウド基盤の新規構築・移行（アプリ開発自体は伴わない、または他チーム管轄）
- 該当しない: アプリ開発とセットで基盤を作る → 該当する開発種別セット＋本セットのインフラ関連文書を併用

## 体制

- 主担当Role: Cloud Infrastructure Engineer
- 関与Role: SRE / Platform Engineer（運用設計）

## 工程順ドキュメント一覧

| # | 工程 | 文書 | テンプレート | 必須/任意 | この種別での記入観点 |
|---|---|---|---|---|---|
| 1 | 企画 | プロジェクト計画書 | `../common/project_plan_template.md` | ◎ | — |
| 2 | 企画 | 現行調査・課題整理 | `../common/as_is_analysis_template.md` | ○ | 既存インフラの制約・契約条件を確認 |
| 3 | 要件 | 要件定義書 | `../../requirements_template.md` | ◎ | — |
| 4 | 要件 | 非機能要件定義書 | `../common/nonfunctional_requirements_template.md` | ◎ | 可用性・災害対策要件を明記 |
| 5 | 設計 | アーキテクチャ設計 | `../../architecture_template.md` | ◎ | — |
| 6 | 設計 | クラウド構成設計書 | `../cloud_infra/cloud_architecture_design_template.md` | ◎ | アカウント・リージョン・冗長構成の判断根拠 |
| 7 | 設計 | ネットワーク設計書 | `../cloud_infra/network_design_template.md` | ◎ | VPC/サブネット/経路は後から変えると全体停止を伴う |
| 8 | 設計 | セキュリティ設計書 | `../common/security_design_template.md` | ◎ | — |
| 9 | 設計 | IaC標準・運用規約 | `../cloud_infra/iac_standards_template.md` | ○ | 手作業変更とIaCの二重管理はドリフト事故を生む |
| 10 | 設計 | コスト設計書 | `../cloud_infra/cost_design_template.md` | ○ | 従量課金の見積り根拠と上限アラートを事前定義 |
| 11 | 実装 | 環境構築手順書 | `../common/environment_setup_guide_template.md` | ○ | — |
| 12 | テスト | テスト計画書 | `../../test_plan_template.md` | ○ | 障害注入・フェイルオーバー試験を含める |
| 13 | 移行 | リリース計画・手順書 | `../common/release_plan_template.md` | ◎ | — |
| 14 | 運用 | 運用設計書 | `../common/operation_design_template.md` | ◎ | — |
| 15 | 運用 | 監視・アラート設計書 | `../common/monitoring_design_template.md` | ◎ | — |
| 16 | 運用 | SLO/SLA定義書 | `../common/slo_sla_definition_template.md` | ◎ | インフラの可用性目標を数値で確定 |
| 17 | 運用 | Runbook | `../../runbook_template.md` | ◎ | — |

## 種別固有の注意事項

既存オンプレミス／他クラウドとの接続がある場合、ネットワーク設計書に接続要件を要件定義段階から含める（後付けは経路変更＝全体停止を伴う）。

## 省略記録

| 文書 | 省略理由 | 判断者 |
|---|---|---|
