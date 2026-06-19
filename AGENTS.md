# Repository Instructions

## Mission
`input/` の課題を読み、実装・設計・テスト・運用に使える成果物を `output/` に作成する。分析者ロールは作らず、必要に応じて分析チーム向けデータ契約と引き継ぎを作る。

## Required Start
1. `input/` と既存 `output/` を確認する。
2. 明示成果物、課題分類、MVP、制約、リスクを整理する。
3. `output/work_plan.md` を作成または更新する。
4. 必要な `skills/` を選び、作業を進める。

## Required Finish
- 成果物は原則として `output/<client>/<YYYYMMDD>/<task-name>/` に保存する。
- 顧客名や日付が特定できない場合だけ、合理的な仮名を置いて前提を明記する。
- `templates/quality_review_request_template.md` を使い、対象、要件、差分、検証証跡、未実施事項を提出する。
- AI Deliverable Quality Reviewerが `output/quality_review_report.md` を作成する。
- 最終判定が `REWORK_REQUIRED` または `BLOCKED` の場合、完了扱いにせず、再作業内容または停止理由として報告する。
- 顧客案件または再利用価値のある成果物は、AI Engineering Knowledge Curatorが第二の脳へ反映し、`output/obsidian_sync_summary.md` を更新する。
- `output/execution_summary.md` と `output/questions.md` を更新する。
- 実行したテスト、未実行テスト、残存リスクを明記する。

## Engineering Rules
- 最小構成を優先するが、認証認可、秘密管理、監視、再実行性、テストを省略しない。
- 不明な外部仕様を断定しない。公式資料または実データで確認する。
- 破壊的変更には理由、影響範囲、移行、ロールバックを付ける。
- 既存成果物と用語、要件ID、データ粒度、API契約を整合させる。
- 質問だけで止めず、合理的な仮定を明記して成果物を作る。
- 作成者自身の確認を独立レビューとして扱わない。
- 専門ReviewerのBlockerをPMOや総合Reviewerが独断で解除しない。

## Writing Style
- 実務担当者がそのまま話しているような、自然で率直な日本語を使う。
- 見出し、箇条書き、表は読みやすさに必要な分だけ使い、細かく分割しすぎない。
- 同じ結論や注意事項を言い換えて繰り返さない。
- 抽象的なAI表現を避け、判断、理由、影響、次の行動を具体的に書く。
- 顧客向け成果物では、専門用語を残しつつ、その意味が文脈から分かるように書く。
