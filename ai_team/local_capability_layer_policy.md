# Local Capability Layer Policy

## 目的

依頼内容解析のフロー（Capability Gap判定）で追加したAI社員（Role）やSkillを、配布される共有層へ混ぜずに、現在の利用者のローカル領域へ閉じる。正本の更新でローカル追加分が消えず、ローカル追加分が正本を汚染しない状態を保つ。

このリポジトリはセレス環境を正本とし、他の利用者は `git clone / pull` でコピーして使う。一方で Capability Gap判定は誰の環境でも走る。両者を両立させるための層の分離を定める。

## 2層モデル

| 層 | 置き場 | 追加権限 | 配布 |
|---|---|---|---|
| Shared Core（正本） | `ai_team/**`、`skills/**`、`templates/**`、`tools/validate_repository.py` | セレスのみ（Celes Human Gate） | `git clone / pull` で全利用者へ |
| User-local Capability Layer | `.local/capability/**` | 現在の利用者自身 | 禁止（非配布） |

`.local/` は `.gitignore`、`tools/validate_repository.py` のprivate path契約、`ai_team/governance/architecture_contract.yaml` の `privacy.private_state` の3つで非配布が保証されている。ローカル層はこの既存の保護をそのまま使う。

## ローカル層の構造

```text
.local/capability/
├── local_capability_registry.yaml   # ローカルRole / Skillの一覧（この利用者限定の正本）
├── local_decision_log.md            # 追加・変更・廃止の判断記録
├── roles/<role_id>.md               # ai_team/roles/*.md と同じ見出し契約に準拠
├── skills/skill-<name>/             # skills/skill-*/ と同じ4面ファイル契約に準拠
│   ├── README.md
│   ├── skill.yaml
│   ├── SKILL.md
│   └── agents/openai.yaml
├── templates/                       # ローカル成果物テンプレート
└── promotion/                       # 正本への昇格提案（任意）
```

`local_capability_registry.yaml` と `local_decision_log.md` の雛形は共有層にある（`templates/agent_creation/local_capability_registry_template.yaml` と `templates/agent_creation/local_decision_log_template.md`）。雛形は配布されるが、記入後の実体は `.local/` 配下のため配布されない。

`.local/capability/` が存在しない場合は正常なno-opとして継続する。エラーにしない。Second Brainのrootが無い場合と同じ扱いとする（`personalization_policy.md`）。

## 命名規約

ローカルIDには接頭辞を付ける。Role IDは `local_<name>`、Skillディレクトリは `skill-local-<name>` とする。

理由は、成果物や判断記録の上でローカル由来かどうかを一意に判別できるようにするためと、将来の正本追加とID衝突したときに衝突箇所を特定できるようにするため。衝突した場合はローカル側を改名する（正本を改名しない）。

## 解決順序と上書き禁止

- 依頼受付時に読むのは、正本の3ビュー（`agent_registry.md` / `capability_matrix.md` / `role_skill_map.md`）と、存在する場合の `.local/capability/local_capability_registry.yaml`。
- ローカル層は**追加専用**である。正本のRole / Skill定義を上書き・再定義してはならない。上書きを許すと同名Roleの挙動が利用者ごとに分岐し、正本の記述と成果物の説明が食い違う。
- 正本Roleの守備範囲をローカルで補いたい場合は、正本ファイルを書き換えず、ローカル層に別IDのRole / Skillとして追加する。

## 正本環境の判定

次を順に確認し、**いずれか1つでも満たさない、または確認できない場合は「派生環境」とする**。派生環境は共有層へ追加できない。

1. `git remote get-url origin` のhostとpathが、`architecture_contract.yaml` の `growth_authority.canonical_repository` の宣言値と一致する。
2. canonical repositoryへのpush権限が確認できる（`git push --dry-run` が成功する、または `gh repo view <canonical_repository> --json viewerPermission` が `ADMIN` / `WRITE`）。

**URLの比較規則**: scheme、userinfo、末尾の `.git` を除去し、hostを小文字化した `host/owner/repo` 形式で比較する。`https://github.com/owner/repo.git`、`git@github.com:owner/repo.git`、`https://github.com/owner/repo` はいずれも `github.com/owner/repo` に正規化して同一と扱う。

判定できない場合に派生環境へ倒すのは、誤って共有層へ書き込む事故を防ぐため。逆方向の誤り（正本環境を派生と誤判定する）は、共有層への追加が拒否されるだけで復旧できる。

**push権限は必要条件であって十分条件ではない**。push権限はcanonical repositoryへの書き込み可否を示すだけで、操作者がセレス本人であることの証明ではない（将来canonicalにcollaboratorを追加した場合、その環境も条件2を満たす）。したがって共有層への追加は、環境判定の通過に加えて**セレスの明示指示を常に必要とする**。

**誤判定時の回避**: セレスがfork、別remote、detachedな作業コピーで作業している場合、条件1を満たさない。この場合に限り、依頼で「この環境を正本環境として扱う」と明示することで条件1を緩和してよい。ただし**条件2（canonical repositoryへのpush権限）は宣言では代替できず、必ず実測する**。理由は、宣言だけで共有層への書き込みを許すと、派生環境の利用者も自分の環境の依頼者として同じ宣言ができてしまい、この節のfail-safe設計が無効化されるため。緩和を使った場合は、宣言の原文と条件2の実測結果の両方を記録する。

