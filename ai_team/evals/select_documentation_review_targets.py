#!/usr/bin/env python3
"""Select changed-scope documentation targets without performing semantic review."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path, PurePosixPath

import yaml


ROOT = Path(__file__).resolve().parents[2]
DOCUMENT_SUFFIXES = {".md", ".yaml", ".yml", ".json"}


def matches(path: str, pattern: str) -> bool:
    if pattern.endswith("/**"):
        return path.startswith(pattern[:-3].rstrip("/") + "/")
    return PurePosixPath(path).match(pattern)


def normalize_path(path: str) -> str:
    """Normalize separators without stripping leading dotfile components."""
    normalized = path.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def select_targets(changed_paths: list[str], policy: dict) -> list[str]:
    """Expand changed documentation through the policy's bounded dependency map."""
    normalized = {normalize_path(path) for path in changed_paths}
    targets = {
        path
        for path in normalized
        if Path(path).suffix.lower() in DOCUMENT_SUFFIXES
    }
    rules = policy.get("level_2_semantic", {}).get("dependency_rules", [])
    for rule in rules:
        triggers = rule.get("when_changed", []) if isinstance(rule, dict) else []
        if any(matches(path, pattern) for path in normalized for pattern in triggers):
            targets.update(rule.get("include", []))
    return sorted(targets)


def git_changed_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "diff", "--name-only", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git diff failed")
    untracked = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--others", "--exclude-standard"],
        check=False,
        capture_output=True,
        text=True,
    )
    if untracked.returncode:
        raise RuntimeError(untracked.stderr.strip() or "git ls-files failed")
    return sorted(
        {
            line.strip()
            for line in (result.stdout + "\n" + untracked.stdout).splitlines()
            if line.strip()
        }
    )


def run(root: Path) -> dict:
    policy_path = root / "ai_team/governance/documentation_quality_policy.yaml"
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    changed = git_changed_paths(root)
    return {
        "schema_version": "1.0",
        "changed_paths": changed,
        "semantic_review_targets": select_targets(changed, policy),
        "semantic_review_performed": False,
        "note": "Selection is deterministic; semantic findings require an independent reviewer.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    print(json.dumps(run(args.root), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
