# Agent Registry Entry

<!-- ai_team/agent_registry.md のAgent一覧へ追加する1行の下書き -->
<!-- 正本は ai_team/capability_registry.yaml。登録前にrole entryが存在することを確認する。 -->

| Agent Role | 主な責任 | 対応領域 | 主なSkills | 優先実行環境 | デフォルトモデル | デフォルト工数 | 使用条件 |
|---|---|---|---|---|---|---|---|
| （AI <Role名>） | （1行） | （領域） | （skill-...） | （呼び出し元Runtime準拠の推奨） | （非拘束推奨） | （非拘束推奨） | （起動条件） |

## 記入ルール

- 優先実行環境・デフォルトモデル・デフォルト工数は非拘束の推奨。正本は `ai_team/model_effort_selection_policy.md`。
- 能力評価・数値スコアは書かない（capability_registry.yaml のevaluation値のみ転記可）。
- 使用条件は「どんな依頼のときに選ぶか」を1文で。
- 追加後、`ai_team/agent_registry.md` の更新履歴に日付・内容・根拠を追記する。
