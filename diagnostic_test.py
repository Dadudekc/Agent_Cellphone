#!/usr/bin/env python3
"""
Diagnostic Test for Broadcast Issues
Tests broadcast functionality with proper delays
"""

import time
from agent_cell_phone import AgentCellPhone, MsgTag

def test_broadcast_with_delays():
    """Test broadcast with proper delays between messages."""
    
    print("🔍 Diagnostic Test: Broadcast with Delays")
    print("=" * 50)
    
    try:
        acp = AgentCellPhone(layout_mode="8-agent")
        print(f"✅ Loaded 8-agent layout")
        print(f"📋 Agents: {acp.get_available_agents()}")
        print()
        
        # Test 1: Individual messages with delays
        print("📤 Test 1: Individual messages (should work)")
        print("-" * 40)
        
        for i, agent in enumerate(acp.get_available_agents()[:3]):  # Test first 3 agents
            message = f"Individual test {i+1}: Clean message"
            print(f"📤 Sending to {agent}: {message}")
            acp.send(agent, message, MsgTag.VERIFY)
            time.sleep(1.0)  # 1 second delay
        
        print()
        
        # Test 2: Manual broadcast with delays
        print("📢 Test 2: Manual broadcast with delays")
        print("-" * 40)
        
        broadcast_msg = "MANUAL BROADCAST: Testing with delays"
        print(f"📢 Broadcasting: {broadcast_msg}")
        
        for agent in acp.get_available_agents():
            print(f"📤 Sending to {agent}")
            acp.send(agent, broadcast_msg, MsgTag.CAPTAIN)
            time.sleep(0.5)  # 0.5 second delay between each
        
        print()
        
        # Test 3: Quick broadcast (original method)
        print("⚡ Test 3: Quick broadcast (may have issues)")
        print("-" * 40)
        
        quick_msg = "QUICK BROADCAST: No delays"
        print(f"⚡ Broadcasting: {quick_msg}")
        
        acp.broadcast(quick_msg, MsgTag.TASK)
        
        print()
        print("✅ Diagnostic test completed!")
        print("📝 Check if Test 1 and 2 work cleanly, Test 3 may show corruption")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_broadcast_with_delays() 