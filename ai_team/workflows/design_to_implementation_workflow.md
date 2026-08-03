# Design to Implementation Workflow

## 目的
承認済み設計を、小さく検証可能な実装単位へ変換する。

## 開始条件
- 基本設計が承認された
- 既存実装へ機能追加する
- FDE経由案件では engineering_handoff.md の受入条件・現場制約・非スコープを実装まで維持する（変更時はFDE経由で顧客合意を取る）

## 主担当
- AI Tech Lead
- AI Fullstack Engineer
- AI Frontend Engineer
- AI Backend Engineer
- AI Cloud / Infrastructure Engineer

## 手順
1. 設計決定、未決事項、互換性制約を確認する
2. 縦切りの実装単位と依存関係を決める
3. API・DB・イベント・UI契約を固定する
4. マイグレーションとfeature flagを設計する
5. コード、設定、IaC、テストを同時に変更する
6. READMEと運用手順を更新する

## 品質ゲート
- 既存機能の非破壊
- 秘密情報の分離
- マイグレーションの前後互換
- ローカル・CIでの再現

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- detailed_design.md
- task_breakdown.md
- 実装コード
- migration
- README更新

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 新方針との整合

- **繰り返し作業**: 実装対象ファイル・コンポーネントが3件以上の場合、`iteration_confirmation_policy.md` に従い代表例を先に確認する
- **能力・effort提案**: 設計・実装・検証で必要な能力を `model_selection_policy.md` に従い非拘束で記録する。呼び出し元の現在Modelは変更しない
- **振り返り**: 実装完了後に `retrospective_policy.md` に従い `output/.../_internal/task_retrospective.md` を作成する
- **第二の脳整理**: 成果物が承認されたとき、`obsidian_write_policy.md` のトリガーを満たした場合のみ Knowledge Curator が整理する
- **Capability Gap**: 実装の途中で既存Role / Skillに無い能力が必要と判明した場合は、`capability_gap_policy.md` に従いAI Capability ArchitectがGap判定を行い、必要最小限の追加（Skill追加優先・新Role追加は最後の手段、Celes Human Gate必須）を経てから続行する

## 参照

- `ai_team/iteration_confirmation_policy.md`
- `ai_team/model_selection_policy.md`
- `ai_team/retrospective_policy.md`
- `ai_team/obsidian_write_policy.md`
- `ai_team/capability_gap_policy.md`
