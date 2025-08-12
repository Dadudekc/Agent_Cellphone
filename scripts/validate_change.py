#!/usr/bin/env python3
"""
Validate a change contract against schema and (optionally) staged file changes.

Usage:
  python scripts/validate_change.py --contract docs/changes/2025-08-10-phase2-contract.json [--check-git]
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "config" / "templates" / "change_contract.schema.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(data: dict, schema: dict) -> list:
    """Minimal JSON schema validation to avoid extra deps.

    Only validates required fields, enums, and simple types used here.
    Returns list of errors.
    """
    errors = []

    # required
    required = schema.get("required", [])
    for key in required:
        if key not in data:
            errors.append(f"Missing required field: {key}")

    props = schema.get("properties", {})
    for key, val in data.items():
        if key not in props:
            if not schema.get("additionalProperties", True):
                errors.append(f"Unexpected field: {key}")
            continue
        spec = props[key]
        t = spec.get("type")
        if t == "string" and not isinstance(val, str):
            errors.append(f"Field {key} must be string")
        if t == "array" and not isinstance(val, list):
            errors.append(f"Field {key} must be array")
        if t == "object" and not isinstance(val, dict):
            errors.append(f"Field {key} must be object")
        # enum
        enum = spec.get("enum")
        if enum is not None and val not in enum:
            errors.append(f"Field {key} not in enum {enum}")
        # nested items minimal checks
        if key == "affected_files" and isinstance(val, list):
            for i, item in enumerate(val):
                if not isinstance(item, dict):
                    errors.append(f"affected_files[{i}] must be object")
                    continue
                if "path" not in item or "op" not in item:
                    errors.append(f"affected_files[{i}] must have path and op")
                if item.get("op") not in ["add", "edit", "remove"]:
                    errors.append(f"affected_files[{i}].op invalid: {item.get('op')}")

    return errors


def get_staged_paths() -> set:
    try:
        out = subprocess.check_output(["git", "diff", "--cached", "--name-only"], text=True)
        return {line.strip().replace("\\", "/") for line in out.splitlines() if line.strip()}
    except Exception:
        return set()


def normalize_path(p: str) -> str:
    return str(Path(p).as_posix())


def check_git_index(contract: dict) -> list:
    errors = []
    staged = get_staged_paths()
    if not staged:
        return ["No staged files found; run 'git add' before commit or omit --check-git."]
    allowed = {normalize_path(item["path"]) for item in contract.get("affected_files", [])}
    extras = [p for p in staged if p not in allowed]
    if extras:
        errors.append("Staged files not declared in contract: " + ", ".join(sorted(extras)))
    return errors


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--contract", required=True, help="Path to contract JSON")
    ap.add_argument("--check-git", action="store_true", help="Ensure staged files match contract")
    args = ap.parse_args()

    schema = load_json(SCHEMA_PATH)
    data = load_json(Path(args.contract))

    errors = validate_schema(data, schema)
    if args.check_git:
        errors.extend(check_git_index(data))

    if errors:
        print("Contract validation FAILED:\n - " + "\n - ".join(errors))
        sys.exit(1)

    print("Contract validation OK:", data.get("id"), data.get("title"))


if __name__ == "__main__":
    main()


