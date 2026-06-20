# RAG and LLM Workflow

## 目的
評価・権限・根拠を先に設計し、本番利用可能なLLM機能を作る。

## 開始条件
- RAG、チャットボット、AI Agentを新設・変更する
- 回答品質や安全性を改善する

## 主担当
- AI / LLM Application Engineer
- AI Data Engineer
- AI Backend Engineer
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer

## 手順
1. 業務価値、誤答影響、人間承認点を定義する
2. 知識ソース、権限、更新、削除を確認する
3. 検索・生成・ツール実行の境界を設計する
4. 代表・境界・攻撃ケースの評価セットを作る
5. 品質、根拠、安全性、コスト、遅延を測る
6. 監視、フィードバック、モデル変更手順を整備する

## 品質ゲート
- 権限付き検索
- 根拠提示と不明回答
- プロンプトインジェクション対策
- 評価セットと回帰基準
- 高影響操作の承認

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- rag_architecture.md
- retrieval_design.md
- prompt_design.md
- evaluation_design.md
- guardrails.md
- llmops_design.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: 評価ケース・プロンプト改善・チューニングが3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **モデル選定**: 各工程（設計・実装・評価・LLMOps）で `model_selection_policy.md` に従いLLMモデルを使い分ける
- **振り返り**: 作業完了後に `retrospective_policy.md` に従い `output/task_retrospective.md` を作成する
- **第二の脳整理**: 成果物が承認されたとき、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
