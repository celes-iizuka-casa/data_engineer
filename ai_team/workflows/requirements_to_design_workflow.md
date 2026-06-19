# Requirements to Design Workflow

## 目的
要求を、受入可能で実装可能な基本設計へ落とす。

## 開始条件
- 新規機能・システムの要件がある
- 要件と実装の解釈差が大きい

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
