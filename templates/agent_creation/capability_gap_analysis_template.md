# Capability Gap Analysis

<!-- 保存先: output/<client>/<日付>/<task>/capability_gap_analysis.md -->
<!-- 判定は必ず既存Role / Skill定義の実読に基づく。名前の印象で判定しない。 -->

## 依頼概要

（依頼の要約。背景・成果物イメージ・制約を1〜3行で）

## 必要能力

- （依頼を完了するために必要な能力を列挙）

## 必要専門領域

- （データ / セキュリティ / インフラ など）

## 必要成果物

- （設計書 / コード / 分析 など、期待される成果物）

## 既存Role確認

| Role | 対応可否 | 理由 |
|---|---|---|
| （候補Role名） | 可 / 一部可 / 不可 | （守備範囲のどの記述に基づくか） |

## 既存Skill確認

| Skill | 対応可否 | 理由 |
|---|---|---|
| （候補Skill名） | 可 / 一部可 / 不可 | （手順・成果物・判断基準の充足状況） |

## Gap分類

<!-- 該当するものを1つ選び、根拠を書く -->
- No Gap
- Skill Gap
- Role Scope Gap
- Workflow Gap
- Template Gap
- Quality Gate Gap
- Agent Gap

判定: （分類）
根拠: （参照した定義と該当記述）

## 推奨対応

（優先順位ラダー「割当 → Skill更新 → Skill追加 → Role明確化 → Workflow / Template / Gate追加 → 新Role」に沿った最小の対応案）

## 追加先レイヤ

判定: （共有層 / ローカル層 / 追加なし）
環境判定: （正本環境 / 派生環境）
確認した内容: （origin URLの正規化後の値と宣言値の一致有無、push権限の実測結果。確認できなかった項目は `unavailable` と書く）
根拠: （`ai_team/local_capability_layer_policy.md` の該当条件）

## 新Roleが必要か

（必要 / 不要。必要ならCREATE基準7項目の充足見込みを記載）

## 新Skillで足りるか

（足りる / 足りない。対象Roleと不足内容）

## 既存Role更新で足りるか

（足りる / 足りない。更新箇所案）

## 判断理由

（上記判定の根拠の要約。確認済み事実 / 推論 / 未確認事項を分ける）

## 次アクション

- （skill-agent-creation / skill-skill-creation / 既存Roleへの割当 など、次の担当と作業）
