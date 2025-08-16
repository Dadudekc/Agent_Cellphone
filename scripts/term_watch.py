#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Terminal Watch:
- wrap: run a command, tee output to terminal + log, maintain heartbeat/state JSON
- watch: scan all agent term_state.json files, detect exited/dead/stalled, emit escalation events

Cross-platform (Windows/macOS/Linux). Requires: psutil
"""

from __future__ import annotations
import argparse, json, os, sys, time, threading, queue, shlex, subprocess, traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
try:
    import psutil
except ImportError:
    print("Missing dependency: psutil. Install with `pip install psutil`.", file=sys.stderr)
    sys.exit(1)

ISO = "%Y-%m-%dT%H:%M:%S.%fZ"

def utcnow_str() -> str:
    return datetime.utcnow().strftime(ISO)

def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    tmp.replace(path)

def append_ndjson(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")

def aggregate_cpu_percent(proc: psutil.Process) -> float:
    """Sum cpu% of proc + descendants. psutil.cpu_percent needs two calls to warm up."""
    total = proc.cpu_percent(interval=None)
    for c in proc.children(recursive=True):
        try:
            total += c.cpu_percent(interval=None)
        except Exception:
            pass
    return total

def safe_proc(pid: int) -> Optional[psutil.Process]:
    try:
        return psutil.Process(pid)
    except Exception:
        return None

def platform_shell_command(cmd: str) -> List[str]:
    if os.name == "nt":
        # Use cmd.exe for broad compatibility
        return ["cmd", "/c", cmd]
    else:
        # POSIX
        return ["bash", "-lc", cmd]

def wrap(args: argparse.Namespace) -> int:
    agent_id = str(args.agent_id)
    root = Path(args.root)
    agent_root = root / f"agent-{agent_id}"
    log_file = agent_root / "term.log"
    state_file = agent_root / "term_state.json"
    events = root / "events.ndjson"

    cmd = args.cmd
    cwd = Path(args.cwd) if args.cwd else Path.cwd()

    # Boot state
    state: Dict[str, Any] = {
        "agent_id": agent_id,
        "cmd": cmd,
        "cwd": str(cwd),
        "started_at": utcnow_str(),
        "last_output_at": None,
        "last_heartbeat_at": utcnow_str(),
        "pid": None,
        "ppid": os.getpid(),
        "exit_code": None,
        "status": "starting",
        "bytes_out": 0,
        "bytes_err": 0,
        "cpu_percent": 0.0,
        "host": os.uname().sysname if hasattr(os, "uname") else "Windows",
        "version": "term_watch/1.0",
    }
    write_json(state_file, state)

    # Launch
    proc = subprocess.Popen(
        platform_shell_command(cmd),
        cwd=str(cwd),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=1,
        universal_newlines=True,
        text=True,
    )
    state["pid"] = proc.pid
    state["status"] = "running"
    write_json(state_file, state)

    # Warm up cpu metrics
    p = safe_proc(proc.pid)
    if p:
        p.cpu_percent(interval=None)
        for c in p.children(recursive=True):
            try: c.cpu_percent(interval=None)
            except Exception: pass

    out_q: "queue.Queue[tuple[str,str]]" = queue.Queue()

    def pump(stream, tag: str):
        nonlocal state
        with log_file.open("a", encoding="utf-8") as lf:
            for line in stream:
                ts = utcnow_str()
                line2 = line.rstrip("\n")
                # Mirror to console
                print(line2, flush=True) if tag == "stdout" else print(line2, file=sys.stderr, flush=True)
                # Log with timestamp + tag
                lf.write(f"[{ts}] [{tag}] {line2}\n")
                if tag == "stdout":
                    state["bytes_out"] += len(line2) + 1
                else:
                    state["bytes_err"] += len(line2) + 1
                state["last_output_at"] = ts
                state["last_heartbeat_at"] = ts
                write_json(state_file, state)
        out_q.put(("eof", tag))

    t_out = threading.Thread(target=pump, args=(proc.stdout, "stdout"), daemon=True)
    t_err = threading.Thread(target=pump, args=(proc.stderr, "stderr"), daemon=True)
    t_out.start(); t_err.start()

    idle_beat = max(1.0, float(args.heartbeat_secs))
    try:
        while True:
            if p:
                try:
                    cpu = aggregate_cpu_percent(p)
                except Exception:
                    cpu = 0.0
            else:
                cpu = 0.0

            state["cpu_percent"] = round(cpu, 2)
            state["last_heartbeat_at"] = utcnow_str()
            write_json(state_file, state)

            if proc.poll() is not None:
                # Process exited
                state["exit_code"] = proc.returncode
                state["status"] = "exited"
                state["last_heartbeat_at"] = utcnow_str()
                write_json(state_file, state)
                append_ndjson(events, {
                    "ts": utcnow_str(),
                    "agent_id": agent_id,
                    "kind": "terminal_exit",
                    "exit_code": proc.returncode,
                    "cmd": cmd,
                    "state_file": str(state_file),
                })
                break

            try:
                item = out_q.get(timeout=idle_beat)
                if item[0] == "eof":
                    # Streams closed; wait for poll in next loop
                    pass
            except queue.Empty:
                pass
            time.sleep(idle_beat)
    except KeyboardInterrupt:
        try:
            proc.terminate()
        except Exception:
            pass
        state["status"] = "terminated"
        state["exit_code"] = proc.returncode
        write_json(state_file, state)
    return proc.returncode if proc and proc.returncode is not None else 0

def classify_status(state: Dict[str, Any], idle_secs: float, cpu_threshold: float) -> str:
    now = datetime.utcnow()
    hb = state.get("last_heartbeat_at")
    lo = state.get("last_output_at")
    exit_code = state.get("exit_code")
    pid = state.get("pid")

    if exit_code is not None:
        return "exited"

    # If no PID or process missing, treat as dead when heartbeat is stale
    pid_ok = pid is not None and safe_proc(int(pid)) is not None

    def age(ts: Optional[str]) -> float:
        if not ts: return float("inf")
        try:
            dt = datetime.strptime(ts, ISO)
            return (now - dt).total_seconds()
        except Exception:
            return float("inf")

    hb_age = age(hb)
    lo_age = age(lo)
    cpu = float(state.get("cpu_percent") or 0.0)

    if not pid_ok and hb_age > (2 * idle_secs):
        return "dead"

    # Soft stall: process alive, no output for idle window, and low CPU
    if pid_ok and lo_age > idle_secs and cpu < cpu_threshold:
        return "stalled"

    return "running"

def watch_once(args: argparse.Namespace) -> int:
    root = Path(args.root)
    idle_secs = float(args.idle_secs)
    cpu_threshold = float(args.cpu_threshold)
    events = root / "events.ndjson"
    escalations = root / "supervisor" / "escalations"
    escalations.mkdir(parents=True, exist_ok=True)

    # Find all term_state.json files
    for state_file in root.glob("agent-*/term_state.json"):
        try:
            state = json.loads(state_file.read_text())
        except Exception:
            continue
        prev = state.get("status")
        curr = classify_status(state, idle_secs=idle_secs, cpu_threshold=cpu_threshold)

        # Persist normalized status if changed
        if prev != curr:
            state["status"] = curr
            write_json(state_file, state)

        # Escalate on stalled/dead
        if curr in ("stalled", "dead"):
            notice = {
                "ts": utcnow_str(),
                "agent_id": state.get("agent_id"),
                "kind": f"terminal_{curr}",
                "pid": state.get("pid"),
                "cmd": state.get("cmd"),
                "status": curr,
                "state_file": str(state_file),
                "idle_secs": idle_secs,
                "cpu_threshold": cpu_threshold,
                "last_output_at": state.get("last_output_at"),
                "last_heartbeat_at": state.get("last_heartbeat_at"),
            }
            append_ndjson(events, notice)
            esc_file = escalations / f"agent-{state.get('agent_id')}_{curr}_{int(time.time())}.json"
            write_json(esc_file, notice)
    return 0

def watch_loop(args: argparse.Namespace) -> int:
    interval = max(2.0, float(args.interval))
    while True:
        try:
            watch_once(args)
        except Exception:
            # Never die silently
            sys.stderr.write("watch loop error:\n" + traceback.format_exc() + "\n")
        time.sleep(interval)

def main():
    p = argparse.ArgumentParser(prog="term_watch")
    sub = p.add_subparsers(dest="sub")

    p_wrap = sub.add_parser("wrap", help="Run a command with heartbeat/logging")
    p_wrap.add_argument("--agent-id", required=True, help="Numeric or string agent id")
    p_wrap.add_argument("--cmd", required=True, help="Command to run inside the terminal")
    p_wrap.add_argument("--cwd", default=None, help="Working directory")
    p_wrap.add_argument("--root", default="runtime/agent_comms", help="Root for agent comms")
    p_wrap.add_argument("--heartbeat-secs", default=1.0, help="Heartbeat frequency")
    p_wrap.set_defaults(func=wrap)

    p_watch = sub.add_parser("watch", help="Scan states and detect stalls/stops")
    p_watch.add_argument("--root", default="runtime/agent_comms", help="Root for agent comms")
    p_watch.add_argument("--idle-secs", default=45, help="Soft stall threshold in seconds")
    p_watch.add_argument("--cpu-threshold", default=1.0, help="CPU% below which we consider idle")
    p_watch.add_argument("--interval", default=10, help="Loop interval (secs)")
    p_watch.add_argument("--loop", action="store_true", help="Run continuously")
    def _watch_entry(a):
        return watch_loop(a) if a.loop else watch_once(a)
    p_watch.set_defaults(func=_watch_entry)

    args = p.parse_args()
    if not args.sub:
        p.print_help()
        return 2
    return args.func(args)

if __name__ == "__main__":
    sys.exit(main())
