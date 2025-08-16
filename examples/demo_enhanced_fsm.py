#!/usr/bin/env python3
"""
Enhanced FSM Demo
=================
Demonstrates personalized, contextual message generation.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fsm import EnhancedFSM

def demo_personalized_messages():
    """Demo personalized message generation"""
    print("🚀 Enhanced FSM Demo - Personalized Message Generation")
    print("=" * 60)
    
    # Initialize FSM
    fsm = EnhancedFSM("D:/repos/Dadudekc")
    
    # Demo agents
    agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]
    
    print("\n📊 Current Agent States:")
    print("-" * 40)
    
    for agent in agents:
        state = fsm.update_agent_state(agent)
        print(f"{agent}: {state.status} - {state.current_repo or 'No repo'}")
    
    print("\n💬 Personalized Message Examples:")
    print("-" * 40)
    
    # Demo different message types
    message_types = ["RESUME", "TASK", "COORDINATE", "RESCUE"]
    
    for agent in agents[:4]:  # Skip Agent-5 (CAPTAIN)
        print(f"\n{agent}:")
        for msg_type in message_types:
            message = fsm.generate_personalized_message(agent, msg_type)
            print(f"  {msg_type}: {message}")
    
    print("\n📈 Coordination Summary:")
    print("-" * 40)
    
    summary = fsm.get_coordination_summary()
    print(f"Active Agents: {summary['overall_progress']['active_agents']}")
    print(f"Stalled Agents: {summary['overall_progress']['stalled_agents']}")
    
    print("\n🎯 Agent Recommendations:")
    print("-" * 40)
    
    for agent in agents[:4]:
        recommendations = fsm.get_agent_recommendations(agent)
        print(f"\n{agent}:")
        for rec in recommendations:
            print(f"  • {rec}")
    
    print("\n✅ Demo Complete!")
    print("\nThe Enhanced FSM now provides:")
    print("• Personalized messages based on actual work")
    print("• Context-aware guidance")
    print("• Progress tracking across repositories")
    print("• Intelligent cycle management")
    print("• Blocker detection and resolution")

if __name__ == "__main__":
    demo_personalized_messages()
