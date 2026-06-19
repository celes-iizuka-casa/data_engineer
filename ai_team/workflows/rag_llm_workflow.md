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
