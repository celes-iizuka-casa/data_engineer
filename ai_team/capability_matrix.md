# Capability Matrix

## 目的

依頼内容から必要能力を抽出し、既存Role / Skillで対応可能か判断するための能力マトリクス。

## 正本と本書の関係

- Role別Capabilityの正本は `ai_team/capability_registry.yaml`。本書は依頼→能力→担当の逆引きview。
- 「対応度」は 対応 / 部分対応 / 不足 の3値のみ。数値スコアや根拠のない評価は書かない。

## Capability一覧

| Capability | 説明 | 対応Role | 対応Skill | 成果物 | 不足時の対応 |
|---|---|---|---|---|---|
| Requirements | 要件定義・受入条件 | AI Product Manager / AI FDE | skill-product-manager / skill-forward-deployed-engineer | requirements.md | Skill更新 |
| FDE / Field Discovery | 現場課題整理・本質課題抽出 | AI Forward Deployed Engineer | skill-field-discovery ほかサブSkill 10本 | field_discovery.md ほか | Skill更新 |
| Architecture | 技術方針・構成設計 | AI Tech Lead | skill-tech-lead | architecture.md / ADR | Skill更新 |
| Frontend | UI / UX・画面設計 | AI Frontend Engineer / AI Fullstack Engineer | skill-frontend-engineer / skill-fullstack-engineer | 画面設計・実装 | Skill更新 |
| Backend | API・業務ロジック・DB | AI Backend Engineer / AI Fullstack Engineer | skill-backend-engineer / skill-fullstack-engineer | API契約・実装 | Skill更新 |
| Data Engineering | 取得・ETL / ELT・品質 | AI Data Engineer | skill-data-engineer | pipeline設計・DDL / dbt | Skill更新 |
| Data Platform | 基盤標準・カタログ | AI Data Platform Engineer | skill-data-platform-engineer | 基盤設計・標準 | Skill更新 |
| Cloud / Infrastructure | クラウド・IaC・ネットワーク | AI Cloud / Infrastructure Engineer | skill-cloud-infrastructure-engineer | IaC・構成図 | Skill更新 |
| SRE / Operations | 監視・運用・インシデント | AI SRE / Platform Engineer | skill-sre-platform-engineer | runbook・SLO | Skill更新 |
| Security / Governance | 認証認可・秘密管理・PII | AI Security / Governance Engineer | skill-security-governance-engineer | 脅威分析・権限設計 | Skill更新 |
| QA / Testing | テスト設計・自動化 | AI QA / Test Automation Engineer | skill-qa-test-automation-engineer | test_plan・テスト | Skill更新 |
| LLM / RAG / AI Agent | RAG・エージェント・LLM評価 | AI / LLM Application Engineer / AI ML Engineer | skill-llm-application-engineer / skill-ml-engineer | RAG設計・eval | Skill更新 |
| Integration | 外部API・SaaS連携 | AI Integration Engineer | skill-integration-engineer | 連携設計・契約 | Skill更新 |
| DevEx / Agent Workflow | Skills設計・validator・実行設計 | AI DevEx / Agent Workflow Engineer | skill-devex-agent-workflow-engineer | workflow・validator | Skill更新 |
| Capability Governance | Gap判定・チーム拡張・乱立防止 | AI Capability Architect | skill-capability-gap-analysis / skill-agent-creation / skill-skill-creation / skill-agent-registry-management | gap分析・提案・registry | Skill更新 |
| Personalization | 利用者に合わせた出力調整 | 全Role（規定はPMOが確認） | 各Role Skill + `personalization_policy.md` | 出力調整の記録 | Workflow / Policy更新 |
| Knowledge Curation | ナレッジ化・第二の脳整理 | AI Engineering Knowledge Curator | skill-engineering-knowledge-curator | obsidian整理・source map | Skill更新 |
| Client Communication | 顧客向け説明・調整材料 | AI FDE / AI Engineering PMO | skill-forward-deployed-engineer / skill-engineering-pmo | 顧客説明資料 | Skill更新 |
| Documentation | ドキュメント標準・整備 | 全Role + AI Engineering Knowledge Curator | 各Role Skill + `templates/development/` | 開発ドキュメント一式 | Template更新 |
| Project Management | 分解・統合・進行 | AI Engineering PMO | skill-engineering-pmo | work_plan・output統合 | Skill更新 |
| Business Analysis | 事業・業務分析 | AI Product Manager / AI FDE（部分対応） | skill-product-manager / skill-pain-point-analysis | 業務分析メモ | Gap判定（必要ならSkill追加） |
| Cost / ROI | コスト・投資対効果 | AI Cloud / Infrastructure Engineer / AI Tech Lead / AI Product Manager（部分対応） | skill-cloud-infrastructure-engineer ほか | コスト試算 | Gap判定（必要ならSkill追加） |
| Legal / Compliance | 法務・コンプライアンス | AI Security / Governance Engineer（部分対応。法務の最終判断は人間） | skill-security-governance-engineer | リスク指摘（最終判断はセレス / 専門家） | Gap判定 + セレス確認必須 |
| Change Management | 導入・変更管理 | AI FDE（部分対応） | skill-adoption-planning | adoption_plan.md | Gap判定（必要ならSkill追加） |
| Training / Enablement | 教育・定着支援 | AI FDE / AI Engineering Knowledge Curator（部分対応） | skill-adoption-planning / skill-engineering-knowledge-curator | 教育・定着計画 | Gap判定（必要ならSkill追加） |

## Capability分類

- Requirements
- FDE / Field Discovery
- Architecture
- Frontend
- Backend
- Data Engineering
- Data Platform
- Cloud / Infrastructure
- SRE / Operations
- Security / Governance
- QA / Testing
- LLM / RAG / AI Agent
- Integration
- DevEx / Agent Workflow
- Capability Governance
- Personalization
- Knowledge Curation
- Client Communication
- Documentation
- Project Management
- Business Analysis
- Cost / ROI
- Legal / Compliance
- Change Management
- Training / Enablement

## Capability Gap判定ルール

- 判定手順・Gap分類7種・優先順位ラダーは `ai_team/capability_gap_policy.md` に従う。
- 「部分対応」の行に該当する依頼は、Gap判定（skill-capability-gap-analysis）を通してから担当を確定する。
- 本書に無いCapabilityが必要になった場合は、行を追加する前にGap判定を行い、判断ログを残す。

## 更新履歴

| 日付 | 内容 | 根拠 |
|---|---|---|
| 2026-08-02 | 初版作成。24分類 + Capability Governance を登録 | セレス指示（Capability Gap / Agent Creation機構の追加依頼） |
