# Design to Implementation Workflow

## 目的
承認済み設計を、小さく検証可能な実装単位へ変換する。

## 開始条件
- 基本設計が承認された
- 既存実装へ機能追加する

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
