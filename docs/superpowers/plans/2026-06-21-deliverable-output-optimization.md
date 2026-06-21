# 提出物の出力最適化 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** AIエンジニアチームの1依頼あたりの提出物を「結論サマリー＋選ばれたRoleの本成果物」の2点を基本にし、それ以外は必要性ゲートを満たした時だけ生成するよう、ポリシー/ワークフロー/テンプレート群を書き換える。

**Architecture:** 成果物を3階層（A=常時 / B=条件付き / C=要求時）に分類し、B/C層は `output/.../_internal/` に隔離する。新規ポリシー `output_optimization_policy.md` を単一の正本とし、既存の「毎回作る」記述（AGENTS.md・input_to_output_workflow.md ほか）をこの正本のゲート参照に置き換える。本成果物テンプレートは「関連セクションのみ＋モード別必須核＋条件付き必須」で間引く。

**Tech Stack:** Markdown のみ（`ai_team/`, `templates/`, `AGENTS.md`）。コード変更・自動テストなし。検証は grep と代表依頼2件のドライランで行う。

**設計の正本:** `docs/superpowers/specs/2026-06-21-deliverable-output-optimization-design.md`

---

## File Structure

新規作成:
- `ai_team/output_optimization_policy.md` — 本最適化の単一の正本（3階層・必要性ゲート・軽量依頼定義・セクション間引き・入力タグ）
- `templates/deliverable_summary_template.md` — 結論サマリーの固定フォーマット

修正:
- `ai_team/workflows/input_to_output_workflow.md` — 各ステップのゲート化、deliverable_summaryを常時化、execution_summaryをC層へ降格、成果物リスト/品質ゲート更新
- `AGENTS.md` — Required Start/Finish をゲート参照に、出力モデルと「関連セクションのみ」を明記
- `ai_team/professional_response_templates.md` — モード別の必須核＋条件付き必須を追記
- `ai_team/model_selection_policy.md` — 「作る条件」と軽量依頼スキップを明記
- `ai_team/retrospective_policy.md` — 「作る条件」と軽量依頼スキップを明記
- `ai_team/README.md` — 新ポリシーへの参照追加

---

## Task 0: フィーチャーブランチを作成

現在 `main` ブランチ直上のため、作業ブランチを切る。

- [ ] **Step 1: ブランチ作成**

Run:
```bash
cd /Users/celesiizuka/Celestian/CASA/data_engineer
git checkout -b feature/deliverable-output-optimization
```
Expected: `Switched to a new branch 'feature/deliverable-output-optimization'`

- [ ] **Step 2: 起点が clean か確認**

Run: `git status`
Expected: 既存の未コミット spec/plan 以外に作業ツリーの変更がないこと（spec/plan は本タスク群で一緒に commit する）

---

## Task 1: 正本ポリシー `output_optimization_policy.md` を作成

**Files:**
- Create: `ai_team/output_optimization_policy.md`

- [ ] **Step 1: ファイルを作成（全文を書き込む）**

ファイル内容（フォルダ構造図は実ファイルでは通常の3連バッククォートのコードフェンスにする）:

~~~md
# Output Optimization Policy

## 目的

1依頼あたりの提出物を「セレスが読むべき最小限」に絞る。デフォルトは結論サマリーと選ばれたRoleの本成果物の2点。それ以外は必要性ゲートを満たした時だけ生成する。ガバナンス（独立品質レビュー・自己レビュー禁止・反復作業ゲート）の判定そのものは維持し、出力の有無だけを条件化する。

## 出力3階層

| 階層 | 中身 | 生成条件 |
|---|---|---|
| A. 常に渡す | `deliverable_summary.md` ＋ 選ばれたRoleの本成果物 | 毎回 |
| B. 条件付き | model_recommendation / iteration_plan＋sample / quality_review_report / task_retrospective / obsidian_sync_summary | 下記ゲートを満たした時だけ |
| C. 要求時のみ | work_plan / quality_review_request / execution_summary（10項目詳細）/ questions（全文） | セレスが明示要求した時、または内部参照用 |

## フォルダ構造

```
output/<client>/<YYYYMMDD>/<task-name>/
├── deliverable_summary.md      # まずこれだけ読めばいい（常時）
├── <deliverable>.md            # Roleの本成果物・関連セクションのみ（常時）
└── _internal/                  # B/C層。普段は開かない
    ├── quality_review_report.md
    ├── model_recommendation.md
    └── ...
```

