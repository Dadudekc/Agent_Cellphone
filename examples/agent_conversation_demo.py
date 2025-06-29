#!/usr/bin/env python3
"""
Agent Conversation Demo
Shows agents 1, 3, and 4 communicating with each other
to build an agent resume system and GUI
"""

import time
import threading
from agent_cell_phone import AgentCellPhone, MsgTag

def agent_1_behavior(acp: AgentCellPhone):
    """Agent-1: Resume System Architect"""
    print(f"🤖 {acp.get_agent_id()} starting as Resume System Architect")
    
    # Start listening for messages
    acp.start_listening()
    
    # Initial coordination message
    acp.coordinate(["Agent-3", "Agent-4"], "COORDINATION TASK: Building agent resume system. Agent-3 handles GUI, Agent-4 handles integration.")
    time.sleep(2)
    
    # Send API specifications to GUI developer
    acp.send("Agent-3", "API endpoints designed: GET /resume/{id}, POST /resume, PUT /resume/{id}, DELETE /resume/{id}. Please integrate into GUI.")
    time.sleep(2)
    
    # Send requirements to integration specialist
    acp.send("Agent-4", "Need integration layer between API and GUI. Resume fields: name, skills, experience, education, contact.")
    time.sleep(2)
    
    # Wait for responses and continue conversation
    time.sleep(5)
    
    # Follow up based on responses
    acp.send("Agent-3", "Great! I've added validation endpoints. Test the API-GUI connection.")
    time.sleep(2)
    acp.send("Agent-4", "Perfect! Let's test the complete system integration.")
    
    # Keep listening for a while
    time.sleep(10)
    acp.stop_listening()

def agent_3_behavior(acp: AgentCellPhone):
    """Agent-3: GUI Developer"""
    print(f"🤖 {acp.get_agent_id()} starting as GUI Developer")
    
    # Start listening for messages
    acp.start_listening()
    
    # Wait for initial coordination
    time.sleep(3)
    
    # Respond to Agent-1's API specifications
    acp.reply("Agent-1", "I'll create the GUI components. What API endpoints do you need?")
    time.sleep(2)
    
    # Send GUI requirements
    acp.send("Agent-1", "I need these resume fields for the GUI: name, skills, experience, education, contact. Can you ensure the API supports all these fields?")
    time.sleep(2)
    
    # Coordinate with integration specialist
    acp.send("Agent-4", "GUI components created: ResumeForm, ResumeList, ResumeView. Ready for API binding.")
    time.sleep(2)
    
    # Wait for responses
    time.sleep(5)
    
    # Status update
    acp.send("Agent-1", "GUI integration complete. All components connected to API endpoints.")
    acp.send("Agent-4", "GUI ready for testing. Data binding working correctly.")
    
    # Keep listening
    time.sleep(10)
    acp.stop_listening()

def agent_4_behavior(acp: AgentCellPhone):
    """Agent-4: Integration Specialist"""
    print(f"🤖 {acp.get_agent_id()} starting as Integration Specialist")
    
    # Start listening for messages
    acp.start_listening()
    
    # Wait for initial coordination
    time.sleep(3)
    
    # Respond to Agent-1's requirements
    acp.reply("Agent-1", "I'll handle the integration layer. Ready to connect API and GUI.")
    time.sleep(2)
    
    # Send integration plan
    acp.send("Agent-1", "I'll create the integration layer. Agent-1, please add validation endpoints. Agent-3, I'll provide the data binding utilities.")
    acp.send("Agent-3", "I'll create the integration layer. Agent-1, please add validation endpoints. Agent-3, I'll provide the data binding utilities.")
    time.sleep(2)
    
    # Wait for responses
    time.sleep(5)
    
    # Status update
    acp.send("Agent-1", "Integration layer complete. Data binding utilities ready. Testing connection between API and GUI.")
    acp.send("Agent-3", "Integration layer complete. Data binding utilities ready. Testing connection between API and GUI.")
    time.sleep(2)
    
    # Final coordination
    acp.coordinate(["Agent-1", "Agent-3"], "Integration testing complete. All systems connected and working.")
    
    # Keep listening
    time.sleep(10)
    acp.stop_listening()

def main():
    """Main demo function"""
    print("🤝 AGENT CONVERSATION DEMO")
    print("=" * 50)
    print("Agents 1, 3, and 4 will communicate to build a resume system")
    print()
    
    # Create agent instances
    agent1 = AgentCellPhone(agent_id="Agent-1", layout_mode="8-agent", test=True)
    agent3 = AgentCellPhone(agent_id="Agent-3", layout_mode="8-agent", test=True)
    agent4 = AgentCellPhone(agent_id="Agent-4", layout_mode="8-agent", test=True)
    
    # Start agent behaviors in separate threads
    threads = []
    
    t1 = threading.Thread(target=agent_1_behavior, args=(agent1,))
    t3 = threading.Thread(target=agent_3_behavior, args=(agent3,))
    t4 = threading.Thread(target=agent_4_behavior, args=(agent4,))
    
    threads.extend([t1, t3, t4])
    
    # Start all agents
    for thread in threads:
        thread.start()
    
    # Wait for all agents to complete
    for thread in threads:
        thread.join()
    
    print()
    print("✅ CONVERSATION DEMO COMPLETED!")
    print()
    
    # Show conversation summaries
    print("📊 CONVERSATION SUMMARIES:")
    print("-" * 30)
    
    print(f"\n{agent1.get_agent_id()} (Resume System Architect):")
    for msg in agent1.get_conversation_history():
        print(f"  {msg}")
    
    print(f"\n{agent3.get_agent_id()} (GUI Developer):")
    for msg in agent3.get_conversation_history():
        print(f"  {msg}")
    
    print(f"\n{agent4.get_agent_id()} (Integration Specialist):")
    for msg in agent4.get_conversation_history():
        print(f"  {msg}")

if __name__ == "__main__":
    main() 