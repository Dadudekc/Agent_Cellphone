#!/usr/bin/env python3
"""
Basic diagnostic test to validate core imports and minimal flows without GUI.
Run via: python tests/diagnostic_test.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

def main() -> int:
    try:
        from agent_cell_phone import AgentCellPhone  # type: ignore
        from inter_agent_framework import InterAgentFramework  # type: ignore
    except Exception as e:
        print(f"[DIAG] import error: {e}")
        return 1

    try:
        acp = AgentCellPhone(agent_id="Agent-1", layout_mode="2-agent", test=True)
        print("[DIAG] AgentCellPhone init OK")
    except Exception as e:
        print(f"[DIAG] AgentCellPhone init error: {e}")
        return 1

    try:
        iaf = InterAgentFramework("Agent-1", layout_mode="2-agent", test=True)
        print("[DIAG] InterAgentFramework init OK")
    except Exception as e:
        print(f"[DIAG] InterAgentFramework init error: {e}")
        return 1

    print("[DIAG] OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


