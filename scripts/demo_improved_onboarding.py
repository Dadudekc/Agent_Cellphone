#!/usr/bin/env python3
"""
Demo: Improved Onboarding System
================================
Demonstrates the improved onboarding system that uses the CLI tool
for agent communication instead of complex hybrid systems.
"""

import subprocess
import time
import sys
from pathlib import Path

def run_cli_command(cmd_args, description=""):
    """Run a CLI command and return the result"""
    try:
        print(f"📤 {description}")
        result = subprocess.run(cmd_args, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.returncode == 0:
            print(f"✅ Success: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Error: {result.stderr.strip()}")
            return False
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def demonstrate_improved_onboarding():
    """Demonstrate the improved onboarding system"""
    print("🎯 Improved Onboarding System Demo")
    print("=" * 60)
    print("This demo shows how the CLI tool is used for agent communication")
    print("instead of complex hybrid systems.")
    print()
    
    # Step 1: Show available layouts
    print("📋 Step 1: Check available layouts")
    run_cli_command([
        "python", "src/agent_cell_phone.py", "--list-layouts"
    ], "Listing available layouts")
    print()
    
    # Step 2: Show available agents in 2-agent mode
    print("📋 Step 2: Check available agents in 2-agent mode")
    run_cli_command([
        "python", "src/agent_cell_phone.py", "--list-agents", "--layout", "2-agent"
    ], "Listing agents in 2-agent mode")
    print()
    
    # Step 3: Send onboarding message to Agent-1
    print("📋 Step 3: Send onboarding message to Agent-1")
    onboarding_message = """Welcome to Dream.OS! You are Agent-1, our System Coordinator.

IMPORTANT: Use the CLI tool for all agent communication:
```bash
python src/agent_cell_phone.py -a Agent-2 -m "Hello from Agent-1!" -t normal
```

Your role is crucial to our success:
• Project coordination and task assignment
• Progress monitoring and bottleneck identification
• Conflict resolution and team leadership

Next steps:
1. Read the onboarding documentation
2. Practice using the CLI tool
3. Coordinate with other agents

You're the leader of our team! 🎉"""
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-1",
        "-m", onboarding_message,
        "-t", "onboarding"
    ], "Sending onboarding message to Agent-1")
    print()
    
    # Step 4: Send task assignment to Agent-2
    print("📋 Step 4: Send task assignment to Agent-2")
    task_message = """Agent-2, please implement the login feature for our web application.

Requirements:
• User authentication with email/password
• Session management
• Password reset functionality
• Security best practices

Please use the CLI tool to communicate your progress:
```bash
python src/agent_cell_phone.py -a Agent-1 -m "Login feature 50% complete" -t reply
```

Expected completion: 2 days"""
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-2",
        "-m", task_message,
        "-t", "task"
    ], "Sending task assignment to Agent-2")
    print()
    
    # Step 5: Demonstrate coordination message
    print("📋 Step 5: Send coordination message")
    coord_message = """Agent-2 and Agent-3, let's coordinate on the API design.

Agent-2: Please design the frontend login interface
Agent-3: Please design the backend authentication API

Let's meet via CLI to discuss integration points:
```bash
python src/agent_cell_phone.py -a Agent-1 -m "Ready to discuss API design" -t coordinate
```"""
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-a", "Agent-2",
        "-m", coord_message,
        "-t", "coordinate"
    ], "Sending coordination message to Agent-2")
    print()
    
    # Step 6: Demonstrate broadcast message
    print("📋 Step 6: Send broadcast message to all agents")
    broadcast_message = """System Update: All agents should now use the CLI tool for communication.

The command format is:
```bash
python src/agent_cell_phone.py -a <TargetAgent> -m '<Your message>' -t <tag>
```

This replaces the complex hybrid systems with a simple, reliable method.
Please acknowledge receipt of this message."""
    
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "-m", broadcast_message,
        "-t", "normal"
    ], "Broadcasting system update to all agents")
    print()
    
    # Step 7: Show test mode
    print("📋 Step 7: Demonstrate test mode")
    run_cli_command([
        "python", "src/agent_cell_phone.py",
        "--test",
        "-a", "Agent-2",
        "-m", "This is a test message - no GUI interaction"
    ], "Testing message in test mode")
    print()
    
    print("🎉 Demo completed!")
    print()
    print("📚 Key Benefits of the CLI Tool:")
    print("  ✅ Simple and reliable")
    print("  ✅ Scriptable for automation")
    print("  ✅ No complex pipe management")
    print("  ✅ Works consistently across platforms")
    print("  ✅ Easy to debug and troubleshoot")
    print()
    print("🚀 Next Steps:")
    print("  1. Use the CLI tool for all agent communication")
    print("  2. Script the CLI for continuous workflows")
    print("  3. Update your onboarding and training materials")
    print("  4. Practice with different message tags")

def demonstrate_onboarding_script():
    """Demonstrate the improved onboarding script"""
    print("\n" + "=" * 60)
    print("🎯 Onboarding Script Demo")
    print("=" * 60)
    
    # Show available agents
    print("📋 Available agents:")
    run_cli_command([
        "python", "scripts/agent_onboarding_sequence.py", "--list-agents"
    ], "Listing available agents for onboarding")
    print()
    
    # Test onboarding for Agent-1
    print("📋 Testing onboarding for Agent-1:")
    run_cli_command([
        "python", "scripts/agent_onboarding_sequence.py", "--agent", "Agent-1", "--test"
    ], "Testing onboarding sequence for Agent-1")
    print()
    
    print("✅ Onboarding script demo completed!")

if __name__ == "__main__":
    demonstrate_improved_onboarding()
    demonstrate_onboarding_script() 