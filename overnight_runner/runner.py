#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import random
import signal
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List
import datetime as _dt
from urllib import request, error

# Ensure src/ is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from agent_cell_phone import AgentCellPhone, MsgTag  # type: ignore


@dataclass
class PlannedMessage:
    tag: MsgTag
    template: str  # accepts {agent}


def build_message_plan(plan: str) -> List[PlannedMessage]:
    plan = plan.lower()
    # Single-repo, beta-readiness focused cadence
    if plan == "single-repo-beta":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume: focus the target repo to reach beta-ready."),
            PlannedMessage(MsgTag.TASK,   "{agent} implement one concrete step toward beta-ready in the focus repo."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} coordinate to avoid duplication; declare your focus area in the repo."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 10-min sync: status vs beta-ready checklist for the focus repo; next verifiable step."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify beta-ready criteria (GUI flows/tests). Attach evidence; summarize gaps if any."),
        ]
    if plan == "resume-only":
        return [PlannedMessage(MsgTag.RESUME, "{agent} resume autonomous operations. Continue working overnight. Summarize hourly.")]
    if plan == "contracts":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} review your assigned contracts in inbox and the repo TASK_LIST.md. Update TASK_LIST.md with next verifiable steps."),
            PlannedMessage(MsgTag.TASK,   "{agent} complete one contract to acceptance criteria. Commit small, verifiable edits; attach evidence."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} post a contract update to Agent-5: task_id, current state, next action, evidence links."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 10-min contract sync: changed, state per task_id, risks, next verifiable action."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify acceptance criteria and tests/build. Provide evidence. If blocked, stage diffs and summarize."),
        ]
    if plan == "autonomous-dev":
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
    if plan == "prd-milestones":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume: align to PRD milestones; pick next milestone and extract a small, verifiable task."),
            PlannedMessage(MsgTag.TASK,   "{agent} implement one step tied to the current PRD milestone; commit with tests/build evidence."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} coordinate on milestone ownership to avoid duplication; declare your current milestone ID."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 10-min sync: status vs active milestone; next verifiable step; risks."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify acceptance against the milestone's criteria; attach evidence and summary."),
        ]
    if plan == "repo-git-setup":
        return [
            PlannedMessage(MsgTag.RESUME, "{agent} resume: configure git for assigned repos using D:/repositories/github_config.json. Do not overwrite. Create branch DreamscapeSWARM-<date> on conflicts. Summarize findings."),
            PlannedMessage(MsgTag.TASK,   "{agent} for each assigned repo: if .git missing -> git init; set origin to https://github.com/<owner>/<repo>.git from github_config.json; commit TASK_LIST.md if new; fetch origin and attempt non-destructive merge; on conflicts, abort and create DreamscapeSWARM-<date> branch; leave notes."),
            PlannedMessage(MsgTag.COORDINATE, "{agent} coordinate: avoid concurrent pushes; open an issue/todo note when manual review is needed; attach repo and branch name."),
            PlannedMessage(MsgTag.SYNC,   "{agent} 10-min sync: per-repo status (origin set? branch? conflicts?), next step, risks."),
            PlannedMessage(MsgTag.VERIFY, "{agent} verify: attach git_setup_report.json path and any push logs for assigned repos."),
        ]
    return build_message_plan("resume-task-sync")


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("overnight_runner")
    p.add_argument("--layout", default="4-agent", help="layout mode (2-agent, 4-agent, 5-agent, 8-agent)")
    p.add_argument("--agents", help="comma-separated list of targets; defaults to all in layout")
    p.add_argument("--captain", help="designated captain agent; captain kickoff goes only to this agent")
    p.add_argument("--resume-agents", default="Agent-1,Agent-2,Agent-4", help="when captain set, cycle messages go to these agents (comma list)")
    p.add_argument("--sender", default="Agent-3", help="sender agent id label for ACP")
    p.add_argument("--interval-sec", type=int, default=600, help="seconds between cycles (default 600=10m)")
    p.add_argument("--duration-min", type=int, help="total minutes to run; alternative to --iterations")
    p.add_argument("--iterations", type=int, help="number of cycles to run; overrides duration if provided")
    p.add_argument("--plan", choices=["resume-only", "resume-task-sync", "aggressive", "autonomous-dev", "contracts", "single-repo-beta", "prd-milestones"], default="autonomous-dev", help="message plan to rotate through")
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
    # Agent workspace root for inbox/outbox and per-agent prompts
    p.add_argument("--workspace-root", default="agent_workspaces", help="root folder for agent workspaces")
    # Single‑repo focus options
    p.add_argument("--single-repo-mode", action="store_true", help="Focus all agents on a single repository until beta‑ready")
    p.add_argument("--focus-repo", help="Repository name to focus when in single‑repo mode. If omitted, the first alphabetical repo from --assign-root is used.")
    p.add_argument("--beta-ready-checklist", default="gui,buttons,happy-path,tests,readme,issues", help="Comma list of beta‑ready criteria to embed in prompts")
    # FSM extensions (optional)
    p.add_argument("--fsm-enabled", action="store_true", help="enable simple FSM orchestration with a designated agent")
    p.add_argument("--fsm-agent", help="agent id who acts as FSM orchestrator (defaults to captain or Agent-5 for 5-agent layout)")
    p.add_argument("--fsm-workflow", default="default", help="workflow name (informational)")
    p.add_argument("--prd-path", help="path to PRD JSON; with --plan prd-milestones, seeds FSM tasks from PRD milestones")
    p.add_argument("--seed-from-tasklists", action="store_true", help="scan repos' TASK_LIST.md to seed FSM queued tasks before running")
    # Contracts tailoring (optional)
    p.add_argument("--contracts-file", help="path to contracts.json to tailor messages per agent")
    # Noise/pacing controls
    p.add_argument("--resume-cooldown-sec", type=int, default=600, help="minimum seconds between RESUME messages per agent")
    p.add_argument("--resume-on-state-change", action="store_true", help="when an agent completes a task (FSM update), trigger RESUME immediately (bypasses cooldown once)")
    p.add_argument("--active-grace-sec", type=int, default=900, help="suppress messages to agents updated within the last N seconds")
    p.add_argument("--per-agent-cooldown-sec", type=int, default=300, help="minimum seconds between ANY messages to the same agent")
    p.add_argument("--suppress-resume", action="store_true", help="do not send RESUME messages at all")
    p.add_argument("--skip-assignments", action="store_true", help="skip initial per-agent repository assignment messages")
    p.add_argument("--skip-captain-kickoff", action="store_true", help="skip captain kickoff message")
    p.add_argument("--skip-captain-fsm-feed", action="store_true", help="skip captain FSM feed prompt")
    # New‑chat throttling knobs for ACP (propagated via env)
    p.add_argument("--new-chat-interval-sec", type=int, default=3600, help="minimum seconds between Ctrl+T new tabs per agent (default 3600=1h)")
    p.add_argument("--default-new-chat", action="store_true", help="request Ctrl+T on first contact only; subsequent sends obey interval throttle")
    # Stall detection / rescue
    p.add_argument("--stalled-threshold-sec", type=int, default=1200, help="if no state update for N seconds, treat agent as stalled")
    p.add_argument("--rescue-on-stall", action="store_true", help="when stalled, override with a RESUME rescue prompt (bypasses cooldown)")
    # Optional focus file name (FFN) to weave into prompts
    p.add_argument("--focus-file", dest="focus_file", help="fully qualified file path to emphasize in prompts (FFN)")
    # Devlog options (Discord)
    p.add_argument("--devlog-webhook", default=os.environ.get("DISCORD_WEBHOOK_URL"), help="Discord webhook URL for devlog notifications (or set DISCORD_WEBHOOK_URL)")
    p.add_argument("--devlog-username", default=os.environ.get("DEVLOG_USERNAME", "Agent Devlog"))
    p.add_argument("--devlog-embed", action="store_true", help="Send embed payloads instead of plain content")
    p.add_argument("--devlog-sends", action="store_true", help="Post a devlog message for each agent send from the runner")
    args = p.parse_args()
    # Propagate ACP throttling to environment so AgentCellPhone honors it
    if args.default_new_chat:
        os.environ["ACP_DEFAULT_NEW_CHAT"] = "1"
    else:
        os.environ.pop("ACP_DEFAULT_NEW_CHAT", None)
    os.environ["ACP_NEW_CHAT_INTERVAL_SEC"] = str(max(0, int(args.new_chat_interval_sec)))
    return args


