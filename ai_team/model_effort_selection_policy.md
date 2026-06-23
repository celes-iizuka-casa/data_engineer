# Model Effort Selection Policy

## 目的

AIエンジニアチームが、依頼内容を解析し、対応するAI社員Role、実行環境、モデル、工数を自動判断するための基準を定義する。`model_selection_policy.md`（必要能力ベースの抽象層）の上に乗る「具体モデル・工数・実行環境」の実体層であり、両者を矛盾させない。

- 抽象層（能力で語る）: `model_selection_policy.md`
- 実体層（具体モデル名・工数・runtimeで語る）: 本ポリシー

## 基本方針

- 依頼内容を作業工程に分解する
- 工程ごとに必要なRoleを選定する
- 工程ごとに実行環境を選定する（`runtime_selection_policy.md`）
- 工程ごとにモデルを選定する
- 工程ごとに工数を選定する
- 判断理由を必ず記録する（`_internal/execution_plan.md` ＋ output.md 制御ブロック）
- 高工数モデルを常用しない
- 低工数で十分な作業は低工数にする
- ただし、設計・セキュリティ・商用化・大規模改修では工数をケチらない
- 繰り返し作業は代表例確認フロー（`iteration_confirmation_policy.md`）と組み合わせる

## 利用可能モデル

### Claude Code

| モデル | 選べる工数 |
|---|---|
| Opus4.8 | 低 / 中 / 高 / 特大 / Max / Ultracode |
| Sonnet4.6 | 低 / 中 / 高 / Max |
| Haiku4.5 | 工数指定なし（軽量タスク用） |

### Codex

| モデル | 選べる工数 |
|---|---|
| GPT-5.5 | 低 / 中 / 高 / 非常に高い |

## 工数の意味

工数は人間の作業時間ではなく、AIモデルに使わせる推論量・作業深度・探索量・編集慎重度を指す。

| 工数 | 使う場面 | 特徴 | 対応 |
|---|---|---|---|
| 低 | 軽微修正 / 要約 / フォーマット / typo / テンプレ単純追記 | 速い・浅い推論・低リスク向き | Claude Code(全モデル) / Codex |
| 中 | 通常ドキュメント / 小〜中設計整理 / 単発SQL・Python修正 / 軽めレビュー | バランス型・通常初期値 | Claude Code(Sonnet/Opus) / Codex |
| 高 | 設計 / 実装 / 検証 / 重要Role・Skill改良 / データ基盤・RAG設計 / 既存コード読解修正 / Sec・運用・テスト観点 | プロ作業の推奨初期値 | Claude Code(Opus/Sonnet) / Codex |
| 特大 | 複雑なチーム改良 / 大きめのアーキ設計 / 複数Role・Skill影響 / 既存構成非破壊の広範囲差分 / 方針ミスの影響大 | 深い検討・全体整合性重視 | Claude Code Opus4.8 |
| Max | 複数ファイル・Skill・Workflow横断の大規模改修 / 設計・実装・検証が混在 / 手戻り大 / 仕様整合性重要 | かなり慎重・代表例確認併用・セレス確認点必須 | Claude Code Opus4.8 / Sonnet4.6 |
| Ultracode | AI社員チーム自体の大規模再設計 / 複雑リポジトリ大規模改修 / 複数サブシステム横断 / 失敗時影響が極大 / セレス明示指定 | 最重量級・常用しない・理由明記必須・原則 execution_plan 先出し・繰り返しは代表例確認必須 | Claude Code Opus4.8 |
| 非常に高い | Codexでの高難度設計・実装・検証 / 複数ファイル横断 / 既存コード・SQL・Terraform・dbt深読み改修 / Sec・運用・品質リスク | Codex側の最重量級・常用しない・理由明記必須 | Codex GPT-5.5 |

## 工数判定基準（作業タイプ別）

| 作業タイプ | 条件 | Claude Code | Codex |
|---|---|---|---|
| 軽量タスク | 単純要約 / 軽微修正 / 低リスク / 影響小 / 技術判断少 | Haiku4.5（工数なし） | GPT-5.5 低 |
| 通常タスク | 単発設計・実装・SQL修正 / 通常レビュー / 影響限定的 | Sonnet4.6 中 | GPT-5.5 中 |
| プロ品質タスク | 「プロとして」依頼 / 設計・実装・検証品質が重要 / 商用化・MVP / 顧客提出物になり得る / Sec・運用・品質観点 | Opus4.8 高 | GPT-5.5 高 |
| 複雑・高リスク | 複数Role影響 / 複数ファイル更新 / 既存構成を壊し得る / 重要設計判断 / リカバリコスト高 / Sec・権限・データ品質 | Opus4.8 特大 | GPT-5.5 高 |
| 大規模改修 | チーム全体再設計 / 大量Role・Skill更新 / 複数Workflow・テンプレ更新 / 複数SQL・コード一括修正 / 全体整合性重要 | Opus4.8 Max | GPT-5.5 非常に高い |
| 超大規模・最重要 | セレスがUltracode明示 / チーム構造を大きく変える / 失敗時影響が極大 / 長大リポジトリ横断 / 全体最適と細部修正の両方 | Opus4.8 Ultracode | GPT-5.5 非常に高い |

