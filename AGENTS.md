# Repository Instructions

## Mission
`input/` の課題を読み、実装・設計・テスト・運用に使える成果物を `output/` に作成する。分析者ロールは作らず、必要に応じて分析チーム向けデータ契約と引き継ぎを作る。

## Required Start
1. `input/` と既存 `output/` を確認する。
2. 明示成果物、課題分類、MVP、制約、リスク、`@role`/`@mode`/`@light`/`@full` タグを整理する。
3. `output_optimization_policy.md` の軽量依頼判定を行う。軽量でなく3工程以上なら `_internal/work_plan.md` を作る（軽量なら作らない）。
4. `runtime_selection_policy.md` と `model_effort_selection_policy.md` に従い、呼び出し元Runtimeを変更せず、確認できたruntime/model Evidenceと推奨effortを記録する。高リスク / 大規模なら `_internal/execution_plan.md` を作る。取得不能なmodel/token/costは推測せず`unavailable`とする。
5. 必要な `skills/` を選び、作業を進める。

## Required Finish
- 成果物は `output/<client>/<YYYYMMDD>/<task-name>/` に保存する。常時はタスクフォルダ直下に `output.md`（制御ブロック＋本成果物を統合した1ファイル）のみ。条件付き/要求時の成果物は `_internal/` 配下に置く（`output_optimization_policy.md`・`deliverable_optimization_policy.md`）。
- 顧客名や日付が特定できない場合だけ、合理的な仮名を置いて前提を明記する。
- 本成果物は「関連セクションのみ＋モード別必須核＋条件付き必須」で作る（`professional_response_templates.md`）。複数Roleが関与した場合はDeliverable Optimizer（PMO）が統合して `output.md` 1本にまとめる。
- 品質レビューは必要性ゲートを満たす場合に実施する。満たさない場合は output.md 先頭ブロックの品質判定を「レビュー対象外」にする。満たす場合は `templates/quality_review_request_template.md` で提出し、Reviewerが `_internal/quality_review_report.md` を作る。
- 最終判定が `REWORK_REQUIRED` または `BLOCKED` の場合、完了扱いにせず、再作業内容または停止理由を output.md 先頭ブロックの「要対応」に書く。
- 顧客案件または再利用価値のある成果物は、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が第二の脳へ反映し、`_internal/obsidian_sync_summary.md` を更新する。
- `output.md` を常時作成する。`execution_summary` と `questions` の独立ファイルは必要性ゲートを満たす時だけ作る。
- 実行したテスト、未実行テスト、残存リスクを output.md または本成果物に明記する。

## Engineering Rules
- 最小構成を優先するが、認証認可、秘密管理、監視、再実行性、テストを省略しない。
- 不明な外部仕様を断定しない。公式資料または実データで確認する。
- 破壊的変更には理由、影響範囲、移行、ロールバックを付ける。
- 既存成果物と用語、要件ID、データ粒度、API契約を整合させる。
- 質問だけで止めず、合理的な仮定を明記して成果物を作る。
- 作成者自身の確認を独立レビューとして扱わない。
- 専門ReviewerのBlockerをPMOや総合Reviewerが独断で解除しない。
- AIエンジニアチームは Claude Code / Codex の両方で実行できる runtime-neutral 構成を保つ（`ai_team/runtime_neutral_design_policy.md`）。

## Writing Style
- 実務担当者がそのまま話しているような、自然で率直な日本語を使う。
- 見出し、箇条書き、表は読みやすさに必要な分だけ使い、細かく分割しすぎない。
- 同じ結論や注意事項を言い換えて繰り返さない。
- 抽象的なAI表現を避け、判断、理由、影響、次の行動を具体的に書く。
- 顧客向け成果物では、専門用語を残しつつ、その意味が文脈から分かるように書く。
- 本成果物は該当する見出しだけ出す。該当なしの見出しは省略する（必須核・条件付き必須は除く）。