A層の2ファイルはタスクフォルダ直下に置く。B/C層は必ず `_internal/` 配下に置く。

## 必要性ゲート

| 成果物 | 作る条件（満たした時だけ） | 満たさない時 |
|---|---|---|
| deliverable_summary | 常に | — |
| Roleの本成果物 | 常に | — |
| work_plan | 3工程以上 or 明示的な除外スコープが要る依頼 | 作らない（サマリーの次アクションで代替） |
| model_recommendation | 2工程以上で必要能力が変わる or 高リスク/セキュリティ工程を含む | 作らない |
| iteration_plan + sample | `iteration_confirmation_policy` の繰り返し判定に該当 | 作らない |
| quality_review_report | Design/Implementation/Verification で「顧客提出物・再利用物・本番/破壊的/セキュリティ影響」のいずれか | 作らない＝サマリーに「レビュー対象外」と明記 |
| questions（独立ファイル） | 未確認事項が実在する場合のみ | 作らない（空ファイルを作らない。少数ならサマリー「要対応」に直書き） |
| task_retrospective | `Completed/Accepted` かつ軽量依頼でない | 作らない |
| obsidian_sync_summary | `obsidian_write_policy` のトリガー かつ 顧客/再利用価値あり | 作らない |
| execution_summary（10項目詳細） | セレスが明示要求 or 大型案件で詳細記録が要る時 | 作らない（サマリーで代替） |

## 軽量依頼の定義

以下をすべて満たす依頼は「軽量依頼」とし、A層の2ファイルだけを出す（B/C層は原則全スキップ）:

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
- `@light` … 強制的に軽量（2ファイルのみ）
- `@full` … 全成果物を出させる

## 参照

- `ai_team/workflows/input_to_output_workflow.md`
- `templates/deliverable_summary_template.md`
- `ai_team/professional_response_templates.md`
- `ai_team/iteration_confirmation_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/model_selection_policy.md`
~~~

- [ ] **Step 2: 作成を検証**

Run: `grep -c "必要性ゲート\|軽量依頼\|_internal/" ai_team/output_optimization_policy.md`
Expected: 1以上（各語が存在する）

- [ ] **Step 3: Commit**

```bash
git add ai_team/output_optimization_policy.md docs/superpowers/specs/2026-06-21-deliverable-output-optimization-design.md docs/superpowers/plans/2026-06-21-deliverable-output-optimization.md
git commit -m "feat(ai_team): add output optimization policy (3-tier + necessity gate)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: 結論サマリーテンプレート `deliverable_summary_template.md` を作成

**Files:**
- Create: `templates/deliverable_summary_template.md`

- [ ] **Step 1: ファイルを作成（全文）**

~~~md
# <タスク名> — 結論サマリー

- 依頼の理解: <1〜2行。チームが何を頼まれたと解釈したか。読み違い検知用>
- 担当: <選ばれたRole> / モード: <Opinion|Design|Implementation|Verification>
- 結論: <数行。一番言いたいこと>
- 品質判定: <PASS | PASS_WITH_CONDITIONS | REWORK_REQUIRED | BLOCKED | レビュー対象外>
- 要対応（セレスへ）: <ブロッキング質問・承認待ち・判断が要る点。無ければ「なし」>
- 次アクション: <チーム側 / セレス側>
- 本成果物: ./<deliverable>.md
- 参考(必要時): ./_internal/...
~~~

- [ ] **Step 2: 作成を検証**

Run: `grep -c "要対応\|品質判定\|依頼の理解" templates/deliverable_summary_template.md`
Expected: 3（各行が存在する）

- [ ] **Step 3: Commit**

```bash
git add templates/deliverable_summary_template.md
git commit -m "feat(templates): add deliverable_summary template (control-panel summary)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: `input_to_output_workflow.md` をゲート化

**Files:**
- Modify: `ai_team/workflows/input_to_output_workflow.md`

このファイルが「毎回12ファイル生成」の主因。ステップをゲート参照に書き換える。

- [ ] **Step 1: 手順セクションを置換**

`## 手順` 配下の現行 1〜15 を、以下に置き換える:

~~~md
## 手順