## Roleごとの初期推奨

Role固定ではなく、依頼内容・工程・リスクに応じて調整する初期値。

| AI社員Role | 優先実行環境 | デフォルトモデル | デフォルト工数 |
|---|---|---|---|
| AI Engineering PMO | Claude Code | Opus4.8 | 高 |
| AI Forward Deployed Engineer | Claude Code | Opus4.8 | 高 |
| AI Tech Lead | Claude Code | Opus4.8 | 高 |
| AI Fullstack Engineer | Codex | GPT-5.5 | 高 |
| AI Frontend Engineer | Codex | GPT-5.5 | 中〜高 |
| AI Backend Engineer | Codex | GPT-5.5 | 高 |
| AI Data Engineer | Codex | GPT-5.5 | 高 |
| AI Data Platform Engineer | Claude Code + Codex | Opus4.8 / GPT-5.5 | 高 |
| AI Cloud / Infrastructure Engineer | Codex | GPT-5.5 | 高 |
| AI SRE / Platform Engineer | Claude Code + Codex | Opus4.8 / GPT-5.5 | 中〜高 |
| AI Security / Governance Engineer | Claude Code | Opus4.8 | 高 |
| AI QA / Test Automation Engineer | Codex | GPT-5.5 | 中〜高 |
| AI / LLM Application Engineer | Claude Code + Codex | Opus4.8 / GPT-5.5 | 高 |
| AI DevEx / Agent Workflow Engineer | Claude Code | Opus4.8 | 高 |
| AI Integration Engineer | Codex | GPT-5.5 | 高 |
| AI Engineering Knowledge Curator | Claude Code | Sonnet4.6 | 中 |
| AI Deliverable Quality Reviewer | Claude Code | Opus4.8 | 高 |

## 作業タイプごとの推奨（併用パターン）

設計から実装まである作業は、工程ごとに実行環境とモデルを切り替える。

| 工程 | 実行環境 | モデル | 工数 |
|---|---|---|---|
| 計画・設計 | Claude Code | Opus4.8 | 高 |
| 実装 | Codex | GPT-5.5 | 高 |
| 検証 | Claude Code / Codex | Opus4.8 / GPT-5.5 | 中 / 高 |

繰り返し作業は `iteration_confirmation_policy.md` の代表例確認フローと組み合わせ、代表例設計→代表例実装→（セレス確認）→全件展開→全件検証の各工程で工数を変える。

## エスカレーション条件（工数を上げる）

以下に該当する場合、工数を上げる。

- 影響範囲が広い / 既存ファイルが多い / 誤ると全体に波及する
- セキュリティ・権限・監査が絡む / データ品質が重要
- 顧客提出物になる / 商用化・本番運用に関係する
- 複数Roleにまたがる
- セレスが「最高」「プロとして」「厳しめ」と依頼している

## ダウングレード条件（工数を下げる）

以下に該当する場合、工数を下げてよい。

- 軽微な修正 / typo修正 / フォーマット修正
- 低リスク / 影響範囲が小さい
- 明確なテンプレート適用
- セレスが「簡単でよい」と明示している

## セレス確認が必要な条件

以下の場合、作業前または全件展開前にセレス確認を入れる。

- 工数が Max / Ultracode / 非常に高い
- 複数ファイルへの一括展開
- 出力体裁の好みが関係する
- 方針が複数考えられる
- 既存チーム構成に大きく影響する
- 第二の脳の構成に影響する
- 顧客提出物になる

ただし、セレスが「確認不要で進めて」と明示した場合は省略してよい。

## 完了条件

- 依頼が工程に分解されている
- 工程ごとに Role / 実行環境 / モデル / 工数 が決まっている
- デフォルトから変更した工程は理由が記録されている
- 高工数（特大/Max/Ultracode/非常に高い）を使う工程は理由が明記されている
- セレス確認が必要な工程が特定されている
- `_internal/execution_plan.md` が作成され、採用 runtime/model/effort が output.md 制御ブロックに表示されている

## 参照

- `ai_team/model_selection_policy.md`（能力ベースの抽象層）
- `ai_team/runtime_selection_policy.md`
- `ai_team/claude_code_execution_policy.md`
- `ai_team/codex_execution_policy.md`
- `ai_team/iteration_confirmation_policy.md`
- `ai_team/output_optimization_policy.md`
- `templates/execution_plan_template.md`
- `ai_team/roles/engineering_pmo.md`
