#!/usr/bin/env python3
"""
Inter-Agent Communication Framework
==================================
Advanced messaging system for coordinated agent operations
- Message routing and filtering
- Command handling and execution
- Protocol validation and error handling
- Real-time communication monitoring
"""

import json
import logging
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime

from .agent_cell_phone import AgentCellPhone, MsgTag

# ──────────────────────────── Configuration
# Repository paths
REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = REPO_ROOT / "core" / "runtime" / "config"

# ──────────────────────────── Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("inter_agent_framework")

# ──────────────────────────── Enums and Data Classes
class MessageType(str, Enum):
    """Message types for routing and handling"""
    COMMAND = "COMMAND"
    STATUS = "STATUS"
    DATA = "DATA"
    QUERY = "QUERY"
    RESPONSE = "RESPONSE"
    BROADCAST = "BROADCAST"
    DIRECT = "DIRECT"
    SYSTEM = "SYSTEM"

@dataclass
class Message:
    """Structured message format"""
    sender: str
    recipient: str
    message_type: MessageType
    command: Optional[str] = None
    args: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    message_id: Optional[str] = None

@dataclass
class CommandHandler:
    """Command handler definition"""
    command: str
    handler: Callable
    description: str
    requires_args: bool = False

# ──────────────────────────── Core Framework Class
class InterAgentFramework:
    """Advanced inter-agent communication framework"""
    
    def __init__(self, agent_id: str, layout_mode: str = "4-agent", test: bool = False):
        self.agent_id = agent_id
        self.layout_mode = layout_mode
        self.test_mode = test
        
        # Initialize core components
        self.acp = AgentCellPhone(layout_mode=layout_mode, test=test)
        self.available_agents = self.acp.get_available_agents()
        
        # Message handling
        self.message_queue: List[Message] = []
        self.command_handlers: Dict[str, CommandHandler] = {}
        self.message_history: List[Message] = []
        
        # Communication state
        self.is_active = False
        self.last_activity = datetime.now()
        
        # Register default command handlers
        self._register_default_handlers()
        
        log.info(f"InterAgentFramework initialized for {agent_id} in {layout_mode} mode")
    
    def _register_default_handlers(self):
        """Register default command handlers"""
        handlers = [
            CommandHandler("ping", self._handle_ping, "Ping another agent", False),
            CommandHandler("status", self._handle_status, "Get agent status", False),
            CommandHandler("resume", self._handle_resume, "Resume agent operations", False),
            CommandHandler("sync", self._handle_sync, "Sync with other agents", True),
            CommandHandler("verify", self._handle_verify, "Verify system state", False),
            CommandHandler("task", self._handle_task, "Assign or report task", True),
            CommandHandler("captain", self._handle_captain, "Take command role", False),
        ]
        
        for handler in handlers:
            self.register_command_handler(handler)
    
    def register_command_handler(self, handler: CommandHandler):
        """Register a new command handler"""
        self.command_handlers[handler.command] = handler
        log.debug(f"Registered command handler: {handler.command}")
    
    def send_message(self, recipient: str, message: Message) -> bool:
        """Send a structured message to a specific agent"""
        try:
            # Format message for transmission
            formatted_msg = self._format_message_for_transmission(message)
            
            # Send via AgentCellPhone
            self.acp.send(recipient, formatted_msg)
            
            # Log message
            self.message_history.append(message)
            log.info(f"Sent message to {recipient}: {message.command or 'DATA'}")
            
            return True
            
        except Exception as e:
            log.error(f"Failed to send message to {recipient}: {e}")
            return False
    
    def broadcast_message(self, message: Message) -> bool:
        """Broadcast a message to all agents"""
        try:
            # Format message for transmission
            formatted_msg = self._format_message_for_transmission(message)
            
            # Send via AgentCellPhone
            self.acp.broadcast(formatted_msg)
            
            # Log message
            self.message_history.append(message)
            log.info(f"Broadcast message: {message.command or 'DATA'}")
            
            return True
            
        except Exception as e:
            log.error(f"Failed to broadcast message: {e}")
            return False
    
    def _format_message_for_transmission(self, message: Message) -> str:
        """Format message for transmission via AgentCellPhone"""
        parts = []
        
        # Add message type tag
        if message.message_type == MessageType.COMMAND:
            parts.append(f"[{message.command.upper()}]")
        elif message.message_type == MessageType.STATUS:
            parts.append("[STATUS]")
        elif message.message_type == MessageType.DATA:
            parts.append("[DATA]")
        elif message.message_type == MessageType.QUERY:
            parts.append("[QUERY]")
        elif message.message_type == MessageType.RESPONSE:
            parts.append("[RESPONSE]")
        elif message.message_type == MessageType.SYSTEM:
            parts.append("[SYSTEM]")
        
        # Add recipient if not broadcast
        if message.recipient != "all":
            parts.append(f"@{message.recipient}")
        
        # Add command and args
        if message.command:
            parts.append(message.command)
            parts.extend(message.args)
        
        # Add data if present
        if message.data:
            parts.append(json.dumps(message.data))
        
        return " ".join(parts)
    
    def send_to_agents(self, agent_ids: List[str], message: Message) -> Dict[str, bool]:
        """Send message to specific agents"""
        results = {}
        for agent_id in agent_ids:
            if agent_id in self.available_agents:
                results[agent_id] = self.send_message(agent_id, message)
            else:
                results[agent_id] = False
                log.warning(f"Agent {agent_id} not available")
        return results
    
    # ──────────────────────────── Default Command Handlers
    def _handle_ping(self, message: Message) -> str:
        """Handle ping command"""
        response = Message(
            sender=self.agent_id,
            recipient=message.sender,
            message_type=MessageType.RESPONSE,
            command="pong",
            data={"status": "active", "timestamp": datetime.now().isoformat()}
        )
        self.send_message(message.sender, response)
        return "Ping responded"
    
    def _handle_status(self, message: Message) -> str:
        """Handle status command"""
        status_data = {
            "agent_id": self.agent_id,
            "status": "active" if self.is_active else "inactive",
            "last_activity": self.last_activity.isoformat(),
            "message_count": len(self.message_history),
            "layout_mode": self.layout_mode
        }
        
        response = Message(
            sender=self.agent_id,
            recipient=message.sender,
            message_type=MessageType.RESPONSE,
            command="status",
            data=status_data
        )
        self.send_message(message.sender, response)
        return "Status sent"
    
    def _handle_resume(self, message: Message) -> str:
        """Handle resume command"""
        self.is_active = True
        self.last_activity = datetime.now()
        log.info(f"Agent {self.agent_id} resumed operations")
        return "Resumed operations"
    
    def _handle_sync(self, message: Message) -> str:
        """Handle sync command"""
        sync_data = message.data if message.data else {}
        log.info(f"Syncing with data: {sync_data}")
        return "Sync completed"
    
    def _handle_verify(self, message: Message) -> str:
        """Handle verify command"""
        verification_data = {
            "agent_id": self.agent_id,
            "framework_version": "1.0.0",
            "components": ["AgentCellPhone", "InterAgentFramework"],
            "status": "verified"
        }
        
        response = Message(
            sender=self.agent_id,
            recipient=message.sender,
            message_type=MessageType.RESPONSE,
            command="verify",
            data=verification_data
        )
        self.send_message(message.sender, response)
        return "Verification completed"
    
    def _handle_task(self, message: Message) -> str:
        """Handle task command"""
        task_description = " ".join(message.args) if message.args else "No task specified"
        log.info(f"Received task: {task_description}")
        return f"Task received: {task_description}"
    
    def _handle_captain(self, message: Message) -> str:
        """Handle captain command"""
        log.info(f"Agent {self.agent_id} taking captain role")
        return "Captain role activated"
    
    # ──────────────────────────── Utility Methods
    def get_status(self) -> Dict[str, Any]:
        """Get current framework status"""
        return {
            "agent_id": self.agent_id,
            "layout_mode": self.layout_mode,
            "is_active": self.is_active,
            "last_activity": self.last_activity.isoformat(),
            "message_count": len(self.message_history),
            "available_agents": self.available_agents,
            "registered_commands": list(self.command_handlers.keys())
        }
    
    def get_message_history(self, limit: Optional[int] = None) -> List[Message]:
        """Get message history, optionally limited to recent messages"""
        if limit:
            return self.message_history[-limit:]
        return self.message_history.copy()
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents in current layout mode"""
        return self.available_agents.copy()

# ──────────────────────────── CLI Interface
def main():
    """CLI interface for the inter-agent framework"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Inter-Agent Communication Framework")
    parser.add_argument("--agent", required=True, help="Agent ID")
    parser.add_argument("--layout", default="4-agent", help="Layout mode")
    parser.add_argument("--test", action="store_true", help="Test mode")
    parser.add_argument("--command", help="Command to execute")
    parser.add_argument("--target", help="Target agent(s)")
    parser.add_argument("--args", nargs="*", help="Command arguments")
    parser.add_argument("--status", action="store_true", help="Show status")
    parser.add_argument("--interactive", action="store_true", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Initialize framework
    framework = InterAgentFramework(args.agent, args.layout, args.test)
    
    if args.status:
        status = framework.get_status()
        print(json.dumps(status, indent=2))
        return
    
    if args.interactive:
        print(f"🎮 Interactive mode for {args.agent}")
        print("Commands: send <agent> <message>, broadcast <message>, status, quit")
        
        while True:
            try:
                cmd = input(f"iaf[{args.agent}]> ").strip()
                
                if cmd.lower() in ['quit', 'exit', 'q']:
                    break
                
                parts = cmd.split()
                if len(parts) < 2:
                    print("Usage: send <agent> <message>, broadcast <message>, status, or quit")
                    continue
                
                if parts[0].lower() == 'send':
                    if len(parts) < 3:
                        print("Usage: send <agent> <message>")
                        continue
                    target = parts[1]
                    message_text = ' '.join(parts[2:])
                    
                    message = Message(
                        sender=args.agent,
                        recipient=target,
                        message_type=MessageType.COMMAND,
                        command="custom",
                        args=[message_text]
                    )
                    
                    success = framework.send_message(target, message)
                    print(f"✅ Sent to {target}" if success else f"❌ Failed to send to {target}")
                
                elif parts[0].lower() == 'broadcast':
                    message_text = ' '.join(parts[1:])
                    
                    message = Message(
                        sender=args.agent,
                        recipient="all",
                        message_type=MessageType.BROADCAST,
                        command="broadcast",
                        args=[message_text]
                    )
                    
                    success = framework.broadcast_message(message)
                    print("✅ Broadcast sent" if success else "❌ Broadcast failed")
                
                elif parts[0].lower() == 'status':
                    status = framework.get_status()
                    print(json.dumps(status, indent=2))
                
                else:
                    print("Unknown command. Use: send, broadcast, status, or quit")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    elif args.command:
        # Execute single command
        if not args.target:
            print("❌ --target required for command execution")
            return
        
        message = Message(
            sender=args.agent,
            recipient=args.target,
            message_type=MessageType.COMMAND,
            command=args.command,
            args=args.args or []
        )
        
        success = framework.send_message(args.target, message)
        print(f"✅ Command sent" if success else "❌ Command failed")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
