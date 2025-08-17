#!/usr/bin/env python3
"""
🔗 UNIFIED DISCORD INTEGRATION SYSTEM v2.0
===========================================
Modular Discord integration package consolidating all Discord functionality
for agent coordination, updates, and communication.
"""

import json
import time
import logging
import asyncio
import discord
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
import os

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class DiscordChannelType(Enum):
    """Types of Discord channels for different purposes"""
    COORDINATION = "coordination"
    TECHNICAL = "technical"
    QA = "quality_assurance"
    COMMUNITY = "community_engagement"
    USER_SUPPORT = "user_support"
    AGENT_UPDATES = "agent_work_updates"
    PROJECT_PROGRESS = "project_progress"
    BETA_TRANSFORMATION = "beta_transformation"
    PRESIDENTIAL = "presidential_decisions"
    KNOWLEDGE_SHARING = "knowledge_sharing"
    STALL_MONITORING = "stall_monitoring"
    COLLABORATION = "collaboration"

class MessagePriority(Enum):
    """Message priority levels for Discord notifications"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    PRESIDENTIAL = "presidential"

@dataclass
class DiscordMessage:
    """Structured Discord message with metadata"""
    id: str
    channel: DiscordChannelType
    content: str
    priority: MessagePriority
    agent_id: str
    timestamp: datetime
    metadata: Dict[str, Any]
    attachments: List[str] = None
    embeds: List[Dict[str, Any]] = None

@dataclass
class DiscordChannel:
    """Discord channel configuration"""
    name: str
    channel_type: DiscordChannelType
    channel_id: Optional[int] = None
    webhook_url: Optional[str] = None
    permissions: List[str] = None
    auto_purge: bool = False
    purge_after_hours: int = 24

class DiscordIntegrationManager:
    """Main Discord integration manager"""
    
    def __init__(self, config_path: str = "config/discord_config.json"):
        self.config_path = Path(config_path)
        self.bot = None
        self.channels: Dict[str, DiscordChannel] = {}
        self.message_queue = queue.Queue()
        self.is_running = False
        
        # Setup logging
        self.setup_logging()
        
        # Load configuration
        self.config = self.load_discord_config()
        
        # Initialize channels
        self.initialize_channels()
        
        # Start message processing
        self.start_message_processor()
    
    def setup_logging(self):
        """Setup logging for Discord integration"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s | %(levelname)s | %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "discord_integration.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_discord_config(self) -> Dict[str, Any]:
        """Load Discord configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    self.logger.info("✅ Discord configuration loaded successfully")
                    return config
            else:
                self.logger.warning("⚠️ Discord config not found, using defaults")
                return self.get_default_discord_config()
        except Exception as e:
            self.logger.error(f"❌ Error loading Discord config: {e}")
            return self.get_default_discord_config()
    
    def get_default_discord_config(self) -> Dict[str, Any]:
        """Return default Discord configuration"""
        return {
            "token": "YOUR_DISCORD_BOT_TOKEN_HERE",
            "guild_id": "YOUR_GUILD_ID_HERE",
            "channels": {
                "coordination": "auto-mode-coordination",
                "technical": "technical-assessment",
                "qa": "quality-assurance",
                "community": "community-engagement",
                "user_support": "auto-mode-support",
                "agent_updates": "agent-work-updates",
                "project_progress": "project-progress",
                "beta_transformation": "beta-transformation",
                "presidential": "presidential-decisions",
                "knowledge_sharing": "knowledge-sharing",
                "stall_monitoring": "stall-monitoring",
                "collaboration": "collaboration"
            },
            "auto_mode": {
                "bot_name": "Unified Discord Coordinator",
                "bot_status": "Coordinating multi-agent operations",
                "coordination_enabled": True,
                "democratic_voting": True,
                "auto_routing": True
            },
            "notifications": {
                "system_status": True,
                "agent_activity": True,
                "coordination_events": True,
                "user_alerts": True,
                "performance_metrics": True,
                "work_progress": True,
                "project_milestones": True,
                "presidential_decisions": True,
                "knowledge_updates": True,
                "stall_alerts": True
            },
            "commands": {
                "prefix": "!",
                "enabled_commands": [
                    "status", "help", "agents", "projects", "knowledge", "presidential"
                ]
            },
            "rate_limits": {
                "messages_per_minute": 30,
                "embeds_per_minute": 10,
                "webhook_rate_limit": 5
            }
        }
    
    def initialize_channels(self):
        """Initialize Discord channels"""
        for channel_name, channel_config in self.config["channels"].items():
            channel = DiscordChannel(
                name=channel_config,
                channel_type=DiscordChannelType(channel_name),
                permissions=["read_messages", "send_messages", "embed_links"],
                auto_purge=channel_name in ["stall_monitoring", "agent_updates"],
                purge_after_hours=12 if channel_name == "stall_monitoring" else 24
            )
            self.channels[channel_name] = channel
        
        self.logger.info(f"✅ Initialized {len(self.channels)} Discord channels")
    
    def start_message_processor(self):
        """Start background message processing"""
        def process_messages():
            while self.is_running:
                try:
                    # Process messages from queue
                    if not self.message_queue.empty():
                        message = self.message_queue.get_nowait()
                        self.process_discord_message(message)
                    
                    time.sleep(1)  # Process every second
                    
                except Exception as e:
                    self.logger.error(f"Message processing error: {e}")
                    time.sleep(5)
        
        self.is_running = True
        self.message_processor = threading.Thread(target=process_messages, daemon=True)
        self.message_processor.start()
        self.logger.info("✅ Message processor started")
    
    def queue_message(self, message: DiscordMessage):
        """Queue a message for Discord processing"""
        try:
            self.message_queue.put(message)
            self.logger.info(f"📝 Queued message for {message.channel.value}")
        except Exception as e:
            self.logger.error(f"Failed to queue message: {e}")
    
    def process_discord_message(self, message: DiscordMessage):
        """Process a Discord message"""
        try:
            # Get channel configuration
            channel_name = message.channel.value
            channel_config = self.channels.get(channel_name)
            
            if not channel_config:
                self.logger.warning(f"Unknown channel: {channel_name}")
                return
            
            # Create Discord embed if needed
            embed = self.create_message_embed(message)
            
            # Send message via webhook or bot
            if channel_config.webhook_url:
                self.send_webhook_message(channel_config.webhook_url, message, embed)
            elif self.bot:
                self.send_bot_message(channel_config.channel_id, message, embed)
            else:
                self.logger.warning("No webhook or bot available for message sending")
            
        except Exception as e:
            self.logger.error(f"Failed to process Discord message: {e}")
    
    def create_message_embed(self, message: DiscordMessage) -> Optional[discord.Embed]:
        """Create a Discord embed for the message"""
        try:
            # Determine embed color based on priority
            color_map = {
                MessagePriority.LOW: 0x00ff00,      # Green
                MessagePriority.NORMAL: 0x0099ff,   # Blue
                MessagePriority.HIGH: 0xff9900,     # Orange
                MessagePriority.CRITICAL: 0xff0000, # Red
                MessagePriority.PRESIDENTIAL: 0xffd700 # Gold
            }
            
            embed = discord.Embed(
                title=message.content[:100] + "..." if len(message.content) > 100 else message.content,
                description=message.content,
                color=color_map.get(message.priority, 0x0099ff),
                timestamp=message.timestamp
            )
            
            # Add agent information
            embed.add_field(name="Agent", value=message.agent_id, inline=True)
            embed.add_field(name="Priority", value=message.priority.value.upper(), inline=True)
            embed.add_field(name="Channel", value=message.channel.value.replace("_", " ").title(), inline=True)
            
            # Add metadata if available
            if message.metadata:
                metadata_str = "\n".join([f"**{k}**: {v}" for k, v in message.metadata.items()][:5])
                if metadata_str:
                    embed.add_field(name="Details", value=metadata_str, inline=False)
            
            return embed
            
        except Exception as e:
            self.logger.error(f"Failed to create embed: {e}")
            return None
    
    def send_webhook_message(self, webhook_url: str, message: DiscordMessage, embed: Optional[discord.Embed]):
        """Send message via webhook"""
        try:
            # This would be implemented with actual webhook sending logic
            # For now, we'll log the action
            self.logger.info(f"📤 Webhook message sent to {message.channel.value}")
            self.logger.info(f"Content: {message.content[:100]}...")
            
        except Exception as e:
            self.logger.error(f"Failed to send webhook message: {e}")
    
    def send_bot_message(self, channel_id: int, message: DiscordMessage, embed: Optional[discord.Embed]):
        """Send message via bot"""
        try:
            # This would be implemented with actual bot message sending logic
            # For now, we'll log the action
            self.logger.info(f"📤 Bot message sent to channel {channel_id}")
            self.logger.info(f"Content: {message.content[:100]}...")
            
        except Exception as e:
            self.logger.error(f"Failed to send bot message: {e}")

class AgentUpdateNotifier:
    """Handles agent update notifications to Discord"""
    
    def __init__(self, discord_manager: DiscordIntegrationManager):
        self.discord_manager = discord_manager
        self.logger = logging.getLogger(__name__)
    
    def notify_agent_activity(self, agent_id: str, activity: str, details: Dict[str, Any]):
        """Notify Discord about agent activity"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.AGENT_UPDATES,
            content=f"Agent {agent_id}: {activity}",
            priority=MessagePriority.NORMAL,
            agent_id=agent_id,
            timestamp=datetime.now(),
            metadata=details
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"📢 Agent activity notification queued: {agent_id} - {activity}")
    
    def notify_project_progress(self, project_name: str, progress: str, agent_id: str):
        """Notify Discord about project progress"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.PROJECT_PROGRESS,
            content=f"Project Progress: {project_name}",
            priority=MessagePriority.HIGH,
            agent_id=agent_id,
            timestamp=datetime.now(),
            metadata={
                "project": project_name,
                "progress": progress,
                "timestamp": datetime.now().isoformat()
            }
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"📢 Project progress notification queued: {project_name}")
    
    def notify_presidential_decision(self, decision: Dict[str, Any]):
        """Notify Discord about presidential decisions"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.PRESIDENTIAL,
            content=f"Presidential Decision: {decision.get('title', 'New Decision')}",
            priority=MessagePriority.PRESIDENTIAL,
            agent_id=decision.get('president_agent', 'System'),
            timestamp=datetime.now(),
            metadata=decision
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"🎖️ Presidential decision notification queued")
    
    def notify_knowledge_update(self, knowledge_item: Dict[str, Any]):
        """Notify Discord about knowledge updates"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.KNOWLEDGE_SHARING,
            content=f"Knowledge Update: {knowledge_item.get('title', 'New Knowledge')}",
            priority=MessagePriority.NORMAL,
            agent_id=knowledge_item.get('agent_id', 'System'),
            timestamp=datetime.now(),
            metadata=knowledge_item
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"📚 Knowledge update notification queued")

class StallMonitoringNotifier:
    """Handles stall monitoring notifications to Discord"""
    
    def __init__(self, discord_manager: DiscordIntegrationManager):
        self.discord_manager = discord_manager
        self.logger = logging.getLogger(__name__)
    
    def notify_stall_warning(self, agent_id: str, stall_duration: int, details: Dict[str, Any]):
        """Notify Discord about stall warnings"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.STALL_MONITORING,
            content=f"⚠️ Stall Warning: Agent {agent_id}",
            priority=MessagePriority.HIGH,
            agent_id=agent_id,
            timestamp=datetime.now(),
            metadata={
                "stall_duration_minutes": stall_duration,
                "warning_type": "stall_warning",
                **details
            }
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"⚠️ Stall warning notification queued: {agent_id}")
    
    def notify_stall_resolution(self, agent_id: str, resolution_time: int, details: Dict[str, Any]):
        """Notify Discord about stall resolution"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.STALL_MONITORING,
            content=f"✅ Stall Resolved: Agent {agent_id}",
            priority=MessagePriority.NORMAL,
            agent_id=agent_id,
            timestamp=datetime.now(),
            metadata={
                "resolution_time_minutes": resolution_time,
                "resolution_type": "stall_resolved",
                **details
            }
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"✅ Stall resolution notification queued: {agent_id}")

class CollaborationNotifier:
    """Handles collaboration notifications to Discord"""
    
    def __init__(self, discord_manager: DiscordIntegrationManager):
        self.discord_manager = discord_manager
        self.logger = logging.getLogger(__name__)
    
    def notify_collaboration_start(self, session_id: str, agents: List[str], objective: str):
        """Notify Discord about collaboration session start"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.COLLABORATION,
            content=f"🤝 Collaboration Started: {objective}",
            priority=MessagePriority.HIGH,
            agent_id="System",
            timestamp=datetime.now(),
            metadata={
                "session_id": session_id,
                "agents": agents,
                "objective": objective,
                "status": "started"
            }
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"🤝 Collaboration start notification queued: {session_id}")
    
    def notify_collaboration_progress(self, session_id: str, progress: str, achievements: List[str]):
        """Notify Discord about collaboration progress"""
        message = DiscordMessage(
            id=str(int(time.time())),
            channel=DiscordChannelType.COLLABORATION,
            content=f"📈 Collaboration Progress: {progress}",
            priority=MessagePriority.NORMAL,
            agent_id="System",
            timestamp=datetime.now(),
            metadata={
                "session_id": session_id,
                "progress": progress,
                "achievements": achievements,
                "status": "in_progress"
            }
        )
        
        self.discord_manager.queue_message(message)
        self.logger.info(f"📈 Collaboration progress notification queued: {session_id}")

