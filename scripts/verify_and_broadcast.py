#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from agent_cell_phone import AgentCellPhone, MsgTag  # type: ignore


def main() -> int:
    acp = AgentCellPhone(layout_mode="8-agent", test=True)

    verify_msg = "Coordinate test 4: Long message with spaces and punctuation!"
    task_msg = "QUICK BROADCAST: No delays"

    # Send VERIFY message to all agents (broadcast)
    acp.broadcast(verify_msg, MsgTag.VERIFY)

    # Send TASK quick broadcast to all agents
    acp.broadcast(task_msg, MsgTag.TASK)

    # Collect minimal evidence
    evidence = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "layout": acp.get_layout_mode(),
        "agents": acp.get_available_agents(),
        "messages": [
            {"tag": MsgTag.VERIFY.value, "content": verify_msg},
            {"tag": MsgTag.TASK.value, "content": task_msg},
        ],
    }

    # Write evidence into Agent-3 inbox
    inbox_dir = Path("agent_workspaces") / "Agent-3" / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)
    out_path = inbox_dir / f"sync_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_verify_broadcast.json"
    out_path.write_text(json.dumps({
        "type": "sync",
        "from": "Agent-3",
        "to": "Agent-3",
        "topic": "VERIFY test 4 + TASK quick broadcast",
        "summary": "Performed headless sends for verify-4 and quick task broadcast.",
        "details": evidence,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Evidence written to: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())



