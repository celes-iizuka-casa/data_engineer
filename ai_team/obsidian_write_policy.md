# Obsidian Write Policy

## 目的

第二の脳への書き込みタイミングを制御し、未確定情報が正式ナレッジに混ざることを防ぐ。

## 第二の脳ルートパス

```
{{SECOND_BRAIN_ROOT}}
```

**設定方法:**
- Codex 環境: `/Users/celesiizuka/Codex/CASA/second_brain/data_engineer/`
- Celestian 環境: `/Users/celesiizuka/Celestian/CASA/second_brain/data_engineer/`（存在しない場合は別途作成）
- 実際に使用するパスは、AI Engineering Knowledge Curator の実行前に確認する
- パスが存在しない場合は、セレスに確認してから書き込む

## 基本方針

- 第二の脳への正式書き込みは作業完了後
- Draft中の成果物は正式ナレッジ化しない
- セレス承認前の一括展開前サンプルは正式ナレッジ化しない
- 必要な場合のみ `99_Inbox/` に一時メモを残す
- `Completed` / `Accepted` / `Obsidian Synced` を正式書き込みトリガーにする

## 正式書き込みトリガー

以下のいずれかを満たした場合に AI Engineering Knowledge Curator を起動する:

- `output/.../output.md` が作成・更新された（先頭ブロックのステータスが `Completed` / `Accepted`）
- `output/final_deliverables_index.md` が作成された
- セレスが成果物を承認した（ステータス: `Accepted`）
- 繰り返し作業の全件展開が完了した
- 検証レポートが完了した
- 作業ステータスが `Completed` / `Accepted` になった
- セレスが「第二の脳にまとめて」「Obsidianに整理して」と明示した

## 書き込み保留条件

以下のステータスでは正式書き込みを保留する:

- `Draft`
- `In Progress`
- `Waiting for Celes Review`
- `Waiting for Approval`
- `Needs Clarification`
- `Verification Pending`

必要な場合は `99_Inbox/` に一時メモとして置くことは許可する。
ただし、正式なMOC更新・パターン化・ADR化は `Completed` / `Accepted` 以降にする。

## Knowledge Curator の実行手順

1. 作業ステータスを確認する
2. 正式書き込みトリガーを満たしているか確認する
3. 満たしていなければ保留する
4. 満たしていれば `{{SECOND_BRAIN_ROOT}}` のパスを確認する
5. パスが存在しない場合はセレスに確認する
6. 成果物を解析する
7. プロジェクトノートを作成する
8. 技術ナレッジを抽出する
9. パターン化できるものを整理する
10. ADRにすべき判断を抽出する
11. MOCを更新する
12. source_mapを作成する
13. `output/obsidian_sync_summary.md` を作成する

## FDE知識の保存先マッピング

FDE成果物（Completed / Accepted後）は以下に整理する:

| FDE知識 | 保存先候補 |
|---|---|
| 顧客課題整理パターン / Field Discoveryの観点 | `02_Knowledge/fde/` |
| Business Flow Mappingのパターン / MVPスコープの切り方 / Engineering Handoffの型 / 導入・定着の観点 / Success Metricsの設計パターン / Feedback Loopの改善パターン | `03_Patterns/fde_patterns/` |
| FDEテンプレートの再利用形 | `06_Templates/fde/` |
| MOC更新 | `00_MOC/engineering_moc.md` |

## 参照

- `ai_team/roles/engineering_knowledge_curator.md`
- `../skills/skill-engineering-knowledge-curator/SKILL.md`
