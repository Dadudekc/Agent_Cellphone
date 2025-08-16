#!/usr/bin/env python3
"""
Autonomous CAPTAIN Demo
======================
Demonstrates Agent-5's autonomous coordination capabilities.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fsm import AutonomousCaptain

def demo_autonomous_captain():
    """Demo autonomous CAPTAIN capabilities"""
    print("🎖️ Autonomous CAPTAIN Demo - Agent-5 Self-Coordination")
    print("=" * 60)
    
    # Initialize autonomous CAPTAIN
    captain = AutonomousCaptain("D:/repos/Dadudekc")
    
    print("\n📊 CAPTAIN Task Overview:")
    print("-" * 40)
    
    for task in captain.tasks:
        status_emoji = "🟢" if task.status == "completed" else "🟡" if task.status == "in_progress" else "🔴"
        priority_emoji = "🚨" if task.priority == "high" else "⚠️" if task.priority == "medium" else "ℹ️"
        
        print(f"{status_emoji} {priority_emoji} {task.title}")
        print(f"   Status: {task.status}")
        print(f"   Priority: {task.priority}")
        print(f"   Description: {task.description}")
        print()
    
    print("\n🧠 CAPTAIN Self-Prompt:")
    print("-" * 40)
    
    # Generate self-prompt
    self_prompt = captain.self_prompt()
    print(self_prompt)
    
    print("\n🎯 Executing CAPTAIN Actions:")
    print("-" * 40)
    
    # Run CAPTAIN cycle
    captain.run_captain_cycle()
    
    print("\n✅ Demo Complete!")
    print("\nThe Autonomous CAPTAIN now provides:")
    print("• Self-prompting and task generation")
    print("• Smart new chat logic (starter vs input coordinates)")
    print("• Autonomous decision making")
    print("• Priority-based task execution")
    print("• Real-time agent coordination")
    print("• Blocker detection and resolution")

if __name__ == "__main__":
    demo_autonomous_captain()