## 追加先の決定

Capability Gap判定で分類と最小対応を決めたあと、**書き込む前に**追加先の層を決める。

| 条件 | 追加先 |
|---|---|
| 派生環境 | ローカル層のみ。`ai_team/**`、`skills/**`、`templates/**`、`tools/validate_repository.py` へは書かない |
| 正本環境 + セレスの明示指示で正本へ追加 | 共有層（`agent_creation_policy.md` / `skill_creation_policy.md` の共有層向け手順） |
| 正本環境 + 個人的・実験的な追加 | ローカル層（セレス自身のパーソナライゼーションも同じ機構で扱う） |

No Gapと、既存Roleへ割り当てるだけのRole Scope Gapは、何も追加しないため層の判断が不要。

## 承認

| 層 | Gate | 記録先 | 独立レビュー |
|---|---|---|---|
| ローカル層 | 現在の利用者自身 | `.local/capability/local_decision_log.md` | 必須ではない。Risk Medium以上では推奨 |
| 共有層 | Celes Human Gate | `ai_team/governance/ai_employee_lifecycle_registry.yaml` / `skill_lifecycle_registry.yaml` | 必須 |

`local_decision_log.md` には、追加日、追加したRole / Skill、追加理由、Capability Gap判定、既存で足りなかった理由、影響範囲、Rollback手順を残す。共有層のdecision_history / promotion_historyのappend-only契約はローカル層には適用しない（ローカル層は共有層のライフサイクル登録簿に載らない）。

ローカル層の追加物はcanonicalを名乗らない。成果物の実行記録には、ローカル層のRole / Skillを使ったことを明記する。

## 正本への昇格

ローカル層で有用と分かったRole / Skillは、次の経路で共有層へ昇格を提案できる。自動昇格はしない。

1. ローカル層で実運用Evidenceを蓄積する（`capability_growth_policy.yaml` の `candidate_rules` に準拠。反復パターンは2件以上、Criticalは1件でも可）。
2. `.local/capability/promotion/` に昇格提案を作る。次を必ず含める。
   - 昇格候補のRole / Skill IDと、共有層で使う正式ID（`local_` 接頭辞を外した名前）
   - 追加理由と、既存の正本Role / Skillで足りない理由
   - 守備範囲と、責任を持たない領域
   - 必要なSkill / Template / Quality Gate
   - ローカル層での利用実績（件数、成果物、うまくいかなかった点）
   - 個人属性・顧客情報・raw evidenceを除去した独立Evidence

   raw evidence（顧客情報・個人属性を含む生の記録）は `.local/capability/` に置かない。`capability_growth_policy.yaml` の `raw_evidence_storage.allowed_roots`（`.local/evidence` と `output`）に従い、`.local/capability/promotion/` には非個人化済みの独立Evidenceだけを置く。
3. セレス環境で受領し、Capability Gap再判定 → CREATE基準7項目 → Before/After Eval → 独立レビュー → Celes Human Gate（`capability_growth_policy.yaml` の流れ）を通す。
4. **昇格提案が受理された時点で**ローカル定義を無効化し（`local_capability_registry.yaml` で `result: promoted` に更新して割当対象から外す）、`git pull` 後に削除する。受理からpullまでの間に正本定義とローカル定義が同時に有効になる期間を作らない。

REJECTされた場合もローカル層での利用は続けてよい。それがパーソナライゼーションの範囲であることを意味する。ただしREJECTの事実と理由を `local_decision_log.md` に残す。根拠を足さないまま同じ提案を再提出しないため。

## 検証の扱い

`tools/validate_repository.py` はローカル層を検査しない。`.local/` はgit ignore対象のため未追跡ファイル走査の対象外で、ドキュメント走査の対象ディレクトリにも含まれないため。

したがってローカル層のRole / Skillは、共有層と同じ見出し契約・キー契約に**利用者の責任で**準拠させる。準拠しなくてもvalidatorは失敗しないが、昇格時に共有層の契約検査で必ず落ちる。

検査が効かないことの運用上の帰結は次のとおり。

- 契約違反は検出されない代わりに、**成果物の品質として現れる**（必須セクションの欠落、判断根拠の不足など）。初回利用前に、見出し契約とキー契約を自己点検する。
- ローカル層のRole / Skillを使って作った成果物にも、`ai_team/review/risk_based_quality_gates.yaml` の判定を**通常どおり適用する**。ローカル層であることは独立レビューを省略する理由にならない。
- ローカル層のRole / Skillを使ったことは成果物の実行記録に明記し、読み手が品質の前提を判断できるようにする。

## 完了条件

- 追加先の層が決まっており、判定根拠（正本環境か派生環境か、どちらの条件で判定したか）が記録されている。
- 派生環境で共有層のファイルを変更していない。
- ローカル層への追加が `local_capability_registry.yaml` と `local_decision_log.md` の両方に記録されている。
- 成果物の実行記録に、ローカル層のRole / Skillを使った事実が書かれている。

## 参照

- `ai_team/personalization_policy.md`
- `ai_team/capability_gap_policy.md`
- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_lifecycle_policy.md`
- `ai_team/governance/architecture_contract.yaml`
- `ai_team/governance/capability_growth_policy.yaml`
