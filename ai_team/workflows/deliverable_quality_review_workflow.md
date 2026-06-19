# Deliverable Quality Review Workflow

## 目的
各AI社員の成果物を独立・横断レビューし、セレスが判断できる最終品質報告へ変換する。

## 開始条件
- AI社員が成果物を提出した
- 顧客共有・実装着手・本番リリースの判定が必要
- 再作業後の再レビューを行う

## 主担当
- AI Deliverable Quality Reviewer
- AI Engineering PMO
- AI Tech Lead
- AI QA / Test Automation Engineer
- AI Security / Governance Engineer
- AI SRE / Platform Engineer

## 手順
1. 作成者がquality_review_request.md、成果物、差分、検証証跡を提出する
2. PMOが対象範囲、要件、必須専門Reviewer、期限を確認する
3. 専門Reviewerが担当観点の判定と証跡を提出する
4. Deliverable Quality Reviewerが成果物間の整合性と未検証領域を確認する
5. 指摘をP0からP3へ分類し、修正案、責任者、期限を付ける
6. PASS、PASS_WITH_CONDITIONS、REWORK_REQUIRED、BLOCKEDを判定する
7. quality_review_report.mdの冒頭に結論、重要指摘、セレスへの判断依頼を記載する
8. 再作業時は指摘IDを維持し、修正証跡を確認して再判定する

## 品質ゲート
- 作成者と最終Reviewerが分離されている
- 必須専門レビューと検証証跡が揃っている
- P0・P1が未解消なら承認しない
- P2の条件付き承認には責任者・期限・影響受容がある
- 確認していない領域をN/Aまたは未確認として明示する

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- quality_review_request.md
- quality_review_report.md
- finding_register.md
- 再作業指示
- セレスへの判断依頼

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。
