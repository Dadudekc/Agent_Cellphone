#!/usr/bin/env python3
"""
Overnight Runner – Agent Cell Phone scheduler
=============================================
Sends periodic resume/coordination prompts to agents using the Agent Cell Phone (ACP).

Usage examples:
  python scripts/overnight_runner.py --layout 4-agent --agents Agent-1,Agent-2,Agent-3,Agent-4 \
      --interval-sec 900 --duration-min 480 --sender Agent-3

Quick test (no mouse/keyboard movement):
  python scripts/overnight_runner.py --layout 4-agent --iterations 1 --interval-sec 2 --test

Live single iteration sanity check:
  python scripts/overnight_runner.py --layout 4-agent --iterations 1 --interval-sec 2 --sender Agent-3
"""

from __future__ import annotations

import argparse
import signal
import sys
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict
import os
import random

from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from agent_cell_phone import AgentCellPhone, MsgTag  # noqa: E402


@dataclass
class PlannedMessage:
    tag: MsgTag
    template: str  # accepts {agent}


def build_message_plan(plan: str) -> List[PlannedMessage]:
    plan = plan.lower()
    if plan == "resume-only":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume autonomous operations. Continue working overnight. Summarize hourly."),
        ]
    if plan == "autonomous-dev":
        # Alternating prompts designed to foster autonomous progress and peer interaction
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume autonomous development. Choose the highest-leverage task from your assigned repos and begin now."),
            PlannedMessage(MsgTag.TASK,   "{agent} implement one concrete improvement (tests/build/lint/docs/refactor). Prefer reuse over new code. Commit in small, verifiable edits."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} prompt a peer agent with your next step and ask for a quick sanity check. Incorporate feedback, avoid duplication."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 10-min sync: what changed, open TODO, and the next verifiable action. Keep momentum; avoid placeholders."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify outcomes (tests/build). If blocked by permissions, stage diffs and summarize impact + next steps for review."),
        ]
    if plan == "resume-task-sync":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume operations. Maintain uninterrupted focus. Report blockers."),
            PlannedMessage(MsgTag.TASK,   "{agent} choose highest-impact repo under D:\\repositories. Ship 1 measurable improvement."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} coordinate with team. Hand off incomplete work with clear next steps."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 30-min sync: brief status, next step, risks."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify tests/build. If blocked by approvals, prepare changes and summaries."),
        ]
    if plan == "aggressive":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume now. Prioritize compilers: tests/build>lint>docs>CI."),
            PlannedMessage(MsgTag.TASK,   "{agent} implement 1-2 fixes from failing tests or lints. Stage diffs with clear messages."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} request handoff from peers. Consolidate partial work into a single branch plan."),
            PlannedMessage(MsgTag.SYNC,   "{agent} sync: what changed, what remains, ETA by next cycle."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify outcomes. Prepare a concise summary for morning review."),
        ]
    # default
    return build_message_plan("resume-task-sync")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("overnight_runner")
    p.add_argument("--layout", default="4-agent", help="layout mode (2-agent, 4-agent, 8-agent)")
    p.add_argument("--agents", help="comma-separated list of targets; defaults to all in layout")
    p.add_argument("--captain", help="designated captain agent; if set, only the captain is messaged and coordinates others")
    p.add_argument("--sender", default="Agent-3", help="sender agent id label for ACP")
    p.add_argument("--interval-sec", type=int, default=600, help="seconds between cycles (default 600=10m)")
    p.add_argument("--duration-min", type=int, help="total minutes to run; alternative to --iterations")
    p.add_argument("--iterations", type=int, help="number of cycles to run; overrides duration if provided")
    p.add_argument("--plan", choices=["resume-only", "resume-task-sync", "aggressive", "autonomous-dev"], default="autonomous-dev",
                   help="message plan to rotate through")
    p.add_argument("--test", action="store_true", help="dry-run; do not move mouse/keyboard")
    p.add_argument("--stagger-ms", type=int, default=2000, help="delay between sends per agent within a cycle (ms)")
    p.add_argument("--jitter-ms", type=int, default=500, help="random +/- jitter added to stagger (ms)")
    p.add_argument("--initial-wait-sec", type=int, default=60, help="wait before first cycle to let preamble/assignments settle")
    p.add_argument("--phase-wait-sec", type=int, default=15, help="wait between preamble, assignments, and captain kickoff")
    p.add_argument("--preamble", action="store_true", help="send anti-duplication coordination preamble at start")
    p.add_argument("--assign-root", default="D:/repositories", help="root folder to assign repositories from")
    p.add_argument("--max-repos-per-agent", type=int, default=5, help="limit of repos per agent in assignment")
    p.add_argument("--comm-root", default="D:/repositories/_agent_communications", help="central communications root (non-invasive)")
    p.add_argument("--create-comm-folders", action="store_true", help="create central communications folders and kickoff notes")
    return p.parse_args()


