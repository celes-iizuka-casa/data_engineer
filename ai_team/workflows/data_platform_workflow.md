# Data Platform Workflow

## 目的
ソース取得から利用者提供まで、再処理可能なデータプロダクトを作る。

## 開始条件
- 新しいデータソースを取り込む
- Core / Martや基盤標準を追加する

## 主担当
- AI Data Engineer
- AI Data Platform Engineer
- AI Integration Engineer
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer

## 手順
1. ソース契約、粒度、キー、更新・削除仕様を確認する
2. Raw / Staging / Core / Martと保持期間を設計する
3. 増分、遅延到着、重複排除、バックフィルを設計する
4. DDL、変換、品質テスト、リコンシリエーションを実装する
5. 権限、分類、リネージ、カタログを登録する
6. SLA、監視、再実行Runbookを検証する

## 品質ゲート
- 粒度・主キー・時刻定義
- 再実行して同じ結果になる
- 品質エラーが可視化される
- 利用者契約と機密区分がある

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- data_architecture.md
- data_pipeline_design.md
- DDL / dbt models
- data_quality_rules.md
- lineage.md
- operation_runbook.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: DDL・変換・パイプライン定義が3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **能力・effort提案**: 設計・実装・検証で必要な能力を `model_selection_policy.md` に従い非拘束で記録する。呼び出し元の現在Modelは変更しない
- **振り返り**: パイプライン完成後に `retrospective_policy.md` に従い `output/.../_internal/task_retrospective.md` を作成する
- **第二の脳整理**: 成果物が承認されたとき、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
