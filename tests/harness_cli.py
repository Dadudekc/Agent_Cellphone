#!/usr/bin/env python3
"""
Test Harness for Dream.OS Agent Cell Phone
Simple command-line interface for testing agent communication
"""

import argparse
import sys

from src.services.agent_cell_phone import AgentCellPhone, MsgTag


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

try:
    from src.agent_cell_phone import AgentCellPhone, MsgTag
except ImportError:
    print("Error: Could not import AgentCellPhone")
    sys.exit(1)

def main():
    """Main test harness function"""
    parser = argparse.ArgumentParser(description="Dream.OS Agent Cell Phone Test Harness")
    parser.add_argument("--mode", choices=["individual", "broadcast"], default="broadcast",
                       help="Message mode (individual or broadcast)")
    parser.add_argument("--message", "-m", required=True,
                       help="Message to send")
    parser.add_argument("--target", "-t", default="all",
                       help="Target agent (for individual mode)")
    parser.add_argument("--layout", "-l", default="8-agent",
                       choices=["2-agent", "4-agent", "8-agent"],
                       help="Layout mode")
    parser.add_argument("--test", action="store_true",
                       help="Run in test mode")
    parser.add_argument("--tag", choices=["NORMAL", "COMMAND", "STATUS", "ERROR", "CAPTAIN", "SYNC"],
                       default="NORMAL", help="Message tag")
    
    args = parser.parse_args()
    
    try:
        # Initialize agent cell phone
        acp = AgentCellPhone(layout_mode=args.layout, test=args.test)
        
        print("📱 Agent Cell Phone Test Harness")
        print("=" * 40)
        print(f"Mode: {'TEST' if args.test else 'LIVE'}")
        print(f"Layout: {args.layout}")
        print()
        
        # Get message tag
        try:
            msg_tag = MsgTag[args.tag]
        except KeyError:
            msg_tag = MsgTag.NORMAL
        
        if args.mode == "individual":
            print(f"📤 Sending individual message to {args.target}")
            print(f"[SEND] {args.target}: {args.message}")
            
            success, result = acp.send(args.target, args.message, msg_tag)
            
            if success:
                print(f"✅ Message sent successfully: '{args.message}'")
            else:
                print(f"❌ Failed to send message: {result}")
                
        else:  # broadcast
            print(f"📢 Testing broadcast message in {args.layout} mode")
            print(f"[SEND] All agents: {args.message}")
            
            acp.broadcast(args.message, msg_tag)
            print(f"✅ Broadcast sent successfully: '{args.message}'")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
