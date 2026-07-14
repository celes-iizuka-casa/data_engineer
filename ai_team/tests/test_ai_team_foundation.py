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

    def test_capability_and_skill_sets_match_repository(self) -> None:
        capability = yaml.safe_load(
            (ROOT / "ai_team/capability_registry.yaml").read_text(encoding="utf-8")
        )
        lifecycle = yaml.safe_load(
            (ROOT / "ai_team/governance/skill_lifecycle_registry.yaml").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(
            set(validator.ROLES), {item["id"] for item in capability["roles"]}
        )
        self.assertEqual(
            set(validator.SKILLS), {item["id"] for item in lifecycle["skills"]}
        )
        for item in lifecycle["skills"]:
            with self.subTest(skill=item["id"]):
                self.assertEqual("ACTIVE", item["state"])
                self.assertEqual("ACTIVE", item["candidate_state"])
                self.assertEqual("UPDATE", item["disposition"])
                self.assertEqual(
                    validator.skill_content_revision(item["id"], ROOT),
                    item["active_revision"],
                )
                self.assertEqual(
                    validator.skill_content_revision(item["id"], ROOT),
                    item["candidate_revision"],
                )
                self.assertEqual("promoted", item["transition"]["human_gate_status"])
        decision = lifecycle["human_gate_decision"]
        self.assertEqual("Celes", decision["decided_by"])
        self.assertEqual("PROMOTE", decision["decision"])

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
        self.assertEqual(2, len(human_gate["allOf"]))

    def test_all_required_engineering_scenarios_exist(self) -> None:
        golden = yaml.safe_load(
            (ROOT / "ai_team/evals/golden_cases.yaml").read_text(encoding="utf-8")
        )
        self.assertEqual(15, len(golden["cases"]))
        self.assertEqual(
            15, len({case["id"] for case in golden["cases"]})
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


if __name__ == "__main__":
    unittest.main()
