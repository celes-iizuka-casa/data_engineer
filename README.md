# AI Engineering Team

セレス向けのAI社員エンジニアチーム運用リポジトリです。
`input/` に依頼・資料・エラー・顧客メモを置き、AI Agentが専門Roleとして意見、設計、実装、検証を行い、成果物を `output/` に作成します。

単なる作業代行ではなく、データエンジニアリング、業務アプリ、AI Agent、FDE、PMO、SRE、セキュリティ、QAなどの観点を分担し、MVPと商用化・保守性・運用性のバランスを見ます。

## 目的

このリポジトリの目的は、セレスからの依頼を「実務で使える成果物」に変換することです。

- 顧客課題、設計相談、実装依頼、レビュー依頼を専門Roleに振り分ける
- 依頼を Professional Opinion / Design / Implementation / Verification Mode に分類する
- 必要なテンプレート、Skill、Workflowを使って成果物を作る
- 成果物を `output/<client>/<YYYYMMDD>/<task-name>/output.md` に統合する
- 必要に応じて品質レビュー、実行計画、ナレッジ化を行う

## 基本コンセプト

このリポジトリでは、AI Agentを「便利なチャット相手」ではなく、専門職能を持つAI社員として扱います。

主な考え方は以下です。

- セレスの依頼に無条件で同意しない
- 危ない設計、曖昧な要件、運用で詰まりそうな構成は率直に指摘する
- ただし否定だけで終わらず、MVPとして現実的な代替案を出す
- 不明な外部仕様、未確認のライブラリ機能、顧客事情を断定しない
- 認証認可、秘密管理、監視、再実行性、テスト、データ品質を後回しにしない

## 主な機能

### 1. 依頼の受付

`input/` に依頼文、顧客資料、設計メモ、エラー内容、コード断片などを配置します。

例:

```text
input/Lograph/Looker_BigQuery_運用キャッチアップ依頼.md
input/トヨテック/ClouderaのDataVizに関する初学者への共有.md
```

### 2. Role選定

`ai_team/role_scope_matrix.md` に基づき、依頼に合うRoleを選びます。

代表的なRole:

- `AI Engineering PMO`: 課題分類、作業分解、成果物統合、進行管理
- `AI Forward Deployed Engineer`: 顧客・現場課題整理、MVPスコープ、導入観点
- `AI Tech Lead`: 技術方針、アーキテクチャ、非機能要件、品質ゲート
- `AI Data Engineer`: ETL/ELT、SQL、dbt、DWH、データ品質、再実行性
- `AI Data Platform Engineer`: データ基盤標準化、メタデータ、リネージ、共通パイプライン
- `AI Fullstack / Backend / Frontend Engineer`: 業務アプリやWebアプリの設計・実装
- `AI Security / Governance Engineer`: 認証認可、IAM、監査、機密情報、データ保護
- `AI QA / Test Automation Engineer`: テスト方針、テスト自動化、検証レポート
- `AI Deliverable Quality Reviewer`: 成果物の独立品質レビュー
- `AI Engineering Knowledge Curator`: 再利用価値のある成果物のナレッジ化

### 3. Professional Mode分類

依頼内容を `ai_team/request_mode_policy.md` に従って分類します。

- `Professional Opinion Mode`: 妥当性、懸念、判断、代替案を出す
- `Professional Design Mode`: 設計、アーキテクチャ、非機能、運用を整理する
- `Professional Implementation Mode`: コード、SQL、設定、テストを実装する
- `Professional Verification Mode`: 検証、レビュー、再現手順、修正案を出す

### 4. 成果物の最適化

成果物は原則として1依頼につき `output.md` 1本に統合します。
詳細な計画、品質レビュー、実行サマリーなどは必要性ゲートを満たす場合だけ `_internal/` に作成します。

標準構成:

```text
output/<client>/<YYYYMMDD>/<task-name>/
├── output.md
└── _internal/
    ├── execution_plan.md
    ├── quality_review_report.md
    └── ...
```

軽量依頼では `_internal/work_plan.md` を作らず、すぐに成果物へ進みます。

### 5. Claude Code / Codex 両対応

このリポジトリは Claude Code と Codex の両方で実行できる runtime-neutral 構成です。

- Role / Skill / Workflow設計、方針整理、FDE設計は Claude Code を優先
- 既存ファイル修正、コード、SQL、テスト、機械的な差分実装は Codex を優先
- 設計と実装が混在する場合は併用

判断基準は以下を参照します。

- `ai_team/runtime_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/runtime_neutral_design_policy.md`
- `claude_code_team_execution.md`
- `codex_team_execution.md`

### 6. テンプレートとSkill