def compute_iterations(args: argparse.Namespace) -> int:
    if args.iterations:
        return max(1, args.iterations)
    if args.duration_min and args.interval_sec > 0:
        return max(1, int((args.duration_min * 60) // args.interval_sec))
    return 1


def _post_discord(webhook: str | None, username: str, use_embed: bool, title: str, description: str) -> None:
    if not webhook:
        return
    payload: dict = {"username": username}
    if use_embed:
        payload["embeds"] = [{"title": title, "description": description, "color": 5814783}]
    else:
        payload["content"] = f"**{title}**\n{description}"
    try:
        data = __import__("json").dumps(payload).encode("utf-8")
        req = request.Request(webhook, data=data, headers={"Content-Type": "application/json"})
        with request.urlopen(req, timeout=6):
            pass
    except (error.HTTPError, error.URLError, Exception):
        pass


def discover_repositories(root_path: str) -> List[str]:
    repos: List[str] = []
    if not os.path.isdir(root_path):
        return repos
    # Common non-repo directories to exclude at the root
    exclude_names = {
        ".git", ".github", ".vscode", ".idea", ".pytest_cache", "__pycache__",
        "node_modules", "venv", ".venv", "dist", "build", ".mypy_cache", ".ruff_cache", ".tox", ".cache"
    }
    try:
        for name in sorted(os.listdir(root_path)):
            if name in exclude_names or name.startswith('.'):
                continue
            path = os.path.join(root_path, name)
            if not os.path.isdir(path):
                continue
            markers = [
                ".git", "requirements.txt", "package.json", "pyproject.toml", "setup.py", ".env", "README.md"
            ]
            if any(os.path.exists(os.path.join(path, m)) for m in markers):
                repos.append(name)
    except Exception:
        pass
    return repos


def assign_repositories(root_path: str, agents: List[str], max_per_agent: int) -> Dict[str, List[str]]:
    repo_names = discover_repositories(root_path)
    if not repo_names or not agents:
        return {}
    assignments: Dict[str, List[str]] = {a: [] for a in agents}
    idx = 0
    for repo in repo_names:
        target = agents[idx % len(agents)]
        if len(assignments[target]) >= max_per_agent:
            rotated = False
            for j in range(1, len(agents) + 1):
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


def load_contracts_map(contracts_file: str | None) -> Dict[str, List[dict]]:
    """Load contracts.json and return mapping of assignee -> list[contract].
    Contract keys expected: task_id, title, description, acceptance_criteria, evidence, assignee, repo, repo_path.
    """
    mapping: Dict[str, List[dict]] = {}
    if not contracts_file:
        return mapping
    try:
        import json as _j
        from pathlib import Path as _P
        p = _P(contracts_file)
        if not p.exists():
            return {}
        items = _j.loads(p.read_text(encoding="utf-8"))
        if not isinstance(items, list):
            return {}
        for c in items:
            if not isinstance(c, dict):
                continue
            assignee = c.get("assignee") or ""
            if not assignee:
                continue
            mapping.setdefault(assignee, []).append(c)
    except Exception:
        return {}
    return mapping


def build_tailored_message(agent: str, tag: MsgTag, contracts: List[dict]) -> str:
    """Create a per-agent message based on assigned contracts.
    Falls back to generic when no contracts are available for the agent.
    """
    # Choose the first contract for concise prompts
    c = contracts[0] if contracts else None
    if not c:
        # Generic fallback aligned to FSM
        if tag == MsgTag.RESUME:
            return f"{agent} resume on your assigned contract(s). Check inbox, execute one small, verifiable step, then send fsm_update to Agent-5 (task_id,state,summary,evidence)."
        if tag == MsgTag.TASK:
            return f"{agent} complete one contract to acceptance criteria. Commit small, verifiable edits with tests/build evidence; then fsm_update to Agent-5."
        if tag == MsgTag.SYNC:
            return f"{agent} 10-min contract sync: changed, state per task_id, risks, next verifiable action."
        if tag == MsgTag.VERIFY:
            return f"{agent} verify tests/build and attach evidence. If blocked by permissions, stage diffs and summarize."
        return f"{agent} continue operations."

    task_id = c.get("task_id", "")
    title = c.get("title", "contract")
    repo = c.get("repo", "")
    repo_path = c.get("repo_path", "")
    ac = c.get("acceptance_criteria") or []
    ev = c.get("evidence") or []

    if tag == MsgTag.RESUME:
        ac_line = ("; ".join(ac)) if isinstance(ac, list) else str(ac)
        return (
            f"{agent} resume: {task_id} — {title} ({repo}).\n"
            f"Acceptance: {ac_line}.\n"
            f"Evidence: {', '.join(ev) if isinstance(ev, list) else ev}.\n"
            f"Path: {repo_path}. After progress, send fsm_update to Agent-5 (task_id,state,summary,evidence)."
        )
    if tag == MsgTag.TASK:
        return (
            f"{agent} task: {task_id} — {title}. Execute one small, verifiable step in {repo_path}.\n"
            f"Commit with tests/build evidence; then send fsm_update to Agent-5."
        )
    if tag == MsgTag.SYNC:
        return (
            f"{agent} sync: {task_id} — state update and next action. Include brief summary + evidence links in fsm_update to Agent-5."
        )
    if tag == MsgTag.VERIFY:
        return (
            f"{agent} verify: run tests/build for {repo}. Attach output links in fsm_update; if blocked, stage diffs and summarize."
        )
    # Generic fallback for other tags
    return f"{agent} continue on {task_id}: {title}."


def read_agent_state(agent: str) -> Dict[str, str]:
    """Read agent_workspaces/Agent-X/state.json written by the listener."""
    try:
        p = Path("agent_workspaces") / agent / "state.json"
        if not p.exists():
            return {}
        import json as _j
        return _j.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def is_recently_active(agent: str, active_grace_sec: int) -> bool:
    st = read_agent_state(agent)
    updated = st.get("updated")
    if not updated:
        return False
    try:
        # updated format: YYYY-MM-DDTHH:MM:SS
        ts = _dt.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S")
        age = (_dt.datetime.utcnow() - ts).total_seconds()
        return age < float(active_grace_sec)
    except Exception:
        return False


def is_stalled(agent: str, stalled_threshold_sec: int) -> bool:
    """True if agent hasn't updated state.json within stalled_threshold_sec. Missing file counts as stalled."""
    st = read_agent_state(agent)
    updated = st.get("updated")
    if not updated:
        return True
    try:
        ts = _dt.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S")
        age = (_dt.datetime.utcnow() - ts).total_seconds()
        return age >= float(stalled_threshold_sec)
    except Exception:
        return True


def main() -> int:
    args = parse_args()

    # For 5-agent layout, prefer Agent-5 as captain and contracts plan if none provided
    if args.layout == "5-agent":
        if not args.captain:
            args.captain = "Agent-5"
        if args.resume_agents == "Agent-1,Agent-2,Agent-4":
            args.resume_agents = "Agent-1,Agent-2,Agent-3,Agent-4"
        if args.plan == "autonomous-dev":
            args.plan = "contracts"

    # Resolve focus repo for single‑repo mode
    focus_repo: str | None = None
    if args.single_repo_mode:
        if args.focus_repo:
            focus_repo = args.focus_repo
        else:
            try:
                repos = discover_repositories(args.assign_root)
                focus_repo = repos[0] if repos else None
            except Exception:
                focus_repo = None
        # Default plan for single‑repo focus if not explicitly set
        if args.plan not in ("single-repo-beta", "contracts"):
            args.plan = "single-repo-beta"

    acp = AgentCellPhone(agent_id=args.sender, layout_mode=args.layout, test=args.test)
    available = acp.get_available_agents()

    # Determine kickoff target(s) and cycle targets
    captain = args.captain
    if captain:
        kickoff_targets = [captain]
        # For cycles, use provided resume-agents list (defaults to 1,2,4)
        resume_agents = [a.strip() for a in args.resume_agents.split(',') if a.strip()]
        cycle_targets = [a for a in resume_agents if a in available]
        if not cycle_targets:
            # Fallback: all except captain
            cycle_targets = [a for a in available if a != captain]
    else:
        if args.agents:
            kickoff_targets = [a.strip() for a in args.agents.split(',') if a.strip()]
        else:
            kickoff_targets = available
        cycle_targets = kickoff_targets

    if not cycle_targets:
        print(f"No valid cycle targets in layout {args.layout}. Available: {available}")
        return 2

    plan = build_message_plan(args.plan)
    # Optional PRD -> FSM seeding when requested
    if args.plan == "prd-milestones" and getattr(args, "prd_path", None):
        try:
            from overnight_runner.fsm_bridge import seed_tasks_from_prd  # type: ignore
            result = seed_tasks_from_prd(args.prd_path, workflow_id=args.fsm_workflow)
            if not result.get("ok"):
                print(f"PRD seed failed: {result.get('error')}")
            else:
                print(f"PRD seed ok: created {result.get('count',0)} tasks")
        except Exception as _exc:
            print(f"PRD seed exception: {_exc}")
    # Optional seed from repo TASK_LIST.md files
    if getattr(args, "seed_from_tasklists", False):
        try:
            from overnight_runner.fsm_bridge import seed_tasks_from_tasklists  # type: ignore
            tl_res = seed_tasks_from_tasklists(workflow_id=args.fsm_workflow)
            if not tl_res.get("ok"):
                print(f"TASK_LIST seed failed: {tl_res.get('error')}")
            else:
                print(f"TASK_LIST seed ok: created {tl_res.get('count',0)} tasks")
        except Exception as _exc:
            print(f"TASK_LIST seed exception: {_exc}")
    # Resolve contracts file if not explicitly provided: pick latest from communications/overnight_*/<fsm-agent>/contracts.json
    contracts_file = args.contracts_file
    if not contracts_file:
        try:
            from pathlib import Path as _P
            comms = _P("D:/repositories/communications")
            if comms.exists():
                overnight_dirs = sorted([p for p in comms.iterdir() if p.is_dir() and p.name.startswith("overnight_")])
                latest = overnight_dirs[-1] if overnight_dirs else None
                if latest is not None:
                    fsm_agent = args.fsm_agent or captain or ("Agent-5" if args.layout == "5-agent" else None)
                    if fsm_agent:
                        cand = latest / fsm_agent / "contracts.json"
                        if cand.exists():
                            contracts_file = str(cand)
        except Exception:
            pass
    contracts_map = load_contracts_map(contracts_file)
    total_cycles = compute_iterations(args)

    stop_flag = {"stop": False}

    def handle_sigint(_sig, _frame):
        stop_flag["stop"] = True
        print("\nSTOP: Stopping after current cycle...")

    signal.signal(signal.SIGINT, handle_sigint)

    print(f"Overnight Runner starting (layout={args.layout}, sender={args.sender}, test={args.test})")
    try:
        _post_discord(args.devlog_webhook, args.devlog_username, args.devlog_embed,
                      "Overnight Runner starting",
                      f"layout={args.layout} | sender={args.sender} | plan={args.plan}")
    except Exception:
        pass
    print(f"Kickoff targets: {kickoff_targets}")
    print(f"Cycle targets: {cycle_targets}")
    print(f"Plan: {args.plan} | Interval: {args.interval_sec}s | Cycles: {total_cycles}")
    if args.fsm_enabled:
        fsm_agent = args.fsm_agent or captain or ("Agent-5" if args.layout == "5-agent" else None)
        print(f"FSM: enabled | agent={fsm_agent} | workflow={args.fsm_workflow}")
    if args.single_repo_mode:
        print(f"Single-repo mode: focus_repo={(focus_repo or 'N/A')} | checklist={args.beta_ready_checklist}")

    # Optional preamble
    if args.preamble:
        preamble = (
            "COLLAB NORMS: Avoid duplication, stubs, and shims. Reuse existing modules across repos. "
            "Always search for prior art before adding code; prefer refactor/reuse. "
            "Ship real, verifiable improvements (tests/build/docs). Keep edits small and cohesive. "
            f"Encourage agent-to-agent prompting: propose next steps to a peer, request feedback, then iterate. "
            f"Check each repo's TASK_LIST.md first; update it as you work. Use central comms at {args.comm_root} for notes/handoffs."
        )
        for agent in kickoff_targets:
            try:
                acp.send(agent, preamble, MsgTag.COORDINATE)
            except Exception:
                pass
        time.sleep(max(0, args.phase_wait_sec))

    # Optional assignments
    if not args.skip_assignments:
        assignments: Dict[str, List[str]] = {}
        try:
            if args.single_repo_mode:
                target_repo = focus_repo
                if not target_repo:
                    repos = discover_repositories(args.assign_root)
                    target_repo = repos[0] if repos else None
                if target_repo:
                    checklist = ", ".join([s.strip() for s in str(args.beta_ready_checklist).split(',') if s.strip()])
                    msg = (
                        f"Assignment: SINGLE-REPO FOCUS - {target_repo}. "
                        f"Goal: reach beta-ready tonight. Criteria: {checklist}. "
                        f"Action: open {target_repo}/TASK_LIST.md (or create), pick highest‑leverage item; keep edits small and verifiable."
                    )
                    for agent in cycle_targets:
                        try:
                            # Avoid forcing a new tab here to prevent double-onboarding.
                            # Initial onboarding already opened a new chat; rely on per-agent throttling for future Ctrl+T.
                            acp.send(agent, msg, MsgTag.TASK, new_chat=False)
                        except Exception:
                            pass
                    time.sleep(max(0, args.phase_wait_sec))
            else:
                assignments = assign_repositories(args.assign_root, cycle_targets, args.max_repos_per_agent)
                if assignments:
                    for agent, repos in assignments.items():
                        if not repos:
                            continue
                        # Filter out obvious non-repo noise from assignments just in case
                        filtered = [r for r in repos if r.lower() not in {".pytest_cache", "__pycache__", ".cache", "node_modules", "dist", "build"}]
                        if not filtered:
                            continue
                        summary = ", ".join(filtered)
                        msg = (
                            f"Assignment: focus these repos tonight: {summary}. "
                            f"Objectives: reduce duplication, consolidate utilities, add tests, and commit small, verifiable improvements. "
                            f"Action: open TASK_LIST.md in each repo (if present), pick the highest-leverage item, and update status as you progress."
                        )
                        try:
                            acp.send(agent, msg, MsgTag.TASK)
                        except Exception:
                            pass
                    time.sleep(max(0, args.phase_wait_sec))
        except Exception:
            pass

    # Captain kickoff goes only to captain
    if captain and not args.skip_captain_kickoff:
        kickoff = (
            "You are CAPTAIN tonight. Coordinate all agents. "
            "Tasks: 1) Plan assignments avoiding duplication 2) Prompt peers for sanity checks 3) Ensure work is real (no stubs) 4) Write handoffs in comms folder. "
            "Create a short TODO for yourself: (a) update repo TASK_LIST.md entries across active repos (b) draft/align FSM contracts per agent (states, transitions) (c) next verification step."
        )
        try:
            acp.send(captain, kickoff, MsgTag.CAPTAIN)
        except Exception:
            pass
        if args.fsm_enabled:
            fsm_agent = args.fsm_agent or captain
            try:
                acp.send(
                    fsm_agent,
                    (
                        "FSM ORCHESTRATION: Facilitate autonomous development across agents. "
                        "Ensure state transitions: task→executing, sync→syncing, verify→verifying, and keep agents unblocked. "
                        "Action now: Create a TODO list for yourself — 1) update TASK_LIST.md in active repos (ensure clear next steps) 2) document/update FSM contracts per agent (states/transitions) 3) schedule verification."
                    ),
                    MsgTag.COORDINATE,
                )
            except Exception:
                pass
        if args.fsm_enabled and not args.skip_captain_fsm_feed:
            # prompt captain to feed FSM via Agent-5
            fsm_note = "[FSM_FEED] Submit updates (task_id, state, summary, evidence) to Agent-5; Agent-5 will assign next steps from workflow."
            try:
                acp.send(captain, fsm_note, MsgTag.COORDINATE)
            except Exception:
                pass

    # Create comm folders optionally
    if args.create_comm_folders:
        try:
            setup_comm_folders(args.comm_root, available, discover_repositories(args.assign_root))
            if captain:
                write_comm_kickoff(args.comm_root, captain, args.plan)
        except Exception:
            pass

    time.sleep(max(0, args.initial_wait_sec))

    last_sent: Dict[str, Dict[str, float]] = {}
    # Track last any-message time per agent for global cooldown
    last_any_sent: Dict[str, float] = {}
    # Signal path for immediate resume on state-changes
    signal_dir = Path("D:/repositories/communications/_signals")
    # Track last repo focus we announced per agent, to decide when to re-open a new chat
    last_focus_repo_sent: Dict[str, str | None] = {a: None for a in available}
    for cycle in range(total_cycles):
        if stop_flag["stop"]:
            break
        planned = plan[cycle % len(plan)]
        print(f"\nCycle {cycle+1}/{total_cycles} - tag={planned.tag.name}")
        if args.fsm_enabled:
            # In FSM mode, captain triggers fsm_request to Agent-5 each cycle
            try:
                import time as _t, json as _j
                from pathlib import Path as _P
                # Drop fsm_request into Agent-5 inbox
                payload = {
                    "type": "fsm_request",
                    "from": captain or args.sender,
                    "to": args.fsm_agent,
                    "workflow": args.fsm_workflow,
                    "agents": cycle_targets,
                    "focus_repo": focus_repo,
                    "timestamp": _t.strftime("%Y-%m-%dT%H:%M:%S"),
                }
                inbox = _P("agent_workspaces") / args.fsm_agent / "inbox"
                inbox.mkdir(parents=True, exist_ok=True)
                fn = inbox / f"fsm_request_{_t.strftime('%Y%m%d_%H%M%S')}.json"
                fn.write_text(_j.dumps(payload, indent=2), encoding="utf-8")
            except Exception:
                pass
        for agent in cycle_targets:
            # Check for immediate resume signal and honor it once by bypassing cooldown
            force_resume = False
            try:
                if args.resume_on_state_change and planned.tag == MsgTag.RESUME and signal_dir.exists():
                    sig = signal_dir / f"resume_now_{agent}.signal"
                    if sig.exists():
                        force_resume = True
                        try:
                            sig.unlink()
                        except Exception:
                            pass
            except Exception:
                pass
            # If FSM is enabled, adjust RESUME content to inbox-driven flow
            agent_contracts = contracts_map.get(agent, []) or contracts_map.get(f"Agent-{agent}", [])

            # Pacing guards
            # 1) active grace: if agent updated state recently, skip to reduce noise/duplication
            try:
                from pathlib import Path as _P
            except Exception:
                pass
            from pathlib import Path as _P  # already imported above
            def _recent():
                try:
                    p = _P("agent_workspaces") / agent / "state.json"
                    if not p.exists():
                        return False
                    import json as _j
                    data = _j.loads(p.read_text(encoding="utf-8"))
                    updated = data.get("updated")
                    if not updated:
                        return False
                    ts = _dt.datetime.strptime(updated, "%Y-%m-%dT%H:%M:%S")
                    return (_dt.datetime.utcnow() - ts).total_seconds() < float(args.active_grace_sec)
                except Exception:
                    return False
            if _recent():
                continue
            # 2) stall detection (optional)
            stalled = False
            if args.__dict__.get("rescue_on_stall"):
                try:
                    stalled = is_stalled(agent, args.__dict__.get("stalled_threshold_sec", 1200))
                except Exception:
                    stalled = False
            # 3) per-agent global cooldown: avoid sending too frequently to the same agent
            if (time.time() - last_any_sent.get(agent, 0.0)) < float(args.per_agent_cooldown_sec):
                continue
            # 4) resume cooldown: limit RESUME frequency (unless force or stalled rescue)
            if planned.tag == MsgTag.RESUME and not (force_resume or stalled) and (args.suppress_resume or (time.time() - last_sent.get(agent, {}).get("RESUME", 0.0) < args.resume_cooldown_sec)):
                continue

            # Build content (tailored when available)
            if contracts_map:
                content = build_tailored_message(agent, planned.tag, agent_contracts)
            else:
                if args.__dict__.get("rescue_on_stall") and stalled:
                    checklist = ", ".join([s.strip() for s in str(args.beta_ready_checklist).split(',') if s.strip()])
                    content = (
                        f"{agent} resume. You appear stalled. Regain focus and continue on the beta-ready checklist: {checklist}. "
                        f"Open TASK_LIST.md, pick the next verifiable step, and after completion send an fsm_update (task_id,state,summary,evidence)."
                    )
                elif args.plan == "single-repo-beta":
                    repo_line = f"Focus repo: {focus_repo}. " if focus_repo else "Focus a valid repository under D:/repositories (not caches/temp). "
                    checklist = ", ".join([s.strip() for s in str(args.beta_ready_checklist).split(',') if s.strip()])
                    if planned.tag == MsgTag.RESUME:
                        content = (
                            f"{agent} resume. {repo_line}Goal: reach beta-ready tonight. "
                            f"Checklist: {checklist}. Start with GUI loads cleanly; all buttons/menus wired; happy-path flows; basic tests; README quickstart."
                        )
                    elif planned.tag == MsgTag.TASK:
                        content = (
                            f"{agent} implement one concrete step toward beta-ready in {focus_repo or 'the focus repo'}: "
                            f"e.g., wire a missing button handler, fix a flow, add a smoke test. Commit small, verifiable edits with evidence."
                        )
                    elif planned.tag == MsgTag.COORDINATE:
                        content = (
                            f"{agent} coordinate to avoid duplication in {focus_repo or 'the focus repo'}: declare your current component area, "
                            f"search first for reuse, and request a quick sanity check from a peer before large changes."
                        )
                    elif planned.tag == MsgTag.SYNC:
                        content = (
                            f"{agent} 10-min sync: status vs beta-ready checklist for {focus_repo or 'the focus repo'}; next verifiable step; risks."
                        )
                    elif planned.tag == MsgTag.VERIFY:
                        content = (
                            f"{agent} verify: run GUI smoke, tests/build for {focus_repo or 'the focus repo'}. Attach evidence. "
                            f"If blocked, stage diffs and summarize the gap + next step."
                        )
                    else:
                        content = planned.template.format(agent=agent)
                else:
                    if args.fsm_enabled and planned.tag == MsgTag.RESUME:
                        # Include per-agent workspace and inbox directories in the guidance
                        workspace_dir = os.path.join(args.workspace_root, agent)
                        inbox_dir = os.path.join(workspace_dir, "inbox")
                        ffn_line = f"\nFocus file: {args.focus_file}" if getattr(args, "focus_file", None) else ""
                        content = (
                            f"{agent} check your inbox for new assignments. Create/refresh your TASK_LIST.md based on assigned tasks,"
                            f" then execute sequentially with small, verifiable edits. Post evidence and updates via inbox.\n"
                            f"Workspace: {workspace_dir}\nInbox: {inbox_dir}{ffn_line}"
                        )
                    else:
                        content = planned.template.format(agent=agent)
            # Decide whether to request new-chat (Ctrl+T) for this send.
            # Only open a new tab when recovering from a stall or when focus repo changes.
            use_new_chat = False
            if planned.tag == MsgTag.RESUME and force_resume:
                use_new_chat = True
            elif args.single_repo_mode and focus_repo and last_focus_repo_sent.get(agent) != focus_repo:
                use_new_chat = True
            try:
                acp.send(agent, content, planned.tag, new_chat=use_new_chat)
                if args.devlog_sends:
                    _post_discord(
                        args.devlog_webhook,
                        args.devlog_username,
                        args.devlog_embed,
                        f"SEND {planned.tag.name} -> {agent}",
                        (content[:900] + "…") if len(content) > 900 else content,
                    )
                now_ts = time.time()
                last_any_sent[agent] = now_ts
                last_sent.setdefault(agent, {})[planned.tag.name] = now_ts
                if args.single_repo_mode:
                    last_focus_repo_sent[agent] = focus_repo
            except Exception:
                pass
            base = args.stagger_ms / 1000.0
            jitter = (args.jitter_ms / 1000.0) if args.jitter_ms else 0.0
            delay = base + random.uniform(-jitter, jitter)
            time.sleep(max(0.0, delay))

        if cycle < total_cycles - 1:
            remaining = args.interval_sec
            while remaining > 0 and not stop_flag["stop"]:
                time.sleep(min(1.0, remaining))
                remaining -= 1

    print("\nOvernight Runner finished")
    try:
        _post_discord(args.devlog_webhook, args.devlog_username, args.devlog_embed,
                      "Overnight Runner finished", "Done")
    except Exception:
        pass
    return 0


def setup_comm_folders(root: str, agents: List[str], repo_names: List[str]) -> None:
    os.makedirs(root, exist_ok=True)
    for agent in agents:
        agent_dir = os.path.join(root, agent)
        os.makedirs(agent_dir, exist_ok=True)
        readme = os.path.join(agent_dir, "README.txt")
        if not os.path.exists(readme):
            with open(readme, 'w', encoding='utf-8') as f:
                f.write("Agent communication notes, handoffs, and status logs. Keep concise and actionable.\n")
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



