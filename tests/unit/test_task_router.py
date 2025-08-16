import asyncio
import pathlib
import sys

import pytest

# Allow importing TaskRouter without executing package __init__
repo_root = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(repo_root / "project_repository" / "orchestrator"))
from task_router import TaskRouter  # type: ignore


def test_prd_ingest_and_task_budget() -> None:
    router = TaskRouter()
    prd = {"name": "demo", "requirements": ["feat1", "feat2"]}
    tasks = router.ingest_prd(prd)
    assert len(tasks) == 2
    assert router.task_counter == 2  # budget reflects total tasks

    t1 = asyncio.run(router.get_next_task("Agent-1"))
    assert t1["status"] == "assigned"
    t2 = asyncio.run(router.get_next_task("Agent-2"))
    assert t2["id"] != t1["id"]


def test_task_assignment_gate_and_path_blocking() -> None:
    router = TaskRouter()
    prd = {"name": "demo", "requirements": ["feat"]}
    router.ingest_prd(prd)
    asyncio.run(router.get_next_task("Agent-1"))
    # Agent-1 already has a task, gate returns same task
    same = asyncio.run(router.get_next_task("Agent-1"))
    assert same["assigned_to"] == "Agent-1"
    # No more tasks remain; Agent-2 is blocked
    assert asyncio.run(router.get_next_task("Agent-2")) is None


def test_complete_task_updates_status() -> None:
    router = TaskRouter()
    prd = {"name": "demo", "requirements": ["feat"]}
    router.ingest_prd(prd)
    task = asyncio.run(router.get_next_task("Agent-1"))
    asyncio.run(router.complete_task("Agent-1", task))
    status = router.get_system_status()
    assert status["tasks"]["completed"] == 1
    assert status["tasks"]["completion_rate"] == 100
