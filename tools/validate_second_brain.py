#!/usr/bin/env python3
"""Validate the curated Obsidian engineering knowledge base."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml


REQUIRED_DIRECTORIES = [
    "00_MOC",
    "01_Projects",
    "02_Knowledge/data_engineering",
    "02_Knowledge/backend",
    "02_Knowledge/frontend",
    "02_Knowledge/cloud",
    "02_Knowledge/sre",
    "02_Knowledge/security",
    "02_Knowledge/qa",
    "02_Knowledge/ai_llm",
    "02_Knowledge/integration",
    "03_Patterns/architecture_patterns",
    "03_Patterns/db_design_patterns",
    "03_Patterns/api_design_patterns",
    "03_Patterns/data_pipeline_patterns",
    "03_Patterns/testing_patterns",
    "03_Patterns/operation_patterns",
    "04_Decision_Logs",
    "05_Troubleshooting/snowflake",
    "05_Troubleshooting/python",
    "05_Troubleshooting/api",
    "05_Troubleshooting/terraform",
    "05_Troubleshooting/ci_cd",
    "05_Troubleshooting/data_quality",
    "90_Templates",
    "99_Inbox",
]

REQUIRED_FILES = [
    "README.md",
    "00_MOC/engineering_moc.md",
    "00_MOC/data_engineering_moc.md",
    "00_MOC/backend_moc.md",
    "00_MOC/frontend_moc.md",
    "00_MOC/cloud_infra_moc.md",
    "00_MOC/ai_llm_moc.md",
    "00_MOC/qa_sre_security_moc.md",
    "00_MOC/project_index.md",
    "04_Decision_Logs/adr_index.md",
    "05_Troubleshooting/error_index.md",
    "90_Templates/project_note_template.md",
    "90_Templates/architecture_note_template.md",
    "90_Templates/decision_log_template.md",
    "90_Templates/troubleshooting_template.md",
    "90_Templates/learning_note_template.md",
    "90_Templates/source_map_template.md",
    "99_Inbox/unsorted.md",
]

PROJECT_FILES = [
    "overview.md",
    "decisions.md",
    "architecture_summary.md",
    "implementation_summary.md",
    "test_summary.md",
    "risks_and_issues.md",
    "next_actions.md",
    "source_map.md",
]

REQUIRED_FRONTMATTER = {
    "title",
    "type",
    "project",
    "domain",
    "status",
    "created",
    "updated",
    "source",
    "tags",
    "related",
    "managed_by",
}

WIKI_LINK = re.compile(r"\[\[([^\]]+)\]\]")


def parse_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("frontmatter is missing")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("frontmatter terminator is missing")
    value = yaml.safe_load(parts[1])
    if not isinstance(value, dict):
        raise ValueError("frontmatter is not a mapping")
    return value, parts[2]


def note_candidates(root: Path, current: Path, target: str) -> list[Path]:
    clean = target.split("|", 1)[0].split("#", 1)[0].strip()
    if not clean:
        return []
    relative = Path(clean)
    candidates = [
        (current.parent / relative).with_suffix(".md"),
        (root / relative).with_suffix(".md"),
    ]
    candidates.extend(root.rglob(f"{relative.name}.md"))
    return candidates


def validate(root: Path) -> list[str]:
    errors: list[str] = []

    if not root.is_dir():
        return [f"Knowledge base does not exist: {root}"]

    for relative in REQUIRED_DIRECTORIES:
        if not (root / relative).is_dir():
            errors.append(f"Missing directory: {relative}")

    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"Missing file: {relative}")

    projects_root = root / "01_Projects"
    project_dirs = (
        sorted(path for path in projects_root.iterdir() if path.is_dir())
        if projects_root.is_dir()
        else []
    )
    if not project_dirs:
        errors.append("No project directories found under 01_Projects")
    for project in project_dirs:
        for filename in PROJECT_FILES:
            if not (project / filename).is_file():
                errors.append(f"Missing project file: {project.name}/{filename}")

    markdown_files = sorted(root.rglob("*.md"))
    if not markdown_files:
        errors.append("No Markdown files found")
        return errors

    for path in markdown_files:
        relative = path.relative_to(root)
        try:
            frontmatter, body = parse_frontmatter(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{relative}: {exc}")
            continue

        missing = sorted(REQUIRED_FRONTMATTER - set(frontmatter))
        if missing:
            errors.append(
                f"{relative}: missing frontmatter keys: {', '.join(missing)}"
            )
        if frontmatter.get("managed_by") != "engineering_knowledge_curator":
            errors.append(f"{relative}: unexpected managed_by")
        for key in ("source", "tags", "related"):
            if not isinstance(frontmatter.get(key), list):
                errors.append(f"{relative}: {key} must be a list")

        if relative.name == "source_map.md":
            if "Curated Notes" not in body or "Review Status" not in body:
                errors.append(f"{relative}: source map table is incomplete")

        for raw_target in WIKI_LINK.findall(body):
            if raw_target.startswith(("http://", "https://", "file://")):
                continue
            candidates = note_candidates(root, path, raw_target)
            if not any(candidate.is_file() for candidate in candidates):
                errors.append(
                    f"{relative}: broken wiki link [[{raw_target}]]"
                )

    index = root / "00_MOC/project_index.md"
    if index.is_file():
        _, body = parse_frontmatter(index)
        for project in project_dirs:
            expected = f"01_Projects/{project.name}/overview"
            if expected not in body:
                errors.append(
                    f"00_MOC/project_index.md: project not linked: {project.name}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    args = parser.parse_args()

    root = args.root.resolve()
    errors = validate(root)
    markdown_count = len(list(root.rglob("*.md"))) if root.is_dir() else 0
    if errors:
        print(
            f"Second brain validation failed: {markdown_count} notes, "
            f"{len(errors)} errors"
        )
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Second brain validation passed: {markdown_count} notes, 0 errors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
