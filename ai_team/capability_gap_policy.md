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

## 完了条件

- Gap分類が7種のいずれかに、根拠の引用付きで一意に決まっている。
- 対応案が優先順位ラダーに沿って選ばれ、上位の代替案を却下した理由が書かれている。
- 次アクションと担当（Role / Skill）が明確になっている。
- 判定結果が `capability_gap_analysis.md` として記録され、追加が発生する場合は各Creation Skillへ引き継がれている。

## 参照

- `ai_team/agent_creation_policy.md`
- `ai_team/skill_creation_policy.md`
- `ai_team/agent_lifecycle_policy.md`
- `ai_team/capability_registry.yaml`
- `ai_team/workflows/input_to_output_workflow.md`