`templates/` には要件定義、設計、テスト、運用、データ基盤、FDE、品質レビューなどのテンプレートがあります。
`skills/` にはRoleごとの実行指針があります。

主なディレクトリ:

```text
ai_team/     # Role定義、運用ポリシー、レビュー基準
skills/      # Role別Skill定義
templates/   # 成果物テンプレート
input/       # 依頼・資料・メモ
output/      # 生成成果物
tools/       # 検証・変換・生成スクリプト
tests/       # pytestテスト
```

## 利用するメリット

- 依頼が曖昧でも、前提・MVP・リスク・次アクションに分解しやすい
- データ基盤、AI Agent、業務アプリ、FDE、PMOを同じ運用ルールで扱える
- 成果物が `output.md` に統合されるため、読むべきファイルが増えすぎにくい
- RoleとModeが分かれるため、意見、設計、実装、検証の責任範囲を明確にしやすい
- テンプレートとSkillにより、案件ごとの成果物品質を揃えやすい
- 軽量依頼と重い依頼を分けられるため、過剰なドキュメント作成を避けやすい
- 顧客提出物や再利用価値のある成果物は、品質レビューやナレッジ化につなげやすい

## デメリット・向かないケース

- 小さなメモや一問一答には、Role選定や成果物形式が重く感じることがある
- ポリシー、Skill、テンプレートが多いため、初回は読む場所を迷いやすい
- 外部仕様や顧客固有情報が不足している場合、仮定ベースの成果物になる
- 独立品質レビューが必要な依頼では、軽いチャットより時間がかかる
- AI Agentの運用前提があるため、人間だけで使う場合はルールを取捨選択する必要がある

## 使用する際の注意点

### 機密情報を入れない

`input/` や `output/` には、APIキー、パスワード、接続文字列、個人情報、顧客の機密情報をそのまま置かないでください。必要な場合はマスク済みサンプル、スキーマ、項目定義、エラー抜粋に変換します。

### 未確認仕様を断定しない

外部サービス、ライブラリ、クラウド仕様、SaaS APIの挙動は、公式資料または実データで確認してから書きます。確認できていない場合は「未確認」「仮定」として明記します。

### outputを増やしすぎない

基本は `output.md` 1本です。`execution_summary.md`、`questions.md`、`work_plan.md` などの独立ファイルは、必要性ゲートを満たす場合だけ作ります。

### 品質レビューを自己レビューにしない

作成者自身の確認は独立レビューではありません。顧客提出物、本番影響、セキュリティ影響、再利用価値がある成果物は、必要に応じて `AI Deliverable Quality Reviewer` が独立レビューします。

### MVPでも運用観点を捨てない

MVPではスコープを小さくしますが、認証認可、秘密管理、監視、ログ、テスト、再実行性、ロールバック方針を完全に省略しないでください。

## セットアップ

### 1. リポジトリを取得する

```bash
git clone <repository-url>
cd data_engineer
```

既にローカルにある場合は、このディレクトリを開きます。

```bash
cd /Users/celesiizuka/Celestian/CASA/data_engineer
```

### 2. Python環境を用意する

Python 3.9以降を推奨します。

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-dev.txt
```

テストを実行する場合は `pytest` も必要です。環境に入っていない場合は追加します。

```bash
python3 -m pip install pytest
```

### 3. リポジトリ構造を検証する

```bash
python3 tools/validate_repository.py
```

このコマンドは、Role、Skill、Workflow、Templateの存在や基本契約を確認します。

### 4. テストを実行する

```bash
python3 -m pytest tests/ -v
```

特定テストだけ実行する場合:

```bash
python3 -m pytest tests/test_split_table_statements.py -v
```

## 基本的な使い方

### 1. 依頼を `input/` に置く

顧客名または案件名ごとにサブディレクトリを作り、依頼文や資料を配置します。

```text
input/<client>/<task>.md
```

依頼には以下があると処理しやすくなります。

- 背景
- 目的
- 期待する成果物
- 現在の制約
- 入力データや対象コード
- 期限や優先度
- 顧客提出物か内部利用か

### 2. 依頼タイプを分類する

`ai_team/request_mode_policy.md` を見て、依頼が意見、設計、実装、検証のどれかを判断します。

自然文でも問題ありません。必要なら以下のタグを依頼文に付けます。

```text
@role:data_engineer
@mode:design
@light
@full
```

### 3. RoleとSkillを選ぶ

`ai_team/role_scope_matrix.md` を見て担当Roleを選び、対応する `skills/skill-*/README.md` と `SKILL.md` を確認します。

例:

- データパイプライン設計: `skill-data-engineer`
- データ基盤標準化: `skill-data-platform-engineer`
- 顧客課題整理: `skill-forward-deployed-engineer`
- 業務アプリ実装: `skill-fullstack-engineer`
- 品質レビュー: `skill-deliverable-quality-reviewer`

### 4. 成果物を作成する

成果物は以下に保存します。

```text
output/<client>/<YYYYMMDD>/<task-name>/output.md
```

顧客名や日付が特定できない場合だけ、合理的な仮名を置き、前提として明記します。

### 5. 必要に応じてレビューする

以下に該当する場合は、品質レビューを検討します。

- 顧客提出物
- 本番運用に影響する成果物
- セキュリティ、認証認可、機密情報、権限が絡む成果物
- 複数案件で再利用する成果物
- 破壊的変更や大きな設計判断を含む成果物

## よく使うコマンド

```bash
# リポジトリ構造とSkill契約の検証
python3 tools/validate_repository.py

