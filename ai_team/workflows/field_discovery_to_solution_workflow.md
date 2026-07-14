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
- AI Forward Deployed Engineer（親Skill + サブSkill 10本）
- AI Tech Lead
- AI Security / Governance Engineer
- AI QA / Test Automation Engineer
- AI Deliverable Quality Reviewer
- AI Engineering Knowledge Curator（現在利用者の明示依頼、またはAccepted + 再利用価値 + Local root確認後）

## 手順
1. PMOが入力、明示要求、既存output、制約を棚卸しする
2. `../personalization_policy.md` に従い、利用可能な現在利用者のLocal profile / Second Brainだけを任意参照する
3. 依頼内容を解析し、FDE起動条件（`../fde/fde_operating_model.md`）で要否を判定する
4. AI FDEが skill-field-discovery / skill-stakeholder-mapping で顧客・現場背景、関係者、利用シーンを整理する
5. skill-pain-point-analysis で表面的な要望、本質課題、現場制約、未決事項を分ける
6. skill-business-flow-mapping で現状業務フローとあるべき業務フロー・ギャップを整理する
7. skill-mvp-scoping でMVPスコープ、対象外、成功条件、受入条件を定義する
8. skill-solution-framing で解決方針候補を整理し、Tech Leadが技術的な実現可能性、代替案、主要リスクを確認する
9. skill-engineering-handoff でRole別依頼を含む engineering_handoff.md を作成し、同じ呼び出し元Runtime内の専門Roleへ渡す。別Runtimeが必要な場合は自動切替せずhandoff候補として記録する
10. QA、Security、SREの該当観点を早期に確認する
11. 実装・設計・検証へ進む（`requirements_to_design_workflow.md` / `design_to_implementation_workflow.md`）
12. skill-adoption-planning / skill-success-metrics-design で導入・定着・効果測定を整理する
13. skill-feedback-to-backlog で現場フィードバックの回収とBacklog化の仕組みを作る（`../fde/fde_feedback_loop.md`）
14. Quality Reviewerへレビュー依頼と証跡を提出する（`../fde/fde_quality_gate.md` を併用）
15. 現在利用者の明示依頼、またはAccepted + 再利用価値 + Local root確認後だけ、Knowledge CuratorがLocal Second Brainへ整理する（`../obsidian_write_policy.md`）

## 品質ゲート
- 顧客課題と解決策が対応している
- 利用者、意思決定者、運用者が分離されている
- 現場制約と技術制約が区別されている
- MVPでやること、やらないこと、将来拡張が明確
- 受入条件、成功指標、未決事項がある
- 後続エンジニアが実装判断できる粒度になっている
- `../fde/fde_quality_gate.md` の該当成果物チェックに合格している
- Personalization（利用者タイプ別の出し分け）が反映されている

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- field_discovery.md / customer_context.md / discovery_questions.md
- stakeholder_map.md
- pain_point_analysis.md / problem_statement.md
- current_business_flow.md / target_business_flow.md / business_flow_gap.md
- mvp_scope.md / non_scope.md
- solution_framing.md
- engineering_handoff.md
- adoption_plan.md / success_metrics.md
- feedback_log.md（回収の仕組み）

テンプレートは `../../templates/fde/fde_template_index.md` を正とする。

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。
- FDE→各Roleの経路別詳細は `../fde/fde_engineering_handoff_guide.md` と `../handoff_policy.md` に従う。

## 参照

- `../fde/fde_operating_model.md`（起動条件・基本フロー）
- `../fde/fde_quality_gate.md`
- `../personalization_policy.md`
- `../runtime_selection_policy.md`（呼び出し元Runtime従属）
- `../model_effort_selection_policy.md`（現在Runtime内の非拘束effort推奨）
