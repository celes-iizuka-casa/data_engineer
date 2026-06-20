# Feedback Optimization Policy

## 目的

セレスからのフィードバックを解析し、AIエンジニアチームのRole、Skills、Workflow、Templatesを継続的に改善する。

## 基本方針

- フィードバックを一回限りの修正として扱わない
- 再発するフィードバックはチーム改善対象にする
- Role定義に問題があるのか、Skill手順に問題があるのか、テンプレートに問題があるのかを分ける
- セレスの好みと、品質基準を分けて整理する
- 必要な改善は提案する
- 勝手に大きく改修せず、改善提案として出す

## フィードバックとして扱うもの

- 方向性は良い / 方向性が違う
- 粒度が粗い / 粒度が細かすぎる
- AIっぽい / もっと自然に
- 余計なことが多い / もっと簡潔に / もっと詳しく
- これは不要 / これは必要
- この観点が足りない
- こういう前提で考えて
- Claude Code前提じゃなくていい / Codexも使っている
- 確認してから進めて / 一気にやらないで
- もっとプロとして意見して / 無理に賛同しないで

## フィードバック分類

- 方針ズレ
- 粒度ズレ
- 出力形式ズレ
- 文章トーンズレ
- 技術観点不足
- 業務観点不足
- セキュリティ観点不足
- 運用観点不足
- 検証観点不足
- 確認フロー不足
- モデル選定不足
- Obsidian整理タイミング不足
- Role守備範囲不足
- Skill手順不足
- テンプレート不足

## 解析手順

1. セレスのフィードバックを抽出する
2. フィードバックの種類を分類する
3. どのRole / Skill / Workflow / Templateに関係するか特定する
4. 一時的な修正でよいか、恒久的な改善が必要か判断する
5. 改善案を作成する
6. 必要に応じて改善対象ファイルを提案する
7. セレス承認後に反映する

## 注意点

- セレスのフィードバックを過剰一般化しない
- 一回だけの好みを全体ルールにしない
- 繰り返し発生する指摘はルール化を検討する
- 技術品質を下げる方向の最適化はしない
- セレスの作業スタイルに合わせつつ、プロとして必要な指摘は残す

## 作成する成果物

- `output/feedback_analysis.md`（フォーマット: `templates/feedback_analysis_template.md`）
- `output/team_improvement_proposal.md`（フォーマット: `templates/team_improvement_proposal_template.md`）

## 完了条件

- フィードバックが分類されている
- 改善対象が特定されている
- 改善案が提示されている
- 必要に応じてチーム改善提案が作成されている

## 参照

- `ai_team/roles/engineering_pmo.md`
- `ai_team/roles/devex_agent_workflow_engineer.md`
- `templates/feedback_analysis_template.md`
- `templates/team_improvement_proposal_template.md`
