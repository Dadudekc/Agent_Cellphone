#!/usr/bin/env python3
"""
Test Starter Location Box Functionality
=======================================
Demonstrates how the new starter_location_box solves the input box position change issue.
"""

import sys
import os
import time

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from utils.coordinate_finder import CoordinateFinder
except ImportError as e:
    print(f"Import error: {e}")
    print("Please run from the project root directory")
    sys.exit(1)

def test_starter_location_system():
    """Test the new starter location box system."""
    print("🧪 Testing Starter Location Box System")
    print("=" * 50)
    
    # Initialize coordinate finder
    finder = CoordinateFinder()
    
    # Test for 4-agent mode
    print("\n📋 Testing 4-Agent Mode Coordinates:")
    print("-" * 40)
    
    for agent_id in ["agent-1", "agent-2", "agent-3", "agent-4"]:
        print(f"\n🎯 {agent_id.upper()}:")
        
        # Get starter location (consistent position)
        starter_coords = finder.get_starter_location(agent_id)
        if starter_coords:
            x, y = starter_coords
            print(f"  Starter Location: ({x}, {y}) - Consistent position")
        else:
            print(f"  Starter Location: Not found")
        
        # Get input box location (may change after messages)
        input_coords = finder.get_input_box_location(agent_id)
        if input_coords:
            x, y = input_coords
            print(f"  Input Box:        ({x}, {y}) - May change after messages")
        else:
            print(f"  Input Box:        Not found")
    
    print("\n" + "=" * 50)
    print("💡 HOW THIS SOLVES THE PROBLEM:")
    print("=" * 50)
    print("1. BEFORE: Only had input_box coordinates")
    print("   - Input box position changes after sending first message")
    print("   - Subsequent clicks miss the target")
    print("   - System becomes unreliable")
    print()
    print("2. AFTER: Added starter_location_box coordinates")
    print("   - Starter location remains consistent")
    print("   - Click starter location first to activate agent")
    print("   - Then click input box to type message")
    print("   - System remains reliable across multiple messages")
    print()
    print("3. WORKFLOW:")
    print("   Step 1: Click starter_location_box to activate agent")
    print("   Step 2: Click input_box to type message")
    print("   Step 3: Send message")
    print("   Step 4: Repeat from Step 1 for next message")
    print()
    print("✅ This ensures consistent agent interaction!")

def simulate_agent_interaction():
    """Simulate how agent interaction would work with the new system."""
    print("\n🔄 SIMULATED AGENT INTERACTION WORKFLOW")
    print("=" * 50)
    
    finder = CoordinateFinder()
    agent_id = "agent-1"
    
    print(f"Simulating interaction with {agent_id}...")
    
    # Step 1: Get starter location
    starter_coords = finder.get_starter_location(agent_id)
    if not starter_coords:
        print(f"❌ No starter location found for {agent_id}")
        return
    
    x, y = starter_coords
    print(f"Step 1: Click starter location at ({x}, {y})")
    print("        → This activates the agent window")
    
    # Step 2: Get input box location
    input_coords = finder.get_input_box_location(agent_id)
    if not input_coords:
        print(f"❌ No input box location found for {agent_id}")
        return
    
    x, y = input_coords
    print(f"Step 2: Click input box at ({x}, {y})")
    print("        → This positions cursor for typing")
    
    # Step 3: Type and send message
    message = "Hello from starter location system!"
    print(f"Step 3: Type message: '{message}'")
    print("        → Press Enter to send")
    
    print("\n✅ Message sent successfully!")
    print("🔄 For next message, repeat Steps 1-3")
    print("   (Starter location remains consistent)")

if __name__ == "__main__":
    test_starter_location_system()
    simulate_agent_interaction() 