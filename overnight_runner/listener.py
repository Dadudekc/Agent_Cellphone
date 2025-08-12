#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from urllib import request, error

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from core.inbox_listener import InboxListener  # type: ignore
from core.message_pipeline import MessagePipeline  # type: ignore
from core.command_router import CommandRouter  # type: ignore


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("overnight_listener")
    p.add_argument("--agent", default="Agent-3")
    p.add_argument("--inbox")
    p.add_argument("--poll", type=float, default=0.2)
    p.add_argument("--devlog-webhook", default=os.environ.get("DISCORD_WEBHOOK_URL"), help="Discord webhook URL for devlog notifications (or set DISCORD_WEBHOOK_URL)")
    p.add_argument("--devlog-username", default=os.environ.get("DEVLOG_USERNAME", "Agent Devlog"))
    p.add_argument("--devlog-embed", action="store_true", help="Send embed payloads instead of plain content")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    agent = args.agent
    inbox_dir = args.inbox or os.path.join("agent_workspaces", agent, "inbox")
    devlog_webhook = args.devlog_webhook
    devlog_username = args.devlog_username
    devlog_use_embed = bool(args.devlog_embed)

    pipeline = MessagePipeline()
    router = CommandRouter()

    # Simple per-agent state file under agent_workspaces/Agent-X/state.json
    state_dir = Path("agent_workspaces") / agent
    state_dir.mkdir(parents=True, exist_ok=True)
    state_path = state_dir / "state.json"

    def load_state() -> dict:
        try:
            return json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {"state": "idle"}
        except Exception:
            return {"state": "idle"}

    def save_state(data: dict) -> None:
        try:
            state_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def _now() -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%S")

    def _post_discord(title: str, description: str) -> None:
        if not devlog_webhook:
            return
        payload: dict = {"username": devlog_username}
        if devlog_use_embed:
            payload["embeds"] = [{"title": title, "description": description, "color": 5814783}]
        else:
            payload["content"] = f"**{title}**\n{description}"
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(devlog_webhook, data=data, headers={"Content-Type": "application/json"})
        try:
            with request.urlopen(req, timeout=5) as _:
                pass
        except error.HTTPError:
            pass
        except error.URLError:
            pass

    listener = InboxListener(inbox_dir=inbox_dir, poll_interval_s=args.poll, pipeline=pipeline)
    def on_message(data: dict) -> None:
        print(f"[INBOX] {agent} <- {json.dumps(data, ensure_ascii=False)}")
        # Idempotent processing: move into processing/ is assumed inside InboxListener;
        # here we only route and persist minimal state
        st = load_state()
        msg_type = str(data.get("type", "")).lower()
        schema_version = int(data.get("schema_version", 1)) if isinstance(data.get("schema_version", 1), int) else 1
        ttl_s = data.get("ttl_s")
        created_at = data.get("created_at")
        # Respect ttl when provided
        if isinstance(ttl_s, (int, float)) and created_at:
            try:
                from datetime import datetime
                created = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S")
                age = (datetime.utcnow() - created).total_seconds()
                if age > float(ttl_s):
                    return
            except Exception:
                pass
        next_state = st.get("state", "idle")
        if msg_type == "task":
            next_state = "executing"
        elif msg_type == "sync":
            next_state = "syncing"
        elif msg_type == "ack":
            next_state = st.get("state", "idle")
        elif msg_type == "note":
            next_state = st.get("state", "idle")
        elif msg_type in ("verify", "resume"):
            # if such types are used via inbox
            next_state = "verifying" if msg_type == "verify" else "ready"

        st.update({
            "last_message": data,
            "state": next_state,
            "updated": _now(),
            "schema_version": schema_version,
        })
        save_state(st)

        # If a task_id present, update consolidated contracts file and optionally patch TASK_LIST.md
        try:
            if "task_id" in data:
                comms_root = Path("D:/repositories/communications")
                # find latest overnight_* folder
                latest = None
                if comms_root.exists():
                    candidates = sorted([p for p in comms_root.iterdir() if p.is_dir() and p.name.startswith("overnight_")])
                    latest = candidates[-1] if candidates else None
                if latest is not None:
                    agent_dir = latest / agent
                    contracts_path = agent_dir / "FSM_CONTRACTS" / "contracts.json"
                    if not contracts_path.exists():
                        contracts_path = agent_dir / "contracts.json"
                    if contracts_path.exists():
                        import json as _j
                        try:
                            arr = _j.loads(contracts_path.read_text(encoding="utf-8"))
                        except Exception:
                            arr = []
                        updated = False
                        target_repo_path = data.get("repo_path")
                        for c in arr:
                            if isinstance(c, dict) and c.get("task_id") == data.get("task_id"):
                                if "state" in data:
                                    c["state"] = data["state"]
                                if "evidence" in data:
                                    existing = c.get("evidence") or []
                                    new_ev = data["evidence"] if isinstance(data["evidence"], list) else [data["evidence"]]
                                    c["evidence"] = existing + new_ev
                                target_repo_path = c.get("repo_path")
                                c["updated"] = _now()
                                updated = True
                                break
                        if not updated:
                            entry = {k: v for k, v in data.items() if k in ("task_id", "state", "summary", "evidence", "repo_path")}
                            entry["updated"] = _now()
                            arr.append(entry)
                        contracts_path.parent.mkdir(parents=True, exist_ok=True)
                        contracts_path.write_text(_j.dumps(arr, ensure_ascii=False, indent=2), encoding="utf-8")

                        # Patch TASK_LIST.md conservatively: append or update state badge next to the first matching title line
                        try:
                            if target_repo_path and isinstance(target_repo_path, str):
                                tl = Path(target_repo_path) / "TASK_LIST.md"
                                if tl.exists() and "state" in data:
                                    lines = tl.read_text(encoding="utf-8").splitlines()
                                    new_lines = []
                                    found = False
                                    for line in lines:
                                        if not found and line.strip().startswith("- [") and data.get("summary") and data["summary"] in line:
                                            # rewrite with state badge
                                            found = True
                                            if "(state:" in line:
                                                # replace existing badge
                                                import re as _re
                                                newline = _re.sub(r"\(state:[^)]+\)", f"(state: {data['state']})", line)
                                            else:
                                                newline = f"{line} (state: {data['state']})"
                                            new_lines.append(newline)
                                        else:
                                            new_lines.append(line)
                                    if found:
                                        tl.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
                        except Exception:
                            pass
        except Exception:
            pass

        # Devlog to Discord (optional): summarize meaningful events
        try:
            if devlog_webhook:
                msg_type = str(data.get("type", "")).lower()
                task_id = data.get("task_id") or ""
                repo_path = data.get("repo_path") or ""
                summary = data.get("summary") or data.get("message") or ""
                state = data.get("state") or st.get("state") or ""
                title = f"{agent} {msg_type.upper()} {task_id}".strip()
                desc_parts = []
                if state:
                    desc_parts.append(f"state: {state}")
                if summary:
                    desc_parts.append(f"summary: {summary}")
                if repo_path:
                    desc_parts.append(f"repo: {repo_path}")
                if "evidence" in data:
                    ev = data["evidence"]
                    if isinstance(ev, list):
                        desc_parts.append("evidence: " + "; ".join(map(str, ev))[:900])
                description = " | ".join(desc_parts) or json.dumps(data)[:1000]
                _post_discord(title, description)
        except Exception:
            pass

        # Attempt to route through CommandRouter if it supports this type
        try:
            router.route(data)
        except Exception:
            pass

    listener.on_message(on_message)
    listener.start()
    print(f"Listening for {agent} inbox at: {inbox_dir}")

    try:
        while True:
            item = pipeline.process_once()
            if item is not None:
                to_agent, message = item
                print(f"[PIPELINE] enqueue -> to={to_agent} msg={message}")
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        print("Stopped inbox listener")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())







