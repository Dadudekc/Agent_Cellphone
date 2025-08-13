#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import sys
import runpy


def main() -> int:
    p = argparse.ArgumentParser("send_visible")
    p.add_argument("--layout", default="5-agent")
    p.add_argument("--tag", default="captain")
    p.add_argument("--msg", required=True)
    args = p.parse_args()
    os.environ.setdefault("ACP_DISABLE_FAILSAFE", "1")
    sys.argv = [
        "agent_cell_phone.py",
        "--layout", args.layout,
        "--msg", args.msg,
        "--tag", args.tag,
    ]
    runpy.run_path("src/agent_cell_phone.py", run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


