#!/usr/bin/env python3
"""
Send a single specific onboarding message to all agents
"""

from agent_cell_phone import AgentCellPhone, MsgTag
import time

def send_single_onboarding():
    """Send the specific onboarding message to all agents"""
    print("📱 Sending single onboarding message via broadcast")
    print("=" * 50)
    
    # Create agent cell phone instance
    acp = AgentCellPhone(layout_mode="8-agent")
    
    # The specific onboarding message from user
    message = "onboarding system_overview_1 You are part of the Agent Cell Phone system - Inter-agent communication and collaboration platform."
    
    print(f"📋 Message: {message}")
    print(f"🎯 Broadcasting to all agents...")
    
    # Broadcast to all agents
    acp.broadcast(message, MsgTag.ONBOARDING)
    
    print("\n✅ ONBOARDING MESSAGE SENT!")
    print("📱 Method: Agent Cell Phone Broadcast")
    print("🎯 Target: All agents in 8-agent layout")

if __name__ == "__main__":
    send_single_onboarding() 