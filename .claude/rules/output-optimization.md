---
description: 成果物出力の最適化ルール。A層はoutput.md 1ファイル、B/C層は必要性ゲート後のみ _internal/ に出力する。
paths:
  - output/**
---

# Output Optimization Rules

## 出力3階層

| 階層 | 内容 | 生成条件 |
|---|---|---|
| **A層（常時）** | `output.md`（本成果物・制御ブロックを内包した統合1ファイル） | 毎回、タスクフォルダ直下 |
| **B層（条件付き）** | execution_plan / iteration_plan＋sample / quality_review_report / task_retrospective / obsidian_sync_summary | 下記ゲートを満たした時だけ `_internal/` に作成 |
| **C層（要求時）** | work_plan / quality_review_request / execution_summary / questions | セレスが明示要求した時のみ |

## 軽量依頼（A層 output.md 1ファイルのみ、B/C層全スキップ）

以下を**すべて**満たす場合:
- 単一工程で完結
- 顧客提出物でない
- 本番/セキュリティ/破壊的変更を伴わない
- 取り消し可能（リスクが低い）

## 必要性ゲート（B層の作成判定）

| 成果物 | 作成条件 |
|---|---|
| quality_review_report | risk_based_quality_gatesでMedium以上、または顧客提出物/再利用物として追加レビューが必要 |
| task_retrospective | Completed/Accepted かつ 軽量依頼でない |
| execution_plan | 2工程以上で必要能力が変わる or 高リスク/セキュリティ工程。Runtime/Modelは切り替えずEvidenceと非拘束effortを記録 |
| iteration_plan + sample | iteration_confirmation_policy の繰り返し判定に該当 |
| obsidian_sync_summary | obsidian_write_policy のORトリガーを満たし、実際にLocal Second Brainへ書き込んだ |

## フォルダ構造

```
output/<client>/<YYYYMMDD>/<task-name>/
├── output.md                   # A層（常時）—制御ブロック＋本成果物の統合1ファイル
└── _internal/                  # B/C層（条件付き・普段は開かない）
    ├── quality_review_report.md
    └── ...
```

## 本成果物のセクション間引き

- テンプレの見出しは「今回中身がある項目だけ」出力する。該当なしは省略し「該当なし」とも書かない。
- モード別必須核は必ず出す（`professional_response_templates.md` 参照）。
- 本番/破壊的変更 → ロールバックを必須化。認証認可・秘密・個人情報・外部公開 → セキュリティを必須化。
