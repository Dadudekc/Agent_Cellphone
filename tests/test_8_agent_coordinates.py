#!/usr/bin/env python3
"""
8-Agent Coordinate Test Script
Tests all 8 agent coordinates by sending individual and broadcast messages
"""

import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from services.agent_cell_phone import AgentCellPhone, MsgTag

def test_8_agent_coordinates():
    """Test all 8 agent coordinates with individual and broadcast messages."""
    
    print("🧪 Testing 8-Agent Coordinate System")
    print("=" * 50)
    
    # Initialize AgentCellPhone with 8-agent layout
    try:
        acp = AgentCellPhone(layout_mode="8-agent")
        print(f"✅ Successfully loaded 8-agent layout")
        print(f"📋 Available agents: {acp.get_available_agents()}")
        print()
    except Exception as e:
        print(f"❌ Failed to initialize 8-agent layout: {e}")
        return False
    
    # Test individual messages to each agent
    print("📤 Testing Individual Messages:")
    print("-" * 30)
    
    test_messages = [
        "Coordinate test 1: Basic functionality check",
        "Coordinate test 2: Special characters @#$%^&*()",
        "Coordinate test 3: Numbers 1234567890",
        "Coordinate test 4: Long message with spaces and punctuation!",
        "Coordinate test 5: Unicode test: 🚀📱💻",
        "Coordinate test 6: Agent communication protocol test",
        "Coordinate test 7: System integration verification",
        "Coordinate test 8: Final coordinate validation"
    ]
    
    agents = acp.get_available_agents()
    success_count = 0
    
    for i, agent in enumerate(agents):
        try:
            message = test_messages[i] if i < len(test_messages) else f"Test message for {agent}"
            print(f"📤 Sending to {agent}: {message[:50]}...")
            
            acp.send(agent, message, MsgTag.VERIFY)
            success_count += 1
            
            # Small delay between messages
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ Failed to send to {agent}: {e}")
    
    print(f"\n✅ Individual messages: {success_count}/{len(agents)} successful")
    print()
    
    # Test broadcast message
    print("📢 Testing Broadcast Message:")
    print("-" * 30)
    
    try:
        broadcast_msg = "🎯 BROADCAST TEST: All 8 agents should receive this message simultaneously!"
        print(f"📢 Broadcasting: {broadcast_msg}")
        
        acp.broadcast(broadcast_msg, MsgTag.CAPTAIN)
        print("✅ Broadcast message sent successfully")
        
    except Exception as e:
        print(f"❌ Broadcast failed: {e}")
    
    print()
    
    # Test with different message tags
    print("🏷️ Testing Different Message Tags:")
    print("-" * 30)
    
    tag_tests = [
        (MsgTag.RESUME, "Resume operation test"),
        (MsgTag.SYNC, "Sync status test"),
        (MsgTag.VERIFY, "Verify coordinates test"),
        (MsgTag.TASK, "Task assignment test")
    ]
    
    for tag, message in tag_tests:
        try:
            print(f"🏷️ Testing {tag.value} tag: {message}")
            acp.send("Agent-1", message, tag)
            time.sleep(0.3)
        except Exception as e:
            print(f"❌ Tag test failed for {tag.value}: {e}")
    
    print()
    
    # Summary
    print("📊 Test Summary:")
    print("=" * 50)
    print(f"✅ 8-Agent layout loaded successfully")
    print(f"✅ Individual messages: {success_count}/{len(agents)} agents tested")
    print(f"✅ Broadcast functionality tested")
    print(f"✅ Message tags tested")
    print()
    print("🎯 If you see messages appearing in all 8 Cursor instances,")
    print("   the coordinate system is working correctly!")
    print()
    print("📝 Check the devlog files in agent-*/ directories for message logs")
    
    return success_count == len(agents)

def test_coordinate_validation():
    """Additional validation of coordinate data."""
    print("\n🔍 Coordinate Validation:")
    print("-" * 30)
    
    try:
        acp = AgentCellPhone(layout_mode="8-agent")
        
        # Check coordinate ranges
        for agent, coords in acp._coords.items():
            x, y = coords["input_box"]["x"], coords["input_box"]["y"]
            print(f"📍 {agent}: ({x}, {y})")
            
            # Basic sanity checks
            if abs(x) > 3000 or abs(y) > 2000:
                print(f"⚠️  Warning: {agent} has unusual coordinates")
        
        print("✅ Coordinate validation complete")
        
    except Exception as e:
        print(f"❌ Coordinate validation failed: {e}")

if __name__ == "__main__":
    print("🚀 Starting 8-Agent Coordinate Test Suite")
    print("=" * 60)
    print()
    
    # Run main test
    success = test_8_agent_coordinates()
    
    # Run coordinate validation
    test_coordinate_validation()
    
    print()
    print("🏁 Test suite completed!")
    if success:
        print("🎉 All tests passed - coordinate system is ready!")
    else:
        print("⚠️  Some tests failed - check coordinate configuration")
