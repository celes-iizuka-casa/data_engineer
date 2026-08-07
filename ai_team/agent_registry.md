# Agent Registry

## 目的

AIエンジニアチームに存在するAI社員Roleを一覧管理し、依頼内容に応じて適切なAI社員を選定できるようにする。

## 正本と本書の関係

- 能力・責任・ハンドオフの正本は `ai_team/capability_registry.yaml`、状態の正本は `ai_team/governance/ai_employee_lifecycle_registry.yaml`。本書は依頼受付時に読む一覧view。
- 優先実行環境・デフォルトモデル・デフォルト工数は非拘束の推奨。実行は常に呼び出し元Runtimeと現在選択済みModelを継承する（`ai_team/model_effort_selection_policy.md`）。
- 能力評価の数値スコアは記載しない（根拠なきスコア禁止）。
- 本書は配布される共有層のRoleだけを載せる。利用者ローカルで追加したRoleは `.local/capability/local_capability_registry.yaml` にあり、依頼受付時は本書と併せて読む（`ai_team/local_capability_layer_policy.md`）。

## Agent一覧

| Agent Role | 主な責任 | 対応領域 | 主なSkills | 優先実行環境 | デフォルトモデル | デフォルト工数 | 使用条件 |
|---|---|---|---|---|---|---|---|
| AI Engineering PMO | 課題分類・作業分解・成果物統合（Deliverable Optimizer） | Project Management | skill-engineering-pmo | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | 複数Role案件・成果物統合・依頼の入口整理 |
| AI Capability Architect | 依頼解析→Capability Gap判定→最小のチーム拡張設計・乱立防止 | Capability Governance | skill-capability-gap-analysis / skill-agent-creation / skill-skill-creation / skill-agent-registry-management | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high（チーム構造変更時はvery_high） | 新種の依頼で対応可否が不明なとき・Role / Skill追加要否の判断 |
| AI Forward Deployed Engineer | 現場課題整理・MVPスコープ・Engineering Handoff・導入定着 | FDE / Field Discovery | skill-forward-deployed-engineer（+サブSkill 10本） | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | 顧客・現場課題が曖昧なとき・業務フロー整理 |
| AI Deliverable Quality Reviewer | 独立品質レビュー・重大度判定 | Quality Review | skill-deliverable-quality-reviewer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | risk_based_quality_gates.yamlでIndependent Reviewがrequired |
| AI Engineering Knowledge Curator | ナレッジ化・Local Second Brain整理 | Knowledge Curation | skill-engineering-knowledge-curator | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium | 明示依頼またはAccepted+再利用価値+root確認済み |
| AI Tech Lead | 技術方針・アーキテクチャ・技術選定 | Architecture | skill-tech-lead | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | 設計判断・トレードオフ・レガシー刷新 |
| AI Fullstack Engineer | MVP実装・フロント/バック横断 | Application | skill-fullstack-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | 縦切りMVP・画面とAPIの接続 |
| AI Frontend Engineer | UI / UX・画面遷移 | Frontend | skill-frontend-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium | 画面設計・アクセシビリティ |
| AI Backend Engineer | API・業務ロジック・DB設計 | Backend | skill-backend-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | API契約・トランザクション・冪等性 |
| AI Data Engineer | データ取得・ETL / ELT・品質 | Data Engineering | skill-data-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | パイプライン・dbt / SQL・データ品質 |
| AI Data Platform Engineer | 基盤標準・カタログ・信頼性・移行統制 | Data Platform | skill-data-platform-engineer / skill-data-platform-migration | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | 共有基盤・メタデータ・ガバナンス標準、基盤移行のwave・照合・cutover/rollback |
| AI Cloud / Infrastructure Engineer | クラウド構成・IaC・IAM実装 | Cloud / Infrastructure | skill-cloud-infrastructure-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | ネットワーク・プロビジョニング・IaC review |
| AI SRE / Platform Engineer | 本番運用・監視・インシデント | SRE / Operations | skill-sre-platform-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | SLO・可観測性・障害対応 |
| AI Security / Governance Engineer | 認証認可・秘密管理・ガバナンス | Security / Governance | skill-security-governance-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | 秘匿情報・PII・権限設計・脅威分析 |
| AI QA / Test Automation Engineer | テスト方針・自動化・回帰 | QA / Testing | skill-qa-test-automation-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | テスト設計・検証証跡 |
| AI / LLM Application Engineer | RAG・LLMアプリ・AI Agent | LLM / RAG / AI Agent | skill-llm-application-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | RAG設計・ガードレール・LLM評価 |
| AI DevEx / Agent Workflow Engineer | Skills設計・AI社員ワークフロー・validator | DevEx / Agent Workflow | skill-devex-agent-workflow-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | エージェント運用・両Runtime対応の実行設計 |
| AI Integration Engineer | 外部API・SaaS連携・OAuth | Integration | skill-integration-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | 外部契約・リトライ・互換性 |
| AI Product Manager | 要件定義・優先順位・受入条件 | Product Management | skill-product-manager | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | medium〜high | スコープ管理・見積り妥当性 |
| AI ML Engineer | 特徴量・学習評価・MLOps | ML | skill-ml-engineer | 呼び出し元Runtime | 現在Model（observed/declaredのみ記録） | high | モデル学習・サービング・ドリフト監視 |

## Agent追加ルール

- `ai_team/agent_creation_policy.md` に従う。新Role追加は最後の手段で、CREATE基準7項目の証跡とCeles Human Gate記録を必須とする。
- 追加時は本書・`capability_matrix.md`・`role_skill_map.md`・`team_overview.md`・`role_scope_matrix.md` を同時に更新する。

## Agent更新ルール

- Role定義・capability entryの変更はrevision変更となるため、`ai_employee_lifecycle_registry.yaml` にUPDATE候補として登録し、eval・独立レビュー・Human Gateを通す（`ai_team/agent_lifecycle_policy.md`）。

## Agent非推奨化ルール

- DEPRECATEもHuman Gateを要する。「使われていない」だけを根拠にしない。後継の割当先を明記する。

## Agent削除ルール

- 物理削除は行わない。DEPRECATED状態の維持と本書上の「retired」表示で表現し、decision_historyは保持する。

## 更新履歴

| 日付 | 内容 | 根拠 |
|---|---|---|
| 2026-08-02 | 初版作成。既存19Role + AI Capability Architect（CREATE）を登録 | セレス指示（Capability Gap / Agent Creation機構の追加依頼）・Celes-HG-20260802-CAPABILITY-ARCHITECT-CREATE |
| 2026-08-07 | AI Data Platform Engineerへ`skill-data-platform-migration`候補を追加 | CelesのSkill実装指示。Lifecycleは独立レビュー済み/HUMAN_GATE pending、ACTIVE未昇格 |
