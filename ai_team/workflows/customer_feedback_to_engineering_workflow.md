# Customer Feedback to Engineering Workflow

## 目的
顧客・現場からのフィードバックを、バグ、仕様変更、運用課題、教育課題、改善要望へ分類し、次の開発サイクルへ渡す。

## 開始条件
- 導入後のフィードバックがある
- PoCやデモ後の改善要望がある
- 顧客から不満、利用停止、誤操作、運用負荷の声が出ている
- 仕様変更か教育課題か判断が必要

## 主担当
- AI Forward Deployed Engineer
- AI Engineering PMO
- AI Tech Lead
- AI QA / Test Automation Engineer
- AI SRE / Platform Engineer
- AI Engineering Knowledge Curator
- AI Deliverable Quality Reviewer

## 手順
1. AI FDE（skill-feedback-to-backlog）がフィードバックの出典、発生日、利用者、業務場面を記録する
2. AI FDEがバグ、仕様変更、改善要望、運用課題、教育課題、データ品質課題、セキュリティ課題に分類する（`../fde/fde_feedback_loop.md`）
3. AI FDEが影響範囲、頻度、業務影響、回避策の有無を整理し、improvement_backlog.md へ変換する（対応しないものは理由を記録）
4. MVP内で直すもの、次期拡張へ回すもの、教育で対応するものを分ける（仕様変更は本質課題の再確認を経る）
5. Tech Leadと専門エンジニアが技術影響と修正方針を確認する
6. QAが再現条件、受入条件、回帰テスト観点を定義する
7. PMOが優先順位、担当、期限、セレスへの判断依頼を整理する
8. Knowledge Curatorが再利用できる失敗パターンと判断ログを第二の脳へ反映する

## 品質ゲート
- フィードバックの出典と業務場面が追跡できる
- 事象、原因仮説、対応方針が混ざっていない
- バグと仕様変更と教育課題が分離されている
- 優先順位に顧客価値、頻度、影響、工数の根拠がある
- 受入条件と検証方法がある
- 対応しないものの理由が明記されている

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- feedback_log.md
- post_deployment_findings.md
- improvement_backlog.md
- acceptance_criteria.md
- training_notes.md
- quality_review_request.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。

## 参照

- `../fde/fde_feedback_loop.md`（分類・優先順位・Backlog変換の詳細）
- `../fde/fde_quality_gate.md`（Feedback Loop品質チェック）
- `../../templates/feedback_log_template.md` / `../../templates/feedback_analysis_template.md`
