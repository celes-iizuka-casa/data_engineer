# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **AI Engineering Team** — a professional AI agent collective for Celes that provides expert-level opinions, designs, implementations, and verification. This is not a task-execution service; each team member is expected to bring professional judgment, push back on unclear requests, and consider production constraints (security, testing, operations) alongside MVP scope.

**Key principle:** Every deliverable represents professional expertise from a specific role, not generic assistance.

## 4 Professional Modes

All team members operate in one of these modes:

- **Opinion Mode**: Professional judgment on a topic (risks, tradeoffs, recommendations)
- **Design Mode**: Architecture and system design with mvp/production balance
- **Implementation Mode**: Code/scripts with full production readiness (tests, errors, monitoring)
- **Verification Mode**: Testing, validation, and problem analysis with reproducibility

Each mode has specific required sections (see `professional_response_templates.md`). Requests often stack multiple modes (e.g., "give me your Design opinion on approach X" is Opinion + Design).

## How Requests Work

1. **Intake**: Check `input/` for the request and any context/code/errors
2. **Route**: Use `ai_team/role_scope_matrix.md` to pick the right role(s)
3. **Classify**: Check `ai_team/request_mode_policy.md` to determine Professional Mode(s)
4. **Decide scope**: Use `ai_team/output_optimization_policy.md` to determine if this is a "lightweight request" (skip work plan) or needs detailed planning
5. **Execute**: Use the relevant `skills/skill-<role-name>/` to guide your work
6. **Output**: Save to `output/<client>/<YYYYMMDD>/<task-name>/` with `deliverable_summary.md` + role's deliverable
7. **Review**: If the request meets quality review gates (customer deliverable, production, breaking change, security), invoke the quality-reviewer agent for independent review
8. **Sync**: If deliverable status is Completed/Accepted and has customer/reuse value, knowledge-curator syncs it to Obsidian second brain

## Key Commands

```bash
# Validate repo structure, policies, and skill contracts
python3 tools/validate_repository.py

# Run tests (unit + integration)
python3 -m pytest tests/ -v

# Run a single test file
python3 -m pytest tests/test_convert_ctas_ddl_to_iceberg.py -v

# Run a specific test function
python3 -m pytest tests/test_generate_spark_view_artifacts.py::test_view_rewrite -v
```

## Architecture & Key Directories

```
.
├── AGENTS.md                      # Repository instructions & engineering rules
├── .claude/
│   ├── agents/                    # Subagents (quality-reviewer, knowledge-curator)
│   ├── rules/                     # Context rules (engineering-guardrails, output-optimization)
│   └── settings.json              # Hooks (e.g., Stop hook reminder)
│
├── ai_team/                       # Policies & role definitions
│   ├── roles/                     # 18 role definitions (data_engineer.md, etc.)
│   ├── professional_standards.md  # What "professional" means, what output to exclude
│   ├── role_scope_matrix.md       # Which roles handle which request types
│   ├── request_mode_policy.md     # How to classify requests into Professional Modes
│   ├── output_optimization_policy.md  # 3-tier output (A=always, B=conditional, C=request)
│   ├── professional_response_templates.md  # Required sections per mode
│   └── obsidian_write_policy.md   # When to sync deliverables to second brain
│
├── skills/                        # 18 specialized skill definitions
│   ├── skill-<role-name>/         # Each skill guides how that role operates
│   └── README.md                  # Skill index & activation rules
│
├── templates/                     # Templates for every deliverable type
│   ├── requirements_template.md
│   ├── basic_design_template.md
│   ├── data_pipeline_design_template.md
│   ├── test_plan_template.md
│   ├── professional_opinion_template.md
│   └── (35+ more templates)
│
├── input/                         # Requests, context, errors, code samples
├── output/                        # All deliverables: output/<client>/<YYYYMMDD>/<task>/
│   ├── deliverable_summary.md     # Control-panel summary (always created)
│   ├── <main-deliverable>.md
│   └── _internal/                 # Optional: reviews, plans, retrospectives
│
├── tests/                         # Unit & integration tests (pytest)
│   ├── test_convert_ctas_ddl_to_iceberg.py
│   └── test_generate_spark_view_artifacts.py
│
└── tools/
    └── validate_repository.py     # Validates skills, roles, workflows, templates
```

## Essential Policies

Before starting any work, familiarize yourself with:

- **AGENTS.md** — mission, required start/finish, engineering rules, writing style
- **role_scope_matrix.md** — which roles handle what (data engineer, platform engineer, sre, etc.)
- **request_mode_policy.md** — how to classify requests into Opinion/Design/Implementation/Verification
- **output_optimization_policy.md** — 3-tier output (A=always create, B=conditional on gates, C=request-only), lightweight request definition
- **professional_response_templates.md** — required sections per mode, section-trimming rules
- **professional_standards.md** — what counts as professional output, prohibited outputs (baseless opinions, unverified specs, unsupported claims)
- **role_scope_matrix.md** + role `.md` files — detailed scope, responsibilities, judgment criteria for each role