def compute_iterations(args: argparse.Namespace) -> int:
    if args.iterations:
        return max(1, args.iterations)
    if args.duration_min and args.interval_sec > 0:
        return max(1, int((args.duration_min * 60) // args.interval_sec))
    # default: one cycle
    return 1


def main() -> int:
    args = parse_args()

    acp = AgentCellPhone(agent_id=args.sender, layout_mode=args.layout, test=args.test)
    available = acp.get_available_agents()

    if args.captain:
        targets = [args.captain]
    elif args.agents:
        targets = [a.strip() for a in args.agents.split(',') if a.strip()]
    else:
        targets = available

    # Restrict to known agents in current layout
    targets = [t for t in targets if t in available]
    if not targets:
        print(f"No valid targets in layout {args.layout}. Available: {available}")
        return 2

    plan = build_message_plan(args.plan)
    total_cycles = compute_iterations(args)

    stop_flag = {"stop": False}

    def handle_sigint(_sig, _frame):
        stop_flag["stop"] = True
        print("\nSTOP: Stopping after current cycle...")

    signal.signal(signal.SIGINT, handle_sigint)

    print(f"Overnight Runner starting (layout={args.layout}, sender={args.sender}, test={args.test})")
    print(f"Targets: {targets}")
    print(f"Plan: {args.plan} | Interval: {args.interval_sec}s | Cycles: {total_cycles}")

    # Optional preamble to set collaboration norms and anti-duplication policy
    if args.preamble:
        preamble = (
            "COLLAB NORMS: Avoid duplication, stubs, and shims. Reuse existing modules across repos. "
            "Always search for prior art before adding code; prefer refactor/reuse. "
            "Ship real, verifiable improvements (tests/build/docs). Keep edits small and cohesive. "
            f"Encourage agent-to-agent prompting: propose next steps to a peer, request feedback, then iterate. "
            f"Check each repo's TASK_LIST.md first; update it as you work. Use central comms at {args.comm_root} for notes/handoffs."
        )
        for agent in targets:
            try:
                acp.send(agent, preamble, MsgTag.COORDINATE)
            except Exception as e:
                print(f"Preamble send failed for {agent}: {e}")
        # allow time for agents to react to preamble
        time.sleep(max(0, args.phase_wait_sec))

    # Optional repository assignments to reduce overlap
    assignments: Dict[str, List[str]] = {}
    try:
        assignments = assign_repositories(args.assign_root, targets, args.max_repos_per_agent)
    except Exception as e:
        print(f"Assignment step skipped: {e}")

    if assignments:
        for agent, repos in assignments.items():
            if not repos:
                continue
            summary = ", ".join(repos)
            msg = (
                f"Assignment: focus these repos tonight: {summary}. "
                f"Objectives: reduce duplication, consolidate utilities, add tests, and commit small, verifiable improvements. "
                f"Action: open TASK_LIST.md in each repo (if present), pick the highest-leverage item, and update status as you progress."
            )
            try:
                acp.send(agent, msg, MsgTag.TASK)
            except Exception as e:
                print(f"Assignment send failed for {agent}: {e}")
        # allow time for agents to start on assignments
        time.sleep(max(0, args.phase_wait_sec))

    # Captain kickoff
    if args.captain:
        captain = targets[0]
        kickoff = (
            "You are CAPTAIN tonight. Coordinate all agents in the 4-agent layout. "
            "Tasks: 1) Plan assignments avoiding duplication 2) Prompt peers for sanity checks 3) Ensure work is real (no stubs) 4) Write handoffs in comms folder."
        )
        try:
            acp.send(captain, kickoff, MsgTag.CAPTAIN)
        except Exception as e:
            print(f"Captain kickoff failed for {captain}: {e}")

    # Create central communications folders and kickoff notes
    if args.create_comm_folders:
        try:
            setup_comm_folders(args.comm_root, available, discover_repositories(args.assign_root))
            # Drop a captain README
            if args.captain:
                write_comm_kickoff(args.comm_root, args.captain, args.plan)
        except Exception as e:
            print(f"Comm folder setup skipped: {e}")

    # give a buffer before the first cycle so agents can coordinate
    time.sleep(max(0, args.initial_wait_sec))

    for cycle in range(total_cycles):
        if stop_flag["stop"]:
            break
        msg_idx = cycle % len(plan)
        planned = plan[msg_idx]

        print(f"\nCycle {cycle+1}/{total_cycles} - tag={planned.tag.name}")
        for i, agent in enumerate(targets):
            # Format content
            content = planned.template.format(agent=agent)
            try:
                acp.send(agent, content, planned.tag)
            except Exception as e:
                print(f"Send failed for {agent}: {e}")
            # stagger to avoid rapid window focus switching
            base = args.stagger_ms / 1000.0
            jitter = (args.jitter_ms / 1000.0) if args.jitter_ms else 0.0
            delay = base + random.uniform(-jitter, jitter)
            time.sleep(max(0.0, delay))

        # sleep between cycles
        if cycle < total_cycles - 1:
            remaining = args.interval_sec
            while remaining > 0 and not stop_flag["stop"]:
                time.sleep(min(1.0, remaining))
                remaining -= 1

    print("\nOvernight Runner finished")
    return 0


def discover_repositories(root_path: str) -> List[str]:
    """Discover top-level repositories in the given root directory.
    Returns directory names under root that look like repos.
    """
    repos: List[str] = []
    if not os.path.isdir(root_path):
        return repos
    try:
        for name in sorted(os.listdir(root_path)):
            path = os.path.join(root_path, name)
            if not os.path.isdir(path):
                continue
            # Heuristics: treat as repo if it contains any code marker
            markers = [".git", "requirements.txt", "package.json", "pyproject.toml", "setup.py", ".env", "README.md"]
            if any(os.path.exists(os.path.join(path, m)) for m in markers):
                repos.append(name)
    except Exception:
        pass
    return repos


def assign_repositories(root_path: str, agents: List[str], max_per_agent: int) -> Dict[str, List[str]]:
    """Divide discovered repositories among agents to minimize overlap."""
    repo_names = discover_repositories(root_path)
    if not repo_names or not agents:
        return {}
    assignments: Dict[str, List[str]] = {a: [] for a in agents}
    idx = 0
    for repo in repo_names:
        target = agents[idx % len(agents)]
        if len(assignments[target]) >= max_per_agent:
            # find next with capacity
            rotated = False
            for j in range(1, len(agents)+1):
                candidate = agents[(idx + j) % len(agents)]
                if len(assignments[candidate]) < max_per_agent:
                    target = candidate
                    rotated = True
                    break
            if not rotated:
                break
        assignments[target].append(repo)
        idx += 1
    return assignments


def setup_comm_folders(root: str, agents: List[str], repo_names: List[str]) -> None:
    os.makedirs(root, exist_ok=True)
    # Create per-agent folders
    for agent in agents:
        agent_dir = os.path.join(root, agent)
        os.makedirs(agent_dir, exist_ok=True)
        readme = os.path.join(agent_dir, "README.txt")
        if not os.path.exists(readme):
            with open(readme, 'w', encoding='utf-8') as f:
                f.write("Agent communication notes, handoffs, and status logs. Keep concise and actionable.\n")
    # Create per-repo note folders
    repo_root = os.path.join(root, "repos")
    os.makedirs(repo_root, exist_ok=True)
    for repo in repo_names:
        repo_dir = os.path.join(repo_root, repo)
        os.makedirs(repo_dir, exist_ok=True)
        readme = os.path.join(repo_dir, "README.txt")
        if not os.path.exists(readme):
            with open(readme, 'w', encoding='utf-8') as f:
                f.write("Repo-specific coordination notes. Link PRs/commits and open TODOs.\n")


def write_comm_kickoff(root: str, captain: str, plan: str) -> None:
    captain_dir = os.path.join(root, captain)
    os.makedirs(captain_dir, exist_ok=True)
    kickoff_path = os.path.join(captain_dir, "CAPTAIN_KICKOFF.txt")
    with open(kickoff_path, 'w', encoding='utf-8') as f:
        f.write(
            "Captain kickoff instructions\n"
            "- Coordinate agents in 4-agent layout\n"
            "- Avoid duplication; prefer reuse/refactor across repos\n"
            "- Prompt peers for quick reviews; integrate feedback\n"
            f"- Plan: {plan}\n"
            "- Keep comms and handoffs in this folder and repos/ subfolder\n"
        )


if __name__ == "__main__":
    raise SystemExit(main())


