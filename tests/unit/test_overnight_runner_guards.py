#!/usr/bin/env python3
"""
Test overnight runner guard functions.
"""

import pytest
import pathlib
from unittest.mock import patch, MagicMock
from datetime import datetime

from src.orchestrators.overnight_runner import run_guard, advance_state, process_task, Task


def test_run_guard_truncates_output(tmp_path: pathlib.Path) -> None:
    script = tmp_path / "big.py"
    script.write_text("print('a'*6000)")
    result = run_guard("big", f"python {script.name}", tmp_path)
    assert result["ok"]
    assert len(result["stdout"]) == 5000
    assert result["stdout"].endswith("\n")
    assert set(result["stdout"].strip()) == {"a"}


def test_advance_state_gates() -> None:
    fsm = {"states": {"Build": {"on_pass": "Review", "on_fail": "Quarantine"}}}
    assert advance_state(fsm, "Build", True) == "Review"
    assert advance_state(fsm, "Build", False) == "Quarantine"
    assert advance_state(fsm, "Unknown", True) == "Unknown"


def test_process_task_blocks_non_actionable() -> None:
    task = Task(id="1", repo="r", branch="main", state="Plan")
    result = process_task(task, {"states": {}})
    assert result["note"].startswith("Skipped")
    assert result["from"] == "Plan" and result["to"] == "Plan"
