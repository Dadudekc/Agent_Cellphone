#!/usr/bin/env python3
"""
CLI Test Harness for Agent Cell Phone
Simulates agent messaging for testing and development
Supports multiple layout modes (2-agent, 4-agent, 8-agent)
"""

import argparse
import sys
import time
from pathlib import Path

# Ensure src directory is on the import path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from services.agent_cell_phone import AgentCellPhone, MsgTag


def test_send_message(agent_id: str, target_agent: str, message: str, layout_mode: str = "2-agent", test_mode: bool = True):
    """Test sending a single message"""
    print(f"🧪 Testing message from {agent_id} to {target_agent} in {layout_mode} mode")
    
    try:
        # Initialize agent
        acp = AgentCellPhone(layout_mode=layout_mode, test=test_mode)
        
        # Send message
        acp.send(target_agent, message)
        
        print(f"✅ Message sent successfully: '{message}'")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_broadcast(message: str, layout_mode: str = "2-agent", test_mode: bool = True):
    """Test broadcasting to all agents"""
    print(f"📢 Testing broadcast message in {layout_mode} mode")
    
    try:
        # Initialize agent
        acp = AgentCellPhone(layout_mode=layout_mode, test=test_mode)
        
        # Broadcast message
        acp.broadcast(message)
        
        print(f"✅ Broadcast sent successfully: '{message}'")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_exec_mode(agent_id: str, mode_key: str, layout_mode: str = "2-agent", test_mode: bool = True, **kwargs):
    """Test executing a predefined mode"""
    print(f"🎯 Testing mode execution for {agent_id} with mode '{mode_key}' in {layout_mode} mode")
    
    try:
        # Initialize agent
        acp = AgentCellPhone(layout_mode=layout_mode, test=test_mode)
        
        # Execute mode
        acp.exec_mode(agent_id, mode_key, **kwargs)
        
        print(f"✅ Mode '{mode_key}' executed successfully for {agent_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_coordinate_loading(layout_mode: str = "2-agent"):
    """Test coordinate loading and validation for specific layout mode"""
    print(f"🗺️ Testing coordinate loading for {layout_mode} mode")
    
    try:
        acp = AgentCellPhone(layout_mode=layout_mode, test=True)
        
        # Access coordinates (they're loaded in __init__)
        coords = acp._coords
        
        print(f"✅ Loaded {len(coords)} agent coordinates for {layout_mode} mode:")
        for agent_id, coord_data in coords.items():
            x, y = coord_data["input_box"]["x"], coord_data["input_box"]["y"]
            print(f"  {agent_id}: ({x}, {y})")
            
        return True
        
    except Exception as e:
        print(f"❌ Error loading coordinates: {e}")
        return False


def list_available_layouts():
    """List all available layout modes"""
    print("📋 Available layout modes:")
    print("=" * 40)
    
    try:
        acp = AgentCellPhone(layout_mode="2-agent", test=True)  # Use any mode to initialize
        layouts = acp.get_available_layouts()
        
        for layout in layouts:
            # Get agent count for this layout
            temp_acp = AgentCellPhone(layout_mode=layout, test=True)
            agent_count = len(temp_acp.get_available_agents())
            print(f"  {layout} ({agent_count} agents)")
            
        return True
        
    except Exception as e:
        print(f"❌ Error listing layouts: {e}")
        return False


def list_agents_in_layout(layout_mode: str = "2-agent"):
    """List all agents available in a specific layout mode"""
    print(f"👥 Available agents in {layout_mode} mode:")
    print("=" * 40)
    
    try:
        acp = AgentCellPhone(layout_mode=layout_mode, test=True)
        agents = acp.get_available_agents()
        
        for agent in agents:
            print(f"  {agent}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")
        return False


def interactive_mode(layout_mode: str = "2-agent", test_mode: bool = True):
    """Interactive mode for manual testing"""
    print(f"🎮 Interactive mode for {layout_mode} layout")
    print("Commands: send <agent> <message>, broadcast <message>, mode <agent> <mode_key>, quit")
    
    try:
        acp = AgentCellPhone(layout_mode=layout_mode, test=test_mode)
        
        while True:
            try:
                cmd = input(f"acp[{layout_mode}]> ").strip()
                
                if cmd.lower() in ['quit', 'exit', 'q']:
                    break
                    
                parts = cmd.split()
                if len(parts) < 2:
                    print("Usage: send <agent> <message>, broadcast <message>, mode <agent> <mode_key>, or quit")
                    continue
                    
                if parts[0].lower() == 'send':
                    if len(parts) < 3:
                        print("Usage: send <agent> <message>")
                        continue
                    agent = parts[1]
                    message = ' '.join(parts[2:])
                    acp.send(agent, message)
                    print(f"✅ Sent to {agent}")
                    
                elif parts[0].lower() == 'broadcast':
                    message = ' '.join(parts[1:])
                    acp.broadcast(message)
                    print(f"✅ Broadcast sent")
                    
                elif parts[0].lower() == 'mode':
                    if len(parts) < 3:
                        print("Usage: mode <agent> <mode_key>")
                        continue
                    agent = parts[1]
                    mode_key = parts[2]
                    acp.exec_mode(agent, mode_key)
                    print(f"✅ Mode '{mode_key}' executed for {agent}")
                    
                else:
                    print("Unknown command. Use: send, broadcast, mode, or quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")


def demo_sequence(layout_mode: str = "2-agent"):
    """Run a complete demo sequence for a specific layout mode"""
    print(f"🎬 Running Agent Cell Phone Demo for {layout_mode} mode")
    print("=" * 50)
    
    # Test coordinate loading
    if not test_coordinate_loading(layout_mode):
        return
        
    print()
    
    # Test individual sends (use first two agents available)
    try:
        acp = AgentCellPhone(layout_mode=layout_mode, test=True)
        agents = acp.get_available_agents()
        
        if len(agents) >= 2:
            test_send_message("Agent-1", "Agent-2", "Hello from Agent-1!", layout_mode)
            time.sleep(1)
            test_send_message("Agent-2", "Agent-1", "Hello from Agent-2!", layout_mode)
            time.sleep(1)
        else:
            print(f"⚠️  {layout_mode} mode only has {len(agents)} agent(s), skipping individual sends")
        
        print()
        
        # Test broadcast
        test_broadcast("Broadcast test message", layout_mode)
        
        print()
        print("🎉 Demo completed!")
        
    except Exception as e:
        print(f"❌ Error in demo: {e}")


def main():
    parser = argparse.ArgumentParser(description="Agent Cell Phone Test Harness")
    parser.add_argument("--agent", default="Agent-1", help="Agent ID for testing")
    parser.add_argument("--target", help="Target agent for send command")
    parser.add_argument("--message", help="Message content")
    parser.add_argument("--layout", default="2-agent", choices=["2-agent", "4-agent", "8-agent"], 
                       help="Layout mode")
    parser.add_argument("--mode", choices=["send", "broadcast", "exec_mode", "coords", "interactive", "demo", "list-layouts", "list-agents"], 
                       default="demo", help="Test mode")
    parser.add_argument("--mode-key", help="Mode key for exec_mode")
    parser.add_argument("--test", action="store_true", default=True, help="Run in test mode (default)")
    parser.add_argument("--live", action="store_true", help="Run in live mode (overrides --test)")
    
    args = parser.parse_args()
    
    # Determine test mode
    test_mode = not args.live
    
    print("📱 Agent Cell Phone Test Harness")
    print("=" * 40)
    print(f"Mode: {'TEST' if test_mode else 'LIVE'}")
    print(f"Layout: {args.layout}")
    print()
    
    if args.mode == "send":
        if not args.target or not args.message:
            print("❌ send mode requires --target and --message")
            sys.exit(1)
        test_send_message(args.agent, args.target, args.message, args.layout, test_mode)
        
    elif args.mode == "broadcast":
        if not args.message:
            print("❌ broadcast mode requires --message")
            sys.exit(1)
        test_broadcast(args.message, args.layout, test_mode)
        
    elif args.mode == "exec_mode":
        if not args.target or not args.mode_key:
            print("❌ exec_mode requires --target and --mode-key")
            sys.exit(1)
        test_exec_mode(args.target, args.mode_key, args.layout, test_mode)
        
    elif args.mode == "coords":
        test_coordinate_loading(args.layout)
        
    elif args.mode == "list-layouts":
        list_available_layouts()
        
    elif args.mode == "list-agents":
        list_agents_in_layout(args.layout)
        
    elif args.mode == "interactive":
        interactive_mode(args.layout, test_mode)
        
    elif args.mode == "demo":
        demo_sequence(args.layout)


if __name__ == "__main__":
    main()
