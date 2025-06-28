#!/usr/bin/env python3
"""
Test Inter-Agent Communication Framework
=======================================
Demonstrates messaging between Agent-1 through Agent-4
using the advanced inter-agent communication framework
"""

import time
import json
from inter_agent_framework import InterAgentFramework, Message, MessageType

def test_agent_communication():
    """Test communication between Agent-1 through Agent-4"""
    
    print("🤖 Inter-Agent Communication Framework Test")
    print("=" * 50)
    print("Testing messaging between Agent-1 through Agent-4")
    print()
    
    # Initialize framework for Agent-1 (controller)
    print("📡 Initializing Agent-1 as controller...")
    agent1 = InterAgentFramework("Agent-1", layout_mode="4-agent", test=True)
    
    # Test 1: Individual messages to each agent
    print("\n📤 Test 1: Individual Messages")
    print("-" * 30)
    
    test_messages = [
        ("Agent-2", "Hello from Agent-1! Ready for collaboration?"),
        ("Agent-3", "Agent-3, please verify your status and report back."),
        ("Agent-4", "Agent-4, prepare for task assignment.")
    ]
    
    for target, message_text in test_messages:
        print(f"📤 Sending to {target}: {message_text}")
        
        message = Message(
            sender="Agent-1",
            recipient=target,
            message_type=MessageType.COMMAND,
            command="custom",
            args=[message_text]
        )
        
        success = agent1.send_message(target, message)
        print(f"   {'✅ Success' if success else '❌ Failed'}")
        time.sleep(0.5)
    
    # Test 2: Command-based communication
    print("\n🎯 Test 2: Command-Based Communication")
    print("-" * 30)
    
    commands = [
        ("Agent-2", "ping", []),
        ("Agent-3", "status", []),
        ("Agent-4", "verify", []),
    ]
    
    for target, command, args in commands:
        print(f"🎯 Sending {command} command to {target}")
        
        message = Message(
            sender="Agent-1",
            recipient=target,
            message_type=MessageType.COMMAND,
            command=command,
            args=args
        )
        
        success = agent1.send_message(target, message)
        print(f"   {'✅ Success' if success else '❌ Failed'}")
        time.sleep(0.5)
    
    # Test 3: Task assignment
    print("\n📋 Test 3: Task Assignment")
    print("-" * 30)
    
    tasks = [
        ("Agent-2", "Coordinate data collection and analysis"),
        ("Agent-3", "Monitor system performance and generate reports"),
        ("Agent-4", "Handle external API integrations and data validation")
    ]
    
    for target, task_description in tasks:
        print(f"📋 Assigning task to {target}: {task_description}")
        
        message = Message(
            sender="Agent-1",
            recipient=target,
            message_type=MessageType.COMMAND,
            command="task",
            args=[task_description]
        )
        
        success = agent1.send_message(target, message)
        print(f"   {'✅ Success' if success else '❌ Failed'}")
        time.sleep(0.5)
    
    # Test 4: Broadcast communication
    print("\n📢 Test 4: Broadcast Communication")
    print("-" * 30)
    
    broadcast_messages = [
        "All agents: System initialization complete. Begin operations.",
        "Status check: All agents report current operational status.",
        "Emergency protocol: Prepare for coordinated response sequence."
    ]
    
    for broadcast_msg in broadcast_messages:
        print(f"📢 Broadcasting: {broadcast_msg}")
        
        message = Message(
            sender="Agent-1",
            recipient="all",
            message_type=MessageType.BROADCAST,
            command="broadcast",
            args=[broadcast_msg]
        )
        
        success = agent1.broadcast_message(message)
        print(f"   {'✅ Success' if success else '❌ Failed'}")
        time.sleep(0.5)
    
    # Test 5: Multi-agent coordination
    print("\n🤝 Test 5: Multi-Agent Coordination")
    print("-" * 30)
    
    coordination_sequence = [
        ("Agent-2", "sync", ["data_collection", "analysis_pipeline"]),
        ("Agent-3", "sync", ["performance_metrics", "reporting_system"]),
        ("Agent-4", "sync", ["api_integrations", "validation_rules"]),
    ]
    
    for target, command, args in coordination_sequence:
        print(f"🤝 Coordinating with {target}: {command} {' '.join(args)}")
        
        message = Message(
            sender="Agent-1",
            recipient=target,
            message_type=MessageType.COMMAND,
            command=command,
            args=args
        )
        
        success = agent1.send_message(target, message)
        print(f"   {'✅ Success' if success else '❌ Failed'}")
        time.sleep(0.5)
    
    # Test 6: Captain role activation
    print("\n👑 Test 6: Captain Role Activation")
    print("-" * 30)
    
    print("👑 Agent-1 taking captain role...")
    
    message = Message(
        sender="Agent-1",
        recipient="all",
        message_type=MessageType.COMMAND,
        command="captain",
        args=["Taking command of all operations"]
    )
    
    success = agent1.broadcast_message(message)
    print(f"   {'✅ Success' if success else '❌ Failed'}")
    
    # Test 7: Status reporting
    print("\n📊 Test 7: Status Reporting")
    print("-" * 30)
    
    print("📊 Agent-1 Framework Status:")
    status = agent1.get_status()
    print(json.dumps(status, indent=2))
    
    # Test 8: Message history
    print("\n📜 Test 8: Message History")
    print("-" * 30)
    
    history = agent1.get_message_history(limit=10)
    print(f"📜 Last {len(history)} messages:")
    for i, msg in enumerate(history, 1):
        print(f"   {i}. {msg.sender} → {msg.recipient}: {msg.command or 'DATA'}")
    
    # Summary
    print("\n🎉 Test Summary")
    print("=" * 50)
    print("✅ Inter-Agent Communication Framework Test Completed")
    print(f"📡 Controller: Agent-1")
    print(f"👥 Target Agents: Agent-2, Agent-3, Agent-4")
    print(f"📨 Total Messages Sent: {len(agent1.message_history)}")
    print(f"🎯 Layout Mode: {agent1.layout_mode}")
    print(f"🧪 Test Mode: {agent1.test_mode}")
    print()
    print("🚀 Framework is ready for real agent communication!")
    print("   Remove --test flag for live operation.")

def test_agent_responses():
    """Test how agents would respond to messages"""
    
    print("\n🔄 Agent Response Simulation")
    print("=" * 50)
    
    # Simulate Agent-2 responses
    print("🤖 Agent-2 Response Simulation:")
    agent2 = InterAgentFramework("Agent-2", layout_mode="4-agent", test=True)
    
    # Simulate receiving a ping
    ping_message = Message(
        sender="Agent-1",
        recipient="Agent-2",
        message_type=MessageType.COMMAND,
        command="ping",
        args=[]
    )
    
    print("📥 Agent-2 received ping from Agent-1")
    agent2.message_history.append(ping_message)
    
    # Simulate response
    response = Message(
        sender="Agent-2",
        recipient="Agent-1",
        message_type=MessageType.RESPONSE,
        command="pong",
        data={"status": "active", "timestamp": "2025-06-28T15:30:00"}
    )
    
    print("📤 Agent-2 responding with pong")
    agent2.message_history.append(response)
    
    # Show Agent-2 status
    status = agent2.get_status()
    print(f"📊 Agent-2 Status: {status['message_count']} messages processed")
    
    print("\n✅ Response simulation completed")

if __name__ == "__main__":
    test_agent_communication()
    test_agent_responses() 