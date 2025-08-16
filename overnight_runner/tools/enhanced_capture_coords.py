#!/usr/bin/env python3
"""Enhanced Coordinate Capture Tool for Cursor Agent Layouts

Combines the best of both worlds:
- Enter key timing (user-friendly) from calibrate_coords.py
- Command line flexibility from capture_coords.py
- Better error handling and backup functionality

Usage examples:
  # Interactive mode (recommended)
  python overnight_runner/tools/enhanced_capture_coords.py --layout 5-agent --agent Agent-1
  
  # Batch capture for all agents in a layout
  python overnight_runner/tools/enhanced_capture_coords.py --layout 5-agent --all-agents
  
  # Quick capture with specific fields
  python overnight_runner/tools/enhanced_capture_coords.py --layout 4-agent --agent Agent-2 --field input
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enhanced coordinate capture tool with Enter key timing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive capture for Agent-1 in 5-agent layout
  python enhanced_capture_coords.py --layout 5-agent --agent Agent-1
  
  # Capture all agents in 4-agent layout
  python enhanced_capture_coords.py --layout 4-agent --all-agents
  
  # Quick capture of just input box
  python enhanced_capture_coords.py --layout 2-agent --agent Agent-2 --field input
        """
    )
    parser.add_argument("--layout", default="5-agent", 
                       help="Window layout (e.g., 5-agent, 4-agent, 8-agent)")
    parser.add_argument("--agent", help="Specific agent ID, e.g., Agent-1")
    parser.add_argument("--all-agents", action="store_true",
                       help="Capture coordinates for all agents in the layout")
    parser.add_argument("--field", choices=["input", "starter", "both"],
                       default="both", help="Which location to update")
    parser.add_argument("--output", help="Output file path (default: auto-detect)")
    parser.add_argument("--backup", action="store_true", default=True,
                       help="Create backup of existing file (default: True)")
    parser.add_argument("--force", action="store_true",
                       help="Overwrite without confirmation")
    return parser.parse_args(argv)


def get_screen_info() -> tuple[int, int]:
    """Get basic screen information"""
    try:
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        print(f"📱 Screen detected: {screen_width}x{screen_height}")
        return screen_width, screen_height
    except ImportError:
        print("⚠️  pyautogui not available, using default coordinates")
        return 1920, 1080


def get_agent_descriptions(layout: str) -> Dict[str, str]:
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


def capture_agent_coordinates(agent: str, description: str, field: str) -> Optional[Dict[str, Any]]:
    """Capture coordinates for a single agent using Enter key timing"""
    print(f"\n🎯 Capturing {agent}")
    print(f"   Description: {description}")
    print("   Instructions:")
    
    coords = {}
    
    try:
        import pyautogui
        
        # Capture input box coordinates
        if field in ("input", "both"):
            print("   1. Move your mouse to the agent's input box location (where messages are typed)")
            print("   2. Press Enter when ready")
            input("   Press Enter when mouse is at input box location... ")
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
        
    except Exception as e:
        print(f"   ❌ Capture failed: {e}")
        return None


def load_existing_coordinates(file_path: Path) -> Dict[str, Any]:
    """Load existing coordinates from file"""
    if file_path.exists():
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Could not load existing coordinates: {e}")
    return {}


def create_backup(file_path: Path) -> Optional[Path]:
    """Create backup of existing file"""
    if file_path.exists():
        backup_path = file_path.with_suffix('.json.backup')
        try:
            file_path.rename(backup_path)
            print(f"📦 Created backup: {backup_path}")
            return backup_path
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
    return None


def save_coordinates(coordinates: Dict[str, Any], file_path: Path, backup: bool = True) -> bool:
    """Save coordinates to file with optional backup"""
    try:
        # Create backup if requested and file exists
        if backup and file_path.exists():
            create_backup(file_path)
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save coordinates
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(coordinates, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Coordinates saved to: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save coordinates: {e}")
        return False


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    
    # Validate arguments
    if not args.agent and not args.all_agents:
        print("❌ Error: Must specify either --agent or --all-agents")
        return 1
    
    if args.agent and args.all_agents:
        print("❌ Error: Cannot specify both --agent and --all-agents")
        return 1
    
    # Check for pyautogui
    try:
        import pyautogui
    except ImportError:
        print("❌ Error: pyautogui is required for coordinate capture")
        print("Install with: pip install pyautogui")
        return 2
    
    # Get screen info
    screen_width, screen_height = get_screen_info()
    
    # Get agent descriptions for the layout
    agent_descriptions = get_agent_descriptions(args.layout)
    if not agent_descriptions:
        print(f"❌ Error: Unknown layout '{args.layout}'")
        print(f"Available layouts: {', '.join(['2-agent', '4-agent', '5-agent', '8-agent'])}")
        return 1
    
    # Determine output file path
    if args.output:
        output_path = Path(args.output)
    else:
        # Auto-detect based on project structure
        output_path = Path(__file__).resolve().parents[2] / "runtime" / "agent_comms" / "cursor_agent_coords.json"
    
    print(f"🎯 Enhanced Coordinate Capture Tool")
    print(f"📁 Layout: {args.layout}")
    print(f"💾 Output: {output_path}")
    print(f"📱 Screen: {screen_width}x{screen_height}")
    print()
    
    # Load existing coordinates
    existing_coords = load_existing_coordinates(output_path)
    
    # Determine which agents to capture
    if args.all_agents:
        agents_to_capture = list(agent_descriptions.keys())
        print(f"📋 Capturing coordinates for all {len(agents_to_capture)} agents")
    else:
        agents_to_capture = [args.agent]
        if args.agent not in agent_descriptions:
            print(f"❌ Error: Agent '{args.agent}' not found in {args.layout} layout")
            print(f"Available agents: {', '.join(agent_descriptions.keys())}")
            return 1
        print(f"📋 Capturing coordinates for {args.agent}")
    
    print()
    print("⚠️  Make sure you have Cursor open with the correct agent layout before continuing!")
    print("   Position your mouse over each location when prompted.")
    print()
    
    # Confirm before proceeding
    if not args.force:
        try:
            input("Press Enter to begin coordinate capture... ")
        except KeyboardInterrupt:
            print("\n⚠️  Capture cancelled.")
            return 0
    
    # Capture coordinates for each agent
    layout_coords = existing_coords.get(args.layout, {})
    
    for agent in agents_to_capture:
        description = agent_descriptions[agent]
        coords = capture_agent_coordinates(agent, description, args.field)
        
        if coords:
            layout_coords[agent] = coords
            print(f"   ✅ {agent} coordinates captured successfully")
        else:
            print(f"   ⚠️  {agent} coordinates capture failed, skipping")
    
    # Update the main coordinates structure
    existing_coords[args.layout] = layout_coords
    
    # Save coordinates
    if save_coordinates(existing_coords, output_path, args.backup):
        print(f"\n✅ Coordinate capture complete for {args.layout} layout!")
        print(f"   Captured {len(layout_coords)} agents")
        print(f"   File saved to: {output_path}")
        return 0
    else:
        print(f"\n❌ Failed to save coordinates")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