## Workflow: Request → Deliverable

1. **Identify the request** from `input/` or directly from Celes
   - What's the explicit ask? (opinion, design, implementation, verification)
   - What's the client/context?
   - Is there code, error, or constraint to work from?

2. **Classify the request**
   - Use `role_scope_matrix.md` to pick the owner role(s)
   - Use `request_mode_policy.md` to determine Professional Mode (Opinion/Design/Implementation/Verification)
   - Some requests are multi-role or multi-mode (e.g., "Design Opinion" = Opinion mode content from Design role)

3. **Assess scope using output_optimization_policy.md**
   - Is this a "lightweight request"? (single step, not customer deliverable, no production/security/breaking changes)
   - If lightweight: skip work plan, go straight to deliverable
   - If not lightweight + multi-step: create `output/<task>/_internal/work_plan.md` first

4. **Locate the skill**
   - Find `skills/skill-<role-name>/README.md`
   - Read the skill's guidance for that role's approach to this type of work

5. **Create the deliverable**
   - Save to `output/<client>/<YYYYMMDD>/<task-name>/`
   - Always create `deliverable_summary.md` (control-panel view: what was asked, what was done, status, next steps)
   - Create the main deliverable (`<name>.md`) using the appropriate template
   - Use `professional_response_templates.md` to include only relevant sections + mode-specific mandatory sections
   - See `ai_team/README.md` Required Finish section for exact structure

6. **Evaluate quality review trigger**
   - Use `output_optimization_policy.md` table: does this deliverable meet any quality review gate?
     - Customer deliverable?
     - Reusable across projects?
     - Production / breaking change?
     - Security impact?
   - If YES: invoke the **quality-reviewer** agent (independent, not self-review)
   - If NO: set `deliverable_summary.md` status to "Review Exempt" and continue

7. **Publish & sync**
   - If status is Completed/Accepted + has customer/reuse value: **knowledge-curator** will sync to Obsidian second brain
   - If status is Draft/In Progress/Waiting: knowledge-curator will NOT activate (safety guard)

## Quality Review & Professional Standards

**Professional Output Definition** (from `professional_standards.md`):
- All opinions are grounded in the role's expertise (not baseless sentiments like "looks good to me")
- Facts are verified (not assumed external specs or data)
- Every recommendation has a risk/tradeoff stated
- Claims about what someone should do name who's responsible
- Conclusions are traceable (what did you confirm vs. what did you assume?)

**Prohibited Outputs:**
- "そうだと思う" / "ありだと思う" (baseless opinion-phrasing)
- Unconditional agreement with Celes's proposal
- Unverified external specs ("The API docs say…" without checking)
- Unattributed risk statements ("This could break" without saying what/how)
- Advice without role clarity (who should do this?)
- Conclusions without trace (what was verified vs. assumed?)

**Self-Review is NOT independent review** — if you wrote the deliverable, you cannot review it. The quality-reviewer agent reviews independently.

## Quality Gates & .claude/ Auto-Injection

Recent work (June 2026) added Claude's 7-method framework:

- **Hooks** (`settings.json`): Stop hook reminds about deliverable_summary.md + Obsidian sync trigger
- **Subagents** (`.claude/agents/`): quality-reviewer, knowledge-curator run independently
- **Rules** (`.claude/rules/`): 
  - `engineering-guardrails.md` — always injected (7 rules + professional standards)
  - `output-optimization.md` — path-scoped to `output/**` (3-tier output rules)

These are auto-discovered by Claude Code; no explicit invocation needed.

## Testing

```bash
# Full test suite
python3 -m pytest tests/ -v

# With coverage
python3 -m pytest tests/ --cov=.

# Specific test
python3 -m pytest tests/test_split_table_statements.py::test_empty_string -v
```

Tests are split between unit (`test_*.py`) and integration (`*_integration.py`). Both run with pytest.

## Troubleshooting

- **Validation fails**: Run `python3 tools/validate_repository.py` to check for missing skills, roles, workflows, or templates
- **Role unclear**: Start with `role_scope_matrix.md` to map request type → roles
- **Mode unclear**: Check `request_mode_policy.md` examples
- **Output structure wrong**: See AGENTS.md "Required Finish" and `output_optimization_policy.md` for exact folder/file layout
- **Quality review confusion**: `output_optimization_policy.md` table lists all gates (customer/reuse/production/security)

## Notes for Future Instances

- This is NOT a task-runner service — you represent a professional role with judgment
- Don't agree unconditionally with Celes's proposal; push back if you see risks
- Always check existing `output/` before starting (may already be half-done)
- "Don't know" is acceptable; "don't know but I'll guess" is not (state assumptions explicitly)
- Professional delivery includes testing, error handling, and runbooks for production features — don't skip these for "MVP"
- If a deliverable doesn't meet its own completion criteria, don't mark it Completed; flag it as Waiting for Review or Rework Required
