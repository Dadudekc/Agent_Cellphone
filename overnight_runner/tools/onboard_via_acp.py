#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
import time
from typing import List


def run(args_list: List[str]) -> int:
    try:
        p = subprocess.run([sys.executable] + args_list, check=True)
        return p.returncode
    except subprocess.CalledProcessError as e:
        return e.returncode


def main() -> int:
    p = argparse.ArgumentParser("onboard_via_acp")
    p.add_argument("--layout", default="5-agent")
    p.add_argument("--agents", default="Agent-1,Agent-2,Agent-3,Agent-4,Agent-5")
    p.add_argument("--sender", default="Agent-3")
    p.add_argument("--sleep-ms", type=int, default=400)
    args = p.parse_args()

    agents = [a.strip() for a in args.agents.split(',') if a.strip()]

    base_msg = (
        "Welcome. New chat initialized. Single‑repo focus until beta‑ready. "
        "Follow FSM: check your inbox for assignments; create/refresh TASK_LIST.md; execute small, verifiable edits. "
        "Beta‑ready checklist: GUI loads, buttons wired, happy‑path flows, basic tests, README quickstart, issues tracked. "
        "Post evidence and updates via inbox."
    )

    for agent in agents:
        cmd = [
            "src/agent_cell_phone.py",
            "--layout", args.layout,
            "--agent", agent,
            "--msg", base_msg,
            "--tag", "coordinate",
            "--new-chat",
        ]
        rc = run(cmd)
        time.sleep(max(0, args.sleep_ms) / 1000.0)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())








