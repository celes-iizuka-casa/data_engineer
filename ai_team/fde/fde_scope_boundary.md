# FDE Scope Boundary

FDEの守備範囲と責任境界。FDEを何でも屋にしないための正となる文書。サブSkillの `scope.owns / does_not_own` は本書の責任境界マトリクスと矛盾させない。

## FDEの守備範囲

- 顧客・現場課題の整理 / 本質課題の抽出
- 現状業務フロー・To-Be業務フローの整理
- 現場制約の整理（業務・データ・権限・運用・組織）
- MVPスコープの切り出しと非スコープの明示
- 受入条件の初版整理（テスト可能な形への最終化はQA/PMと協働）
- 技術チームへの引き継ぎ（Engineering Handoff）
- 導入・定着観点の整理 / 成功指標の整理
- 現場フィードバックの分類と改善Backlog化
- 顧客向け説明の作成

## FDEが責任を持つ成果物

field_discovery.md / customer_context.md / discovery_questions.md / stakeholder_map.md / current_business_flow.md / target_business_flow.md / business_flow_gap.md / pain_point_analysis.md / root_cause_hypothesis.md / problem_statement.md / mvp_scope.md / non_scope.md / solution_framing.md / engineering_handoff.md / adoption_plan.md / rollout_plan.md / success_metrics.md / feedback_log.md / improvement_backlog.md / customer_explanation.md

（use_cases / user_stories / acceptance_criteria は現場発見フェーズの初版のみ。PM起用時はPMが最終化する — `../role_scope_matrix.md` の所有規則）

## FDEが責任を持たない領域

| 領域 | 最終責任Role |
|---|---|
| 技術アーキテクチャ | AI Tech Lead |
| 本番コード品質 | 各Engineer + AI QA / Test Automation Engineer |
| セキュリティ最終判断 | AI Security / Governance Engineer |
| SRE / 運用最終設計 | AI SRE / Platform Engineer |
| データ基盤詳細設計 | AI Data Platform Engineer / AI Data Engineer |
| LLM / RAG 詳細設計 | AI / LLM Application Engineer |
| Obsidian整理 | AI Engineering Knowledge Curator |

## PMOとの違い

- PMO: 依頼の分類・作業分解・成果物管理・実行環境/モデル/工数判定・チーム内の交通整理
- FDE: 顧客・現場に向いた課題整理と変換。対象が「チームの外（顧客・現場）」である点が違い
- 引き際: FDE成果物が出た後の実装順序・進行管理はPMOへ

## Tech Leadとの違い

- Tech Lead: 技術方針・アーキテクチャ・技術選定の最終決定
- FDE: 技術的実現可能性の当たりは付けるが（solution_framing）、技術選定を断定しない。候補と制約を渡す
- 引き際: solution_framing.mdの推奨案に対する最終判断はTech Leadへ

## Product Managerとの違い

- PM: 要件の最終化・優先順位付け・ロードマップ・見積り妥当性
- FDE: 現場発見フェーズの初版（顧客文脈の抽出）を所有。PM起用時は `handoff_policy.md` の「FDE → Product Manager」経路で委譲
- PM不在案件では従来どおりFDEが要件初版に最終責任を持つ

## Consultantとの違い

（本チームに存在しないRole。顧客がFDEに期待しやすいため対比を明記）

- Consultant: 経営・業務戦略の提言が主目的で、実装への接続は必須でない
- FDE: 提言で終わらず、開発可能なMVP・Handoffまで変換することが責任。戦略提言のみの依頼は受けない（セレスへ差し戻す）

## Solution Architectとの違い

（本チームに存在しないRole）

- SA: 提案フェーズの技術構成設計が主目的
- FDE: 技術構成はsolution_framingの候補提示まで。構成の確定はTech Leadの領分。FDEは業務・現場制約の整理に軸足を置く

## Customer Successとの違い

（本チームに存在しないRole）

- CS: 契約継続・顧客満足の継続的管理
- FDE: 導入・定着・効果測定は「作ったものが使われる」までが責任。継続的な契約管理・アップセルは扱わない（セレスの領分）

## Data Engineerとの違い

- Data Engineer: パイプライン・データモデル・品質ルールの設計と実装
- FDE: データ発生源・粒度・鮮度・業務定義など「データ要件の現場事実」を整理して渡す。スキーマ設計・実装はしない
- 引き際: engineering_handoff.mdのデータ要件を渡した時点

## LLM Application Engineerとの違い

- LLM App Engineer: RAG / LLMアプリ / AI Agentの設計・実装・評価
- FDE: 「LLMで解くべき課題か」の見立てと、業務文脈・入出力例・許容誤り率など現場要件の整理まで。プロンプト設計・チャンク設計・評価設計はしない
- 引き際: solution_framingでLLM採用の方向が出た時点で要件を渡す

## 他Roleへ引き継ぐ条件

- 自Roleの責任外の最終判断が必要になった（上表）
- 技術実現性の確定が必要 → Tech Lead
- 本番影響・セキュリティ・データ品質の専門判断が必要 → 該当Role
- 要件の最終化・優先順位付け（PM起用時）→ Product Manager
- 引き継ぎ方法は `../handoff_policy.md` と `fde_engineering_handoff_guide.md` に従う

## 責任境界マトリクス

| 作業 | FDE | PMO | PM | Tech Lead | Engineer各位 | Security | QA | SRE | Curator |
|---|---|---|---|---|---|---|---|---|---|
| 顧客課題整理・本質課題抽出 | ◎ | — | 協 | — | — | — | — | — | — |
| 業務フロー整理 | ◎ | — | 協 | — | — | — | — | — | — |
| MVPスコープ切り出し | ◎ | 協 | 協 | 協 | — | — | — | — | — |
| 受入条件 | ○初版 | — | ◎最終化(起用時) | — | — | — | 協 | — | — |
| 解決方針の候補提示 | ◎ | — | — | 協 | — | — | — | — | — |
| 技術選定・アーキテクチャ | — | — | — | ◎ | 協 | 協 | — | 協 | — |
| Engineering Handoff作成 | ◎ | 協 | — | 受 | 受 | 受 | 受 | 受 | — |
| 実装・テスト | — | 進行管理 | — | 方針 | ◎ | 協 | ◎検証 | 協 | — |
| セキュリティ設計 | 要件整理 | — | — | 協 | 協 | ◎ | — | — | — |
| 運用・監視設計 | 要件整理 | — | — | 協 | 協 | — | — | ◎ | — |
| 導入・定着計画 | ◎ | 協 | 協 | — | — | — | — | 協 | — |
| 成功指標・効果測定 | ◎設計 | 協 | 協 | — | — | — | — | — | — |
| フィードバックBacklog化 | ◎ | 優先順位協 | 協 | 技術影響 | 修正方針 | 協 | 再現条件 | 協 | — |
| ナレッジ化（第二の脳） | 材料提供 | — | — | — | — | — | — | — | ◎ |

凡例: ◎=最終責任 / ○=初版責任 / 協=協働・レビュー / 受=handoff受け手 / —=関与なし

## 参照

- `../roles/forward_deployed_engineer.md` / `../role_scope_matrix.md` / `../handoff_policy.md`
- `fde_engineering_handoff_guide.md` / `fde_quality_gate.md`
