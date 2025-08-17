#!/usr/bin/env python3
import json, os, sys, subprocess, time, pathlib, shutil, datetime as dt
from dataclasses import dataclass, field
from typing import Dict, List, Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "fsm.yml"
TASKS_DIR = ROOT / "runtime" / "tasks"
REPORTS_DIR = ROOT / "runtime" / "overnight" / dt.datetime.now().strftime("overnight_%Y%m%d")
ARTIFACTS_DIR = REPORTS_DIR / "artifacts"
HEARTBEATS = ROOT / "runtime" / "agent_comms" / "agents"
DIGEST_MD = REPORTS_DIR / "digest.md"
DIGEST_JSON = REPORTS_DIR / "digest.json"

try:
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore
    # We don't raise or exit here so that modules which only need helper
    # functions (e.g. tests for ``run_guard``) can still import this module
    # without requiring the optional ``pyyaml`` package.

def sh(cmd, cwd=None, capture=False) -> subprocess.CompletedProcess:
    return subprocess.run(cmd if isinstance(cmd, list) else cmd.split(),
                          cwd=cwd, text=True, capture_output=capture, check=False)

def load_yaml(p):
    """Load a YAML file.

    Falls back to JSON parsing when ``pyyaml`` isn't available.  This keeps the
    module usable in minimal environments while still supporting the expected
    YAML syntax when the dependency is installed.
    """
    text = open(p, "r", encoding="utf-8").read()
    if yaml is not None:
        return yaml.safe_load(text)
    # Fallback: try JSON so simple dict-like configs still load during tests
    try:
        import json
        return json.loads(text)
    except Exception as exc:  # pragma: no cover - depends on file contents
        raise RuntimeError("YAML parsing requires pyyaml to be installed") from exc

@dataclass
class Task:
    id: str
    repo: str
    branch: str
    state: str
    path: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)
    file_path: pathlib.Path = None

def read_tasks() -> List[Task]:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    tasks = []
    for fp in TASKS_DIR.glob("*.json"):
        data = json.loads(fp.read_text())
        tasks.append(Task(
            id=data["id"], repo=data["repo"], branch=data.get("branch","main"),
            state=data.get("state","Plan"), path=data.get("path",""),
            meta=data.get("meta",{}), file_path=fp))
    return tasks

def write_task(t: Task):
    d = {"id": t.id, "repo": t.repo, "branch": t.branch, "state": t.state,
         "path": t.path, "meta": t.meta}
    t.file_path.write_text(json.dumps(d, indent=2))

def ensure_repo(task: Task) -> pathlib.Path:
    workdir = REPORTS_DIR / "work" / task.id
    workdir.mkdir(parents=True, exist_ok=True)
    if (workdir / ".git").exists():
        sh("git fetch --all --prune", cwd=workdir)
    else:
        sh(f"git clone {task.repo} .", cwd=workdir)
    sh(f"git checkout {task.branch}", cwd=workdir)
    sh("git pull --ff-only", cwd=workdir)
    return workdir

def run_guard(name: str, cmd: str, cwd: pathlib.Path) -> Dict[str, Any]:
    started = dt.datetime.now().isoformat()
    res = sh(cmd, cwd=cwd, capture=True)
    ended = dt.datetime.now().isoformat()
    ok = res.returncode == 0
    out = {
        "guard": name, "cmd": cmd, "ok": ok, "rc": res.returncode,
        "stdout": res.stdout[-5000:] if res.stdout else "",  # keep digest small
        "stderr": res.stderr[-5000:] if res.stderr else "",
        "started": started, "ended": ended,
    }
    return out

def heartbeat_scan(max_age_sec=900):
    findings = []
    if not HEARTBEATS.exists(): return findings
    now = dt.datetime.now().timestamp()
    for hb in HEARTBEATS.glob("*/heartbeat.json"):
        try:
            ts = json.loads(hb.read_text()).get("ts_epoch", 0)
            if now - ts > max_age_sec:
                findings.append({"agent": hb.parent.name, "status": "stale", "age_sec": int(now - ts)})
        except Exception:
            findings.append({"agent": hb.parent.name, "status": "invalid"})
    return findings

def advance_state(fsm, state, guards_ok: bool) -> str:
    spec = fsm["states"].get(state, {})
    if "on_pass" in spec or "on_fail" in spec:
        return spec["on_pass"] if guards_ok else spec["on_fail"]
    return spec.get("next", state)

def process_task(task: Task, fsm: Dict[str, Any]) -> Dict[str, Any]:
    result = {"task": task.id, "from": task.state, "to": task.state, "guards": [], "ok": True}
    if task.state not in ("Build", "Review", "Deploy", "Quarantine", "Rollback"):
        result["note"] = "Skipped: state not actionable."
        return result

    repo_path = ensure_repo(task)
    guards = (fsm["states"].get(task.state, {}) or {}).get("guards", [])
    all_ok = True
    for g in guards:
        cmd = fsm["guards"][g]
        gr = run_guard(g, cmd, repo_path)
        result["guards"].append(gr)
        if not gr["ok"]: all_ok = False
        # write per-guard artifact
        afp = ARTIFACTS_DIR / task.id / f"{task.state}_{g}.json"
        afp.parent.mkdir(parents=True, exist_ok=True)
        afp.write_text(json.dumps(gr, indent=2))

    new_state = advance_state(fsm, task.state, all_ok)
    result["to"] = new_state; result["ok"] = all_ok
    task.state = new_state
    write_task(task)
    return result

def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    fsm = load_yaml(CONFIG)
    tasks = [t for t in read_tasks() if t.state in ("Build","Review","Deploy","Quarantine","Rollback")]
    summary = {"ts": dt.datetime.now().isoformat(), "processed": [], "heartbeats": heartbeat_scan()}
    for t in tasks:
        outcome = process_task(t, fsm)
        summary["processed"].append(outcome)

    DIGEST_JSON.write_text(json.dumps(summary, indent=2))

    # render simple digest.md (no Jinja dependency)
    lines = [f"# 🌙 Overnight Digest — {dt.datetime.now():%Y-%m-%d}",
             f"- Tasks processed: {len(summary['processed'])}",
             f"- Stale agents: {len([h for h in summary['heartbeats'] if h.get('status')=='stale'])}",
             "", "## Task Outcomes"]
    for o in summary["processed"]:
        status = "✅" if o["ok"] else "❌"
        lines.append(f"- {status} **{o['task']}**: {o['from']} → {o['to']} ({len(o['guards'])} checks)")
    if summary["heartbeats"]:
        lines += ["", "## Agent Heartbeats"]
        for h in summary["heartbeats"]:
            if h["status"]=="stale":
                lines.append(f"- ⚠️ {h['agent']}: stale {h['age_sec']}s")
            else:
                lines.append(f"- ❔ {h['agent']}: {h['status']}")
    DIGEST_MD.write_text("\n".join(lines))
    print(f"Wrote {DIGEST_JSON} and {DIGEST_MD}")

if __name__ == "__main__":
    main()
