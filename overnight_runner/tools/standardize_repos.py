#!/usr/bin/env python3
from __future__ import annotations

import argparse, json, os
from pathlib import Path


PRD_TEMPLATE = """# Product Requirements

repo: {repo}

## Vision

Describe the repo's purpose, users, and value.

## Personas

- Developer
- Reviewer

## Milestones

- id: mvp
  title: Minimum Viable Product
  acceptance: Basic flows pass and README quickstart works

"""

TASK_LIST_TEMPLATE = """# Task List

repo: {repo}

- [ ] task_id: tl-001
  title: Establish smoke tests
  state: new
  acceptance_criteria:
    - Basic GUI buttons work
    - Smoke tests pass in CI

- [ ] task_id: tl-002
  title: Add PRD and templates
  state: new
  acceptance_criteria:
    - PRD.md present and reviewed
    - TASK_LIST.md formatted to standard

"""


def discover_repos(root: Path) -> list[Path]:
    exclude = {".git", ".github", ".vscode", ".idea", ".pytest_cache", "__pycache__", "node_modules", "venv", ".venv", "dist", "build", ".mypy_cache", ".ruff_cache", ".tox", ".cache", "communications"}
    repos: list[Path] = []
    if not root.is_dir():
        return repos
    for p in sorted(root.iterdir()):
        if not p.is_dir() or p.name in exclude or p.name.startswith("."):
            continue
        markers = [".git", "README.md", "pyproject.toml", "package.json", "requirements.txt"]
        if any((p / m).exists() for m in markers):
            repos.append(p)
    return repos


def ensure_templates(repo: Path) -> None:
    prd = repo / "PRD.md"
    tasks = repo / "TASK_LIST.md"
    if not prd.exists():
        prd.write_text(PRD_TEMPLATE.format(repo=repo.name), encoding="utf-8")
    if not tasks.exists():
        tasks.write_text(TASK_LIST_TEMPLATE.format(repo=repo.name), encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser("standardize_repos")
    ap.add_argument("--root", default="D:/repos", help="root path of repositories")
    args = ap.parse_args()
    root = Path(args.root)
    count = 0
    for repo in discover_repos(root):
        ensure_templates(repo)
        count += 1
    print(f"Standardized {count} repos under {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


