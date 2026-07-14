# Capability Growth Workflow

## 目的

Celes環境で得た実務Evidenceから改善候補を作り、実装者による自己昇格や他利用者のPrivate State収集を防ぎながらCanonicalへ昇格できるようにする。

## 入力

- Local Private execution evidence
- Reviewer findings / Human feedback / retrospective
- baseline Role / Skill revision
- reusable eval cases

## 手順

1. `new_execution_evidence.py`または同schemaでRaw EvidenceをLocal Private pathへ記録する。
2. 単発事象は`OBSERVED`とし、Critical単発または反復Evidenceだけを`GAP_CANDIDATE`へ進める。
3. Root causeをAgent / Skill / Workflow / Documentation / Tooling / Knowledge / Eval / Unknownへ分類する。
4. 新Skill作成前に既存Skill更新、merge、workflow、documentation、agent definition、tool、evalの順で代替を確認する。
5. baseline revisionとcandidate revisionを固定し、同じEval contractでBefore/Afterを実行する。
6. Candidate実装に関与していないEvaluatorが結果を判定する。
7. Independent ReviewerがP0/P1、regression、privacy、Provider neutrality、Evidence integrityを確認する。
8. Celesが`ai_team/governance/human_gate.schema.json`でPROMOTE / REJECT / REWORK / ROLLBACKを決める。
9. PROMOTE時だけ人間がcommit/pushを行う。自動push・remote telemetry・他利用者Evidence取込は禁止する。

## 判定

- Evidence不足: `UNKNOWN — insufficient evidence`
- P0/P1未解消: promotion不可
- Before/Afterの条件差: comparison無効
- Token/cost未計測: `value: null / evidence_type: unavailable`
- Personal preferenceだけのsignal: Personalizationへ留める

## Rollback

Promoted revision、戻し先revision、reason、Evidence refs、Celes decisionを記録する。Rollbackも自動実行しない。

## 完了条件

- Improver、Evaluator、Reviewer、Human approverが分離されている。
- Baseline/Candidate/Eval contractを追跡できる。
- Raw EvidenceとSecond BrainがGit配布されていない。
- Canonical promotionがCeles Human Gate前に行われていない。
