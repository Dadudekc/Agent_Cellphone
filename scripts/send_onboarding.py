#!/usr/bin/env python3
"""
Send onboarding messages to agents using the agent cell phone system
"""

from agent_cell_phone import AgentCellPhone, MsgTag
import time

def send_onboarding_messages():
    """Send onboarding messages to agents"""
    print("📱 Sending onboarding messages using Agent Cell Phone")
    print("=" * 50)
    
    # Create agent cell phone instance
    acp = AgentCellPhone(layout_mode="8-agent")
    
    # Onboarding messages
    onboarding_messages = [
        "onboarding introduction_1 Welcome to the Agent Cell Phone system! You are an AI agent - an autonomous software entity designed to collaborate with other agents.",
        "onboarding introduction_2 As an agent, you have: 1) Unique identity and capabilities, 2) Communication protocols, 3) Task execution abilities, 4) Learning and adaptation skills.",
        "onboarding introduction_3 You are part of a multi-agent system where collaboration and coordination enable complex problem-solving beyond individual capabilities.",
        "onboarding introduction_4 Your role is to work autonomously while maintaining communication with other agents for coordinated operations.",
        "onboarding system_overview_1 You are part of the Agent Cell Phone system - Inter-agent communication and collaboration platform.",
        "onboarding system_overview_2 System architecture: Multi-agent system with PyAutoGUI-based messaging enabling real-time agent communication.",
        "onboarding system_overview_3 Key components: AgentCellPhone, InterAgentFramework, Message Protocol, Command Handlers working together seamlessly.",
        "onboarding system_overview_4 Your capabilities include: Individual messaging, Broadcast communication, Command execution, Status monitoring for effective collaboration.",
        "onboarding protocol_1 Communication Protocol: Use structured messages with sender, recipient, type, command, and args.",
        "onboarding protocol_2 Message Types: COMMAND, STATUS, DATA, QUERY, RESPONSE, BROADCAST, DIRECT, SYSTEM.",
        "onboarding protocol_3 Commands: ping, status, resume, sync, verify, task, captain, and custom commands.",
        "onboarding protocol_4 Broadcast vs Individual: Use broadcast for system-wide messages, individual for targeted communication."
    ]
    
    # Send onboarding messages to all agents
    for i, message in enumerate(onboarding_messages, 1):
        print(f"\n📋 Sending onboarding message {i}/{len(onboarding_messages)}")
        print("-" * 40)
        
        # Broadcast to all agents
        acp.broadcast(message, MsgTag.ONBOARDING)
        time.sleep(1)
    
    print("\n✅ ONBOARDING MESSAGES SENT TO ALL AGENTS!")
    print("📱 Method: Agent Cell Phone System")
    print("🎯 Target: All agents in 8-agent layout")
    print("📋 Total messages: 12 onboarding messages")

if __name__ == "__main__":
    send_onboarding_messages() 