# Skill Creation Policy

## 目的

既存Roleに新しい能力を追加する必要がある場合に、新Skillを追加する基準を定義する。判断の担当RoleはAI Capability Architect（`skills/skill-skill-creation`）。

## 新Skillを追加してよい条件

- 既存Roleの責任範囲内である（責任範囲外なら新Role検討へ）
- 既存Skillでは手順・成果物・判断基準が不足している
- 再利用性がある
- 成果物テンプレートを定義できる
- Quality Gate（レビュー観点・完了条件）を定義できる
- 他Role / 他Skillとの連携が明確である

## 新Skillを追加しない条件

- 既存SkillのREADME更新で十分
- 既存テンプレート更新で十分
- 一度しか使わない
- 成果物がない
- 判断基準が定義できない

## 追加先レイヤ

作成に着手する前に、追加先が共有層かローカル層かを `local_capability_layer_policy.md` の基準で決める。**派生環境（正本環境と判定できない環境）では共有層へ追加できない。**

共有層のSkill一覧は完全一致契約で守られている（`tools/validate_repository.py` の `SKILLS` 定数、`skills/index.yaml`、`skill_lifecycle_registry.yaml`、`skill_eval_bindings.yaml` の4箇所が一致していなければvalidatorが失敗する）。派生環境で共有層へSkillを1本足すと、これら共有ファイルすべてに差分が出て、正本を `git pull` した時点で衝突する。ローカル層へ置けばこの問題は起きない。

## 新Skill追加時に作成するもの（共有層へ追加する場合）

- `skills/skill-<capability>/README.md`（24見出し契約）
- `skills/skill-<capability>/skill.yaml`（20キー契約。`legacy_id` は `skill_<capability>` 形式）
- `skills/skill-<capability>/SKILL.md`（500行以内）
- `skills/skill-<capability>/agents/openai.yaml`（`$skill-<capability>` 参照）
- 必要に応じたtemplate
- 必要に応じたquality gate（レビュー観点の追記）

## 新Skill追加時に必ず更新するもの（共有層へ追加する場合）

以下はセレス環境で正本へ追加する場合の手順である。派生環境では実行しない。

- `skills/index.yaml`（name / legacy_id / role / modes）
- `skills/README.md`（Skill索引）
- `tools/validate_repository.py` のSKILLSリスト
- `ai_team/governance/skill_lifecycle_registry.yaml`（CREATE entry + Celes Human Gate記録）
- `ai_team/evals/skill_eval_bindings.yaml`（positive / negative case + conflict_group）
- `ai_team/evals/run_foundation_evals.py` のEXPECTED_SKILLS（件数契約）
- `ai_team/role_skill_map.md` / `ai_team/capability_matrix.md` / `ai_team/agent_registry.md`
- `output/.../new_skill_creation_report.md`（追加理由・判断ログ）

## ローカル層へ追加する場合

派生環境、およびセレス環境での個人的・実験的な追加はこちらを使う。共有層のファイルには一切触れない。

- `.local/capability/skills/skill-local-<capability>/` 一式（README.md / skill.yaml / SKILL.md / agents/openai.yaml。共有層と同じ契約に準拠させる）
- `.local/capability/local_capability_registry.yaml`（Skillの一覧・担当Role・modes）
- `.local/capability/local_decision_log.md`（追加日・追加理由・Capability Gap判定・既存Skillで足りない理由・影響範囲・Rollback手順）
- `.local/capability/templates/`（必要な場合）

`SKILLS` 定数、`skills/index.yaml`、`skills/README.md`、`skill_lifecycle_registry.yaml`、`skill_eval_bindings.yaml`、`EXPECTED_SKILLS`、正本3ビューの更新は**いずれも不要**である。Celes Human Gateも不要で、記録先は `local_decision_log.md` になる。

## 承認とHuman Gate（共有層へ追加する場合）

本節は共有層への追加にのみ適用する。ローカル層への追加は現在の利用者自身が判断でき、記録先は `local_decision_log.md` になる。

- Skillの正式化（ACTIVE promotion）は `skill_lifecycle_registry.yaml` の契約どおり、独立レビューとCeles Human Gate記録を必要とする。
- セレスが依頼文でSkill追加を明示指示した場合は、その指示をHuman Gate記録のevidenceとして即時記録してよい。
- 影響範囲が限定的なサブSkill追加（既存Roleの責務内・既存Workflowに自然に追加できる）は、提案と作成を同一タスクで進めてよいが、Gate記録は必ず残す。

## 完了条件

**共有層へ追加した場合:**

- 追加条件（責務内・不足・再利用性・評価可能）の証跡が `new_skill_creation_report.md` に記録されている。
- 4面ファイルと登録内容がvalidator契約を満たし、`python3 tools/validate_repository.py` がPASSしている。
- eval binding（positive / negative case）が定義され、Foundation evalsがPASSしている。
- Celes Human Gate記録が `skill_lifecycle_registry.yaml` に存在する。

**ローカル層へ追加した場合:**

- 追加先をローカル層と判定した根拠が記録されている。
- 共有層のファイルに差分が出ていない（`git status` で確認する）。
- `local_capability_registry.yaml` と `local_decision_log.md` の両方に記録がある。
- 成果物の実行記録に、ローカル層のSkillを使った事実が書かれている。

## 参照

- `ai_team/capability_gap_policy.md`
- `ai_team/local_capability_layer_policy.md`
- `ai_team/agent_creation_policy.md`
- `ai_team/governance/skill_lifecycle_registry.yaml`
- `skills/README.md`
- `templates/agent_creation/new_skill_definition_template.md`
