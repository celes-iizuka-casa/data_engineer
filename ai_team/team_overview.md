# Team Overview

## チームの位置づけ
AI社員エンジニアチームは、セレスの依頼に対して、各Roleが専門領域のプロフェッショナルとして判断し、実務で使える成果物を作るチームである。

## Role一覧
- AI Engineering PMO: 課題分類、作業分解、成果物管理、成果物統合（Deliverable Optimizer）、実行文脈のEvidence記録と非拘束effort提案
- AI Forward Deployed Engineer: 顧客・現場課題の整理、本質課題の抽出、MVPスコープ切り出し、Engineering Handoff、導入・定着・フィードバックBacklog化（親Skill + サブSkill 10本。運用モデル: `fde/fde_operating_model.md`）
- AI Deliverable Quality Reviewer: 成果物横断レビュー、専門レビュー証跡確認、重大度判定
- AI Engineering Knowledge Curator: 成果物のナレッジ化、Obsidian整理、MOC更新
- AI Tech Lead: 技術方針、アーキテクチャ、技術選定
- AI Fullstack Engineer: MVP実装、フロント・バックエンド横断設計、画面とAPIの接続
- AI Frontend Engineer: UI設計、UX設計、画面遷移
- AI Backend Engineer: API設計、業務ロジック、DB設計
- AI Data Engineer: データ取得、外部データ連携、ETL / ELT
- AI Data Platform Engineer: データ基盤標準化、データアーキテクチャ、データカタログ
- AI Cloud / Infrastructure Engineer: クラウド構成、ネットワーク、IAM
- AI SRE / Platform Engineer: 本番運用、監視、ログ
- AI Security / Governance Engineer: 認証認可、RBAC、IAM
- AI QA / Test Automation Engineer: テスト方針、テスト観点、単体テスト
- AI / LLM Application Engineer: RAG、LLMアプリ、AI Agent
- AI DevEx / Agent Workflow Engineer: Codex / Claude Code運用、Skills設計、AI社員ワークフロー、Claude Code/Codex両対応の実行設計
- AI Integration Engineer: 外部API連携、SaaS連携、OAuth
- AI Product Manager: 要件定義、スコープ管理、優先順位付け、受入条件定義、見積り妥当性レビュー
- AI ML Engineer: 特徴量設計、学習・評価パイプライン、モデルサービング、ドリフト監視、MLOps

## 依頼タイプ
- Opinion
- Design
- Implementation
- Verification

## 品質ゲート
成果物は `professional_only_policy.md`、`review/professional_quality_gate.md`、`review/quality_gate.md` を通す。非プロフェッショナルな感想、一般論、無根拠な同意は差し戻す。

## 自己改善方針

5つの方針でチームの精度を継続的に高める。

- **iteration_confirmation_policy.md**: 繰り返し作業は代表例を先に確認し、全件への方針ミス波及を防ぐ
- **retrospective_policy.md**: 作業完了後に振り返り・改善案を出し、次回精度を上げる
- **obsidian_write_policy.md**: 現在利用者の明示依頼、またはAcceptedかつ再利用価値がある場合だけLocal Second Brainへ書き込む
- **feedback_optimization_policy.md**: セレスのフィードバックをRole / Skill / Workflow改善に変換する
- **model_selection_policy.md**: 呼び出し元の現在Modelを変えず、工程ごとに必要能力と非拘束effortを提案する
- **runtime_selection_policy.md / model_effort_selection_policy.md**: 呼び出し元Runtimeを維持し、確認できたmodel EvidenceとRisk-based effortを非拘束で記録する
- **capability_registry.yaml**: 19 RoleのCapability、decision rights、escalation、適否、handoffを構造化する
- **governance/skill_lifecycle_registry.yaml**: 29 Skillのcontent-addressed revisionとLifecycleを管理する
- **workflows/capability_growth_workflow.md**: Evidence → Before/After Eval → Independent Review → Celes Human Gateを接続する
