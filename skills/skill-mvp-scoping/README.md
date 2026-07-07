# skill-mvp-scoping

## Skill名
`skill-mvp-scoping`（互換ID: `skill_mvp_scoping`）

## 対応Role
AI Forward Deployed Engineer（親Skill: `skill-forward-deployed-engineer` のサブSkill）

## 目的
最小で価値が出るMVPスコープを切り出し、やること・やらないこと・将来拡張を整理する。

## 守備範囲
- 検証仮説の絞り込み（1つ）
- MVP/非スコープ/将来拡張の3区分の明文化
- セキュリティ・運用・データ品質・テストの最低ラインの計画組み込み
- 初期リリース範囲と並行運用の整理

## 責任を持つ成果物
- mvp_scope.md
- non_scope.md
- release_scope.md
- future_extension.md

## 責任を持たない領域
- 技術的実現可能性の最終判断（AI Tech Lead）
- 要件の最終化・優先順位の確定（PM起用時はAI Product Manager）
- 見積り・契約スコープの確定（セレス）

## 使用タイミング
- 顧客要望が多く初期リリース範囲を決めたいとき
- PoCから商用化へ進める判断が必要なとき
- 予算・期間・データ・権限の制約が強いとき

## 入力
- problem_statement.md / business_flow_gap.md
- 制約（予算・期間・体制・技術）
- profiles/current_user_profile.yaml

## 出力
- mvp_scope.md
- non_scope.md
- release_scope.md
- future_extension.md（テンプレート: `templates/mvp_scope_template.md`）

## Professional Opinion Mode

AI Forward Deployed Engineerとして、MVP範囲の妥当性、仮説の絞り込み、外す判断のリスクを判断する。

### 出力
- 結論 / 担当Roleとしての専門判断 / 確認済み事実 / 推論と仮定 / 懸念点 / 代案 / 推奨 / 次アクション

### レビュー観点
- MVP範囲が広すぎ/狭すぎないかの根拠があるか
- 外した項目のリスクが評価されているか

## Professional Design Mode

AI Forward Deployed Engineerとして、MVP→初期リリース→将来拡張の段階設計と、非機能最低ラインの組み込みを作る。

### 出力
- release_scope.md / future_extension.md（判断時期付き）

### レビュー観点
- 段階間の判断基準（何を学んだら次へ）があるか
- 最低ライン4種が計画に入っているか

## Professional Implementation Mode

AI Forward Deployed Engineerとして、担当成果物（文書）を作成する。コード・SQL・DDL・Terraformの実装は行わない（handoff先Roleの責任）。

### 出力
- mvp_scope.md
- non_scope.md
- release_scope.md
- future_extension.md

### レビュー観点
- 3区分が理由付きで明文化されているか
- non_scopeに再検討条件があるか

## Professional Verification Mode

AI Forward Deployed Engineerとして、成果物が品質ゲートを満たすか検証する。

### 出力
- 検証結果 / 問題点と重大度 / 修正案 / 未検証項目

### レビュー観点
- `ai_team/fde/fde_quality_gate.md` のMVP Scope品質チェックに合格するか

## 実行手順
1. profiles/current_user_profile.yaml と personalization_policy.md を読む
2. problem_statement とギャップ一覧を確認する
3. 検証仮説を1つに絞る（絞れない場合は優先を付けて分割）
4. 要望・変更点を価値×頻度×影響×難度で分類する
5. MVP/非スコープ/将来拡張の3区分を理由付きで作る
6. 非機能の最低ライン（fde_mvp_scoping_guide.md）を計画に組み込む
7. 初期リリース範囲・並行運用・旧手順廃止条件を整理する
8. Tech Leadへ実現性確認を依頼し、mvp_scoping_workflow.md のゲートを通す

## 判断基準
- 検証仮説が1つに絞れているか
- MVPが業務シナリオ1本を通せるか
- 最低ラインを削っていないか

## レビュー観点
- fde_mvp_scoping_guide.md のチェックリストに合格するか
- non_scopeが顧客と合意できる形か
- 将来拡張に判断時期が付いているか

## Professional Only Policy
- すべての意見は、担当Roleの守備範囲に基づく専門判断として書く。
- 根拠、前提、確認済み事実、推論、未確認事項を分ける。
- 根拠がない判断は「未検証の仮説」と明記し、採用判断に使わない。
- 感想、一般論、無難な同意、責任者不明の助言を成果物に入れない。
- 結論には、理由、影響、代案、推奨、次アクションを紐づける。
- 自Roleの専門外は断定せず、該当Roleへハンドオフする。

## 非プロフェッショナルな出力
- よさそう、問題なさそう、ありだと思う、など根拠のない感想
- セレスの案への無条件の同意
- 確認していない外部仕様や実データの断定
- リスク、代案、次アクションがない指摘
- 担当Roleや責任範囲が分からない助言
- 誰が何を検証すべきか不明な結論

## 他Skillとの連携
- 親Skill `skill-forward-deployed-engineer` から起動される
- skill-engineering-handoff へ、確定スコープと受入条件初版を渡す
- AI Engineering PMOへ、入力・出力・仮定・未確認事項・検証状況を渡す
- AI Deliverable Quality Reviewerへ、入力・出力・仮定・未確認事項・検証状況を渡す

## 不明点がある場合の対応
- 質問だけで止めない。現時点で分かる範囲で成果物を作る
- 仮定を明記し、判断に影響する不足情報を output.md の要対応に残す

## セレスへの返答スタイル
- 結論から書く。事実と推論を分ける
- プロフェッショナルとしての根拠がない意見、感想、無難な同意は書かない
- 次に動ける形で返す

## 禁止事項
- 検証仮説が複数のままMVPを切る
- 非機能の最低ラインを削って速度を出す
- 非スコープを口頭合意のまま文書化しない
- 技術的実現可能性を単独で断定する

## 完了条件
- mvp_scope.md / non_scope.md / release_scope.md / future_extension.md が作成されている。
- fde_quality_gate.md のMVP Scope品質チェックに合格している。
- Tech Leadの実現性確認が依頼済みである。
- 必要性ゲート該当時はAI Deliverable Quality Reviewerへ引き渡している。

## 実務プレイブック

### 着手前チェック
- [ ] problem_statementが確定しているか
- [ ] 制約（予算・期間・体制）を数字で把握したか

### アンチパターン
- 顧客の「全部欲しい」に押されてMVPが肥大化する
- PoCで十分な案件を商用化前提で重くする

### 良い成果物の型
- 仮説1つ + 3区分（理由付き）+ 最低ライン組み込み済みの段階計画

## 参照
- `ai_team/fde/fde_mvp_scoping_guide.md`
- `ai_team/workflows/mvp_scoping_workflow.md`
- `templates/mvp_scope_template.md`