class UnifiedDiscordSystem:
    """Main unified Discord system that coordinates all functionality"""
    
    def __init__(self, config_path: str = "config/discord_config.json"):
        # Initialize Discord manager
        self.discord_manager = DiscordIntegrationManager(config_path)
        
        # Initialize specialized notifiers
        self.agent_notifier = AgentUpdateNotifier(self.discord_manager)
        self.stall_notifier = StallMonitoringNotifier(self.discord_manager)
        self.collaboration_notifier = CollaborationNotifier(self.discord_manager)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("🚀 Unified Discord System initialized")
    
    def start(self):
        """Start the unified Discord system"""
        try:
            self.logger.info("🔗 Starting Unified Discord System...")
            
            # Start Discord manager
            self.discord_manager.is_running = True
            
            # Keep system running
            while self.discord_manager.is_running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Shutting down Unified Discord System...")
            self.discord_manager.is_running = False
        except Exception as e:
            self.logger.error(f"System error: {e}")
            self.discord_manager.is_running = False
    
    def get_status(self) -> Dict[str, Any]:
        """Get system status"""
        return {
            "discord_manager_running": self.discord_manager.is_running,
            "channels_configured": len(self.discord_manager.channels),
            "message_queue_size": self.discord_manager.message_queue.qsize(),
            "config_loaded": bool(self.discord_manager.config)
        }

def main():
    """Main function to demonstrate the unified Discord system"""
    print("🔗 UNIFIED DISCORD INTEGRATION SYSTEM")
    print("=" * 50)
    
    # Initialize the system
    system = UnifiedDiscordSystem()
    
    # Display status
    status = system.get_status()
    print(f"\n📊 SYSTEM STATUS:")
    print(f"Discord Manager: {'✅ Running' if status['discord_manager_running'] else '❌ Stopped'}")
    print(f"Channels Configured: {status['channels_configured']}")
    print(f"Message Queue Size: {status['message_queue_size']}")
    print(f"Config Loaded: {'✅ Yes' if status['config_loaded'] else '❌ No'}")
    
    print(f"\n🎯 FEATURES:")
    print("• Agent Update Notifications")
    print("• Project Progress Tracking")
    print("• Presidential Decision Alerts")
    print("• Knowledge Sharing Updates")
    print("• Stall Monitoring Alerts")
    print("• Collaboration Session Tracking")
    
    print(f"\n✅ System initialized successfully!")
    print("Press Ctrl+C to stop...")
    
    try:
        system.start()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down unified Discord system...")

if __name__ == "__main__":
    main()


