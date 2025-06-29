#!/usr/bin/env python3
"""
Send specific onboarding messages to all agents via broadcast
"""

from agent_cell_phone import AgentCellPhone, MsgTag
import time

def send_specific_onboarding():
    """Send specific onboarding messages to all agents"""
    print("📱 Sending specific onboarding messages via broadcast")
    print("=" * 50)
    
    # Create agent cell phone instance
    acp = AgentCellPhone(layout_mode="8-agent")
    
    # Specific onboarding messages from user
    specific_messages = [
        "onboarding system_overview_1 You are part of the Agent Cell Phone system - Inter-agent communication and collaboration platform.",
        "onboarding system_overview_2 System architecture: Multi-agent system with PyAutoGUI-based messaging enabling real-time agent communication."
    ]
    
    # Send each message to all agents via broadcast
    for i, message in enumerate(specific_messages, 1):
        print(f"\n📋 Message {i}/{len(specific_messages)}")
        print(f"   {message}")
        print(f"   Broadcasting to all agents...")
        
        # Broadcast to all agents
        acp.broadcast(message, MsgTag.ONBOARDING)
        
        # Wait between messages
        time.sleep(2)
    
    print("\n✅ SPECIFIC ONBOARDING MESSAGES SENT!")
    print("📱 Method: Agent Cell Phone Broadcast")
    print("🎯 Target: All agents in 8-agent layout")

if __name__ == "__main__":
    send_specific_onboarding() 