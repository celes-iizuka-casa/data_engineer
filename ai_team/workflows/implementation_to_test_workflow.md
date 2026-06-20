# Implementation to Test Workflow

## 目的
変更リスクに応じた検証を行い、リリース可否を判断する。

## 開始条件
- 実装差分が完成した
- リリース候補を作成した

## 主担当
- AI QA / Test Automation Engineer
- AI Tech Lead
- AI Security / Governance Engineer
- AI SRE / Platform Engineer

## 手順
1. 変更差分と影響範囲を確認する
2. 単体・結合・契約・E2E・データ品質テストを配分する
3. lint、型、静的解析、脆弱性検査を実行する
4. 代表・境界・異常・権限ケースを実行する
5. 性能、監視、ロールバックを確認する
6. 結果、未テスト範囲、残存リスクを記録する

## 品質ゲート
- 重大な既知不具合がない
- 受入条件を満たす
- 本番監視とロールバックが準備済み
- 例外承認に期限と責任者がある

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- test_result.md
- quality_gate_result.md
- release_notes.md
- remaining_issues.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: テストケース・検証対象が3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **モデル選定**: 検証・テスト生成の工程で `model_selection_policy.md` に従いモデルを使い分ける
- **振り返り**: 検証完了後に `retrospective_policy.md` に従い `output/task_retrospective.md` を作成する
- **第二の脳整理**: 検証完了後、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
