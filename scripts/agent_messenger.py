#!/usr/bin/env python3
"""
Agent Messenger CLI
==================
Simple command-line interface for messaging Agent-1 through Agent-4
using the Inter-Agent Communication Framework
"""

import argparse
import json
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from inter_agent_framework import InterAgentFramework, Message, MessageType

def main():
    parser = argparse.ArgumentParser(description="Agent Messenger - Send messages to Agent-1 through Agent-4")
    parser.add_argument("--sender", default="Controller", help="Sender agent ID")
    parser.add_argument("--target", required=True, choices=["Agent-1", "Agent-2", "Agent-3", "Agent-4", "all"], 
                       help="Target agent(s)")
    parser.add_argument("--message", help="Message content")
    parser.add_argument("--command", choices=["ping", "status", "resume", "sync", "verify", "task", "captain"], 
                       help="Command to execute")
    parser.add_argument("--args", nargs="*", help="Command arguments")
    parser.add_argument("--test", action="store_true", default=True, help="Test mode (default)")
    parser.add_argument("--live", action="store_true", help="Live mode (overrides --test)")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Determine test mode
    test_mode = not args.live
    
    # Initialize framework
    framework = InterAgentFramework(args.sender, layout_mode="4-agent", test=test_mode)
    
    if args.interactive:
        interactive_mode(framework)
    elif args.command:
        # Execute command
        if args.target == "all":
            message = Message(
                sender=args.sender,
                recipient="all",
                message_type=MessageType.COMMAND,
                command=args.command,
                args=args.args or []
            )
            success = framework.broadcast_message(message)
            print(f"✅ Command '{args.command}' broadcast to all agents" if success else "❌ Command failed")
        else:
            message = Message(
                sender=args.sender,
                recipient=args.target,
                message_type=MessageType.COMMAND,
                command=args.command,
                args=args.args or []
            )
            success = framework.send_message(args.target, message)
            print(f"✅ Command '{args.command}' sent to {args.target}" if success else "❌ Command failed")
    
    elif args.message:
        # Send message
        if args.target == "all":
            message = Message(
                sender=args.sender,
                recipient="all",
                message_type=MessageType.BROADCAST,
                command="broadcast",
                args=[args.message]
            )
            success = framework.broadcast_message(message)
            print(f"✅ Message broadcast to all agents" if success else "❌ Broadcast failed")
        else:
            message = Message(
                sender=args.sender,
                recipient=args.target,
                message_type=MessageType.COMMAND,
                command="custom",
                args=[args.message]
            )
            success = framework.send_message(args.target, message)
            print(f"✅ Message sent to {args.target}" if success else "❌ Message failed")
    
    else:
        parser.print_help()

def interactive_mode(framework):
    """Interactive mode for messaging agents"""
    print(f"🎮 Interactive Agent Messenger")
    print(f"📡 Sender: {framework.agent_id}")
    print(f"👥 Available targets: Agent-1, Agent-2, Agent-3, Agent-4, all")
    print("Commands: send <target> <message>, command <target> <cmd> [args], status, quit")
    print()
    
    while True:
        try:
            cmd = input(f"messenger[{framework.agent_id}]> ").strip()
            
            if cmd.lower() in ['quit', 'exit', 'q']:
                break
            
            parts = cmd.split()
            if len(parts) < 2:
                print("Usage: send <target> <message>, command <target> <cmd> [args], status, or quit")
                continue
            
            if parts[0].lower() == 'send':
                if len(parts) < 3:
                    print("Usage: send <target> <message>")
                    continue
                
                target = parts[1]
                message_text = ' '.join(parts[2:])
                
                if target == "all":
                    message = Message(
                        sender=framework.agent_id,
                        recipient="all",
                        message_type=MessageType.BROADCAST,
                        command="broadcast",
                        args=[message_text]
                    )
                    success = framework.broadcast_message(message)
                else:
                    message = Message(
                        sender=framework.agent_id,
                        recipient=target,
                        message_type=MessageType.COMMAND,
                        command="custom",
                        args=[message_text]
                    )
                    success = framework.send_message(target, message)
                
                print(f"✅ Sent to {target}" if success else f"❌ Failed to send to {target}")
            
            elif parts[0].lower() == 'command':
                if len(parts) < 3:
                    print("Usage: command <target> <cmd> [args]")
                    continue
                
                target = parts[1]
                command = parts[2]
                args = parts[3:] if len(parts) > 3 else []
                
                if target == "all":
                    message = Message(
                        sender=framework.agent_id,
                        recipient="all",
                        message_type=MessageType.COMMAND,
                        command=command,
                        args=args
                    )
                    success = framework.broadcast_message(message)
                else:
                    message = Message(
                        sender=framework.agent_id,
                        recipient=target,
                        message_type=MessageType.COMMAND,
                        command=command,
                        args=args
                    )
                    success = framework.send_message(target, message)
                
                print(f"✅ Command '{command}' sent to {target}" if success else f"❌ Failed to send command to {target}")
            
            elif parts[0].lower() == 'status':
                status = framework.get_status()
                print(json.dumps(status, indent=2))
            
            else:
                print("Unknown command. Use: send, command, status, or quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main() 