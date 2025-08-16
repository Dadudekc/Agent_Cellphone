#!/usr/bin/env python3
"""
Coordinate Calibration Tool
===========================
This tool helps you calibrate screen coordinates for all agent modes.
It will create a proper cursor_agent_coords.json file with accurate coordinates.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

def get_screen_info():
    """Get basic screen information"""
    try:
        import pyautogui
        screen_width, screen_height = pyautogui.size()
        print(f"📱 Screen detected: {screen_width}x{screen_height}")
        return screen_width, screen_height
    except ImportError:
        print("⚠️  pyautogui not available, using default coordinates")
        return 1920, 1080

def calibrate_agent_position(agent_name: str, description: str) -> Dict[str, Any]:
    """Calibrate coordinates for a single agent"""
    print(f"\n🎯 Calibrating {agent_name}")
    print(f"   Description: {description}")
    print("   Instructions:")
    print("   1. Move your mouse to the agent's input box location (where messages are typed)")
    print("   2. Press Enter when ready")
    print("   3. Move mouse to the agent's starter location (where Ctrl+T opens new chats)")
    print("   4. Press Enter when ready")
    
    try:
        input("Press Enter when mouse is at input box location...")
        import pyautogui
        input_x, input_y = pyautogui.position()
        print(f"   ✅ Input box: ({input_x}, {input_y})")
        
        input("Press Enter when mouse is at starter location...")
        starter_x, starter_y = pyautogui.position()
        print(f"   ✅ Starter location: ({starter_x}, {starter_y})")
        
        return {
            "input_box": {"x": input_x, "y": input_y},
            "starter_location_box": {"x": starter_x, "y": starter_y}
        }
        
    except Exception as e:
        print(f"   ❌ Calibration failed: {e}")
        return None

def calibrate_5_agent_mode() -> Dict[str, Any]:
    """Calibrate the 5-agent mode layout"""
    print("\n🚀 Calibrating 5-Agent Mode")
    print("=" * 50)
    
    # Define agent descriptions for 5-agent mode
    agents = {
        "Agent-1": "Top-left quadrant - input at bottom, output at top",
        "Agent-2": "Top-right quadrant - input at bottom, output at top", 
        "Agent-3": "Bottom-left quadrant - input at bottom, output at top",
        "Agent-4": "Bottom-right quadrant - input at bottom, output at top",
        "Agent-5": "Center area - input and output in middle"
    }
    
    layout = {}
    
    for agent, description in agents.items():
        coords = calibrate_agent_position(agent, description)
        if coords:
            layout[agent] = coords
        else:
            print(f"   ⚠️  Skipping {agent} due to calibration failure")
    
    return layout

def calibrate_4_agent_mode() -> Dict[str, Any]:
    """Calibrate the 4-agent mode layout"""
    print("\n🚀 Calibrating 4-Agent Mode")
    print("=" * 50)
    
    agents = {
        "Agent-1": "Top-left quadrant - input at bottom, output at top",
        "Agent-2": "Top-right quadrant - input at bottom, output at top",
        "Agent-3": "Bottom-left quadrant - input at bottom, output at top", 
        "Agent-4": "Bottom-right quadrant - input at bottom, output at top"
    }
    
    layout = {}
    
    for agent, description in agents.items():
        coords = calibrate_agent_position(agent, description)
        if coords:
            layout[agent] = coords
        else:
            print(f"   ⚠️  Skipping {agent} due to calibration failure")
    
    return layout

def calibrate_2_agent_mode() -> Dict[str, Any]:
    """Calibrate the 2-agent mode layout"""
    print("\n🚀 Calibrating 2-Agent Mode")
    print("=" * 50)
    
    agents = {
        "Agent-1": "Left side - input and output on left",
        "Agent-2": "Right side - input and output on right"
    }
    
    layout = {}
    
    for agent, description in agents.items():
        coords = calibrate_agent_position(agent, description)
        if coords:
            layout[agent] = coords
        else:
            print(f"   ⚠️  Skipping {agent} due to calibration failure")
    
    return layout

def calibrate_8_agent_mode() -> Dict[str, Any]:
    """Calibrate the 8-agent mode layout"""
    print("\n🚀 Calibrating 8-Agent Mode")
    print("=" * 50)
    
    agents = {
        "Agent-1": "Top row, left - input and output at top",
        "Agent-2": "Top row, center-left - input and output at top",
        "Agent-3": "Top row, center-right - input and output at top",
        "Agent-4": "Top row, right - input and output at top",
        "Agent-5": "Bottom row, left - input and output at bottom",
        "Agent-6": "Bottom row, center-left - input and output at bottom",
        "Agent-7": "Bottom row, center-right - input and output at bottom",
        "Agent-8": "Bottom row, right - input and output at bottom"
    }
    
    layout = {}
    
    for agent, description in agents.items():
        coords = calibrate_agent_position(agent, description)
        if coords:
            layout[agent] = coords
        else:
            print(f"   ⚠️  Skipping {agent} due to calibration failure")
    
    return layout

def save_coordinates(coordinates: Dict[str, Any], file_path: str):
    """Save coordinates to file with backup"""
    file_path = Path(file_path)
    
    # Create backup if file exists
    if file_path.exists():
        backup_path = file_path.with_suffix('.json.backup')
        print(f"📦 Creating backup: {backup_path}")
        file_path.rename(backup_path)
    
    # Save new coordinates
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(coordinates, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Coordinates saved to: {file_path}")

def main():
    print("🎯 Agent Coordinate Calibration Tool")
    print("=" * 50)
    print()
    print("This tool will help you calibrate screen coordinates for all agent modes.")
    print("With the new response capture system, we only need 2 coordinates per agent:")
    print("  - input_box: where messages are typed")
    print("  - starter_location_box: where Ctrl+T opens new chats")
    print("Make sure you have Cursor open and agent windows positioned before starting.")
    print()
    
    # Get screen info
    screen_width, screen_height = get_screen_info()
    
    # Ask which modes to calibrate
    print("Available modes to calibrate:")
    print("1. 5-agent mode (recommended for SWARM workflow)")
    print("2. 4-agent mode")
    print("3. 2-agent mode") 
    print("4. 8-agent mode")
    print("5. All modes")
    print()
    
    try:
        choice = input("Enter your choice (1-5): ").strip()
        
        coordinates = {}
        
        if choice == "1":
            coordinates["5-agent"] = calibrate_5_agent_mode()
        elif choice == "2":
            coordinates["4-agent"] = calibrate_4_agent_mode()
        elif choice == "3":
            coordinates["2-agent"] = calibrate_2_agent_mode()
        elif choice == "4":
            coordinates["8-agent"] = calibrate_8_agent_mode()
        elif choice == "5":
            coordinates["5-agent"] = calibrate_5_agent_mode()
            coordinates["4-agent"] = calibrate_4_agent_mode()
            coordinates["2-agent"] = calibrate_2_agent_mode()
            coordinates["8-agent"] = calibrate_8_agent_mode()
        else:
            print("❌ Invalid choice. Exiting.")
            return
        
        # Save coordinates
        if coordinates:
            save_coordinates(coordinates, "runtime/agent_comms/cursor_agent_coords.json")
            print("\n✅ Calibration complete!")
            print("You can now start the overnight runner with accurate coordinates.")
        else:
            print("\n❌ No coordinates were calibrated. Please try again.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Calibration interrupted. No changes were saved.")
    except Exception as e:
        print(f"\n❌ Calibration failed: {e}")

if __name__ == "__main__":
    main()
