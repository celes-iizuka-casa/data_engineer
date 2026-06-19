# Request Mode Policy

## 目的
セレスからの依頼文を、Professional Opinion / Design / Implementation / Verification Modeへ分類する。

## 分類表
| 依頼例 | 判定するモード |
|---|---|
| どう思う？ | Professional Opinion Mode |
| 妥当？ | Professional Opinion Mode |
| 正直どう？ | Professional Opinion Mode |
| 設計して | Professional Design Mode |
| 構成考えて | Professional Design Mode |
| SQL書いて | Professional Implementation Mode |
| 実装して | Professional Implementation Mode |
| Terraform作って | Professional Implementation Mode |
| 検証して | Professional Verification Mode |
| 問題ない？ | Professional Verification Mode |
| レビューして | Professional Verification Mode |

## 複数モードに該当する場合
原則は Opinion → Design → Implementation → Verification の順で処理する。ただし、明確に実装依頼の場合は、設計を必要最小限にして実装を優先する。

## 完了条件
- 依頼タイプが明記されている。
- 選定Roleと成果物が明記されている。
- 不明点がある場合も仮定を置いて進んでいる。
