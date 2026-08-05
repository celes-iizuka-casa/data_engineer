# Risk-based Team Formation Workflow

## 目的

固定チームを全員起動せず、Current Requestに必要なCapability、Risk、Reviewerだけを選ぶ。

## 入力

- Current Explicit Request
- Current Evidence
- `capability_registry.yaml`
- `ai_team/review/risk_based_quality_gates.yaml`
- Role / Skillの守備範囲とhandoff条件

## 手順

1. Task type、domain、ambiguity、impact、reversibility、external dependencyを分類する。
2. Production、destructive、schema/data loss、Security/PII、financial、blast radiusからRisk levelを決める。
3. 必須Capabilityを列挙し、`capability_registry.yaml`からPrimary Roleを必要最小限で選ぶ。
4. Primary Roleがownsしない領域だけSupporting Roleへhandoffする。
5. 通常Taskでは、cleanなCanonical checkout（内容hashが`skill_lifecycle_registry.yaml`の`state: ACTIVE` / `active_revision`と一致）から必要なSkillだけ選ぶ。Celes環境の明示的なCapability Growth / Eval Taskに限り、未commit working treeの`candidate_revision`を評価実行できる。その場合はExecution Evidenceへcandidate revisionと評価目的を記録し、Human Gate前にCanonical配布しない。working treeがactiveと異なり、かつcandidate評価Taskでもない場合は停止する。未使用Skillを数合わせで起動しない。
6. Risk levelに対応するIndependent/Specialist ReviewerとHuman Gateを選ぶ。
7. 選定理由、使用しない主要Role、assumptions、unknownsをexecution planまたはoutput制御ブロックへ記録する。

## 禁止事項

- 毎回全Roleを起動する
- Provider/ModelでRoleを選ぶ
- Capability scoreをEvidenceなしで作る
- Specialist RoleのBlockerをPMOや総合Reviewerが解除する
- High/Critical Riskでrequired gateを省略する
- Candidate Skillを通常Taskのactive Skillとして扱う

## 完了条件

- Taskに必要なCapabilityがRoleへ対応している。
- Role/Skillの追加が最小で、不要起動の理由を説明できる。
- Risk levelとQuality Gateが一致している。
- caller Runtimeを変更していない。
