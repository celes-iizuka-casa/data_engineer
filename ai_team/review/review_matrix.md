# Review Matrix

## 共通レビュー観点
| 観点 | 主Reviewer | 必須確認 |
|---|---|---|
| 目的・要件適合 | Engineering PMO / Quality Reviewer | 目的、対象外、受入条件、成果物の対応 |
| 現場適合・導入定着 | Forward Deployed Engineer / PMO | 利用者、業務フロー、現場制約、成功指標、定着リスク |
| 事実性・根拠 | Quality Reviewer | 主張の出典、実行ログ、未確認事項 |
| 技術・アーキテクチャ | Tech Lead | 境界、整合性、互換性、移行、障害モード |
| 実装・テスト | QA / 実装ロール | 正常・異常・境界・回帰、再現性 |
| データ品質 | Data Engineer / Data Platform | 粒度、キー、履歴、欠損、重複、鮮度、再実行 |
| Security・ガバナンス | Security | 認証認可、PII、秘密、監査、テナント分離 |
| 信頼性・運用 | SRE | SLO、監視、アラート、復旧、Runbook、容量 |
| 性能・スケール | Tech Lead / SRE | 負荷、ボトルネック、上限、拡張戦略 |
| コスト・商用化 | Tech Lead / PMO | MVPコスト、運用負荷、ライセンス、顧客価値 |
| UI・アクセシビリティ | Frontend / QA | エラー回復、権限表示、操作性、アクセシビリティ |
| LLM品質・安全性 | LLM / Security / QA | 根拠、評価、権限、攻撃耐性、承認、コスト |
| 保守性・再利用性 | Tech Lead / DevEx | 責任境界、設定、文書、拡張、技術負債 |
| 知識化・再利用 | Knowledge Curator | 出典、案件文脈、適用条件、MOC、内部リンク、未解決事項 |
| 成果物間整合 | Quality Reviewer | 用語、要件ID、API、DB、テスト、Runbookの一致 |
| 報告の明瞭さ | Quality Reviewer / PMO | 結論、重要指摘、判断依頼、残存リスク、次の行動 |

## リスク別レビュー深度
| リスク | 例 | 必須レビュー |
|---|---|---|
| Low | 文言修正、内部メモ | Quality Reviewerの簡易レビュー |
| Medium | 非破壊の機能・設計変更 | Tech LeadまたはQA + Quality Reviewer |
| High | 認証、データモデル、外部公開、本番変更 | Tech Lead + QA + Security / SRE + Quality Reviewer |
| Critical | PII、決済、マルチテナント、データ削除、Agent高影響操作 | 全該当専門Reviewer + Quality Reviewer + 人間承認 |

## スコア
- 0: 未確認。判定根拠に使用不可。
- 1: Critical。P0相当。
- 2: Insufficient。P1またはP2相当。
- 3: Acceptable。要求を満たす。
- 4: Strong。要求を満たし、拡張・運用余地も明確。
- N/A: 非該当理由が必要。

スコアは説明補助であり、平均点で最終判定しない。
