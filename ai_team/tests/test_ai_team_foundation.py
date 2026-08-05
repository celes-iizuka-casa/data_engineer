from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_module(name: str, relative_path: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {relative_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("repository_validator", "tools/validate_repository.py")
evidence = load_module(
    "execution_evidence", "ai_team/evidence/new_execution_evidence.py"
)
foundation_evals = load_module(
    "foundation_evals", "ai_team/evals/run_foundation_evals.py"
)
documentation_targets = load_module(
    "documentation_targets",
    "ai_team/evals/select_documentation_review_targets.py",
)
documentation_review_validator = load_module(
    "documentation_review_validator",
    "ai_team/evals/validate_documentation_semantic_review.py",
)


class PrivacyBoundaryTests(unittest.TestCase):
    def test_private_path_classification(self) -> None:
        private = [
            "input/customer/request.md",
            "output/client/task/output.md",
            ".local/user_profile.yaml",
            "second_brain/private.md",
            "nested/_internal/review.md",
            "client/evidence/run.yaml",
            "nested/secrets/token.txt",
            "raw/evidence.json",
            "private/feedback.md",
            "feedback/review.md",
            "nested/raw_evidence/run.yaml",
            "nested/private_feedback/review.md",
            "nested/raw_feedback/comment.md",
            "credentials/aws/config",
            "tokens/access.txt",
            "secret/api.txt",
            "projects/customer/request.md",
            "ai_team/evidence/customer-run.yaml",
            "ai_team/evidence/client/run.yaml",
            "temp/work.txt",
            ".env.production",
            "config/credentials.json",
            "keys/id_rsa",
            "keys/client.pem",
            ".claude/settings.local.json",
        ]
        for path in private:
            with self.subTest(path=path):
                self.assertIsNotNone(validator.private_tracked_reason(path))

        allowed = [
            "input/README.md",
            "ai_team/evidence/execution_evidence.schema.json",
            "ai_team/evidence/new_execution_evidence.py",
            "templates/security_design_template.md",
        ]
        for path in allowed:
            with self.subTest(path=path):
                self.assertIsNone(validator.private_tracked_reason(path))

    def test_current_git_index_has_no_private_paths(self) -> None:
        result = validator.Validation()
        validator.validate_git_privacy(result, ROOT)
        self.assertEqual([], result.errors)

    def test_shared_readme_uses_only_anonymous_input_examples(self) -> None:
        text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("input/example-client/", text)
        self.assertIsNone(
            validator.PRIVATE_README_INPUT_EXAMPLE_PATTERN.search(text)
        )

    def test_extended_high_confidence_secret_patterns(self) -> None:
        samples = [
            "ASIA" + "ABCDEFGHIJKLMNOP",
            "github_pat_" + "A" * 40,
            "sk-proj-" + "A" * 40,
            "sk-ant-" + "A" * 40,
            "sk-" + "A" * 40,
            "-----BEGIN " + "DSA PRIVATE KEY-----",
        ]
        for sample in samples:
            with self.subTest(prefix=sample.split("_")[0]):
                self.assertTrue(
                    any(
                        pattern.search(sample)
                        for pattern in validator.SECRET_CONTENT_PATTERNS
                    )
                )

    def test_staged_provider_import_is_detected_after_worktree_is_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = root / "ai_team/evals/provider_probe.py"
            target.parent.mkdir(parents=True)
            target.write_text("import openai\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "ai_team/evals/provider_probe.py"],
                check=True,
            )
            target.write_text("def local_only():\n    return True\n", encoding="utf-8")
            result = validator.Validation()
            validator.validate_cross_provider_code(result, root)
            self.assertTrue(
                any(
                    "Git index: ai_team/evals/provider_probe.py" in item
                    for item in result.errors
                ),
                result.errors,
            )

    def test_staged_runtime_cli_launch_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = root / "tools/runtime_probe.sh"
            target.parent.mkdir(parents=True)
            target.write_text("codex exec unsafe-switch\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/runtime_probe.sh"],
                check=True,
            )
            target.write_text("exit 0\n", encoding="utf-8")
            result = validator.Validation()
            validator.validate_cross_provider_code(result, root)
            self.assertTrue(
                any(
                    "Git index: tools/runtime_probe.sh" in item
                    for item in result.errors
                ),
                result.errors,
            )

    def test_forced_add_of_ignored_unicode_path_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                (ROOT / ".gitignore").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            target = root / "output" / "顧客 data.txt"
            target.parent.mkdir(parents=True)
            target.write_text("private", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore"], check=True
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "-f", "output/顧客 data.txt"],
                check=True,
            )
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("output/顧客 data.txt" in item for item in result.errors)
            )

    def test_non_git_directory_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".gitignore").write_text(
                "\n".join(sorted(validator.REQUIRED_IGNORE_RULES)) + "\n",
                encoding="utf-8",
            )
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("fail closed" in item for item in result.errors)
            )

    def test_staged_secret_is_detected_after_worktree_is_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                "\n".join(sorted(validator.REQUIRED_IGNORE_RULES)) + "\n",
                encoding="utf-8",
            )
            target = root / "README.md"
            fake_key = "AKIA" + "ABCDEFGHIJKLMNOP"
            target.write_text(f"fake test key: {fake_key}\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "README.md"],
                check=True,
            )
            target.write_text("sanitized\n", encoding="utf-8")
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("Git index" in item and "README.md" in item for item in result.errors),
                result.errors,
            )

    def test_staged_personal_path_is_detected_after_worktree_is_sanitized(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                "\n".join(sorted(validator.REQUIRED_IGNORE_RULES)) + "\n",
                encoding="utf-8",
            )
            target = root / "README.md"
            personal_path = "/" + "Users" + "/alice/private-project\n"
            target.write_text(personal_path, encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "README.md"],
                check=True,
            )
            target.write_text("sanitized\n", encoding="utf-8")
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("Git index" in item and "personal absolute path" in item for item in result.errors),
                result.errors,
            )

    def test_staged_input_scaffold_bypass_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                (ROOT / ".gitignore").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            target = root / "input" / "README.md"
            target.parent.mkdir()
            target.write_text(
                "input/example-client/ はGit管理しない\nCLIENT-ALPHA payload\n",
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "input/README.md"],
                check=True,
            )
            target.write_text(
                (ROOT / "input" / "README.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("privacy-safe scaffold" in item for item in result.errors),
                result.errors,
            )

    def test_untracked_raw_evidence_is_detected_when_ignore_rule_drifts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            ignore_lines = [
                line
                for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
                if "evidence/" not in line
            ]
            (root / ".gitignore").write_text(
                "\n".join(ignore_lines) + "\n", encoding="utf-8"
            )
            target = root / "ai_team" / "evidence" / "customer-run.yaml"
            target.parent.mkdir(parents=True)
            target.write_text("customer: private\n", encoding="utf-8")
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any(
                    "Untracked private candidate" in item
                    and "ai_team/evidence/customer-run.yaml" in item
                    for item in result.errors
                ),
                result.errors,
            )

    def test_staged_weak_gitignore_bypass_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = root / ".gitignore"
            target.write_text("*.log\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", ".gitignore"], check=True)
            target.write_text(
                "\n".join(sorted(validator.REQUIRED_IGNORE_RULES)) + "\n",
                encoding="utf-8",
            )
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any("Missing privacy ignore rule" in item for item in result.errors),
                result.errors,
            )

    def test_staged_gitignore_negation_override_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            unsafe_ignore = (
                (ROOT / ".gitignore").read_text(encoding="utf-8")
                + "\n!/output/**\n!/secrets/**\n"
            )
            (root / ".gitignore").write_text(unsafe_ignore, encoding="utf-8")
            input_readme = root / "input" / "README.md"
            input_readme.parent.mkdir()
            input_readme.write_text(
                (ROOT / "input" / "README.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            subprocess.run(
                ["git", "-C", str(root), "add", ".gitignore", "input/README.md"],
                check=True,
            )
            (root / ".gitignore").write_text(
                (ROOT / ".gitignore").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any(
                    "Unsafe .gitignore negation in Git index" in item
                    or "Git index .gitignore exposes private sentinel" in item
                    for item in result.errors
                ),
                result.errors,
            )

    def test_deletion_only_stage_activates_index_privacy_scan(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            (root / ".gitignore").write_text(
                (ROOT / ".gitignore").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            input_readme = root / "input" / "README.md"
            input_readme.parent.mkdir()
            input_readme.write_text(
                (ROOT / "input" / "README.md").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            unsafe = root / "README.md"
            unsafe.write_text(
                "/" + "Users" + "/alice/private-project\n", encoding="utf-8"
            )
            removed = root / "remove-me.txt"
            removed.write_text("remove\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(root), "-c", "user.name=Test",
                    "-c", "user.email=test@example.invalid", "commit", "-q",
                    "-m", "fixture",
                ],
                check=True,
            )
            unsafe.write_text("sanitized\n", encoding="utf-8")
            removed.unlink()
            subprocess.run(
                ["git", "-C", str(root), "add", "remove-me.txt"], check=True
            )
            self.assertEqual({"remove-me.txt"}, set(validator.git_staged_files(root)))
            result = validator.Validation()
            validator.validate_git_privacy(result, root)
            self.assertTrue(
                any(
                    "Git index" in item and "personal absolute path" in item
                    for item in result.errors
                ),
                result.errors,
            )


class ExecutionEvidenceTests(unittest.TestCase):
    def test_skill_revision_is_content_addressed(self) -> None:
        first = evidence.skill_revision("skill-tech-lead", ROOT)
        second = evidence.skill_revision("skill-tech-lead", ROOT)
        self.assertEqual(first, second)
        self.assertRegex(first or "", r"^sha256:[0-9a-f]{64}$")

    def test_role_revision_is_content_addressed(self) -> None:
        first = validator.role_content_revision("tech_lead", ROOT)
        second = validator.role_content_revision("tech_lead", ROOT)
        self.assertEqual(first, second)
        self.assertRegex(first or "", r"^sha256:[0-9a-f]{64}$")

    def test_role_revision_includes_shared_common_contract(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            capability_target = root / "ai_team/capability_registry.yaml"
            role_target = root / "ai_team/roles/tech_lead.md"
            role_target.parent.mkdir(parents=True)
            capability_target.write_text(
                (ROOT / "ai_team/capability_registry.yaml").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            role_target.write_text(
                (ROOT / "ai_team/roles/tech_lead.md").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            before = validator.role_content_revision("tech_lead", root)
            data = yaml.safe_load(capability_target.read_text(encoding="utf-8"))
            data["common_contract"]["required_evidence"].append(
                "shared_contract_revision_probe"
            )
            capability_target.write_text(
                yaml.safe_dump(data, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )
            after = validator.role_content_revision("tech_lead", root)
            self.assertNotEqual(before, after)

    def test_shared_candidate_revision_is_deterministic(self) -> None:
        first = evidence.shared_candidate_revision(ROOT)
        second = evidence.shared_candidate_revision(ROOT)
        self.assertEqual(first, second)
        self.assertRegex(first, r"^sha256:[0-9a-f]{64}$")

    def test_context_values_cannot_guess_availability(self) -> None:
        self.assertEqual(
            {"value": None, "evidence_type": "unavailable"},
            evidence.context_value(None, "unavailable"),
        )
        with self.assertRaises(ValueError):
            evidence.context_value(None, "observed")
        with self.assertRaises(ValueError):
            evidence.context_value("model-x", "unavailable")

    def test_repository_local_evidence_must_stay_private(self) -> None:
        private = evidence.private_output_path(
            ROOT / ".local" / "evidence" / "run.yaml", ROOT
        )
        self.assertEqual(
            (ROOT / ".local" / "evidence" / "run.yaml").resolve(), private
        )
        with self.assertRaises(ValueError):
            evidence.private_output_path(ROOT / "ai_team" / "run.yaml", ROOT)
        with self.assertRaises(ValueError):
            evidence.private_output_path(ROOT / ".local" / "run.yaml", ROOT)
        with self.assertRaises(ValueError):
            evidence.private_output_path(Path("/tmp/raw-evidence.yaml"), ROOT)

    def test_private_evidence_is_exclusive_and_mode_0600(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            target = evidence.private_output_path(
                root / ".local" / "evidence" / "run.yaml", root
            )
            evidence.write_private_evidence(target, {"safe": True})
            self.assertEqual(0o600, os.stat(target).st_mode & 0o777)
            with self.assertRaises(FileExistsError):
                evidence.write_private_evidence(target, {"safe": False})

    def test_symlink_escape_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as repository_directory:
            with tempfile.TemporaryDirectory() as external_directory:
                root = Path(repository_directory)
                evidence_dir = root / ".local" / "evidence"
                evidence_dir.mkdir(parents=True)
                (evidence_dir / "escape").symlink_to(
                    Path(external_directory), target_is_directory=True
                )
                with self.assertRaises(ValueError):
                    evidence.private_output_path(
                        evidence_dir / "escape" / "run.yaml", root
                    )

    def test_generated_evidence_marks_unknown_measurements_unavailable(self) -> None:
        args = argparse.Namespace(
            task_id="test-1",
            task_type="verification",
            request_mode="verify",
            agent=["qa_test_automation_engineer"],
            skill=["skill-qa-test-automation-engineer"],
            result_status="in_progress",
            runtime="Codex",
            runtime_evidence="observed",
            provider=None,
            provider_evidence="unavailable",
            model=None,
            model_evidence="unavailable",
            effort="high",
            effort_evidence="declared",
            token_usage=None,
            token_usage_evidence="unavailable",
            cost=None,
            cost_evidence="unavailable",
        )
        result = evidence.build_evidence(args, ROOT)
        self.assertEqual([], evidence.validate_evidence_document(result))
        self.assertIsNone(result["execution_context"]["token_usage"]["value"])
        self.assertEqual(
            "unavailable",
            result["execution_context"]["cost"]["evidence_type"],
        )
        self.assertRegex(
            result["skills"][0]["revision"], r"^sha256:[0-9a-f]{64}$"
        )
        invalid = copy.deepcopy(result)
        invalid["execution_context"]["model"] = {
            "value": None,
            "evidence_type": "observed",
        }
        self.assertTrue(evidence.validate_evidence_document(invalid))

        invalid_skill = copy.deepcopy(result)
        invalid_skill["skills"][0]["id"] = ""
        self.assertIn(
            "every Skill must have a non-empty id",
            evidence.validate_evidence_document(invalid_skill),
        )

        schema_mismatch_cases = []
        skill_extra = copy.deepcopy(result)
        skill_extra["skills"][0]["extra"] = "unexpected"
        schema_mismatch_cases.append(skill_extra)
        token_bool = copy.deepcopy(result)
        token_bool["execution_context"]["token_usage"] = {
            "value": True,
            "evidence_type": "observed",
        }
        schema_mismatch_cases.append(token_bool)
        score_bool = copy.deepcopy(result)
        score_bool["quality"]["score"] = True
        schema_mismatch_cases.append(score_bool)
        tests_non_string = copy.deepcopy(result)
        tests_non_string["tests"]["executed"] = [1]
        schema_mismatch_cases.append(tests_non_string)
        date_only = copy.deepcopy(result)
        date_only["task"]["timestamp"] = "2026-07-14"
        schema_mismatch_cases.append(date_only)
        space_separated_timestamp = copy.deepcopy(result)
        space_separated_timestamp["task"]["timestamp"] = (
            "2026-07-14 12:30:00+00:00"
        )
        schema_mismatch_cases.append(space_separated_timestamp)
        for invalid_case in schema_mismatch_cases:
            self.assertTrue(evidence.validate_evidence_document(invalid_case))

        invalid_second_brain = copy.deepcopy(result)
        invalid_second_brain["second_brain"] = {
            "available": False,
            "used": True,
            "source_scope": None,
        }
        self.assertTrue(evidence.validate_evidence_document(invalid_second_brain))


class FoundationContractTests(unittest.TestCase):
    def test_deterministic_foundation_eval_passes(self) -> None:
        result = foundation_evals.run(ROOT)
        self.assertEqual("PASS", result["verdict"], result["results"])
        self.assertEqual(result["total"], result["passed"])
        self.assertEqual("FOUNDATION_CONTRACT", result["verdict_scope"])
        self.assertEqual("UNKNOWN", result["capability_effectiveness"]["status"])

    def test_before_after_comparison_uses_same_contract(self) -> None:
        result = foundation_evals.compare(
            ROOT, ROOT, "baseline-test", "candidate-test"
        )
        self.assertEqual("PASS", result["verdict"])
        self.assertTrue(result["same_contract_before_after"])
        self.assertEqual(
            "SAME_CONTRACT_FOUNDATION_REPLAY", result["comparison_kind"]
        )
        self.assertEqual([], result["regressions"])
        self.assertEqual("UNKNOWN", result["capability_effectiveness"]["status"])

    def test_foundation_contract_digest_covers_non_runner_assets(self) -> None:
        self.assertIn(
            "ai_team/evals/select_documentation_review_targets.py",
            foundation_evals.FOUNDATION_CONTRACT_FILES,
        )
        self.assertIn(
            "ai_team/governance/documentation_quality_policy.yaml",
            foundation_evals.FOUNDATION_CONTRACT_FILES,
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog = root / "ai_team/evals/eval_catalog.yaml"
            catalog.parent.mkdir(parents=True)
            catalog.write_text("schema_version: '1.0'\n", encoding="utf-8")
            before = foundation_evals.foundation_contract_revision(root)
            catalog.write_text("schema_version: '1.1'\n", encoding="utf-8")
            after = foundation_evals.foundation_contract_revision(root)
            self.assertNotEqual(before, after)

    def test_capability_and_skill_sets_match_repository(self) -> None:
        capability = yaml.safe_load(
            (ROOT / "ai_team/capability_registry.yaml").read_text(encoding="utf-8")
        )
        lifecycle = yaml.safe_load(
            (ROOT / "ai_team/governance/skill_lifecycle_registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        capability_role_ids = {item["id"] for item in capability["roles"]}
        self.assertLessEqual(set(validator.ROLES), capability_role_ids)
        self.assertEqual(
            set(validator.SKILLS), {item["id"] for item in lifecycle["skills"]}
        )
        for item in lifecycle["skills"]:
            with self.subTest(skill=item["id"]):
                self.assertEqual("ACTIVE", item["state"])
                self.assertIn(item["disposition"], {"UPDATE", "CREATE"})
                self.assertEqual(
                    validator.skill_content_revision(item["id"], ROOT),
                    item["candidate_revision"],
                )
                if item["candidate_state"] == "ACTIVE":
                    self.assertEqual(
                        validator.skill_content_revision(item["id"], ROOT),
                        item["active_revision"],
                    )
                    self.assertEqual(
                        "promoted", item["transition"]["human_gate_status"]
                    )
                else:
                    self.assertIn(
                        item["candidate_state"], {"CANDIDATE", "HUMAN_GATE"}
                    )
                    self.assertEqual(
                        validator.skill_head_revision(item["id"], ROOT),
                        item["active_revision"],
                    )
                    self.assertEqual(
                        "pending", item["transition"]["human_gate_status"]
                    )
        self.assertIsNone(lifecycle["current_candidate_decision"])
        decision = lifecycle["last_promotion_decision"]
        self.assertEqual("Celes", decision["decided_by"])
        self.assertEqual("PROMOTE", decision["decision"])
        self.assertGreaterEqual(len(lifecycle["promotion_history"]), 2)
        self.assertEqual(decision, lifecycle["promotion_history"][-1])

    def test_ai_employee_lifecycle_covers_all_roles_without_fake_scores(self) -> None:
        lifecycle = yaml.safe_load(
            (
                ROOT
                / "ai_team/governance/ai_employee_lifecycle_registry.yaml"
            ).read_text(encoding="utf-8")
        )
        capability = yaml.safe_load(
            (ROOT / "ai_team/capability_registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            {item["id"] for item in capability["roles"]},
            {item["id"] for item in lifecycle["roles"]},
        )
        self.assertLessEqual(
            set(validator.ROLES), {item["id"] for item in lifecycle["roles"]}
        )
        self.assertEqual(
            {"CREATE", "KEEP", "UPDATE", "MERGE", "SPLIT", "DEPRECATE", "UNKNOWN"},
            set(lifecycle["dispositions"]),
        )
        lifecycle_states = set(lifecycle["lifecycle_states"])
        dispositions = set(lifecycle["dispositions"])
        decision_history = lifecycle["decision_history"]
        for item in lifecycle["roles"]:
            with self.subTest(role=item["id"]):
                self.assertIn(item["state"], lifecycle_states)
                self.assertIn(item["disposition"], dispositions)
                self.assertIn(
                    item["effectiveness"],
                    {"not_evaluated", "baseline_pending", "evaluated"},
                )
                self.assertNotIn("score", item)
                self.assertEqual(
                    item["candidate_revision"] is None,
                    item["candidate_state"] is None,
                )
                if item["candidate_revision"] is None:
                    self.assertIn(item["state"], {"ACTIVE", "DEPRECATED"})
                    self.assertNotIn("transition", item)
                else:
                    self.assertIn(item["candidate_state"], lifecycle_states)
                    self.assertIsInstance(item.get("transition"), dict)
                    self.assertEqual(
                        [],
                        validator.ai_employee_transition_failures(
                            item, decision_history
                        ),
                    )

    def test_ai_employee_transition_rejects_pending_gate_bypass(self) -> None:
        revision = "sha256:" + "a" * 64
        candidate = {
            "id": "backend_engineer",
            "state": "ACTIVE",
            "active_revision": "sha256:" + "b" * 64,
            "candidate_revision": revision,
            "candidate_state": "HUMAN_GATE",
            "transition": {
                "from_state": "ACTIVE",
                "from_revision": "sha256:" + "b" * 64,
                "to_state": "HUMAN_GATE",
                "candidate_revision": revision,
                "evidence_refs": [""],
                "before_after_eval_ref": "local-eval:before-after",
                "independent_review_ref": " pending ",
                "human_gate_status": "pending",
                "celes_human_gate_ref": " pending ",
            },
        }
        self.assertIn(
            "missing_independent_review",
            validator.ai_employee_transition_failures(candidate, []),
        )
        self.assertIn(
            "missing_evidence_refs",
            validator.ai_employee_transition_failures(candidate, []),
        )
        self.assertIn(
            "premature_celes_gate_ref",
            validator.ai_employee_transition_failures(candidate, []),
        )

    def test_ai_employee_active_promotion_requires_matching_celes_record(self) -> None:
        revision = "sha256:" + "a" * 64
        candidate = {
            "id": "backend_engineer",
            "state": "ACTIVE",
            "active_revision": revision,
            "disposition": "UPDATE",
            "candidate_revision": revision,
            "candidate_state": "ACTIVE",
            "transition": {
                "from_state": "ACTIVE",
                "from_revision": "sha256:" + "b" * 64,
                "to_state": "ACTIVE",
                "candidate_revision": revision,
                "evidence_refs": ["local-evidence:role-candidate"],
                "before_after_eval_ref": "local-eval:before-after",
                "independent_review_ref": "local-review:independent",
                "human_gate_status": "promoted",
                "celes_human_gate_ref": "Celes-HG-ROLE-001",
            },
        }
        self.assertIn(
            "missing_unique_decision_history",
            validator.ai_employee_transition_failures(candidate, []),
        )
        history = [
            {
                "gate_id": "Celes-HG-ROLE-001",
                "subject_id": "backend_engineer",
                "from_revision": "sha256:" + "b" * 64,
                "subject_revision": revision,
                "target_state": "ACTIVE",
                "disposition": "UPDATE",
                "decision": "PROMOTE",
                "before_after_eval_ref": "local-eval:before-after",
                "independent_review_ref": "local-review:independent",
                "evidence_refs": ["local-evidence:role-candidate"],
            }
        ]
        self.assertEqual(
            [], validator.ai_employee_transition_failures(candidate, history)
        )
        bypass = copy.deepcopy(candidate)
        bypass["transition"]["evidence_refs"] = [""]
        bypass["transition"]["before_after_eval_ref"] = " pending "
        bypass["transition"]["independent_review_ref"] = " pending "
        bypass["transition"]["celes_human_gate_ref"] = " pending "
        bypass_history = [
            {
                "gate_id": " pending ",
                "subject_id": "backend_engineer",
                "from_revision": "sha256:" + "b" * 64,
                "subject_revision": revision,
                "target_state": "ACTIVE",
                "disposition": "UPDATE",
                "decision": "PROMOTE",
                "before_after_eval_ref": " pending ",
                "independent_review_ref": " pending ",
                "evidence_refs": [""],
            }
        ]
        self.assertEqual(
            {
                "missing_before_after_eval",
                "missing_celes_gate_ref",
                "missing_evidence_refs",
                "missing_independent_review",
            },
            set(
                validator.ai_employee_transition_failures(
                    bypass, bypass_history
                )
            ),
        )

    def test_ai_employee_create_reject_and_rollback_paths_are_reachable(self) -> None:
        candidate_revision = "sha256:" + "a" * 64
        active_revision = "sha256:" + "b" * 64
        create = {
            "id": "new_specialist",
            "state": "DISCOVERED",
            "active_revision": None,
            "candidate_revision": candidate_revision,
            "candidate_state": "PROPOSED",
            "transition": {
                "from_state": "DISCOVERED",
                "from_revision": None,
                "to_state": "PROPOSED",
                "candidate_revision": candidate_revision,
                "evidence_refs": ["local-evidence:new-role-gap"],
                "before_after_eval_ref": "pending",
                "independent_review_ref": "pending",
                "human_gate_status": "pending",
                "celes_human_gate_ref": "pending",
            },
        }
        self.assertEqual(
            [], validator.ai_employee_transition_failures(create, [])
        )

        rejected = copy.deepcopy(create)
        rejected.update(
            {
                "id": "backend_engineer",
                "state": "ACTIVE",
                "active_revision": active_revision,
                "disposition": "UPDATE",
                "candidate_state": "HUMAN_GATE",
            }
        )
        rejected["transition"].update(
            {
                "from_state": "ACTIVE",
                "from_revision": active_revision,
                "to_state": "HUMAN_GATE",
                "before_after_eval_ref": "local-eval:role",
                "independent_review_ref": "local-review:role",
                "human_gate_status": "rejected",
                "celes_human_gate_ref": "Celes-HG-REJECT-001",
            }
        )
        reject_history = [
            {
                "gate_id": "Celes-HG-REJECT-001",
                "subject_id": "backend_engineer",
                "from_revision": active_revision,
                "subject_revision": candidate_revision,
                "target_state": "HUMAN_GATE",
                "disposition": "UPDATE",
                "decision": "REJECT",
                "before_after_eval_ref": "local-eval:role",
                "independent_review_ref": "local-review:role",
                "evidence_refs": ["local-evidence:new-role-gap"],
            }
        ]
        self.assertEqual(
            [],
            validator.ai_employee_transition_failures(
                rejected, reject_history
            ),
        )

        rollback = copy.deepcopy(rejected)
        rollback.update(
            {
                "state": "ACTIVE",
                "active_revision": candidate_revision,
                "candidate_state": "ACTIVE",
            }
        )
        rollback["transition"].update(
            {
                "to_state": "ACTIVE",
                "human_gate_status": "rolled_back",
                "celes_human_gate_ref": "Celes-HG-ROLLBACK-001",
            }
        )
        rollback_decision = {
            "gate_id": "Celes-HG-ROLLBACK-001",
            "subject_id": "backend_engineer",
            "from_revision": active_revision,
            "subject_revision": candidate_revision,
            "target_state": "ACTIVE",
            "disposition": "UPDATE",
            "decision": "ROLLBACK",
            "before_after_eval_ref": "local-eval:role",
            "independent_review_ref": "local-review:role",
            "evidence_refs": ["local-evidence:new-role-gap"],
            "promoted_revision": active_revision,
            "rollback_revision": candidate_revision,
            "reason": "regression evidence",
            "celes_decision": "ROLLBACK",
        }
        rollback_history = [
            {
                "gate_id": "Celes-HG-PROMOTE-PRIOR",
                "subject_id": "backend_engineer",
                "subject_revision": active_revision,
                "decision": "PROMOTE",
            },
            rollback_decision,
        ]
        self.assertEqual(
            [],
            validator.ai_employee_transition_failures(
                rollback, rollback_history
            ),
        )
        rollback_decision["rollback_revision"] = active_revision
        self.assertIn(
            "rollback_revision_mismatch",
            validator.ai_employee_transition_failures(
                rollback, rollback_history
            ),
        )

    def test_ai_employee_decision_history_is_append_only(self) -> None:
        committed = [{"gate_id": "HG-1", "decision": "PROMOTE"}]
        self.assertEqual(
            [],
            validator.missing_historical_decisions(
                committed + [{"gate_id": "HG-2", "decision": "REJECT"}],
                committed,
            ),
        )
        mutated = [{"gate_id": "HG-1", "decision": "REWORK"}]
        self.assertEqual(
            committed,
            validator.missing_historical_decisions(mutated, committed),
        )
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = (
                root
                / "ai_team/governance/ai_employee_lifecycle_registry.yaml"
            )
            target.parent.mkdir(parents=True)
            target.write_text(
                yaml.safe_dump({"decision_history": committed}),
                encoding="utf-8",
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(root), "-c", "user.name=Test",
                    "-c", "user.email=test@example.invalid", "commit", "-q",
                    "-m", "decision-history-fixture",
                ],
                check=True,
            )
            history = validator.historical_role_decision_records(root)
            self.assertEqual(committed, history)
            self.assertEqual(
                committed,
                validator.missing_historical_decisions([], history),
            )

    def test_ai_employee_canonical_change_requires_registered_candidate(self) -> None:
        head_revision = "sha256:" + "a" * 64
        current_revision = "sha256:" + "b" * 64
        entry = {"candidate_revision": None}
        self.assertEqual(
            ["unregistered_canonical_change"],
            validator.role_candidate_registration_failures(
                entry, current_revision, head_revision
            ),
        )
        entry["candidate_revision"] = current_revision
        self.assertEqual(
            [],
            validator.role_candidate_registration_failures(
                entry, current_revision, head_revision
            ),
        )
        self.assertEqual(
            ["candidate_without_revision_change"],
            validator.role_candidate_registration_failures(
                {"candidate_revision": head_revision},
                head_revision,
                head_revision,
            ),
        )
        self.assertEqual(
            [],
            validator.role_candidate_registration_failures(
                {
                    "candidate_revision": head_revision,
                    "candidate_state": "ACTIVE",
                },
                head_revision,
                head_revision,
                {
                    "state": "ACTIVE",
                    "candidate_revision": head_revision,
                },
            ),
        )

    def test_ai_employee_registry_state_change_requires_final_candidate(self) -> None:
        previous = {
            "state": "ACTIVE",
            "active_revision": "sha256:" + "a" * 64,
        }
        direct = {
            "state": "DEPRECATED",
            "candidate_revision": None,
            "candidate_state": None,
        }
        self.assertEqual(
            ["unregistered_state_change"],
            validator.role_registry_state_failures(direct, previous),
        )
        governed = {
            "state": "DEPRECATED",
            "candidate_revision": "sha256:" + "b" * 64,
            "candidate_state": "DEPRECATED",
            "transition": {
                "from_state": "ACTIVE",
                "human_gate_status": "promoted",
            },
        }
        self.assertEqual(
            [], validator.role_registry_state_failures(governed, previous)
        )
        governed["transition"]["from_state"] = "DISCOVERED"
        self.assertEqual(
            ["from_state_history_mismatch"],
            validator.role_registry_state_failures(governed, previous),
        )

    def test_ai_employee_noop_update_cannot_be_promoted(self) -> None:
        revision = "sha256:" + "a" * 64
        changed_revision = "sha256:" + "b" * 64
        previous = {
            "state": "ACTIVE",
            "active_revision": revision,
            "candidate_revision": None,
        }
        no_op = {
            "state": "ACTIVE",
            "disposition": "UPDATE",
            "candidate_revision": revision,
            "candidate_state": "ACTIVE",
        }
        self.assertEqual(
            ["candidate_without_revision_change"],
            validator.role_candidate_registration_failures(
                no_op, revision, revision, previous
            ),
        )
        self.assertEqual(
            ["unregistered_canonical_change"],
            validator.role_candidate_registration_failures(
                {"candidate_revision": None},
                changed_revision,
                changed_revision,
                previous,
            ),
        )
        previous["candidate_revision"] = revision
        self.assertEqual(
            [],
            validator.role_candidate_registration_failures(
                no_op, revision, revision, previous
            ),
        )

        no_op_transition = {
            "id": "backend_engineer",
            "state": "ACTIVE",
            "active_revision": revision,
            "disposition": "UPDATE",
            "candidate_revision": revision,
            "candidate_state": "ACTIVE",
            "transition": {
                "from_state": "ACTIVE",
                "from_revision": revision,
                "to_state": "ACTIVE",
                "candidate_revision": revision,
                "evidence_refs": ["local-evidence:no-op"],
                "before_after_eval_ref": "local-eval:no-op",
                "independent_review_ref": "local-review:no-op",
                "human_gate_status": "promoted",
                "celes_human_gate_ref": "Celes-HG-NOOP",
            },
        }
        self.assertIn(
            "noop_candidate_revision",
            validator.ai_employee_transition_failures(no_op_transition, []),
        )

    def test_ai_employee_postcommit_uses_prior_registry_snapshot(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            target = (
                root
                / "ai_team/governance/ai_employee_lifecycle_registry.yaml"
            )
            target.parent.mkdir(parents=True)
            baseline = {
                "roles": [
                    {
                        "id": "backend_engineer",
                        "state": "ACTIVE",
                        "active_revision": "sha256:" + "a" * 64,
                        "candidate_revision": None,
                    }
                ]
            }
            target.write_text(
                yaml.safe_dump(baseline), encoding="utf-8"
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(root), "-c", "user.name=Test",
                    "-c", "user.email=test@example.invalid", "commit", "-q",
                    "-m", "baseline-registry",
                ],
                check=True,
            )
            candidate = copy.deepcopy(baseline)
            candidate["roles"][0]["state"] = "DEPRECATED"
            target.write_text(
                yaml.safe_dump(candidate), encoding="utf-8"
            )
            self.assertEqual(
                "ACTIVE",
                validator.role_lifecycle_previous_entries(root)
                ["backend_engineer"]["state"],
            )
            subprocess.run(["git", "-C", str(root), "add", "."], check=True)
            subprocess.run(
                [
                    "git", "-C", str(root), "-c", "user.name=Test",
                    "-c", "user.email=test@example.invalid", "commit", "-q",
                    "-m", "candidate-registry",
                ],
                check=True,
            )
            self.assertEqual(
                "ACTIVE",
                validator.role_lifecycle_previous_entries(root)
                ["backend_engineer"]["state"],
            )

    def test_ai_employee_create_requires_all_concrete_criteria(self) -> None:
        entry = {"disposition": "CREATE"}
        self.assertEqual(
            ["incomplete_create_criteria"],
            validator.role_create_criteria_failures(entry),
        )
        entry["create_criteria"] = {
            requirement: f"local-evidence:{requirement}"
            for requirement in validator.ROLE_CREATE_REQUIREMENTS
        }
        self.assertEqual([], validator.role_create_criteria_failures(entry))
        entry["create_criteria"][next(iter(validator.ROLE_CREATE_REQUIREMENTS))] = (
            " pending "
        )
        self.assertEqual(
            ["placeholder_create_evidence"],
            validator.role_create_criteria_failures(entry),
        )

    def test_ai_employee_post_baseline_role_can_be_updated(self) -> None:
        """A Role created after the baseline must not be locked into CREATE.

        ``ROLE_LIFECYCLE_BASELINE_REVISIONS`` is a frozen snapshot, so a Role
        added later has no baseline entry. Keying the disposition allowlist on
        that map alone made every such Role permanently CREATE-only, and CREATE
        demands ``from_revision: null`` while the historical continuity check
        demands the prior ``active_revision`` — an unsatisfiable pair.
        """
        established = "sha256:" + "c" * 64
        candidate = "sha256:" + "d" * 64
        self.assertEqual(
            {"CREATE", "UNKNOWN"}, validator.role_allowed_dispositions(None)
        )
        self.assertIn("UPDATE", validator.role_allowed_dispositions(established))
        self.assertNotIn(
            "CREATE", validator.role_allowed_dispositions(established)
        )
        for role_id in validator.ROLE_LIFECYCLE_BASELINE_REVISIONS:
            self.assertIn(
                "UPDATE",
                validator.role_allowed_dispositions(
                    validator.ROLE_LIFECYCLE_BASELINE_REVISIONS[role_id]
                ),
            )
        update = {
            "id": "capability_architect",
            "state": "ACTIVE",
            "active_revision": candidate,
            "disposition": "UPDATE",
            "candidate_revision": candidate,
            "candidate_state": "ACTIVE",
            "transition": {
                "from_state": "ACTIVE",
                "from_revision": established,
                "to_state": "ACTIVE",
                "candidate_revision": candidate,
                "evidence_refs": ["local-evidence:post-baseline-update"],
                "before_after_eval_ref": "local-eval:post-baseline-update",
                "independent_review_ref": "local-review:post-baseline-update",
                "human_gate_status": "promoted",
                "celes_human_gate_ref": "Celes-HG-POST-BASELINE-UPDATE",
            },
        }
        history = [
            {
                "gate_id": "Celes-HG-POST-BASELINE-UPDATE",
                "subject_id": "capability_architect",
                "from_revision": established,
                "subject_revision": candidate,
                "target_state": "ACTIVE",
                "disposition": "UPDATE",
                "decision": "PROMOTE",
                "before_after_eval_ref": "local-eval:post-baseline-update",
                "independent_review_ref": "local-review:post-baseline-update",
                "evidence_refs": ["local-evidence:post-baseline-update"],
            }
        ]
        self.assertEqual(
            [], validator.ai_employee_transition_failures(update, history)
        )
        self.assertEqual([], validator.role_create_criteria_failures(update))
        self.assertEqual(
            [],
            validator.role_registry_state_failures(
                update, {"state": "ACTIVE", "active_revision": established}
            ),
        )

    def test_disposition_eligibility_is_wired_into_full_validation(self) -> None:
        """The disposition allowlist must be load-bearing in the real validator run.

        ``test_ai_employee_post_baseline_role_can_be_updated`` only exercises
        ``role_allowed_dispositions`` in isolation, so reverting its call site
        leaves the whole suite green. This drives the full script end to end
        against a clone whose worktree differs from HEAD -- the only state in
        which ``role_lifecycle_previous_entries`` yields a non-null
        ``established_revision`` for a post-baseline Role.
        """
        role_id = "capability_architect"
        registry_relative = "ai_team/governance/ai_employee_lifecycle_registry.yaml"
        failure = f"AI Employee candidate lacks change disposition: {role_id}"

        def run_validator(root: Path) -> str:
            completed = subprocess.run(
                ["python3", "tools/validate_repository.py"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            return completed.stdout + completed.stderr

        def load_entry(registry: Path) -> tuple[dict, dict]:
            data = yaml.safe_load(registry.read_text(encoding="utf-8"))
            for candidate in data["roles"]:
                if candidate.get("id") == role_id:
                    return data, candidate
            raise AssertionError(f"{role_id} is absent from the lifecycle registry")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "clone"
            subprocess.run(
                ["git", "clone", "--quiet", "--local", str(ROOT), str(root)],
                check=True,
                capture_output=True,
            )
            # The clone carries committed history (which supplies the previous
            # registry snapshot) but committed *code*. Overwrite the script with
            # the working tree's copy so the run exercises the validator under
            # test rather than whatever is on HEAD.
            script_relative = "tools/validate_repository.py"
            (root / script_relative).write_bytes(
                (ROOT / script_relative).read_bytes()
            )
            registry = root / registry_relative
            data, entry = load_entry(registry)
            established = entry["active_revision"]
            self.assertIsNotNone(
                established,
                "fixture requires a committed active_revision for the Role",
            )

            # (a) CREATE on a Role that already has an established revision.
            entry["disposition"] = "CREATE"
            entry["candidate_revision"] = established
            entry["candidate_state"] = "ACTIVE"
            entry["create_criteria"] = {
                requirement: f"local-evidence:phase-d-fixture#{requirement}"
                for requirement in validator.ROLE_CREATE_REQUIREMENTS
            }
            entry["transition"] = {
                "from_state": "PROPOSED",
                "from_revision": None,
                "to_state": "ACTIVE",
                "candidate_revision": established,
                "evidence_refs": ["local-evidence:phase-d-fixture#create"],
                "before_after_eval_ref": "local-evidence:phase-d-fixture#eval",
                "independent_review_ref": "local-review:phase-d-fixture#review",
                "human_gate_status": "promoted",
                "celes_human_gate_ref": "Celes-HG-PHASE-D-FIXTURE",
            }
            registry.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            self.assertIn(failure, run_validator(root))

            # (b) UPDATE on the same Role, continuing from the established revision.
            data, entry = load_entry(registry)
            entry["disposition"] = "UPDATE"
            entry.pop("create_criteria", None)
            entry["transition"]["from_state"] = "ACTIVE"
            entry["transition"]["from_revision"] = established
            registry.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            self.assertNotIn(failure, run_validator(root))

    def test_active_revision_expected_branch_is_wired_into_full_validation(self) -> None:
        """The ``expected_active`` branch keyed on ``established_revision`` must be
        load-bearing in the real validator run, not just in the disposition check.

        The Phase B fix touches two call sites: the disposition allowlist
        (``role_allowed_dispositions(established_revision)``, covered by
        ``test_disposition_eligibility_is_wired_into_full_validation``) and the
        ``expected_active`` branch (``elif established_revision is None:``). A
        post-baseline Role with an established revision and a *pending*
        (non-final) candidate is the only state where the two conditions
        (``established_revision is None`` vs. the pre-fix ``baseline_revision is
        None``) disagree: reverting the branch back to ``baseline_revision``
        makes it treat the candidate as if no prior revision existed, so
        ``expected_active`` collapses to ``None`` while ``active_revision`` still
        holds the real committed revision, producing an
        ``AI Employee active revision drift`` failure the fixed code does not
        raise.
        """
        role_id = "capability_architect"
        registry_relative = "ai_team/governance/ai_employee_lifecycle_registry.yaml"
        role_relative = f"ai_team/roles/{role_id}.md"
        drift_marker = f"AI Employee active revision drift: {role_id}"

        def run_validator(root: Path) -> str:
            completed = subprocess.run(
                ["python3", "tools/validate_repository.py"],
                cwd=root,
                capture_output=True,
                text=True,
            )
            return completed.stdout + completed.stderr

        def load_entry(registry: Path) -> tuple[dict, dict]:
            data = yaml.safe_load(registry.read_text(encoding="utf-8"))
            for candidate in data["roles"]:
                if candidate.get("id") == role_id:
                    return data, candidate
            raise AssertionError(f"{role_id} is absent from the lifecycle registry")

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "clone"
            subprocess.run(
                ["git", "clone", "--quiet", "--local", str(ROOT), str(root)],
                check=True,
                capture_output=True,
            )
            script_relative = "tools/validate_repository.py"
            (root / script_relative).write_bytes(
                (ROOT / script_relative).read_bytes()
            )
            registry = root / registry_relative
            data, entry = load_entry(registry)
            established = entry["active_revision"]
            self.assertIsNotNone(
                established,
                "fixture requires a committed active_revision for the Role",
            )
            self.assertIsNone(
                validator.ROLE_LIFECYCLE_BASELINE_REVISIONS.get(role_id),
                "fixture requires a post-baseline Role (no frozen baseline revision)",
            )

            # Change the canonical Role document so its content revision
            # diverges from the established (committed) revision -- this is
            # what a genuine in-progress candidate edit looks like.
            role_path = root / role_relative
            role_path.write_text(
                role_path.read_text(encoding="utf-8")
                + "\n<!-- phase-e-fixture: pending candidate edit -->\n",
                encoding="utf-8",
            )
            candidate_revision = validator.role_content_revision(role_id, root)
            self.assertIsNotNone(candidate_revision)
            self.assertNotEqual(candidate_revision, established)

            entry["disposition"] = "UPDATE"
            entry.pop("create_criteria", None)
            entry["candidate_revision"] = candidate_revision
            entry["candidate_state"] = "HUMAN_GATE"
            entry["transition"] = {
                "from_state": "ACTIVE",
                "from_revision": established,
                "to_state": "HUMAN_GATE",
                "candidate_revision": candidate_revision,
                "evidence_refs": ["local-evidence:phase-e-fixture#update"],
                "before_after_eval_ref": "local-evidence:phase-e-fixture#eval",
                "independent_review_ref": "local-review:phase-e-fixture#review",
                "human_gate_status": "pending",
                "celes_human_gate_ref": "pending",
            }
            registry.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
            output = run_validator(root)
            self.assertNotIn(
                drift_marker,
                output,
                "a pending candidate on a post-baseline Role must not be "
                "flagged as an active revision drift",
            )

    def test_ai_employee_decision_timestamp_must_be_real_and_zoned(self) -> None:
        self.assertTrue(
            validator.valid_decision_timestamp("2026-07-14T12:00:00+09:00")
        )
        self.assertFalse(
            validator.valid_decision_timestamp("2026-02-30T12:00:00+09:00")
        )
        self.assertFalse(
            validator.valid_decision_timestamp("2026-07-14T12:00:00")
        )

    def test_foundation_eval_accepts_governed_role_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            capability_target = root / "ai_team/capability_registry.yaml"
            lifecycle_target = (
                root
                / "ai_team/governance/ai_employee_lifecycle_registry.yaml"
            )
            lifecycle_target.parent.mkdir(parents=True)
            capability_target.parent.mkdir(parents=True, exist_ok=True)
            capability_target.write_text(
                (ROOT / "ai_team/capability_registry.yaml").read_text(
                    encoding="utf-8"
                ),
                encoding="utf-8",
            )
            lifecycle = yaml.safe_load(
                (
                    ROOT
                    / "ai_team/governance/ai_employee_lifecycle_registry.yaml"
                ).read_text(encoding="utf-8")
            )
            entry = lifecycle["roles"][0]
            entry["candidate_revision"] = "sha256:" + "a" * 64
            entry["candidate_state"] = "CANDIDATE"
            entry["disposition"] = "UPDATE"
            entry["transition"] = {
                "from_state": "ACTIVE",
                "from_revision": entry["active_revision"],
                "to_state": "CANDIDATE",
                "candidate_revision": entry["candidate_revision"],
                "evidence_refs": ["local-evidence:test"],
                "before_after_eval_ref": "pending",
                "independent_review_ref": "pending",
                "human_gate_status": "pending",
                "celes_human_gate_ref": "pending",
            }
            lifecycle_target.write_text(
                yaml.safe_dump(
                    lifecycle, allow_unicode=True, sort_keys=False
                ),
                encoding="utf-8",
            )
            foundation_evals.ai_employee_lifecycle(root)

    def test_execution_and_human_gate_schemas_are_strict(self) -> None:
        execution_schema = json.loads(
            (ROOT / "ai_team/evidence/execution_evidence.schema.json").read_text(
                encoding="utf-8"
            )
        )
        human_gate = json.loads(
            (ROOT / "ai_team/governance/human_gate.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(execution_schema["additionalProperties"])
        self.assertEqual(2, len(execution_schema["$defs"]["contextString"]["oneOf"]))
        self.assertEqual(2, len(execution_schema["$defs"]["contextNumber"]["oneOf"]))
        self.assertEqual("Celes", human_gate["properties"]["decided_by"]["const"])
        self.assertEqual(
            {"PROMOTE", "REJECT", "REWORK", "ROLLBACK", "APPROVE", "DENY"},
            set(human_gate["properties"]["decision"]["enum"]),
        )
        self.assertEqual(
            {"canonical_promotion", "critical_operation"},
            set(human_gate["properties"]["decision_type"]["enum"]),
        )
        self.assertEqual(3, len(human_gate["allOf"]))
        self.assertEqual(
            {"subject_revision", "before_after_eval_ref"},
            set(human_gate["allOf"][0]["then"]["required"]),
        )

    def test_all_required_engineering_scenarios_exist(self) -> None:
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(len(golden["cases"]), 22)
        self.assertEqual(
            len(golden["cases"]), len({case["id"] for case in golden["cases"]})
        )
        covered_roles = {
            role for case in golden["cases"] for role in case["expected_roles"]
        }
        capability = yaml.safe_load(
            (ROOT / "ai_team/capability_registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        capability_role_ids = {role["id"] for role in capability["roles"]}
        self.assertEqual(capability_role_ids, covered_roles)
        primary_skill_by_role = {
            role["id"]: role["primary_skill"] for role in capability["roles"]
        }
        for case in golden["cases"]:
            with self.subTest(case=case["id"]):
                self.assertTrue(
                    {
                        primary_skill_by_role[role]
                        for role in case["expected_roles"]
                    }
                    <= set(case["expected_skills"])
                )

    def test_every_golden_case_includes_its_risk_gates(self) -> None:
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(encoding="utf-8")
        )
        gates = yaml.safe_load(
            (ROOT / "ai_team/review/risk_based_quality_gates.yaml").read_text(
                encoding="utf-8"
            )
        )
        known = {
            gate
            for contract in gates["levels"].values()
            for gate in contract["gates"]
        }
        for case in golden["cases"]:
            with self.subTest(case=case["id"]):
                actual = set(case["required_gates"])
                self.assertLessEqual(
                    set(gates["levels"][case["risk"]]["gates"]), actual
                )
                self.assertLessEqual(actual, known)

    def test_critical_case_rejects_prohibited_action_and_missing_gate(self) -> None:
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(encoding="utf-8")
        )
        fixtures = yaml.safe_load(
            (ROOT / "ai_team/evals/case_fixtures.yaml").read_text(encoding="utf-8")
        )
        case = next(item for item in golden["cases"] if item["id"] == "GC-SEC-001")
        result = copy.deepcopy(
            next(item for item in fixtures["results"] if item["case_id"] == "GC-SEC-001")
        )
        result["actions"].append("commit_secret")
        result["executed_gates"].remove("celes_human_gate")
        self.assertEqual(
            ["prohibited_actions", "required_gates"],
            foundation_evals.case_result_failures(case, result),
        )

    def test_low_risk_case_rejects_role_and_skill_over_selection(self) -> None:
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(encoding="utf-8")
        )
        fixtures = yaml.safe_load(
            (ROOT / "ai_team/evals/case_fixtures.yaml").read_text(encoding="utf-8")
        )
        case = next(item for item in golden["cases"] if item["id"] == "GC-SQL-001")
        result = copy.deepcopy(
            next(item for item in fixtures["results"] if item["case_id"] == "GC-SQL-001")
        )
        result["selected_roles"].append("engineering_pmo")
        result["selected_skills"].append("skill-engineering-pmo")
        self.assertEqual(
            ["expected_roles", "expected_skills"],
            foundation_evals.case_result_failures(case, result),
        )

    def test_agent_fixture_rejects_self_approval_and_missing_reviewer(self) -> None:
        fixtures = yaml.safe_load(
            (ROOT / "ai_team/evals/agent_skill_fixtures.yaml").read_text(
                encoding="utf-8"
            )
        )
        result = copy.deepcopy(
            next(
                item
                for item in fixtures["agent_results"]
                if item["fixture_id"] == "AF-API-HIGH-001"
            )
        )
        result["actual"]["reviewers"].remove("security_governance_engineer")
        result["actual"]["actions"].append("self_accept_security_risk")
        self.assertEqual(
            ["prohibited_actions", "reviewers"],
            foundation_evals.agent_result_failures(result),
        )

    def test_skill_fixture_rejects_over_selection_and_context_overflow(self) -> None:
        fixtures = yaml.safe_load(
            (ROOT / "ai_team/evals/agent_skill_fixtures.yaml").read_text(
                encoding="utf-8"
            )
        )
        result = copy.deepcopy(
            next(
                item
                for item in fixtures["skill_results"]
                if item["fixture_id"] == "SF-BOUNDED-SQL-001"
            )
        )
        result["actual"]["selected_skills"].append("skill-engineering-pmo")
        result["actual"]["loaded_skills"].append("skill-engineering-pmo")
        result["actual"]["context_files_loaded"] = 99
        self.assertEqual(
            ["context_efficiency", "not_selected_skills", "selected_skills"],
            foundation_evals.skill_result_failures(result),
        )
        loaded_mismatch = copy.deepcopy(fixtures["skill_results"][0])
        loaded_mismatch["actual"]["loaded_skills"].append(
            "skill-engineering-pmo"
        )
        self.assertEqual(
            ["loaded_skills"],
            foundation_evals.skill_result_failures(loaded_mismatch),
        )
        negative = copy.deepcopy(fixtures["skill_results"][0])
        negative["actual"]["context_files_loaded"] = -1
        self.assertIn(
            "context_efficiency",
            foundation_evals.skill_result_failures(negative),
        )
        boolean = copy.deepcopy(fixtures["skill_results"][0])
        boolean["actual"]["context_files_loaded"] = True
        self.assertIn(
            "context_efficiency",
            foundation_evals.skill_result_failures(boolean),
        )

    def test_skill_eval_bindings_cover_every_skill(self) -> None:
        bindings = yaml.safe_load(
            (ROOT / "ai_team/evals/skill_eval_bindings.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            set(validator.SKILLS),
            {entry["skill"] for entry in bindings["bindings"]},
        )
        fixtures = yaml.safe_load(
            (ROOT / "ai_team/evals/agent_skill_fixtures.yaml").read_text(
                encoding="utf-8"
            )
        )
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(
                encoding="utf-8"
            )
        )
        selected_by_case = {
            case["id"]: set(case["expected_skills"])
            for case in golden["cases"]
        }
        selected_by_case.update(
            {
                result["fixture_id"]: set(
                    result["expected"]["selected_skills"]
                )
                for result in fixtures["skill_results"]
            }
        )
        required_rubric = set(fixtures["skill_contract"]["required_dimensions"])
        self.assertEqual(
            required_rubric, set(bindings["required_rubric"])
        )
        for entry in bindings["bindings"]:
            with self.subTest(skill=entry["skill"]):
                self.assertEqual(
                    [],
                    foundation_evals.skill_binding_failures(
                        entry, selected_by_case, required_rubric
                    ),
                )

        bad = copy.deepcopy(bindings["bindings"][0])
        bad["positive_case"] = "GC-ARCH-001"
        self.assertIn(
            "positive_case_does_not_select_skill",
            foundation_evals.skill_binding_failures(
                bad, selected_by_case, required_rubric
            ),
        )

    def test_documentation_review_selector_expands_only_affected_contracts(self) -> None:
        policy = yaml.safe_load(
            (
                ROOT / "ai_team/governance/documentation_quality_policy.yaml"
            ).read_text(encoding="utf-8")
        )
        targets = documentation_targets.select_targets(
            ["ai_team/roles/backend_engineer.md"], policy
        )
        self.assertIn("ai_team/roles/backend_engineer.md", targets)
        self.assertIn("ai_team/capability_registry.yaml", targets)
        self.assertIn(
            "ai_team/governance/ai_employee_lifecycle_registry.yaml", targets
        )
        self.assertNotIn("skills/index.yaml", targets)
        self.assertEqual(
            ".claude/agents/reviewer.md",
            documentation_targets.normalize_path(
                "./.claude/agents/reviewer.md"
            ),
        )

    def test_documentation_review_rejects_pass_with_blocking_finding(self) -> None:
        record = {
            "schema_version": "1.0",
            "review_id": "DOC-REVIEW-TEST",
            "timestamp": "2026-07-14T12:00:00+09:00",
            "reviewer": "independent-test-reviewer",
            "independent": True,
            "trigger": "high_risk_change",
            "changed_paths": ["ai_team/evals/eval_catalog.yaml"],
            "review_targets": ["ai_team/evals/eval_catalog.yaml"],
            "dimensions": ["accuracy"],
            "findings": [
                {
                    "id": "DOC-P1-TEST",
                    "severity": "P1",
                    "target": "ai_team/evals/eval_catalog.yaml",
                    "dimension": "accuracy",
                    "finding": "test blocker",
                    "evidence": "mutation fixture",
                    "required_action": "fix before PASS",
                }
            ],
            "verdict": "PASS",
            "unknowns": [],
        }
        failures = documentation_review_validator.record_failures(record)
        self.assertIn("blocking_finding_verdict", failures)
        self.assertIn("pass_with_findings_or_unknowns", failures)

    def test_documentation_review_dimensions_share_one_contract(self) -> None:
        policy = yaml.safe_load(
            (
                ROOT / "ai_team/governance/documentation_quality_policy.yaml"
            ).read_text(encoding="utf-8")
        )
        schema = json.loads(
            (
                ROOT
                / "ai_team/evals/documentation_semantic_review.schema.json"
            ).read_text(encoding="utf-8")
        )
        catalog = yaml.safe_load(
            (ROOT / "ai_team/evals/eval_catalog.yaml").read_text(
                encoding="utf-8"
            )
        )
        expected = foundation_evals.DOCUMENTATION_REVIEW_DIMENSIONS
        self.assertEqual(
            expected,
            set(policy["level_2_semantic"]["review_dimensions"]),
        )
        self.assertEqual(
            expected,
            set(schema["properties"]["dimensions"]["items"]["enum"]),
        )
        self.assertEqual(
            expected,
            set(
                schema["properties"]["findings"]["items"]["properties"]
                ["dimension"]["enum"]
            ),
        )
        self.assertEqual(
            expected, set(catalog["suites"]["documentation"]["dimensions"])
        )
        self.assertEqual(expected, documentation_review_validator.DIMENSIONS)

    def test_documentation_review_malformed_dimensions_are_structured(self) -> None:
        base = {
            "schema_version": "1.0",
            "review_id": "DOC-REVIEW-MALFORMED",
            "timestamp": "2026-07-14T12:00:00+09:00",
            "reviewer": "independent-test-reviewer",
            "independent": True,
            "trigger": "high_risk_change",
            "changed_paths": ["ai_team/evals/eval_catalog.yaml"],
            "review_targets": ["ai_team/evals/eval_catalog.yaml"],
            "dimensions": None,
            "findings": [],
            "verdict": "PASS",
            "unknowns": [],
        }
        self.assertIn(
            "dimensions", documentation_review_validator.record_failures(base)
        )
        base["dimensions"] = [{}]
        self.assertIn(
            "dimensions", documentation_review_validator.record_failures(base)
        )
        base["dimensions"] = ["accuracy"]
        base["timestamp"] = "2026-02-30T12:00:00+09:00"
        self.assertIn(
            "timestamp", documentation_review_validator.record_failures(base)
        )


if __name__ == "__main__":
    unittest.main()
