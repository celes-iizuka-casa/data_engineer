# Field Discovery to Solution Workflow

## 目的
顧客・現場の曖昧な相談を、実装可能な課題、MVPスコープ、技術チームへの引き継ぎへ変換する。

## 開始条件
- 顧客相談、ヒアリングメモ、議事録がinputにある
- 要件が曖昧で、何を作るべきかが未確定
- 業務フロー、現場制約、利用者が整理されていない
- 顧客向け説明やMVP提案が必要

## 主担当
- AI Engineering PMO
- AI Forward Deployed Engineer
- AI Tech Lead
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer
- AI Deliverable Quality Reviewer

## 手順
1. PMOが入力、明示要求、既存output、制約を棚卸しする
2. AI FDEが顧客・現場背景、関係者、利用シーンを整理する
3. 表面的な要望、本質課題、現場制約、未決事項を分ける
4. 現状業務フローとあるべき業務フローを整理する
5. MVPスコープ、対象外、成功条件、受入条件を定義する
6. Tech Leadが技術的な実現可能性、代替案、主要リスクを確認する
7. 専門エンジニアへengineering_handoff.mdを渡す
8. QA、Security、SREの該当観点を早期に確認する
9. Quality Reviewerへレビュー依頼と証跡を提出する

## 品質ゲート
- 顧客課題と解決策が対応している
- 利用者、意思決定者、運用者が分離されている
- 現場制約と技術制約が区別されている
- MVPでやること、やらないこと、将来拡張が明確
- 受入条件、成功指標、未決事項がある
- 後続エンジニアが実装判断できる粒度になっている

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- field_discovery.md
- customer_context.md
- stakeholder_map.md
- mvp_scope.md
- engineering_handoff.md
- adoption_plan.md
- success_metrics.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。
