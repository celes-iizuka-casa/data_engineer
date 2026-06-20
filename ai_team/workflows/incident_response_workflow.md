# Incident Response Workflow

## 目的
障害の検知から復旧、説明、再発防止までを一貫して実行する。

## 開始条件
- SLO違反、データ欠損、セキュリティ事象が検知された
- 顧客影響のある不具合が発生した

## 主担当
- AI SRE / Platform Engineer
- AI Engineering PMO
- AI Tech Lead
- AI Security / Governance Engineer
- 該当実装ロール

## 手順
1. 影響、開始時刻、対象顧客、重大度を判定する
2. 指揮・調査・連絡担当を分ける
3. 拡大防止と安全な暫定復旧を行う
4. 時系列、証拠、判断、変更を記録する
5. 恒久対策と検証を実施する
6. 責任者と期限付きの再発防止を追跡する

## 品質ゲート
- 顧客影響とデータ影響の確認
- 証拠保全
- 復旧後の整合性検証
- 対策の担当・期限・検証方法

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- incident_report.md
- timeline.md
- recovery_result.md
- postmortem.md
- improvement_backlog.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: 対象システム・再発防止策が3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **振り返り**: インシデント収束後に `retrospective_policy.md` に従い `output/task_retrospective.md` を作成する（`postmortem.md` と連動する）
- **第二の脳整理**: 事後報告完了後、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する
- **フィードバック最適化**: 再発防止策についてセレスのフィードバックがある場合、`feedback_optimization_policy.md` に従い分析する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/feedback_optimization_policy.md`
