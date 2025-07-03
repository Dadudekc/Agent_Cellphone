#!/usr/bin/env python3
"""
Coordinate Finder Utility
Helps users find screen coordinates for cursor agent input boxes
1. Supports multiple layout modes (2-agent, 4-agent, 8-agent)
2. Saves coordinates to runtime/config/cursor_agent_coords.json
3. Allows updating and deleting specific agent coordinates
4. Provides a continuous mouse position tracker
5. Supports interactive mode selection
"""

import pyautogui
import time
import json
from pathlib import Path


def find_coordinates():
    """Interactive coordinate finder for cursor agents with mode selection"""
    print("🎯 Cursor Agent Coordinate Finder")
    print("=" * 40)
    print("This utility helps you find screen coordinates for your cursor agent input boxes.")
    print("IMPORTANT: We need TWO coordinates per agent:")
    print("1. Starter Location Box - A consistent location that doesn't change")
    print("2. Input Box - The actual input field (may change after sending messages)")
    print("Move your mouse to each location and press Ctrl+C to capture.")
    print("Press Ctrl+C to exit.\n")
    
    # Select mode
    print("Select layout mode:")
    print("1. 2-agent mode")
    print("2. 4-agent mode") 
    print("3. 8-agent mode")
    
    while True:
        try:
            mode_choice = input("Enter mode (1-3): ").strip()
            if mode_choice in ['1', '2', '3']:
                break
            print("Please enter 1, 2, or 3")
        except KeyboardInterrupt:
            print("\nCoordinate capture cancelled.")
            return
    
    mode_map = {'1': '2-agent', '2': '4-agent', '3': '8-agent'}
    mode_name = mode_map[mode_choice]
    agent_count_map = {'1': 2, '2': 4, '3': 8}
    agent_count = agent_count_map[mode_choice]
    
    print(f"\n📐 Setting up {mode_name} layout ({agent_count} agents)")
    print("=" * 40)
    
    coordinates = {}
    
    try:
        for agent_num in range(1, agent_count + 1):
            agent_id = f"Agent-{agent_num}"
            
            print(f"\n🎯 Setting up coordinates for {agent_id}")
            print("-" * 30)
            
            # Capture starter location box
            print(f"1. Position mouse over {agent_id} STARTER LOCATION BOX...")
            print("   (This should be a consistent location that doesn't change)")
            print("   Press Ctrl+C to capture coordinates...")
            
            # Wait for user to position mouse
            time.sleep(3)
            
            # Get current mouse position for starter location
            x, y = pyautogui.position()
            starter_coords = {"x": x, "y": y}
            
            print(f"   ✅ Captured starter location: ({x}, {y})")
            
            # Capture input box
            print(f"2. Position mouse over {agent_id} INPUT BOX...")
            print("   (This is where you type messages)")
            print("   Press Ctrl+C to capture coordinates...")
            
            # Wait for user to position mouse
            time.sleep(3)
            
            # Get current mouse position for input box
            x, y = pyautogui.position()
            input_coords = {"x": x, "y": y}
            
            print(f"   ✅ Captured input box: ({x}, {y})")
            
            # Store both coordinates
            coordinates[agent_id] = {
                "starter_location_box": starter_coords,
                "input_box": input_coords
            }
            
            print(f"✅ Completed {agent_id} setup")
            
            # Ask if user wants to continue (except for last agent)
            if agent_num < agent_count:
                print("\nContinue to next agent?")
                print("1. Yes")
                print("2. No")
                while True:
                    response = input("Enter choice (1-2): ").strip()
                    if response in ['1', '2']:
                        break
                    print("Please enter 1 or 2")
                if response == '2':
                    break
                
    except KeyboardInterrupt:
        print("\n\nCoordinate capture completed!")
    
    if coordinates:
        print(f"\n📊 Captured coordinates for {len(coordinates)} agents in {mode_name} mode:")
        for agent_id, coord_data in coordinates.items():
            starter_x, starter_y = coord_data["starter_location_box"]["x"], coord_data["starter_location_box"]["y"]
            input_x, input_y = coord_data["input_box"]["x"], coord_data["input_box"]["y"]
            print(f"  {agent_id}:")
            print(f"    Starter: ({starter_x}, {starter_y})")
            print(f"    Input:   ({input_x}, {input_y})")
        
        # Save to file
        save_coordinates(coordinates, mode_name)
    else:
        print("No coordinates captured.")


def save_coordinates(coordinates, mode_name):
    """Save coordinates to cursor agent coordinates file with mode support"""
    try:
        # Create runtime/config directory structure
        config_dir = Path("runtime/config")
        config_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = config_dir / "cursor_agent_coords.json"
        
        # Load existing coordinates if file exists
        all_coordinates = {}
        if filepath.exists():
            with open(filepath, 'r') as f:
                all_coordinates = json.load(f)
        
        # Add or update the mode coordinates
        all_coordinates[mode_name] = coordinates
        
        with open(filepath, 'w') as f:
            json.dump(all_coordinates, f, indent=2)
            
        print(f"\n💾 Saved {mode_name} coordinates to {filepath}")
        print("✅ Coordinates are now ready for use with agent_cell_phone.py")
        
    except Exception as e:
        print(f"❌ Error saving coordinates: {e}")