1. **input確認**: 入力ファイル、既存output、制約を確認する。
2. **依頼内容解析**: `request_mode_policy.md` に従い Opinion / Design / Implementation / Verification を判定する。背景・意図・制約、`@role`/`@mode`/`@light`/`@full` タグ（`output_optimization_policy.md`）を解析する。
3. **軽量依頼か判定**: `output_optimization_policy.md` の軽量依頼定義に照らす。軽量なら A層の2ファイルのみを目標にし、B/C層は原則スキップする。
4. **Role選定**: `role_scope_matrix.md` に従い担当Roleと連携Roleを選ぶ。
5. **（条件付き）work_plan**: 3工程以上 or 明示的除外スコープが要る場合のみ `output/.../_internal/work_plan.md` を作る。
6. **（条件付き）model_recommendation**: 必要性ゲートを満たす場合のみ `output/.../_internal/model_recommendation.md` を作る（`templates/model_selection_template.md`）。
7. **（条件付き）繰り返し作業**: `iteration_confirmation_policy.md` に該当する場合のみ代表例を先に作り、`_internal/iteration_plan.md` と `_internal/sample_output_for_review.md` を作る。ステータス `Waiting for Celes Review`。承認後 `Expanding` で全件展開。
8. **実装・設計・検証**: 担当RoleがProfessional Modeに応じた本成果物を作る。`professional_only_policy.md` と `output_optimization_policy.md` のセクション間引き（関連セクションのみ＋必須核＋条件付き必須）に従う。責任外は `handoff_policy.md` で渡す。
9. **（条件付き）品質レビュー**: 必要性ゲート（顧客提出物・再利用物・本番/破壊的/セキュリティ影響）を満たす場合のみ、Quality Reviewerが `_internal/quality_review_report.md` を作る。満たさない場合はサマリーの品質判定を「レビュー対象外」にする。自己レビューを独立レビュー扱いにしない。
10. **deliverable_summary作成（常時）**: `templates/deliverable_summary_template.md` で `output/.../deliverable_summary.md` を作る。品質判定・要対応・次アクションを集約する。ステータスを `Completed` にする。
11. **（条件付き）task_retrospective**: `Completed/Accepted` かつ軽量依頼でない場合のみ `_internal/task_retrospective.md` を作る（`retrospective_policy.md`）。
12. **（条件付き）feedback_analysis**: セレスのフィードバックがある場合のみ `_internal/feedback_analysis.md` を作る（`feedback_optimization_policy.md`）。
13. **（条件付き）Obsidian整理**: `obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理し、`_internal/obsidian_sync_summary.md` を作る。ステータス `Obsidian Synced`。
14. **（要求時のみ）execution_summary**: セレスが明示要求 or 大型案件の場合のみ `_internal/execution_summary.md`（10項目）を作る。
~~~

- [ ] **Step 2: 成果物リストを置換**

`## 成果物` 配下を以下に置き換える:

~~~md
## 成果物

常時（タスクフォルダ直下）:
- `output/.../deliverable_summary.md`
- Professional Mode別の本成果物

条件付き / 要求時（`output/.../_internal/` 配下）:
- `work_plan.md` / `model_recommendation.md` / `iteration_plan.md` ＋ `sample_output_for_review.md`
- `quality_review_request.md` / `quality_review_report.md`
- `task_retrospective.md` / `feedback_analysis.md` / `team_improvement_proposal.md`
- `obsidian_sync_summary.md` / `execution_summary.md` / `questions.md`
~~~

- [ ] **Step 3: 品質ゲートに構造チェックを追加**

`## 品質ゲート` の末尾に以下の行を追加する:

~~~md
- 軽量依頼では A層の2ファイル（deliverable_summary＋本成果物）のみが出力されている。
- B/C層の成果物は必要性ゲートを満たしたものだけが `_internal/` 配下に置かれている。
- 本成果物に該当なしの見出しが残っていない（必須核と条件付き必須は除く）。
- サマリーの「要対応」に、ブロッキング質問・承認待ち・要判断が集約されている。
~~~

- [ ] **Step 4: 参照に新ポリシーを追加**

`## 参照` の先頭に `- ai_team/output_optimization_policy.md` を（バッククォート付きで）追加する。

- [ ] **Step 5: 検証**

Run: `grep -c "_internal/\|deliverable_summary\|output_optimization_policy" ai_team/workflows/input_to_output_workflow.md`
Expected: 3以上

- [ ] **Step 6: Commit**

