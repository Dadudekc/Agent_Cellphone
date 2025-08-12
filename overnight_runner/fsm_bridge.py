#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, List, Optional
import time
import uuid
from urllib import request, error


FSM_ROOT = Path("fsm_data")
TASKS_DIR = FSM_ROOT / "tasks"
WORKFLOWS_DIR = FSM_ROOT / "workflows"
INBOX_ROOT = Path("agent_workspaces")


@dataclass
class TaskRecord:
    task_id: str
    repo: str
    intent: str
    state: str
    owner: Optional[str] = None
    acceptance_criteria: Optional[str] = None
    evidence_required: Optional[str] = None
    # Extended lifecycle/audit fields
    assigned_at: Optional[str] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    owner_history: List[Dict[str, Any]] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)
    priority: Optional[int] = None
    labels: List[str] = field(default_factory=list)
    blocked_reason: Optional[str] = None
    workflow: Optional[str] = None
    attempt: int = 0


def _read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def load_workflow(workflow_id: str) -> Dict[str, Any]:
    return _read_json(WORKFLOWS_DIR / f"{workflow_id}.json")


def list_task_files() -> List[Path]:
    if not TASKS_DIR.exists():
        return []
    return sorted([p for p in TASKS_DIR.iterdir() if p.suffix == ".json"])


def load_tasks() -> Dict[str, TaskRecord]:
    tasks: Dict[str, TaskRecord] = {}
    for p in list_task_files():
        data = _read_json(p)
        task_id = data.get("task_id") or p.stem
        tr = TaskRecord(
            task_id=task_id,
            repo=data.get("repo", ""),
            intent=data.get("intent", ""),
            state=data.get("state", "new"),
            owner=data.get("owner"),
            acceptance_criteria=data.get("acceptance_criteria"),
            evidence_required=data.get("evidence_required"),
            assigned_at=data.get("assigned_at"),
            started_at=data.get("started_at"),
            completed_at=data.get("completed_at"),
            owner_history=list(data.get("owner_history", [])),
            evidence=list(data.get("evidence", [])),
            priority=data.get("priority"),
            labels=list(data.get("labels", [])),
            blocked_reason=data.get("blocked_reason"),
            workflow=data.get("workflow"),
            attempt=int(data.get("attempt", 0)),
        )
        tasks[task_id] = tr
    return tasks


def _save_task(record: TaskRecord) -> None:
    path = TASKS_DIR / f"{record.task_id}.json"
    data = {
        "task_id": record.task_id,
        "repo": record.repo,
        "intent": record.intent,
        "state": record.state,
        "owner": record.owner,
        "acceptance_criteria": record.acceptance_criteria,
        "evidence_required": record.evidence_required,
        "assigned_at": record.assigned_at,
        "started_at": record.started_at,
        "completed_at": record.completed_at,
        "owner_history": record.owner_history,
        "evidence": record.evidence,
        "priority": record.priority,
        "labels": record.labels,
        "blocked_reason": record.blocked_reason,
        "workflow": record.workflow,
        "attempt": record.attempt,
    }
    _write_json(path, data)


def _now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _write_inbox_message(to_agent: str, payload: Dict[str, Any]) -> Path:
    inbox = INBOX_ROOT / to_agent / "inbox"
    inbox.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    msg_type = payload.get("type", "note")
    # Attach a standard envelope for idempotency/traceability
    message_id = payload.get("id") or str(uuid.uuid4())
    payload["id"] = message_id
    payload.setdefault("created_at", _now_iso())
    payload.setdefault("schema_version", 1)
    payload.setdefault("correlation_id", payload.get("correlation_id", message_id))
    payload.setdefault("causation_id", payload.get("causation_id", message_id))
    fname = f"{msg_type}_{ts}_{to_agent}.json"
    path = inbox / fname
    _write_json(path, payload)
    return path


