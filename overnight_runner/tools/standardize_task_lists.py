#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import List, Tuple
import os

TEMPLATE_MARKER = "<!-- STANDARD_TASK_LIST_v1 -->"

TASK_LIST_TEMPLATE = f"""
{TEMPLATE_MARKER}
# TASK_LIST.md – Roadmap to Beta

Repo: {{repo_name}}

## Roadmap to Beta

- [ ] GUI loads cleanly without errors
- [ ] Buttons/menus wired to working handlers
- [ ] Happy‑path flows implemented and documented
- [ ] Basic tests covering critical paths
- [ ] README quickstart up‑to‑date
- [ ] Triage and address critical issues

## Task List (Small, verifiable steps)

- [ ] Task 1: …
- [ ] Task 2: …
- [ ] Task 3: …

## Acceptance Criteria (per task)

- Clear, testable criteria
- Measurable output or evidence

## Evidence Links

- Link to PRs/commits, screenshots, logs, or test output

## Progress Log

- YYYY‑MM‑DD: note…

"""


def is_repo_dir(path: Path) -> bool:
    """Heuristic to detect a repo root.
    Prefer .git, or common build/manifest files. Avoid counting README/.env alone.
    """
    try:
        if (path / ".git").exists():
            return True
        manifest_markers = [
            "requirements.txt",
            "package.json",
            "pyproject.toml",
            "setup.py",
            "README.md",
        ]
        return any((path / m).exists() for m in manifest_markers)
    except Exception:
        return False


def ensure_task_list(repo_dir: Path, dry_run: bool) -> Tuple[str, str]:
    """Create or standardize TASK_LIST.md in repo_dir.
    Returns (action, path_str) where action is 'created', 'appended', or 'skipped'.
    """
    tl = repo_dir / "TASK_LIST.md"
    try:
        if not tl.exists():
            content = TASK_LIST_TEMPLATE.replace("{repo_name}", repo_dir.name)
            if dry_run:
                return ("create", str(tl))
            tl.write_text(content, encoding="utf-8")
            return ("created", str(tl))

        # Existing file: non‑destructive append if marker missing
        existing = tl.read_text(encoding="utf-8", errors="ignore")
        if TEMPLATE_MARKER in existing:
            return ("skipped", str(tl))
        addition = "\n\n" + TASK_LIST_TEMPLATE.replace("{repo_name}", repo_dir.name)
        if dry_run:
            return ("append", str(tl))
        tl.write_text(existing.rstrip() + addition, encoding="utf-8")
        return ("appended", str(tl))
    except Exception:
        return ("error", str(tl))


def find_repos(root: Path, max_depth: int = 2) -> List[Path]:
    repos: List[Path] = []
    if not root.exists() or not root.is_dir():
        return repos
    exclude_dirs = {
        ".git",
        ".github",
        ".vscode",
        ".idea",
        ".pytest_cache",
        "__pycache__",
        "node_modules",
        "venv",
        ".venv",
        "dist",
        "build",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".cache",
    }
    try:
        start_depth = len(root.parts)
        for dirpath, dirnames, filenames in os.walk(root):
            p = Path(dirpath)
            # Prune excluded directories
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs and not d.startswith('.')]
            depth = len(p.parts) - start_depth
            if depth > max_depth:
                # do not descend further
                dirnames[:] = []
                continue
            if depth >= 1 and is_repo_dir(p):
                repos.append(p)
                # do not descend further into a repo root
                dirnames[:] = []
    except Exception:
        pass
    return repos


def main() -> int:
    ap = argparse.ArgumentParser("standardize_task_lists")
    ap.add_argument("--root", default="D:/repos", help="Root folder containing repositories")
    ap.add_argument("--dry-run", action="store_true", help="Show planned changes without writing")
    ap.add_argument("--max-depth", type=int, default=2, help="Max directory depth to search under root")
    args = ap.parse_args()

    root = Path(args.root)
    repos = find_repos(root, max_depth=max(0, int(args.max_depth)))
    created = appended = skipped = errors = 0
    for repo in repos:
        action, path_str = ensure_task_list(repo, dry_run=args.dry_run)
        if action == "created":
            created += 1
            print(f"CREATED {path_str}")
        elif action == "appended":
            appended += 1
            print(f"APPENDED {path_str}")
        elif action == "create":
            print(f"WOULD CREATE {path_str}")
        elif action == "append":
            print(f"WOULD APPEND {path_str}")
        elif action == "skipped":
            skipped += 1
        else:
            errors += 1
            print(f"ERROR {path_str}")

    print(
        f"\nSummary: repos={len(repos)} created={created} appended={appended} skipped={skipped} errors={errors}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


