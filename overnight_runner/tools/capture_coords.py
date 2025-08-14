#!/usr/bin/env python3
"""Capture Cursor input box coordinates for a given agent/layout.

Writes to src/runtime/config/cursor_agent_coords.json with structure:
{
  "4-agent": {
    "Agent-1": {"input_box": {"x": ..., "y": ...}, "starter_location_box": {...}}
  }
}
Usage (run from D:\\Agent_Cellphone):
  python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Capture input/starter coordinates for an agent")
    parser.add_argument("--layout", default="5-agent", help="Window layout (e.g., 5-agent, 4-agent, 8-agent)")
    parser.add_argument("--agent", required=True, help="Agent ID, e.g., Agent-1")
    parser.add_argument("--delay", type=float, default=6.0, help="Seconds to hover before capture")
    parser.add_argument(
        "--field",
        choices=["input", "starter", "both"],
        default="both",
        help="Which location to update: input, starter, or both (default: both)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        import pyautogui  # type: ignore
    except Exception as exc:
        print(f"pyautogui is required: {exc}", file=sys.stderr)
        return 2

    config_path = Path(__file__).resolve().parents[2] / "src" / "runtime" / "config" / "cursor_agent_coords.json"
    print(f"Hover over {args.agent} input box ({args.layout})... capturing in {args.delay:.1f}s")
    time.sleep(args.delay)
    x, y = pyautogui.position()  # type: ignore[attr-defined]

    data = {}
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}

    layout = data.setdefault(args.layout, {})
    agent = layout.setdefault(args.agent, {})
    # Update fields based on --field selection
    if args.field in ("input", "both"):
        agent["input_box"] = {"x": int(x), "y": int(y)}
    if args.field in ("starter", "both"):
        agent["starter_location_box"] = {"x": int(x), "y": int(y)}

    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    updated = []
    if args.field in ("input", "both"):
        updated.append("input_box")
    if args.field in ("starter", "both"):
        updated.append("starter_location_box")
    fields_str = ", ".join(updated)
    print(f"Updated {config_path} for {args.agent} ({args.layout}): {fields_str} => ({x}, {y})")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())