def _post_discord(title: str, description: str) -> None:
    """Optional devlog to Discord via webhook in environment.
    Set DISCORD_WEBHOOK_URL and optional DEVLOG_USERNAME in .env or env.
    """
    url = os.environ.get("DISCORD_WEBHOOK_URL")
    if not url:
        return
    user = os.environ.get("DEVLOG_USERNAME", "Agent Devlog")
    payload = {
        "username": user,
        "embeds": [{"title": title, "description": description, "color": 5814783}],
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with request.urlopen(req, timeout=8):
            pass
    except (error.HTTPError, error.URLError):
        # Silent failure to avoid breaking FSM; listener may also post devlogs
        pass


def handle_fsm_request(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Select next tasks and assign to agents. Payload may include:
    { 'type':'fsm_request', 'from':'Agent-3', 'to':'Agent-5', 'workflow':'default', 'agents':['Agent-1','Agent-2','Agent-4'] }
    """
    targets: List[str] = payload.get("agents") or []
    workflow_id = payload.get("workflow") or "default"

    _ = load_workflow(workflow_id)  # reserved for future branching by state graph
    tasks = load_tasks()

    assigned: List[Dict[str, Any]] = []
    # simple round-robin: pick tasks with state in {new, queued} and no owner
    open_tasks = [t for t in tasks.values() if t.state in {"new", "queued"} and not t.owner]
    i = 0
    for t in open_tasks:
        if not targets:
            break
        owner = targets[i % len(targets)]
        t.owner = owner
        t.state = "assigned"
        t.assigned_at = _now_iso()
        t.acceptance_criteria = t.acceptance_criteria or "Small, verifiable edit with tests/build evidence."
        t.evidence_required = t.evidence_required or "Link to commit/PR and test/build output."
        t.workflow = workflow_id
        # Track owner history
        t.owner_history.append({"owner": owner, "at": t.assigned_at})
        _save_task(t)
        assignment = {
            "type": "task",
            "from": payload.get("to", "Agent-5"),
            "to": owner,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "task_id": t.task_id,
            "repo": t.repo,
            "intent": t.intent,
            "acceptance_criteria": t.acceptance_criteria,
            "evidence_required": t.evidence_required,
            # Helpful context for downstream tools
            "workflow": workflow_id,
            "repo_path": f"D:/repositories/{t.repo}" if t.repo else None,
            "comm_root_path": str(Path("D:/repositories/communications")),
        }
        _write_inbox_message(owner, assignment)
        assigned.append(assignment)
        i += 1

    # Optional devlog summary
    if assigned:
        preview = []
        for a in assigned[:5]:
            preview.append(f"{a.get('task_id')} → {a.get('to')} ({a.get('repo')})")
        extra = "; more…" if len(assigned) > 5 else ""
        desc = f"workflow: {workflow_id} | count: {len(assigned)}\n" + "\n".join(preview) + extra
        _post_discord("FSM assigned tasks", desc)

    return {"ok": True, "assigned": assigned, "count": len(assigned)}


def handle_fsm_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Update a task record with new state/evidence.
    { 'type':'fsm_update', 'task_id': '...', 'state':'in_progress|blocked|done', 'summary':'...', 'evidence':{...} }
    """
    task_id = payload.get("task_id")
    if not task_id:
        return {"ok": False, "error": "missing task_id"}
    tasks = load_tasks()
    tr = tasks.get(task_id)
    if tr is None:
        return {"ok": False, "error": f"task {task_id} not found"}
    new_state = payload.get("state") or tr.state
    # Transition timestamps
    if tr.state != new_state:
        if new_state in {"in_progress", "executing"} and not tr.started_at:
            tr.started_at = _now_iso()
        if new_state in {"done", "completed"} and not tr.completed_at:
            tr.completed_at = _now_iso()
        tr.state = new_state
    # persist any acceptance/evidence hints
    if payload.get("acceptance_criteria"):
        tr.acceptance_criteria = payload["acceptance_criteria"]
    if payload.get("evidence_required"):
        tr.evidence_required = payload["evidence_required"]
    # Merge evidence
    ev = payload.get("evidence")
    if ev:
        if isinstance(ev, dict):
            ev_list = [ev]
        elif isinstance(ev, list):
            ev_list = [e for e in ev if isinstance(e, dict)]
        else:
            ev_list = []
        now = _now_iso()
        for e in ev_list:
            e.setdefault("ts", now)
        # simple append; caller responsible for dedupe if needed
        tr.evidence.extend(ev_list)
    _save_task(tr)

    # notify captain with a verification summary message
    captain = payload.get("captain") or "Agent-3"
    summary_msg = {
        "type": "verify",
        "from": payload.get("from", "Agent-5"),
        "to": captain,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "task_id": tr.task_id,
        "state": tr.state,
        "summary": payload.get("summary", ""),
    }
    _write_inbox_message(captain, summary_msg)
    # Optional devlog for update
    try:
        ev = payload.get("evidence")
        if isinstance(ev, list):
            ev_str = "; ".join([str(e) for e in ev])
        else:
            ev_str = str(ev) if ev else ""
        desc = f"task_id: {tr.task_id} | state: {tr.state}\nsummary: {payload.get('summary','')}"
        if ev_str:
            desc += f"\nevidence: {ev_str}"
        _post_discord(f"FSM_UPDATE {tr.task_id}", desc)
    except Exception:
        pass
    return {"ok": True, "task_id": tr.task_id, "state": tr.state}






