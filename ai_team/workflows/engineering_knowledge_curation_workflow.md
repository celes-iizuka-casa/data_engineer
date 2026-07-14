# Engineering Knowledge Curation Workflow

## 目的
レビュー済み成果物を、案件文脈と出典を保ちながらObsidianの第二の脳へ再利用可能な形で反映する。

## 開始条件
- 現在利用者が同期を明示した、または成果物がAcceptedかつ再利用価値ありと判定されている
- Quality Reviewerが必要な案件ではPASSまたはPASS_WITH_CONDITIONSである
- 現在利用者のLocal Second Brain rootが明示的に解決できる

## 主担当
- AI Engineering Knowledge Curator
- AI Engineering PMO
- AI Deliverable Quality Reviewer
- AI Tech Lead
- AI DevEx / Agent Workflow Engineer

## 手順
1. 現在利用者とLocal root、同期元成果物、レビュー判定、未確認事項、機密区分を棚卸しする
2. 案件別overview、decisions、architecture、implementation、test、risks、next_actions、source_mapを作る
3. 案件固有情報と再利用可能な知識を分離する
4. Knowledge、Pattern、ADR、Troubleshootingへ必要な内容だけを抽出する
5. MOC、タグ、frontmatter、内部リンクを更新する
6. リンク切れ、重複、出典、未検証主張、機密情報を検証する
7. output/.../_internal/obsidian_sync_summary.mdへ同期結果と未反映事項を報告する

## 品質ゲート
- Quality Reviewerの判定と未確認事項を改変していない
- 原成果物へのsource_mapがある
- MOCから主要ノートへ到達できる
- 案件固有情報を一般知識へ誤昇格していない
- 既存ノートを無条件で上書きしていない
- 秘密情報と未マスキング個人情報がない
- 他利用者のSecond Brainへ読み書きしていない
- Personal preferenceをUniversal capabilityへ昇格していない

ゲート未達の場合は、例外理由、影響、代替統制、責任者、解消期限を記録する。重大なSecurity・データ損失・復旧不能リスクは例外扱いせず停止する。

## 成果物
- 第二の脳のProject Note
- Knowledge / Pattern / ADR / Troubleshooting
- MOC
- source_map.md
- output/.../_internal/obsidian_sync_summary.md

## 引き継ぎルール
- 入力と出力のパスを明記する。
- 仮定、未決事項、既知の制約、検証結果を添付する。
- 次工程の責任者と完了条件を合意する。
