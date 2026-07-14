# Output Optimization Policy

## 目的

1依頼あたりの提出物を「利用者が読むべき最小限」に絞る。デフォルトは結論サマリーと本成果物を統合した`output.md` 1本。それ以外は必要性ゲートを満たした時だけ生成する。

## 出力3階層

| 階層 | 中身 | 生成条件 |
|---|---|---|
| A. 常に渡す | `output.md`（本成果物・制御ブロックを内包した統合1ファイル） | 毎回 |
| B. 条件付き | execution_plan / iteration_plan＋sample / quality_review_report / task_retrospective / obsidian_sync_summary | 下記ゲートを満たした時だけ |
| C. 要求時のみ | work_plan / quality_review_request / execution_summary（10項目詳細）/ questions（全文） | セレスが明示要求した時、または内部参照用 |

複数Roleが関与した場合も Role別成果物を並べず、Deliverable Optimizer（PMO）が統合して `output.md` 1本にまとめる（`deliverable_optimization_policy.md` 参照）。

## フォルダ構造

```
output/<client>/<YYYYMMDD>/<task-name>/
├── output.md                   # 1ファイルで意思決定できる（常時）
└── _internal/                  # B/C層。普段は開かない
    ├── quality_review_report.md
    ├── execution_plan.md
    └── ...
```

A層は `output.md` 1ファイルのみ、タスクフォルダ直下に置く。B/C層は必ず `_internal/` 配下に置く。

## 必要性ゲート

| 成果物 | 作る条件（満たした時だけ） | 満たさない時 |
|---|---|---|
| output.md | 常に | — |
| execution_plan | 高リスク・セキュリティ・大規模改修・複数工程/複数ファイル | 作らない（output.md制御ブロックにcaller RuntimeとEvidence typeを記録） |
| work_plan | 3工程以上 or 明示的な除外スコープが要る依頼 | 作らない（サマリーの次アクションで代替） |
| iteration_plan + sample | `iteration_confirmation_policy` の繰り返し判定に該当 | 作らない |
| quality_review_report | `review/risk_based_quality_gates.yaml`でMedium以上、または顧客提出物・再利用物として追加レビューが必要 | 必須Gateがない場合だけ「レビュー対象外」と明記 |
| questions（独立ファイル） | 未確認事項が実在する場合のみ | 作らない（空ファイルを作らない。少数ならサマリー「要対応」に直書き） |
| task_retrospective | `Completed/Accepted` かつ軽量依頼でない | 作らない |
| obsidian_sync_summary | `obsidian_write_policy` のORトリガーを満たし、実際にLocal Second Brainへ書き込んだ | 作らない |
| execution_summary（10項目詳細） | セレスが明示要求 or 大型案件で詳細記録が要る時 | 作らない（サマリーで代替） |

## 軽量依頼の定義

以下をすべて満たす依頼は「軽量依頼」とし、A層の`output.md` 1ファイルだけを出す（B/C層は原則全スキップ）:

- 単一工程で完結
- 顧客提出物でない
- 本番/セキュリティ/破壊的変更を伴わない
- 取り消し可能（リスクが低い）

## 本成果物のセクション間引き

- テンプレの見出しは「今回中身がある項目だけ」出力する。該当なしの見出しはまるごと省略し、「該当なし」とも書かない。
- ただしモード別の必須核は必ず出す（`professional_response_templates.md` 参照）。
- 条件付き必須:
  - 本番/破壊的変更 → ロールバックを必須化（省略禁止）
  - 認証認可・秘密・個人情報・外部公開を伴う → セキュリティを必須化（省略禁止）

## 入力タグ（任意）

依頼側に必須フォーマットは課さない。自然文から role / mode / scope をチームが判定し、サマリー冒頭「依頼の理解」で言い返す。使いたい時だけ次のワンライナータグを使える:

- `@role:<name>` … 担当Role指定
- `@mode:<opinion|design|impl|verify>` … モード指定
- `@light` … 強制的に軽量（`output.md`のみ）
- `@full` … 全成果物を出させる

## 参照

- `ai_team/workflows/input_to_output_workflow.md`
- `ai_team/deliverable_optimization_policy.md`
- `templates/output_template.md`
- `ai_team/professional_response_templates.md`
- `ai_team/iteration_confirmation_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/model_effort_selection_policy.md`
- `ai_team/runtime_selection_policy.md`
- `ai_team/review/risk_based_quality_gates.yaml`
