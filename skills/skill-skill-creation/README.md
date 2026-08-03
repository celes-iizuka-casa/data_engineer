# skill-skill-creation

## Skill名
`skill-skill-creation`（互換ID: `skill_skill_creation`）

## 対応Role
AI Capability Architect

## 目的
新Roleを追加するほどではないが、既存Roleに能力を追加する必要がある場合に、新Skillを追加する。

## 守備範囲
- Skill Gap確定後の新Skill設計と作成（README / skill.yaml / SKILL.md / agents/openai.yaml 一式）
- 既存Skill更新で足りるかの最終確認（足りるなら新Skillを作らない）
- `skills/index.yaml`・`skill_lifecycle_registry.yaml`・`skill_eval_bindings.yaml` への登録内容の作成
- new_skill_creation_report.md の作成
- 対象Roleとの紐付け（role_skill_map更新内容の作成）

## 責任を持つ成果物
- `skills/skill-<capability>/` 一式
- new_skill_creation_report.md

## 責任を持たない領域
- Gap判定そのもの（skill-capability-gap-analysisへ）
- 新Role追加（skill-agent-creationへ）
- Registry / Matrix / Map viewの反映実務（skill-agent-registry-managementへ）
- 追加Skillを使った実務成果物の品質
- 最終品質判定とCelesの承認判断

## 使用タイミング
- capability_gap_analysisでSkill Gapが確定したとき
- 既存Roleの責務内だが、手順・成果物・判断基準が既存Skillに不足しているとき
- 再利用性と成果物テンプレートが定義できるとき

## 入力
- capability_gap_analysis.md（Skill Gap根拠）
- `ai_team/skill_creation_policy.md`
- 対象Roleの定義と既存Skill
- `templates/agent_creation/new_skill_definition_template.md`

## 出力
- `skills/skill-<capability>/` 一式
- new_skill_creation_report.md

## Professional Opinion Mode

AI Capability Architectとして、新Skill追加の要否・代案（既存Skill更新等）・リスクを判断する。

### 出力
- 結論
- 担当Roleとしての専門判断
- 確認済み事実
- 既存Skill更新で足りない理由
- 代案
- 推奨
- 採用条件
- 次アクション

### レビュー観点
- 担当Roleの守備範囲に基づく意見か
- 根拠、事実、推論、未確認事項が分かれているか
- 無根拠な同意や感想がないか
- 既存Skill・README更新・テンプレート更新の代案が検討されているか
- 再利用性の根拠があるか

## Professional Design Mode

AI Capability Architectとして、新Skillの目的・手順・成果物・判断基準・連携を設計する。

### 出力
- 設計概要
- 前提・仮定
- 対象Roleと目的
- 守備範囲と責任外
- 実行手順と判断基準
- 成果物とテンプレート
- 他Skillとの連携と重複回避
- Quality Gate
- リスク

### レビュー観点
- MVPと商用化のバランスがあるか
- 運用・監視・セキュリティ・テストを後回しにしていないか
- 既存Skillとの重複・競合が説明されているか
- 成果物テンプレートと完了条件が定義されているか

## Professional Implementation Mode

AI Capability Architectとして、新Skill一式と登録内容を契約準拠で作成する。

### 出力
- `skills/skill-<capability>/` 一式（README / skill.yaml / SKILL.md / agents/openai.yaml）
- `skills/index.yaml`・ライフサイクル登録簿・eval bindingsへの登録内容
- new_skill_creation_report.md

### レビュー観点
- 動くだけでなく保守・再実行・エラー処理まで見ているか
- 既存構成を壊していないか
- validator契約（24見出し・20キー・登録簿整合）を満たしているか
- 追加理由と判断ログが残っているか

## Professional Verification Mode

AI Capability Architectとして、新Skill一式が契約・重複回避・ゲートを満たすか検証する。

### 出力
- 検証対象
- 検証観点
- 検証手順
- 検証結果
- 問題点
- 重大度
- 修正案
- 未検証項目

### レビュー観点
- 検証したものと未検証のものが分かれているか
- 問題に重大度と修正案があるか
- 再検証手順があるか
- 既存Skillとの競合が検証されているか

## 実行手順
1. capability_gap_analysis のSkill Gap根拠を確認する
2. `skill_creation_policy.md` の追加条件（責務内・不足・再利用性・評価可能）を照合する
3. 既存Skill更新・テンプレート更新で足りないことを確認する（足りるなら追加しない）
4. 新Skill一式を契約準拠で作成する
5. `skills/index.yaml`・ライフサイクル登録簿・eval bindingsへの登録内容を作成する
6. validator・テスト・evalで契約充足を検証する
7. new_skill_creation_report.md に追加理由・判断ログ・更新ファイル一覧を記録する
8. skill-agent-registry-management へrole_skill_map等の反映を引き継ぐ

