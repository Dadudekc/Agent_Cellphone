#!/usr/bin/env python3
"""Capture Cursor input box coordinates for a given agent/layout.

Writes to src/runtime/config/cursor_agent_coords.json with structure:
{
  "4-agent": {
    "Agent-1": {"input_box": {"x": ..., "y": ...}, "starter_location_box": {...}}
  }
}

Usage (run from D:\\Agent_Cellphone):
  # Countdown timer mode (original)
  python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --delay 6
  
  # Enter key timing mode (recommended)
  python overnight_runner/tools/capture_coords.py --layout 5-agent --agent Agent-5 --enter-timing
  
  # Batch capture for all agents
  python overnight_runner/tools/capture_coords.py --layout 5-agent --all-agents --enter-timing
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
    parser.add_argument("--agent", help="Agent ID, e.g., Agent-1")
    parser.add_argument("--all-agents", action="store_true", help="Capture coordinates for all agents in the layout")
    parser.add_argument("--delay", type=float, default=6.0, help="Seconds to hover before capture (countdown mode)")
    parser.add_argument("--enter-timing", action="store_true", help="Use Enter key timing instead of countdown")
    parser.add_argument(
        "--field",
        choices=["input", "starter", "both"],
        default="both",
        help="Which location to update: input, starter, or both (default: both)",
    )
    return parser.parse_args(argv)


def get_agent_descriptions(layout: str) -> dict[str, str]:
    """Get descriptions for agents in a specific layout"""
    descriptions = {
        "2-agent": {
            "Agent-1": "Left side - input and output on left",
            "Agent-2": "Right side - input and output on right"
        },
        "4-agent": {
            "Agent-1": "Top-left quadrant - input at bottom, output at top",
            "Agent-2": "Top-right quadrant - input at bottom, output at top",
            "Agent-3": "Bottom-left quadrant - input at bottom, output at top",
            "Agent-4": "Bottom-right quadrant - input at bottom, output at top"
        },
        "5-agent": {
            "Agent-1": "Top-left quadrant - input at bottom, output at top",
            "Agent-2": "Top-right quadrant - input at bottom, output at top",
            "Agent-3": "Bottom-left quadrant - input at bottom, output at top",
            "Agent-4": "Bottom-right quadrant - input at bottom, output at top",
            "Agent-5": "Center area - input and output in middle"
        },
        "8-agent": {
            "Agent-1": "Top row, left - input and output at top",
            "Agent-2": "Top row, center-left - input and output at top",
            "Agent-3": "Top row, center-right - input and output at top",
            "Agent-4": "Top row, right - input and output at top",
            "Agent-5": "Bottom row, left - input and output at bottom",
            "Agent-6": "Bottom row, center-left - input and output at bottom",
            "Agent-7": "Bottom row, center-right - input and output at bottom",
            "Agent-8": "Bottom row, right - input and output at bottom"
        }
    }
    return descriptions.get(layout, {})


def capture_coordinates_enter_timing(agent: str, description: str, field: str) -> dict[str, dict[str, int]]:
    """Capture coordinates using Enter key timing (more user-friendly)"""
    print(f"\n🎯 Capturing {agent}")
    print(f"   Description: {description}")
    print("   Instructions:")
    
    coords = {}
    
    # Capture input box coordinates
    if field in ("input", "both"):
        print("   1. Move your mouse to the agent's input box location (where messages are typed)")
        print("   2. Press Enter when ready")
        input("   Press Enter when mouse is at input box location... ")
        import pyautogui
        input_x, input_y = pyautogui.position()
        coords["input_box"] = {"x": int(input_x), "y": int(input_y)}
        print(f"   ✅ Input box: ({input_x}, {input_y})")
    
    # Capture starter location coordinates
    if field in ("starter", "both"):
        print("   3. Move your mouse to the agent's starter location (where Ctrl+T opens new chats)")
        print("   4. Press Enter when ready")
        input("   Press Enter when mouse is at starter location... ")
        starter_x, starter_y = pyautogui.position()
        coords["starter_location_box"] = {"x": int(starter_x), "y": int(starter_y)}
        print(f"   ✅ Starter location: ({starter_x}, {starter_y})")
    
    return coords


def capture_coordinates_countdown(agent: str, delay: float, field: str) -> dict[str, dict[str, int]]:
    """Capture coordinates using countdown timer (original method)"""
    print(f"Hover over {agent} input box... capturing in {delay:.1f}s")
    time.sleep(delay)
    import pyautogui
    x, y = pyautogui.position()
    
    coords = {}
    if field in ("input", "both"):
        coords["input_box"] = {"x": int(x), "y": int(y)}
    if field in ("starter", "both"):
        coords["starter_location_box"] = {"x": int(x), "y": int(y)}
    
    return coords


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    
    # Validate arguments
    if not args.agent and not args.all_agents:
        print("❌ Error: Must specify either --agent or --all-agents")
        return 1
    
    if args.agent and args.all_agents:
        print("❌ Error: Cannot specify both --agent and --all-agents")
        return 1
    
    try:
        import pyautogui  # type: ignore
    except Exception as exc:
        print(f"pyautogui is required: {exc}", file=sys.stderr)
        return 2

    config_path = Path(__file__).resolve().parents[2] / "src" / "runtime" / "config" / "cursor_agent_coords.json"
    
    # Get agent descriptions for the layout
    agent_descriptions = get_agent_descriptions(args.layout)
    if not agent_descriptions:
        print(f"❌ Error: Unknown layout '{args.layout}'")
        print(f"Available layouts: {', '.join(['2-agent', '4-agent', '5-agent', '8-agent'])}")
        return 1
    
    # Determine which agents to capture
    if args.all_agents:
        agents_to_capture = list(agent_descriptions.keys())
        print(f"📋 Capturing coordinates for all {len(agents_to_capture)} agents in {args.layout} layout")
    else:
        agents_to_capture = [args.agent]
        if args.agent not in agent_descriptions:
            print(f"❌ Error: Agent '{args.agent}' not found in {args.layout} layout")
            print(f"Available agents: {', '.join(agent_descriptions.keys())}")
            return 1
    
    print(f"🎯 Coordinate Capture Tool")
    print(f"📁 Layout: {args.layout}")
    print(f"💾 Output: {config_path}")
    print(f"⏱️  Mode: {'Enter key timing' if args.enter_timing else 'Countdown timer'}")
    print()
    
    # Load existing coordinates
    data = {}
    if config_path.exists():
        try:
            data = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception:
            data = {}
    
    layout = data.setdefault(args.layout, {})
    
    # Confirm before proceeding
    if args.enter_timing:
        print("⚠️  Make sure you have Cursor open with the correct agent layout before continuing!")
        print("   Position your mouse over each location when prompted.")
        print()
        try:
            input("Press Enter to begin coordinate capture... ")
        except KeyboardInterrupt:
            print("\n⚠️  Capture cancelled.")
            return 0
    
    # Capture coordinates for each agent
    for agent in agents_to_capture:
        if args.enter_timing:
            coords = capture_coordinates_enter_timing(agent, agent_descriptions[agent], args.field)
        else:
            coords = capture_coordinates_countdown(agent, args.delay, args.field)
        
        # Update the agent's coordinates
        agent_data = layout.setdefault(agent, {})
        for field_name, coord_data in coords.items():
            agent_data[field_name] = coord_data
        
        # Save after each agent (in case of interruption)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        
        # Show what was updated
        updated = []
        if args.field in ("input", "both") and "input_box" in coords:
            updated.append("input_box")
        if args.field in ("starter", "both") and "starter_location_box" in coords:
            updated.append("starter_location_box")
        
        fields_str = ", ".join(updated)
        if args.enter_timing:
            print(f"   ✅ {agent} coordinates captured and saved")
        else:
            print(f"Updated {config_path} for {agent} ({args.layout}): {fields_str} => ({coords.get('input_box', {}).get('x', 'N/A')}, {coords.get('input_box', {}).get('y', 'N/A')})")
    
    print(f"\n✅ Coordinate capture complete for {args.layout} layout!")
    print(f"   Captured {len(agents_to_capture)} agents")
    print(f"   File saved to: {config_path}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())












