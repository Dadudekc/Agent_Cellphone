from __future__ import annotations

import json
import tempfile
from pathlib import Path


def _write_json(path: Path, data: dict) -> None:

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def test_handle_fsm_request_assigns_tasks_and_writes_inbox(monkeypatch):

    temp_root = Path(tempfile.mkdtemp(prefix="acp_fsm_test_"))
    # Import module under test
    import importlib
    fsm_bridge = importlib.import_module("overnight_runner.fsm_bridge")

    # Redirect module paths into our temp sandbox
    fsm_bridge.FSM_ROOT = temp_root / "fsm_data"
    fsm_bridge.TASKS_DIR = fsm_bridge.FSM_ROOT / "tasks"
    fsm_bridge.WORKFLOWS_DIR = fsm_bridge.FSM_ROOT / "workflows"
    fsm_bridge.INBOX_ROOT = temp_root / "agent_workspaces"
    fsm_bridge.REPO_ROOT = temp_root / "repositories"

    # Seed two queued tasks without owners
    t1 = {
        "task_id": "TASK_ALPHA",
        "repo": "sample_repo",
        "intent": "Improve FSM evidence emission",
        "state": "queued",
    }
    t2 = {
        "task_id": "TASK_BETA",
        "repo": "sample_repo",
        "intent": "Wire transitions with guards",
        "state": "queued",
    }
    _write_json(fsm_bridge.TASKS_DIR / "TASK_ALPHA.json", t1)
    _write_json(fsm_bridge.TASKS_DIR / "TASK_BETA.json", t2)

    # Invoke assignment for two target agents
    payload = {
        "type": "fsm_request",
        "from": "Agent-3",
        "to": "Agent-5",
        "workflow": "default",
        "agents": ["Agent-1", "Agent-2"],
    }
    result = fsm_bridge.handle_fsm_request(payload)
    assert result.get("ok"), result
    assert result.get("count") == 2

    # Validate inbox messages for each agent
    inbox = fsm_bridge.INBOX_ROOT
    agent1_msgs = sorted((inbox / "Agent-1" / "inbox").glob("task_*.json"))
    agent2_msgs = sorted((inbox / "Agent-2" / "inbox").glob("task_*.json"))
    assert agent1_msgs and agent2_msgs, "Expected task assignment messages in both agent inboxes"

    # Validate JSON structure
    with agent1_msgs[-1].open("r", encoding="utf-8") as f:
        a1 = json.load(f)
    assert a1.get("type") == "task"
    assert a1.get("to") == "Agent-1"
    assert a1.get("task_id") in {"TASK_ALPHA", "TASK_BETA"}


def test_handle_fsm_update_persists_state_and_evidence(monkeypatch):

    temp_root = Path(tempfile.mkdtemp(prefix="acp_fsm_test_"))
    import importlib
    fsm_bridge = importlib.import_module("overnight_runner.fsm_bridge")

    # Redirect module paths into our temp sandbox
    fsm_bridge.FSM_ROOT = temp_root / "fsm_data"
    fsm_bridge.TASKS_DIR = fsm_bridge.FSM_ROOT / "tasks"
    fsm_bridge.WORKFLOWS_DIR = fsm_bridge.FSM_ROOT / "workflows"
    fsm_bridge.INBOX_ROOT = temp_root / "agent_workspaces"

    # Seed task record to be updated
    task_id = "TASK_EVIDENCE"
    record = {
        "task_id": task_id,
        "repo": "sample_repo",
        "intent": "Add FSM tests",
        "state": "assigned",
        "owner": "Agent-4",
    }
    _write_json(fsm_bridge.TASKS_DIR / f"{task_id}.json", record)

    # Submit an fsm_update with evidence
    update = {
        "type": "fsm_update",
        "from": "Agent-4",
        "task_id": task_id,
        "state": "done",
        "summary": "Unit tests for fsm_bridge pass; evidence attached.",
        "evidence": [
            {"kind": "junit_xml", "path": str(temp_root / "artifacts" / "junit.xml")},
            {"kind": "logs", "path": str(temp_root / "artifacts" / "pytest_output.txt")},
        ],
        "captain": "Agent-3",
    }
    res = fsm_bridge.handle_fsm_update(update)
    assert res.get("ok"), res
    assert res.get("state") == "done"

    # Verify task file was updated with state and evidence
    saved = json.loads((fsm_bridge.TASKS_DIR / f"{task_id}.json").read_text(encoding="utf-8"))
    assert saved.get("state") == "done"
    assert isinstance(saved.get("evidence"), list) and saved["evidence"], "Evidence list should be populated"

    # Verify a verification message was written to captain's inbox
    verify_msgs = sorted((fsm_bridge.INBOX_ROOT / "Agent-3" / "inbox").glob("verify_*.json"))
    assert verify_msgs, "Expected a verify message for the captain"