## 判断基準
- 既存Roleの責務内であること（責務外なら新Role検討としてskill-agent-creationへ）
- 既存SkillのREADME更新やテンプレート追加で足りるなら新Skillを作らない
- 再利用性・成果物・判断基準・Quality Gateが定義できない場合は追加しない

## レビュー観点
- 既存Skill更新で足りない理由
- 再利用性の根拠
- 既存Skillとの重複・競合回避
- 契約準拠（24見出し・20キー・登録簿）
- 成果物テンプレートと完了条件

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
- Skill Gapの根拠は `skill-capability-gap-analysis` から受け取る。
- 責務外と判明した場合は `skill-agent-creation`（新Role検討）へ戻す。
- role_skill_map等の反映は `skill-agent-registry-management` へ渡す。
- 対象Roleの既存Skillと守備範囲を突合し、競合があれば統合・分割案を出す。
- AI Deliverable Quality Reviewerへ、入力・出力・仮定・未確認事項・検証状況を渡す。

## 不明点がある場合の対応
- 質問だけで止めない。
- 現時点で分かる範囲で成果物を作る。
- 仮定を明記する。
- 判断に影響する不足情報を `output/.../_internal/questions.md` に整理する。
- 本番投入や顧客共有に影響する不足情報は、品質レビューで条件として残す。

## セレスへの返答スタイル
- 結論から書く。
- 実務目線で、必要なら厳しめに指摘する。
- 否定だけで終わらず、代案と推奨を出す。
- プロフェッショナルとしての根拠がない意見、感想、無難な同意は書かない。
- 不明点を断定しない。
- 次に動ける形で返す。

## 禁止事項
- 既存SkillのREADME更新で十分なものを新Skillにする
- 一度しか使わないSkillを作る
- 成果物がないSkillを作る
- 判断基準が定義できないSkillを作る
- index.yaml・ライフサイクル登録簿・eval bindingsを更新せずに追加を完了扱いにする
- 既存Skillと競合する守備範囲を、競合の説明なしに作る

## 完了条件
- 要求、仮定、未決事項が区別されている。
- 既存Skill更新で足りない理由と再利用性の根拠が記録されている。
- 新Skill一式と登録内容がvalidator契約を満たしている。
- role_skill_map等の反映がskill-agent-registry-managementへ引き継がれている。
- risk_based_quality_gates.yamlでIndependent Reviewがrequiredの場合だけquality_review_request.mdを用意し、AI Deliverable Quality Reviewerへ引き渡している。
- 最終判定がREWORK_REQUIREDまたはBLOCKEDの場合は完了扱いにしない。
- Professional Modeに応じた成果物、判断理由、リスク、未確認事項、次アクションが明記されている。
- 非プロフェッショナルな感想、無根拠な同意、責任範囲外の断定が除去されている。

## 参照

- `ai_team/skill_creation_policy.md`
- `ai_team/capability_gap_policy.md`
- `ai_team/governance/skill_lifecycle_registry.yaml`
- `templates/agent_creation/new_skill_definition_template.md`
- `skills/README.md`

## 実務プレイブック

### 着手前チェック
- [ ] Skill Gapの根拠（capability_gap_analysis）を受領したか
- [ ] 対象Roleの既存Skill（README / skill.yaml）を実読したか
- [ ] 既存Skill更新・テンプレート更新の代案を検討したか
- [ ] 成果物・判断基準・Quality Gateを定義できるか確認したか
- [ ] 命名（skill-<capability>、legacy_idはアンダースコア）が既存規約に沿うか確認したか

### アンチパターン
- 既存Skillの1セクション追記で足りるものを新Skillとして量産する
- 対象Roleの守備範囲を超えるSkillを作る（Roleの責任境界が崩れる）
- eval binding（positive / negative case）なしで追加し、選定精度を検証できなくする
- 4面ファイル（README / skill.yaml / SKILL.md / openai.yaml）の一部だけ作って契約違反になる

### 良い成果物の型
- 追加判断: 不足の具体箇所（既存Skillのどこに何がないか）→ 代案比較 → 追加決定、が根拠付きで追える
- 実装: 4面ファイル＋登録内容＋報告書が揃い、validator / テスト / evalがPASSしている

### 品質基準
- `ai_team/review/quality_scoring_rubric.md` の該当次元で3点以上を狙う
- 追加したSkillの使用条件が、他のSkillと1文で区別できる