def load_existing_coordinates():
    """Load and display existing coordinates for all modes"""
    try:
        config_file = Path("runtime/config/cursor_agent_coords.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                all_coordinates = json.load(f)
            
            print("📋 Current cursor agent coordinates:")
            print("=" * 40)
            
            for mode_name, coordinates in all_coordinates.items():
                print(f"\n{mode_name.upper()} MODE:")
                for agent_id, coord_data in coordinates.items():
                    starter_x, starter_y = coord_data["starter_location_box"]["x"], coord_data["starter_location_box"]["y"]
                    input_x, input_y = coord_data["input_box"]["x"], coord_data["input_box"]["y"]
                    print(f"  {agent_id}:")
                    print(f"    Starter: ({starter_x}, {starter_y})")
                    print(f"    Input:   ({input_x}, {input_y})")
            return all_coordinates
        else:
            print("❌ No existing coordinates found.")
            return None
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return None


def update_coordinate():
    """Update a specific agent's coordinates in a specific mode"""
    all_coordinates = load_existing_coordinates()
    if not all_coordinates:
        print("No existing coordinates to update. Run find mode first.")
        return
    
    print("\n🔄 Update specific agent coordinates")
    print("=" * 40)
    
    # Show available modes with numbers
    print("Available modes:")
    mode_list = list(all_coordinates.keys())
    for i, mode_name in enumerate(mode_list, 1):
        print(f"{i}. {mode_name}")
    
    while True:
        try:
            mode_choice = input(f"Enter mode number (1-{len(mode_list)}): ").strip()
            if mode_choice.isdigit() and 1 <= int(mode_choice) <= len(mode_list):
                mode_name = mode_list[int(mode_choice) - 1]
                break
            print(f"Please enter a number between 1 and {len(mode_list)}")
        except KeyboardInterrupt:
            print("\nUpdate cancelled.")
            return
    
    coordinates = all_coordinates[mode_name]
    
    # Show available agents for this mode with numbers
    print(f"\nAvailable agents in {mode_name} mode:")
    agent_list = list(coordinates.keys())
    for i, agent_id in enumerate(agent_list, 1):
        print(f"{i}. {agent_id}")
    
    while True:
        try:
            agent_choice = input(f"Enter agent number (1-{len(agent_list)}): ").strip()
            if agent_choice.isdigit() and 1 <= int(agent_choice) <= len(agent_list):
                agent_id = agent_list[int(agent_choice) - 1]
                break
            print(f"Please enter a number between 1 and {len(agent_list)}")
        except KeyboardInterrupt:
            print("\nUpdate cancelled.")
            return
    
    print(f"\nPosition mouse over {agent_id} input box in {mode_name} mode...")
    print("Press Ctrl+C to capture new coordinates...")
    
    try:
        time.sleep(3)
        x, y = pyautogui.position()
        coordinates[agent_id] = {"input_box": {"x": x, "y": y}}
        
        print(f"✅ Updated {agent_id} in {mode_name} mode: ({x}, {y})")
        save_coordinates(coordinates, mode_name)
        
    except KeyboardInterrupt:
        print("\nCoordinate update cancelled.")


def delete_mode():
    """Delete a specific mode's coordinates"""
    all_coordinates = load_existing_coordinates()
    if not all_coordinates:
        print("No existing coordinates to delete.")
        return
    
    print("\n🗑️ Delete mode coordinates")
    print("=" * 40)
    
    # Show available modes with numbers
    print("Available modes:")
    mode_list = list(all_coordinates.keys())
    for i, mode_name in enumerate(mode_list, 1):
        print(f"{i}. {mode_name}")
    
    while True:
        try:
            mode_choice = input(f"Enter mode number to delete (1-{len(mode_list)}): ").strip()
            if mode_choice.isdigit() and 1 <= int(mode_choice) <= len(mode_list):
                mode_name = mode_list[int(mode_choice) - 1]
                break
            print(f"Please enter a number between 1 and {len(mode_list)}")
        except KeyboardInterrupt:
            print("\nDeletion cancelled.")
            return
    
    print(f"Are you sure you want to delete {mode_name} mode?")
    print("1. Yes")
    print("2. No")
    while True:
        try:
            confirm = input("Enter choice (1-2): ").strip()
            if confirm in ['1', '2']:
                break
            print("Please enter 1 or 2")
        except KeyboardInterrupt:
            print("\nDeletion cancelled.")
            return
    
    if confirm == '2':
        print("Deletion cancelled.")
        return
    
    try:
        # Remove the mode
        del all_coordinates[mode_name]
        
        # Save updated coordinates
        config_file = Path("runtime/config/cursor_agent_coords.json")
        with open(config_file, 'w') as f:
            json.dump(all_coordinates, f, indent=2)
        
        print(f"✅ Deleted {mode_name} mode coordinates.")
        
    except Exception as e:
        print(f"❌ Error deleting mode: {e}")


def show_current_position():
    """Show current mouse position continuously"""
    print("🖱️ Current mouse position (Ctrl+C to exit):")
    print("=" * 40)
    
    try:
        while True:
            x, y = pyautogui.position()
            print(f"\rMouse position: ({x}, {y})", end="", flush=True)
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nPosition tracking stopped.")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Cursor Agent Coordinate Finder")
    parser.add_argument("--mode", choices=["find", "track", "show", "update", "delete"], default="find",
                       help="Mode: find (interactive), track (continuous), show (display current), update (modify existing), delete (remove mode)")
    
    args = parser.parse_args()
    
    if args.mode == "find":
        find_coordinates()
    elif args.mode == "track":
        show_current_position()
    elif args.mode == "show":
        load_existing_coordinates()
    elif args.mode == "update":
        update_coordinate()
    elif args.mode == "delete":
        delete_mode()


if __name__ == "__main__":
    main() 