# 全テスト
python3 -m pytest tests/ -v

# CTAS DDL変換ツールのテスト
python3 -m pytest tests/test_convert_ctas_ddl_to_iceberg.py -v

# SQL分割ツールのテスト
python3 -m pytest tests/test_split_table_statements.py -v
```

## 主要ドキュメント

まず読むべきもの:

- `AGENTS.md`: このリポジトリで作業するAI Agent向けの最上位ルール
- `CLAUDE.md`: Claude Code向けの実行ガイド
- `ai_team/README.md`: AI Engineering Teamの基本方針
- `ai_team/role_scope_matrix.md`: Roleごとの責任範囲
- `ai_team/request_mode_policy.md`: 依頼タイプの分類
- `ai_team/output_optimization_policy.md`: 成果物を増やしすぎないためのルール
- `ai_team/runtime_selection_policy.md`: Claude Code / Codex の使い分け
- `ai_team/model_effort_selection_policy.md`: モデルと工数の選定基準
- `ai_team/professional_response_templates.md`: モード別の成果物構成
- `ai_team/review/professional_quality_gate.md`: 品質レビュー基準

## ディレクトリ構成

```text
.
├── AGENTS.md
├── CLAUDE.md
├── README.md
├── ai_team/
│   ├── roles/
│   ├── review/
│   ├── workflows/
│   └── fde/
├── skills/
├── templates/
├── input/
├── output/
├── tools/
├── tests/
├── claude_code_team_execution.md
└── codex_team_execution.md
```

## 成果物作成時の最低限チェック

成果物を作る前:

- 目的、前提、MVP範囲、スケール時の拡張余地を整理したか
- 要件の曖昧さ、設計リスク、運用リスク、データ品質リスク、セキュリティリスクを見たか
- `input/` と既存 `output/` を確認したか
- 軽量依頼か、計画が必要な依頼かを判断したか
- Claude Code / Codex のどちらで進めるべきか判断したか

成果物を出す前:

- `output.md` に本成果物と制御ブロックを統合したか
- 実行したテスト、未実行テスト、残存リスクを書いたか
- 顧客提出物や本番影響がある場合、品質レビューの要否を判断したか
- 破壊的変更がある場合、理由、影響範囲、移行、ロールバックを書いたか
- 不明点を断定せず、仮定と未確認事項に分けたか

## トラブルシュート

### どのRoleを使うか迷う

`ai_team/role_scope_matrix.md` を確認します。顧客・現場課題ならFDE、技術方針ならTech Lead、データ処理ならData Engineer、データ基盤標準化ならData Platform Engineerを起点にします。

### 成果物が増えすぎる

`ai_team/output_optimization_policy.md` を確認します。基本は `output.md` 1本です。`_internal/` は必要性ゲートを満たす場合だけ使います。

### 検証で失敗する

まず以下を実行します。

```bash
python3 tools/validate_repository.py
python3 -m pytest tests/ -v
```

失敗した場合は、エラーメッセージ、対象ファイル、再現コマンドを `input/` に残して、Verification Modeで扱います。

### 顧客情報をどこまで入れてよいか迷う

原則として秘密情報は入れません。顧客名、業務概要、スキーマ、匿名化済みサンプル、マスク済みエラーは扱えますが、APIキー、認証情報、個人情報、契約上の機密情報は入れないでください。

## 運用上の留意点

- ルールが多いため、最初から全ファイルを読むより、依頼に必要なRole、Skill、Templateに絞って読む
- READMEは入口、詳細ルールは `ai_team/` と `skills/` を正とする
- 軽量依頼では過剰な計画書を作らない
- 大きな設計変更、Skill追加、Role変更は既存ポリシーとの整合を確認する
- 再利用価値のある成果物は、レビュー完了後にKnowledge Curatorでナレッジ化を検討する
