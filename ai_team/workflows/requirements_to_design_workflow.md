# Requirements to Design Workflow

## 目的
要求を、受入可能で実装可能な基本設計へ落とす。

## 開始条件
- 新規機能・システムの要件がある
- 要件と実装の解釈差が大きい
- FDEの engineering_handoff.md がある（この場合は本質課題・受入条件・現場制約・非スコープを入力として引き継ぎ、矛盾させない）

## 主担当
- AI Engineering PMO
- AI Tech Lead
- AI Fullstack Engineer
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer

## 手順
1. 目的、利用者、業務価値、対象外を定義する
2. 機能要件、非機能要件、データ要件を分ける
3. 受入条件と優先度を決める
4. アーキテクチャ、責任境界、データフローを設計する
5. 代替案と主要リスクを比較する
6. Security・QA・SRE観点を設計へ反映する

## 品質ゲート
- 要件IDと受入条件
- MVPと将来範囲の分離
- 性能・可用性・権限の数値化
- 実装担当が見積可能な粒度

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- requirements.md
- basic_design.md
- architecture.md
- non_functional_requirements.md
- test_plan.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: 要件・設計ドキュメントが3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **能力・effort提案**: 依頼解析・方針策定・設計で必要な能力を `model_selection_policy.md` に従い非拘束で記録する。呼び出し元の現在Modelは変更しない
- **振り返り**: 設計完了後に `retrospective_policy.md` に従い `output/.../_internal/task_retrospective.md` を作成する
- **第二の脳整理**: 設計成果物が承認されたとき、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
