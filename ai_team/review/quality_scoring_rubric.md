# Quality Scoring Rubric（採点基準）

quality_review_report の「Quality Scorecard」（15次元 × 0–4点）の採点アンカーと、スコアから最終判定への変換規則を定義する。目的は、レビュアーごと・案件ごとの判定のブレをなくし、REWORK の理由をスコアで追跡可能にすること。

## 適用範囲

- AI Deliverable Quality Reviewer が品質レビューを行うすべての成果物に適用する。
- レビュー対象外（output_optimization_policy.md のゲート非該当）の成果物には適用しない。
- 採点は証跡に基づく。証跡なしのスコアは記入しない（0 = not reviewed のままにする）。

## スコアの意味

| スコア | 意味 |
|---|---|
| 4 | strong: 反証を探しても欠陥が見つからない。そのまま顧客共有・本番投入できる |
| 3 | acceptable: 実務投入可能。軽微な改善余地（P3）のみ |
| 2 | insufficient: 使えるが穴がある。P2相当の指摘が対応必要 |
| 1 | critical: このままでは事故る。P0/P1相当 |
| 0 | not reviewed: 未レビュー |
| N/A | 対象外（理由必須） |

## 次元別アンカー（3点の条件 / 1点以下になる典型）

| Dimension | 3点（acceptable）の条件 | 1点以下になる典型 |
|---|---|---|
| Purpose and requirement fit | 依頼の明示要求をすべて満たし、解釈のズレを制御ブロックで検知できる | 依頼と違う成果物。要求の読み違いに気づけない構成 |
| Factual accuracy and evidence | 事実と推測が分離され、外部仕様は出典または実データで確認済み | 未確認の外部仕様の断定。実データと矛盾する記述 |
| Technical correctness and architecture | 技術判断に理由があり、既存構成・用語・契約と整合する | 動かない設計。既存契約（API/スキーマ）を黙って破壊 |
| Cross-artifact consistency and traceability | 要件ID・用語・粒度が成果物間で一致し、判断の出典を追える | 成果物間で数値・用語が矛盾。結論の根拠を追えない |
| Implementation readiness | 次工程がそのまま着手できる粒度（ファイル・手順・前提が具体） | 「あとは実装するだけ」と言いつつ前提・手順が欠落 |
| Test coverage and reproducibility | 検証手順が再実行可能で、実施済みと未実施が区別されている | テスト未実施を実施済みのように見せる。再現手順なし |
| Data quality and data contract | 粒度・主キー・時刻・欠損/重複の扱いが明示され、下流契約が定義されている | 主キー・タイムゾーン未定義。SELECT * 契約 |
| Security, privacy, and governance | 認証認可・秘密管理・個人情報の扱いが該当範囲で明示されている | 秘密情報の平文出力。個人情報の扱い未検討 |
| Reliability, operations, and recovery | 再実行・ロールバック・監視の該当観点が設計に含まれる | 冪等でない再実行。失敗時の復旧手順なし |
| Performance and scalability | 想定負荷とボトルネックが数値または根拠付きで示されている | スケール前提が無根拠。明らかな性能欠陥の看過 |
| Cost and commercial viability | コスト影響が概算され、MVPと商用のバランスに言及がある | コスト無視の過剰設計。運用不能な高度化 |
| Usability and accessibility | 利用者がそのまま使える説明・手順・形式になっている | 読み手が次に何をすべきか分からない |
| Maintainability and reuse | 命名・構造が既存規約に従い、再利用条件が明示されている | 使い捨て構造。既存規約からの無断逸脱 |
| Documentation and handover | 引き継ぎに必要な前提・未決事項・出典が残っている | 暗黙知前提。未決事項の消失 |
| LLM safety and evaluation, if applicable | プロンプト注入・出力検証・評価方法が該当範囲で扱われている | LLM出力を無検証で確定情報として使用 |

## スコア → 最終判定の変換規則

P0/P1 ゲートが常に優先する（スコアで上書きしない）。

| 条件 | 判定 |
|---|---|
| 採点済み全次元が3以上、かつ P0/P1/P2 なし | PASS |
| 採点済み全次元が2以上、かつ P0/P1 なし（P2 は責任者・期限付き） | PASS_WITH_CONDITIONS |
| いずれかの次元が1以下、または P0/P1 あり | REWORK_REQUIRED |
| 証跡不足で採点不能な必須次元がある、または専門Reviewerの未解除Blocker | BLOCKED |

## 品質スコアの表記

- output.md 制御ブロックの「品質スコア」には `平均 X.X / 4.0（採点n次元、N/A除外）` を記載する。
- 最低スコア次元を1つ添える（例: `平均 3.2 / 4.0（最低: Test coverage 2）`）。判定のボトルネックを先頭ブロックで見えるようにするため。

## 提出前チェック（作成Role向けDoD・モード別）

レビュー依頼前に作成Roleが自己確認する。自己確認は独立レビューではない。

### Opinion
- [ ] 確認済み事実と推論・仮定を分けたか
- [ ] 懸念に理由・影響・代案・推奨条件を付けたか
- [ ] 採用条件と採用しない条件を書いたか

### Design
- [ ] セキュリティ・運用・テストを設計に含めたか（後回しにしていないか）
- [ ] MVP範囲と商用化時の拡張範囲を分けたか
- [ ] 既存成果物と用語・要件ID・契約が整合しているか

### Implementation
- [ ] 実行手順・検証手順・ロールバックを付けたか
- [ ] エラー処理と再実行性（冪等性）を確認したか
- [ ] テストを実施し、未実施項目を明記したか

### Verification
- [ ] 検証済みと未検証を分けたか
- [ ] 問題に重大度と修正案を付けたか
- [ ] 再検証手順を残したか

## ゴールデンサンプル（見本）

「3点以上とはどういう状態か」の基準例:

- `templates/examples/golden_sample_output.md` — Opinion モードの output.md 見本
- `templates/examples/golden_sample_quality_review.md` — 採点済みレビューレポートの見本

## 参照

- `review_policy.md` — 判定の定義
- `quality_gate.md` — 必須ゲート
- `../../templates/quality_review_report_template.md` — 記入先
