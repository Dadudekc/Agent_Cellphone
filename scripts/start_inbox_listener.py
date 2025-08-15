#!/usr/bin/env python3
"""
Start an inbox listener for file-based agent messaging.
Thin wrapper for overnight_runner.listener.main

Usage:
  python scripts/start_inbox_listener.py --agent Agent-3
  python scripts/start_inbox_listener.py --agent Agent-3 --inbox agent_workspaces/Agent-3/inbox

Behavior:
  - Tails the inbox directory for new *.json files
  - Enqueues messages into MessagePipeline
  - Prints processed messages and routes known commands via CommandRouter
"""

import sys
from pathlib import Path

# Ensure src/ is on path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

if __name__ == "__main__":
    from overnight_runner.listener import main
    raise SystemExit(main())