```bash
git add ai_team/workflows/input_to_output_workflow.md
git commit -m "refactor(ai_team): gate workflow steps, summary-first output

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: `AGENTS.md` の Required Start/Finish をゲート参照に

**Files:**
- Modify: `AGENTS.md`

- [ ] **Step 1: Required Start を置換**

現行 `## Required Start` 配下を以下に置き換える:

~~~md
## Required Start
1. `input/` と既存 `output/` を確認する。
2. 明示成果物、課題分類、MVP、制約、リスク、`@role`/`@mode`/`@light`/`@full` タグを整理する。
3. `output_optimization_policy.md` の軽量依頼判定を行う。軽量でなく3工程以上なら `_internal/work_plan.md` を作る（軽量なら作らない）。
4. 必要な `skills/` を選び、作業を進める。
~~~

- [ ] **Step 2: Required Finish を置換**

現行 `## Required Finish` 配下を以下に置き換える:

~~~md
## Required Finish
- 成果物は `output/<client>/<YYYYMMDD>/<task-name>/` に保存する。常時はタスクフォルダ直下に `deliverable_summary.md` と本成果物の2点。条件付き/要求時の成果物は `_internal/` 配下に置く（`output_optimization_policy.md`）。
- 顧客名や日付が特定できない場合だけ、合理的な仮名を置いて前提を明記する。
- 本成果物は「関連セクションのみ＋モード別必須核＋条件付き必須」で作る（`professional_response_templates.md`）。
- 品質レビューは必要性ゲートを満たす場合に実施する。満たさない場合はサマリーの品質判定を「レビュー対象外」にする。満たす場合は `templates/quality_review_request_template.md` で提出し、Reviewerが `_internal/quality_review_report.md` を作る。
- 最終判定が `REWORK_REQUIRED` または `BLOCKED` の場合、完了扱いにせず、再作業内容または停止理由をサマリーの「要対応」に書く。
- 顧客案件または再利用価値のある成果物は、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が第二の脳へ反映し、`_internal/obsidian_sync_summary.md` を更新する。
- `deliverable_summary.md` を常時作成する。`execution_summary` と `questions` の独立ファイルは必要性ゲートを満たす時だけ作る。
- 実行したテスト、未実行テスト、残存リスクをサマリーまたは本成果物に明記する。
~~~

- [ ] **Step 3: Writing Style に間引きルールを1行追記**

`## Writing Style` の箇条書き末尾に追加:

~~~md
- 本成果物は該当する見出しだけ出す。該当なしの見出しは省略する（必須核・条件付き必須は除く）。
~~~

- [ ] **Step 4: 検証**

Run: `grep -c "deliverable_summary\|_internal/\|output_optimization_policy\|関連セクション" AGENTS.md`
Expected: 3以上

- [ ] **Step 5: Commit**

```bash
git add AGENTS.md
git commit -m "refactor(agents): gate-based required start/finish, summary-first

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: `professional_response_templates.md` に必須核と間引きルールを追記

**Files:**
- Modify: `ai_team/professional_response_templates.md`

- [ ] **Step 1: 冒頭にルールブロックを追加**

ファイル先頭 `# Professional Response Templates` の直後に挿入:

~~~md
## 適用ルール（output_optimization_policy 準拠）

- 各モードの見出しは「今回中身がある項目だけ」出す。該当なしの見出しは省略する。
- ただしモード別の必須核は必ず出す（下表）。
- 条件付き必須: 本番/破壊的変更ならロールバックを、認証認可・秘密・個人情報・外部公開を伴うならセキュリティを、必須核に昇格させ省略しない。

| モード | 必須核 |
|---|---|
| Opinion | 結論 / 推奨 / 次アクション |
| Design | 設計概要 / 推奨アーキテクチャ / リスク / 完了条件 |
| Implementation | 実装方針 / 作成・修正ファイル / 検証手順 |
| Verification | 検証対象 / 検証結果 / 推奨アクション |
~~~

- [ ] **Step 2: 検証**

Run: `grep -c "必須核\|条件付き必須\|該当なしの見出しは省略" ai_team/professional_response_templates.md`
Expected: 2以上

- [ ] **Step 3: Commit**

```bash
git add ai_team/professional_response_templates.md
git commit -m "feat(ai_team): add section-trimming + mandatory-core rules to response templates

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: `model_selection_policy.md` と `retrospective_policy.md` の作る条件を明文化

**Files:**
- Modify: `ai_team/model_selection_policy.md`
- Modify: `ai_team/retrospective_policy.md`

- [ ] **Step 1: model_selection_policy の出力形式を置換**

`## 出力形式` 配下を以下に置き換える:

