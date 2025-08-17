#!/usr/bin/env python3
"""
Progressive Escalation Demo
===========================
Demonstrates the new progressive escalation system for stalled agents:
1. Shift+Backspace nudge (subtle)
2. Rescue message in existing chat (moderate)  
3. New chat escalation (aggressive)
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from src.services.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")
    sys.exit(1)

def demo_nudge_system():
    """Demonstrate the new nudge system"""
    print("🚀 Progressive Escalation Demo Starting...")
    print("=" * 50)
    
    # Initialize AgentCellPhone
    acp = AgentCellPhone(agent_id="Demo-Runner", layout_mode="5-agent", test=True)
    
    # Get available agents
    agents = acp.get_available_agents()
    print(f"Available agents: {', '.join(agents)}")
    
    if not agents:
        print("❌ No agents available for demo")
        return
    
    # Demo target agent
    target_agent = agents[0]
    print(f"\n🎯 Target agent for demo: {target_agent}")
    
    # Demo 1: Subtle nudge
    print("\n🔧 Demo 1: Subtle Nudge (Shift+Backspace)")
    print("-" * 40)
    try:
        acp.nudge_agent(target_agent, "subtle")
        print("✅ Subtle nudge completed")
    except Exception as e:
        print(f"❌ Subtle nudge failed: {e}")
    
    time.sleep(2)
    
    # Demo 2: Moderate nudge
    print("\n🔧 Demo 2: Moderate Nudge (Clear + Select)")
    print("-" * 40)
    try:
        acp.nudge_agent(target_agent, "moderate")
        print("✅ Moderate nudge completed")
    except Exception as e:
        print(f"❌ Moderate nudge failed: {e}")
    
    time.sleep(2)
    
    # Demo 3: Aggressive nudge
    print("\n🔧 Demo 3: Aggressive Nudge (Visual indicator)")
    print("-" * 40)
    try:
        acp.nudge_agent(target_agent, "aggressive")
        print("✅ Aggressive nudge completed")
    except Exception as e:
        print(f"❌ Aggressive nudge failed: {e}")
    
    time.sleep(2)
    
    # Demo 4: Progressive escalation
    print("\n🚀 Demo 4: Progressive Escalation (Full system)")
    print("-" * 40)
    try:
        rescue_message = (
            f"[DEMO] {target_agent}, this is a progressive escalation test.\n"
            f"Please respond to confirm you received this message.\n"
            f"Status: Testing progressive escalation system"
        )
        
        acp.progressive_escalation(target_agent, rescue_message, MsgTag.RESCUE)
        print("✅ Progressive escalation completed")
        
    except Exception as e:
        print(f"❌ Progressive escalation failed: {e}")
    
    print("\n🎉 Progressive Escalation Demo Completed!")
    print("=" * 50)

def demo_stall_recovery():
    """Demonstrate stall recovery scenarios"""
    print("\n🔄 Stall Recovery Scenarios Demo")
    print("=" * 50)
    
    # Initialize AgentCellPhone
    acp = AgentCellPhone(agent_id="Stall-Recovery-Demo", layout_mode="5-agent", test=True)
    
    # Get available agents
    agents = acp.get_available_agents()
    
    if not agents:
        print("❌ No agents available for demo")
        return
    
    target_agent = agents[0]
    
    # Scenario 1: Terminal appears stalled
    print(f"\n📱 Scenario 1: Terminal appears stalled for {target_agent}")
    print("-" * 50)
    
    try:
        # Simulate detecting a stalled terminal
        print("🔍 Detecting stalled terminal...")
        
        # Apply progressive escalation
        recovery_message = (
            f"[RECOVERY] {target_agent}, terminal appears stalled.\n"
            f"Applying progressive escalation:\n"
            f"1. Shift+Backspace nudge\n"
            f"2. Rescue message\n"
            f"3. New chat if needed\n"
            f"Status: Recovering from stall"
        )
        
        acp.progressive_escalation(target_agent, recovery_message, MsgTag.RESCUE)
        print("✅ Stall recovery escalation completed")
        
    except Exception as e:
        print(f"❌ Stall recovery failed: {e}")
    
    time.sleep(2)
    
    # Scenario 2: Agent not responding
    print(f"\n📱 Scenario 2: Agent not responding to {target_agent}")
    print("-" * 50)
    
    try:
        # Simulate agent not responding
        print("🔍 Detecting unresponsive agent...")
        
        # Try different nudge levels
        print("🔧 Applying subtle nudge...")
        acp.nudge_agent(target_agent, "subtle")
        time.sleep(1)
        
        print("🔧 Applying moderate nudge...")
        acp.nudge_agent(target_agent, "moderate")
        time.sleep(1)
        
        print("🔧 Applying aggressive nudge...")
        acp.nudge_agent(target_agent, "aggressive")
        
        print("✅ Multi-level nudge sequence completed")
        
    except Exception as e:
        print(f"❌ Multi-level nudge failed: {e}")
    
    print("\n🎉 Stall Recovery Demo Completed!")
    print("=" * 50)

def main():
    """Main demo function"""
    print("🎬 Progressive Escalation System Demo")
    print("=" * 60)
    print("This demo showcases the new Shift+Backspace nudge system")
    print("for preventing and recovering from agent terminal stalls.")
    print("")
    
    try:
        # Run nudge system demo
        demo_nudge_system()
        
        # Run stall recovery demo
        demo_stall_recovery()
        
        print("\n🎊 All demos completed successfully!")
        print("=" * 60)
        print("Key benefits of the progressive escalation system:")
        print("• Subtle interventions prevent unnecessary disruption")
        print("• Progressive escalation ensures agent recovery")
        print("• Automatic stall detection and response")
        print("• Fallback to new chat when all else fails")
        
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
