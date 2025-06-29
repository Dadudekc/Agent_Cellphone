#!/usr/bin/env python3
"""
Send messages to agents using the agent cell phone system
"""

from agent_cell_phone import AgentCellPhone
import time

def send_coordination_messages():
    """Send coordination messages to agents 1, 3, and 4"""
    print("📱 Sending coordination messages using Agent Cell Phone")
    print("=" * 50)
    
    # Create agent cell phone instance
    acp = AgentCellPhone(layout_mode="8-agent")
    
    print("🎯 SENDING TO AGENT-1 (Resume System Architect)")
    print("-" * 40)
    acp.send("Agent-1", "COORDINATION TASK: You are assigned to build the agent resume system. Work with Agent-3 and Agent-4. Your role: Design the resume data structure and API endpoints.")
    time.sleep(2)
    
    print("\n🎯 SENDING TO AGENT-3 (GUI Developer)")
    print("-" * 40)
    acp.send("Agent-3", "COORDINATION TASK: You are assigned to build the GUI for the agent resume system. Work with Agent-1 and Agent-4. Your role: Create the user interface and frontend components.")
    time.sleep(2)
    
    print("\n🎯 SENDING TO AGENT-4 (Integration Specialist)")
    print("-" * 40)
    acp.send("Agent-4", "COORDINATION TASK: You are assigned to handle integration between resume system and GUI. Work with Agent-1 and Agent-3. Your role: Connect backend APIs with frontend components.")
    time.sleep(2)
    
    print("\n✅ COORDINATION MESSAGES SENT TO ALL AGENTS!")
    print("📱 Method: Agent Cell Phone System")
    print("🎯 Target: Real cursor positions on screen")
    print("🤝 Agents: Agent-1, Agent-3, Agent-4")

if __name__ == "__main__":
    send_coordination_messages() 