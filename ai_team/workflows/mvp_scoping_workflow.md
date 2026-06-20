# MVP Scoping Workflow

## 目的
顧客価値が出る最小範囲を定義し、過剰実装を避けながら後からスケールできるMVPへ落とす。

## 開始条件
- 顧客要望が多く、初期リリース範囲を決めたい
- PoCから商用化へ進める判断が必要
- 技術的には作れそうだが、現場で使われるか不安
- 予算、期間、データ、環境、権限などの制約が強い

## 主担当
- AI Forward Deployed Engineer
- AI Engineering PMO
- AI Tech Lead
- AI Fullstack Engineer
- AI Data Engineer
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer
- AI Deliverable Quality Reviewer

## 手順
1. 目的、利用者、業務場面、成功条件を確認する
2. すべての要望を顧客価値、頻度、影響、実装難度で分類する
3. MVPで解く課題と解かない課題を分ける
4. 初期リリース範囲、手動運用でよい範囲、将来自動化する範囲を決める
5. Tech Leadが後から詰まらない拡張余地と技術負債を確認する
6. QAが受入条件と現場テスト観点を作る
7. Security、SRE、Dataの必須ゲートを最小範囲に組み込む
8. PMOが実装順序、依存関係、判断事項を整理する

## 品質ゲート
- MVPの目的と成功条件が明確
- MVPに含めること、含めないことが明確
- 手動運用でよい範囲と自動化する範囲が分かれている
- 技術負債の返済条件がある
- 受入条件、現場テスト、導入条件がある
- Security、QA、SREを後回しにしていない

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- mvp_scope.md
- use_cases.md
- user_stories.md
- acceptance_criteria.md
- engineering_handoff.md
- rollout_plan.md
- success_metrics.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: ユーザーストーリー・受入条件が3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **モデル選定**: 依頼解析・方針策定・スコープ定義の各工程で `model_selection_policy.md` に従いモデルを使い分ける
- **振り返り**: MVPスコープ確定後に `retrospective_policy.md` に従い `output/task_retrospective.md` を作成する
- **第二の脳整理**: 成果物が承認されたとき、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
