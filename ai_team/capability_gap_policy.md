# Capability Gap Policy

## 目的

依頼内容に対して、既存AI社員チームの能力が足りているかどうかを判定する。判定の担当RoleはAI Capability Architect（`skills/skill-capability-gap-analysis`）。

## 判定の原則

- 対応可否は `ai_team/capability_registry.yaml`（正本）と実際のRole / Skill定義の実読で判定する。名前の印象で判定しない。
- 参照順序: `agent_registry.md` → `capability_matrix.md` → `role_skill_map.md` → 候補Role / Skillの定義本文。
- 判定結果は `capability_gap_analysis.md`（`templates/agent_creation/capability_gap_analysis_template.md`）に記録する。
- 不明な場合は「UNKNOWN — insufficient evidence」と明記し、仮定を置いて暫定判定する。

## Gap分類

### No Gap

既存Role / Skillで対応可能。既存Roleへ割り当てて終了。

### Skill Gap

既存Roleで担当可能だが、SkillやTemplateが不足している。既存Skill更新または新Skill追加（`skill_creation_policy.md`）で対応する。

### Role Scope Gap

既存Roleの守備範囲を明確化・軽微拡張すれば対応可能。Role定義の更新はガバナンス（UPDATE candidate + Celes Human Gate）を通す。

### Workflow Gap

RoleやSkillではなく、作業順序や連携ルールが不足している。該当Workflowを更新する。

### Template Gap

成果物の型が不足している。`templates/` へテンプレートを追加する。

### Quality Gate Gap

成果物を検証する基準が不足している。`ai_team/review/` の該当ゲートまたはRole / Skillのレビュー観点を更新する。

### Agent Gap

既存Roleでは責任境界が不自然で、新AI社員Roleが必要。`agent_creation_policy.md` とCREATE基準7項目に従い、Celes Human Gateを経て追加する。

## Gap判定後の対応

| Gap分類 | 対応 | 担当 |
|---|---|---|
| No Gap | 既存Roleへ割当 | PMO（Role選定） |
| Skill Gap | 新Skill追加または既存Skill更新 | Capability Architect（skill-skill-creation） |
| Role Scope Gap | 既存Role更新（governed UPDATE） | Capability Architect + Celes Human Gate |
| Workflow Gap | Workflow更新 | Capability Architect + PMO |
| Template Gap | Template追加 | Capability Architect + 対象Role |
| Quality Gate Gap | Quality Gate追加 | Capability Architect + Quality Reviewer |
| Agent Gap | 新AI社員Role追加 | Capability Architect（skill-agent-creation） + Celes Human Gate |

## 優先順位ラダー

不足があった場合の対応は、必ず次の順に検討する。新Role追加は最後の手段。

1. 既存Roleへ割当
2. 既存Skillの更新
3. 既存Roleに新Skillを追加
4. 既存Roleの守備範囲を明確化
5. Workflow / Template / Quality Gateの追加
6. 新しいAI社員Roleの追加

## 追加先レイヤの判定

最小対応を選んだあと、**実際に書き込む前に**、追加先が共有層かローカル層かを決める。判定基準は `local_capability_layer_policy.md` に置く。

- 派生環境（正本環境と判定できない環境）では、追加先は常にローカル層 `.local/capability/` のみ。`ai_team/**`、`skills/**`、`templates/**`、`tools/validate_repository.py` へは書かない。
- 正本環境（セレス環境）では、セレスの明示指示で正本へ追加する場合だけ共有層へ書く。個人的・実験的な追加はローカル層に置く。
- 正本環境かどうかを確認できない場合は派生環境として扱う（共有層へ書かない側に倒す）。
- No Gapと、既存Roleへ割り当てるだけのRole Scope Gapは、何も追加しないためこの判定が不要。

判定結果と根拠（どちらの環境と判定したか、何を確認したか）を `capability_gap_analysis.md` に記録する。

## 完了条件

- Gap分類が7種のいずれかに、根拠の引用付きで一意に決まっている。
- 対応案が優先順位ラダーに沿って選ばれ、上位の代替案を却下した理由が書かれている。
- 追加が発生する場合、追加先レイヤ（共有層 / ローカル層）と判定根拠が記録されている。
- 次アクションと担当（Role / Skill）が明確になっている。
- 判定結果が `capability_gap_analysis.md` として記録され、追加が発生する場合は各Creation Skillへ引き継がれている。

## 参照

- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_lifecycle_policy.md`
- `ai_team/local_capability_layer_policy.md`
- `ai_team/capability_registry.yaml`
- `ai_team/workflows/input_to_output_workflow.md`