~~~md
## 出力形式

`output_optimization_policy.md` の必要性ゲートに従う。2工程以上で必要能力が変わる、または高リスク/セキュリティ工程を含む場合のみ `output/.../_internal/model_recommendation.md` を作る（`../templates/model_selection_template.md`）。単一工程の軽量依頼では作らない。
~~~

- [ ] **Step 2: retrospective_policy の実行タイミングに軽量依頼スキップを追記**

`## 実行タイミング` の箇条書き末尾に追加:

~~~md
- ただし `output_optimization_policy.md` の軽量依頼に該当する場合は作成しない。
~~~

`## 作成する成果物` のパスを `output/.../_internal/task_retrospective.md` に更新する。

- [ ] **Step 3: 検証**

Run: `grep -c "output_optimization_policy\|軽量依頼" ai_team/model_selection_policy.md ai_team/retrospective_policy.md`
Expected: 各ファイルで1以上

- [ ] **Step 4: Commit**

```bash
git add ai_team/model_selection_policy.md ai_team/retrospective_policy.md
git commit -m "refactor(ai_team): make model/retrospective output conditional on necessity gate

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: `ai_team/README.md` に新ポリシー参照を追加

**Files:**
- Modify: `ai_team/README.md`

- [ ] **Step 1: 参照リストに追加**

`## 参照` の `model_selection_policy.md` の行の直後に、バッククォート付きで追加:

~~~md
- `output_optimization_policy.md`
~~~

- [ ] **Step 2: 検証**

Run: `grep -c "output_optimization_policy" ai_team/README.md`
Expected: 1

- [ ] **Step 3: Commit**

```bash
git add ai_team/README.md
git commit -m "docs(ai_team): reference output optimization policy in README

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: 代表依頼2件のドライラン検証

自動テストはないため、ポリシーが意図通り効くかを2件のシナリオで机上確認する。

- [ ] **Step 1: 軽量依頼シナリオを検証**

シナリオ: 「この関数の命名どう思う？」のような単一工程・非顧客・低リスク依頼。
期待: 軽量依頼定義4項目すべてに該当 → 出力は `deliverable_summary.md` ＋ 本成果物（Opinion、必須核=結論/推奨/次アクション）の2ファイルのみ。`_internal/` は作られない。
確認: `ai_team/output_optimization_policy.md` と `ai_team/workflows/input_to_output_workflow.md` を読み、この依頼で B/C層がすべてスキップされる導線になっているか目視確認する。

- [ ] **Step 2: 重量依頼シナリオを検証**

シナリオ: 「本番DBのスキーマ移行を設計して」のような顧客/本番/破壊的依頼。
期待: 軽量依頼に非該当 → quality_review_report（顧客/本番影響でゲート通過）、必要なら model_recommendation/work_plan が `_internal/` に生成。本成果物（Design）はロールバックとセキュリティが条件付き必須で省略不可。サマリーの「品質判定」と「要対応」に判定とブロッカーが集約される。
確認: 同2ファイルを読み、上記が導かれるか目視確認する。

- [ ] **Step 3: 旧パス参照が残っていないか確認**

Run: `grep -rn "execution_summary.md\|quality_review_report.md\|work_plan.md" ai_team/ AGENTS.md | grep -v "_internal/"`
Expected: `_internal/` を伴わない旧パス参照が残っていないこと（残っていれば修正）。

- [ ] **Step 4: 最終 Commit（修正があれば）**

```bash
git add -A
git commit -m "docs(ai_team): fix stale deliverable path references after gating

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Self-Review（作成者チェック結果）

- **Spec coverage:** 3階層=Task1, サマリー=Task2, ゲート化workflow=Task3, AGENTS=Task4, セクション間引き=Task5, model/retrospective条件化=Task6, README=Task7, 検証=Task8。spec全節をカバー。
- **Placeholder scan:** 各タスクに実ファイル全文または確定した置換テキストを記載。TBD/TODOなし。
- **整合性:** ファイルパス・`_internal/` 配置・タグ名（`@role/@mode/@light/@full`）・必須核の語をタスク間で統一。
- **既知の注意:** Task1 のフォルダ構造図は、プラン内では `~~~` フェンスでくるんでいる。実ファイルでは通常の ``` フェンスで書く。
~~~~