#!/usr/bin/env python3
"""
Start an inbox listener for file-based agent messaging.

Usage:
  python scripts/start_inbox_listener.py --agent Agent-3
  python scripts/start_inbox_listener.py --agent Agent-3 --inbox agent_workspaces/Agent-3/inbox

Behavior:
  - Tails the inbox directory for new *.json files
  - Enqueues messages into MessagePipeline
  - Prints processed messages and routes known commands via CommandRouter
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Ensure src/ is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from core.inbox_listener import InboxListener  # type: ignore
from core.message_pipeline import MessagePipeline  # type: ignore
from core.command_router import CommandRouter  # type: ignore


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser("start_inbox_listener")
    p.add_argument("--agent", default="Agent-3", help="Agent id, e.g., Agent-3")
    p.add_argument(
        "--inbox",
        help="Inbox directory (defaults to agent_workspaces/<agent>/inbox)",
    )
    p.add_argument("--poll", type=float, default=0.2, help="Poll interval seconds")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    agent = args.agent
    inbox_dir = args.inbox or os.path.join("agent_workspaces", agent, "inbox")

    pipeline = MessagePipeline()
    router = CommandRouter()

    listener = InboxListener(inbox_dir=inbox_dir, poll_interval_s=args.poll, pipeline=pipeline)

    def on_msg(data):
        print(f"[INBOX] {agent} <- {json.dumps(data, ensure_ascii=False)}")

    listener.on_message(on_msg)
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



