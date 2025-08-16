#!/usr/bin/env python3
"""
Enhanced GUI and PyAutoGUI Queue System Demonstration
-----------------------------------------------------
This script demonstrates the new enhanced GUI capabilities:
• Agent-5 Command Center for controlling other agents
• PyAutoGUI messaging queue to prevent conflicts
• Agent coordination and overnight run facilitation
• Real-time status monitoring and control
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add the overnight_runner directory to the path
sys.path.insert(0, str(Path(__file__).parent / "overnight_runner"))

def demo_pyautogui_queue():
    """Demonstrate the PyAutoGUI queue system."""
    print("🚀 DEMONSTRATING PyAutoGUI QUEUE SYSTEM")
    print("=" * 50)
    
    try:
        from enhanced_gui import PyAutoGUIQueue
        
        # Create queue instance
        queue = PyAutoGUIQueue()
        print("✅ PyAutoGUI queue created successfully")
        
        # Add agents
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        for agent in agents:
            queue.add_agent(agent)
        print(f"✅ Added {len(agents)} agents to queue system")
        
        # Queue some messages
        messages = [
            ("Agent-1", "STATUS: Report current progress", 1),
            ("Agent-2", "TASK: Review technical requirements", 2),
            ("Agent-3", "COORDINATE: Prepare for development session", 1),
            ("Agent-4", "NUDGE: Wake up and report status", 3)
        ]
        
        print("\n📋 Queuing messages...")
        for agent, message, priority in messages:
            if queue.queue_message(agent, message, priority):
                print(f"  ✅ {agent}: {message[:40]}... (Priority: {priority})")
            else:
                print(f"  ❌ {agent}: Failed to queue message")
        
        # Show queue status
        print("\n📊 Queue Status:")
        status = queue.get_queue_status()
        print(f"  Queue Size: {status['queue_size']}")
        print(f"  Processing: {status['processing']}")
        print(f"  Agent Locks: {status['agent_locks']}")
        
        # Wait for processing
        print("\n⏳ Waiting for queue processing...")
        time.sleep(3)
        
        # Show final status
        print("\n📊 Final Queue Status:")
        final_status = queue.get_queue_status()
        print(f"  Queue Size: {final_status['queue_size']}")
        print(f"  Processing: {final_status['processing']}")
        
        # Stop processing
        queue.stop_processing()
        print("✅ Queue processing stopped")
        
    except ImportError as e:
        print(f"❌ Could not import enhanced GUI: {e}")
        print("   Make sure you're running this from the Agent_Cellphone directory")
    except Exception as e:
        print(f"❌ Error during queue demonstration: {e}")

def demo_agent5_command_center():
    """Demonstrate the Agent-5 command center capabilities."""
    print("\n🎯 DEMONSTRATING AGENT-5 COMMAND CENTER")
    print("=" * 50)
    
    try:
        from enhanced_gui import Agent5CommandCenter, PyAutoGUIQueue
        
        # Create mock GUI and command center
        class MockGUI:
            def log_message(self, message):
                print(f"  📝 {message}")
        
        mock_gui = MockGUI()
        queue = PyAutoGUIQueue()
        command_center = Agent5CommandCenter(mock_gui)
        
        print("✅ Agent-5 command center created successfully")
        
        # Demonstrate individual commands
        print("\n📤 Individual Agent Commands:")
        command_center.send_command("Agent-1", "STATUS: Report current progress")
        command_center.send_command("Agent-2", "TASK: Review technical architecture")
        
        # Demonstrate broadcast commands
        print("\n📢 Broadcast Commands:")
        command_center.broadcast_command("COORDINATE: Prepare for development session")
        
        # Demonstrate team coordination
        print("\n🤝 Team Coordination:")
        command_center.coordinate_agents("Implement new feature based on requirements")
        
        # Demonstrate overnight run
        print("\n🚀 Overnight Run Coordination:")
        command_center.start_overnight_run(duration_minutes=60)
        
        # Show queue status
        print("\n📊 Command Center Queue Status:")
        status = command_center.get_queue_status()
        print(f"  Queue Size: {status['queue_size']}")
        print(f"  Processing: {status['processing']}")
        print(f"  Agent Locks: {status['agent_locks']}")
        
        # Stop processing
        command_center.acp_queue.stop_processing()
        print("✅ Command center queue processing stopped")
        
    except ImportError as e:
        print(f"❌ Could not import enhanced GUI: {e}")
        print("   Make sure you're running this from the Agent_Cellphone directory")
    except Exception as e:
        print(f"❌ Error during command center demonstration: {e}")

def demo_agent_cellphone_integration():
    """Demonstrate the enhanced AgentCellPhone integration with the queue system."""
    print("\n📱 DEMONSTRATING AGENT CELLPHONE QUEUE INTEGRATION")
    print("=" * 50)
    
    try:
        # Import the enhanced AgentCellPhone
        sys.path.insert(0, str(Path(__file__).parent / "src" / "services"))
        from agent_cell_phone import AgentCellPhone
        
        # Import the queue system
        from enhanced_gui import PyAutoGUIQueue
        
        # Create queue and AgentCellPhone instances
        queue = PyAutoGUIQueue()
        acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=True)
        
        print("✅ AgentCellPhone and queue created successfully")
        
        # Integrate queue with AgentCellPhone
        acp.set_pyautogui_queue(queue)
        print("✅ Queue integration enabled")
        
        # Test queue-enabled sending
        print("\n📤 Testing Queue-Enabled Sending:")
        agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]
        for agent in agents:
            message = f"QUEUE TEST: Message from {acp.get_agent_id()} to {agent}"
            if acp.send_queued(agent, message, priority=1):
                print(f"  ✅ {agent}: Message queued successfully")
            else:
                print(f"  ❌ {agent}: Failed to queue message")
        
        # Show queue status
        print("\n📊 AgentCellPhone Queue Status:")
        status = acp.get_queue_status()
        print(f"  Queue Size: {status['queue_size']}")
        print(f"  Processing: {status['processing']}")
        print(f"  Agent Locks: {status['agent_locks']}")
        
        # Test queue clearing
        print("\n🗑️ Testing Queue Clear:")
        if acp.clear_queue():
            print("  ✅ Queue cleared successfully")
        else:
            print("  ⚠️ Queue clear not yet implemented")
        
        # Stop processing
        queue.stop_processing()
        print("✅ Queue processing stopped")
        
    except ImportError as e:
        print(f"❌ Could not import required modules: {e}")
        print("   Make sure you're running this from the Agent_Cellphone directory")
    except Exception as e:
        print(f"❌ Error during AgentCellPhone integration demonstration: {e}")

def demo_gui_features():
    """Demonstrate the enhanced GUI features."""
    print("\n🖥️ DEMONSTRATING ENHANCED GUI FEATURES")
    print("=" * 50)
    
    try:
        from enhanced_gui import EnhancedRunnerGUI
        import tkinter as tk
        
        print("✅ Enhanced GUI module imported successfully")
        print("\n🎯 Available GUI Features:")
        print("  • Agent-5 Command Center Tab")
        print("    - Individual agent commands")
        print("    - Broadcast commands")
        print("    - Predefined command buttons")
        print("    - Task management")
        print("    - Command logging")
        
        print("  • Overnight Runner Control Tab")
        print("    - Configuration settings")
        print("    - Listener controls")
        print("    - Runner controls")
        print("    - Utility functions")
        
        print("  • Queue Management Tab")
        print("    - Queue status monitoring")
        print("    - Queue controls (pause/resume)")
        print("    - Agent lock status")
        print("    - Queue statistics")
        
        print("  • Agent Monitoring Tab")
        print("    - Individual agent status")
        print("    - Status checking")
        print("    - Nudge commands")
        print("    - Activity logging")
        
        print("\n💡 To launch the GUI, run:")
        print("   python overnight_runner/enhanced_gui.py")
        
    except ImportError as e:
        print(f"❌ Could not import enhanced GUI: {e}")
        print("   Make sure you're running this from the Agent_Cellphone directory")
    except Exception as e:
        print(f"❌ Error during GUI features demonstration: {e}")

def main():
    """Main demonstration function."""
    print("🚀 ENHANCED GUI AND PYAUTOGUI QUEUE SYSTEM DEMONSTRATION")
    print("=" * 70)
    print("This demonstration showcases the new capabilities:")
    print("• Expanded GUI for commanding Agent-5")
    print("• PyAutoGUI messaging queue to prevent conflicts")
    print("• Agent coordination and overnight run facilitation")
    print("• Real-time status monitoring and control")
    print("=" * 70)
    
    # Run demonstrations
    demo_pyautogui_queue()
    demo_agent5_command_center()
    demo_agent_cellphone_integration()
    demo_gui_features()
    
    print("\n🎉 DEMONSTRATION COMPLETE!")
    print("=" * 70)
    print("💡 Key Benefits of the New System:")
    print("  ✅ Prevents PyAutoGUI conflicts when multiple agents/instances run")
    print("  ✅ Provides centralized Agent-5 command center")
    print("  ✅ Enables coordinated agent management")
    print("  ✅ Offers real-time monitoring and control")
    print("  ✅ Maintains backward compatibility")
    
    print("\n🔧 Next Steps:")
    print("  1. Launch the enhanced GUI: python overnight_runner/enhanced_gui.py")
    print("  2. Use the Agent-5 Command Center to control agents")
    print("  3. Monitor queue status and agent locks")
    print("  4. Coordinate overnight runs and team tasks")
    
    print("\n📖 For more information:")
    print("  • Enhanced GUI: overnight_runner/enhanced_gui.py")
    print("  • PyAutoGUI Queue: PyAutoGUIQueue class")
    print("  • Agent-5 Command Center: Agent5CommandCenter class")
    print("  • AgentCellPhone Integration: Enhanced send() method")

if __name__ == "__main__":
    main()
