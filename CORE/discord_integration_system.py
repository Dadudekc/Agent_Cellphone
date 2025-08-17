#!/usr/bin/env python3
"""
Discord Integration System for Agent Updates
===========================================
Enables agents to automatically post updates to Discord channels
about their work progress, achievements, and coordination activities.
"""

import json
import time
import logging
import asyncio
import discord
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from discord.ext import commands, tasks

class DiscordIntegrationSystem:
    """Discord integration system for agent updates and coordination"""
    
    def __init__(self, config_path: str = "config/discord_config.json"):
        self.config_path = Path(config_path)
        self.bot = None
        self.channels = {}
        self.agent_status = {}
        self.coordination_active = False
        
        # Setup logging
        self.setup_logging()
        
        # Load Discord configuration
        self.config = self.load_discord_config()
        
        # Initialize Discord bot
        self.initialize_discord_bot()
    
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
                "beta_transformation": "beta-transformation"
            },
            "auto_mode": {
                "bot_name": "Auto Mode Coordinator",
                "bot_status": "Coordinating Auto Mode operations",
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
                "project_milestones": True
            },
            "commands": {
                "prefix": "!",
                "auto_mode_status": "!status",
                "agent_status": "!agents",
                "coordination_status": "!coordination",
                "project_status": "!projects",
                "help": "!help"
            }
        }
    
    def initialize_discord_bot(self):
        """Initialize Discord bot with intents and commands"""
        try:
            # Setup bot intents
            intents = discord.Intents.default()
            intents.message_content = True
            intents.guilds = True
            intents.messages = True
            
            # Create bot instance
            self.bot = commands.Bot(
                command_prefix=self.config['commands']['prefix'],
                intents=intents,
                help_command=None
            )
            
            # Setup bot events
            self.setup_bot_events()
            
            # Setup bot commands
            self.setup_bot_commands()
            
            self.logger.info("✅ Discord bot initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Error initializing Discord bot: {e}")
    
    def setup_bot_events(self):
        """Setup Discord bot events"""
        @self.bot.event
        async def on_ready():
            self.logger.info(f"🤖 Discord bot logged in as {self.bot.user}")
            await self.bot.change_presence(
                activity=discord.Activity(
                    type=discord.ActivityType.watching,
                    name="Auto Mode operations"
                )
            )
            
            # Start status update loop
            self.status_update_loop.start()
            
            # Post system startup message
            await self.post_system_startup()
        
        @self.bot.event
        async def on_guild_join(guild):
            self.logger.info(f"🎉 Bot joined guild: {guild.name}")
            await self.setup_guild_channels(guild)
    
    def setup_bot_commands(self):
        """Setup Discord bot commands"""
        @self.bot.command(name="status")
        async def auto_mode_status(ctx):
            """Show Auto Mode system status"""
            status_embed = discord.Embed(
                title="🤖 Auto Mode System Status",
                description="Current system status and metrics",
                color=discord.Color.blue()
            )
            
            status_embed.add_field(
                name="System Status",
                value="🟢 ACTIVE",
                inline=True
            )
            
            status_embed.add_field(
                name="Active Agents",
                value=f"🤖 {len(self.agent_status)}",
                inline=True
            )
            
            status_embed.add_field(
                name="Coordination",
                value="🟢 ACTIVE" if self.coordination_active else "🔴 INACTIVE",
                inline=True
            )
            
            await ctx.send(embed=status_embed)
        
        @self.bot.command(name="agents")
        async def agent_status(ctx):
            """Show agent status and activities"""
            if not self.agent_status:
                await ctx.send("📊 No agent activity data available")
                return
            
            agent_embed = discord.Embed(
                title="🤖 Agent Status & Activities",
                description="Current agent status and recent activities",
                color=discord.Color.green()
            )
            
            for agent_id, agent_data in self.agent_status.items():
                status_emoji = "🟢" if agent_data.get('status') == 'ACTIVE' else "🔴"
                agent_embed.add_field(
                    name=f"{status_emoji} {agent_data.get('name', agent_id)}",
                    value=f"**Status:** {agent_data.get('status', 'UNKNOWN')}\n"
                          f"**Activity:** {agent_data.get('current_activity', 'No activity')}\n"
                          f"**Last Update:** {agent_data.get('last_update', 'Never')}",
                    inline=False
                )
            
            await ctx.send(embed=agent_embed)
        
        @self.bot.command(name="projects")
        async def project_status(ctx):
            """Show project status and progress"""
            project_embed = discord.Embed(
                title="📁 Project Status & Progress",
                description="Current project status and transformation progress",
                color=discord.Color.purple()
            )
            
            # This would integrate with the comprehensive Auto Mode system
            project_embed.add_field(
                name="AI Task Organizer",
                value="🟡 Assessment Ready",
                inline=True
            )
            
            project_embed.add_field(
                name="GPT Automation",
                value="🟡 Assessment Ready",
                inline=True
            )
            
            project_embed.add_field(
                name="Stock Portfolio Manager",
                value="🟡 Assessment Ready",
                inline=True
            )
            
            await ctx.send(embed=project_embed)
        
        @self.bot.command(name="help")
        async def help_command(ctx):
            """Show available commands"""
            help_embed = discord.Embed(
                title="❓ Auto Mode Discord Commands",
                description="Available commands for system monitoring and coordination",
                color=discord.Color.blue()
            )
            
            commands_info = self.config['commands']
            for cmd_name, cmd_desc in commands_info.items():
                if cmd_name != 'prefix':
                    help_embed.add_field(
                        name=f"!{cmd_name}",
                        value=cmd_desc,
                        inline=False
                    )
            
            await ctx.send(embed=help_embed)
    
    async def setup_guild_channels(self, guild):
        """Setup required channels in the guild"""
        try:
            channels_config = self.config['channels']
            
            for channel_name, channel_id in channels_config.items():
                # Check if channel exists
                existing_channel = discord.utils.get(guild.channels, name=channel_id)
                
                if not existing_channel:
                    # Create channel
                    if channel_name in ['coordination', 'technical', 'qa', 'community']:
                        channel_type = discord.ChannelType.text
                    else:
                        channel_type = discord.ChannelType.text
                    
                    new_channel = await guild.create_text_channel(
                        name=channel_id,
                        topic=f"Auto Mode {channel_name.replace('_', ' ').title()} channel"
                    )
                    
                    self.logger.info(f"✅ Created channel: {channel_id}")
                    
                    # Send welcome message
                    welcome_embed = discord.Embed(
                        title=f"🎉 Welcome to {channel_id}",
                        description=f"This channel is for Auto Mode {channel_name.replace('_', ' ').title()} activities",
                        color=discord.Color.green()
                    )
                    
                    await new_channel.send(embed=welcome_embed)
                else:
                    self.logger.info(f"✅ Channel already exists: {channel_id}")
                
                # Store channel reference
                self.channels[channel_name] = existing_channel or new_channel
                
        except Exception as e:
            self.logger.error(f"❌ Error setting up guild channels: {e}")
    
    async def post_system_startup(self):
        """Post system startup message to coordination channel"""
        try:
            if 'coordination' in self.channels:
                startup_embed = discord.Embed(
                    title="🚀 Auto Mode System Started",
                    description="Comprehensive Auto Mode system is now active and monitoring all projects",
                    color=discord.Color.green(),
                    timestamp=datetime.utcnow()
                )
                
                startup_embed.add_field(
                    name="System Status",
                    value="🟢 ACTIVE",
                    inline=True
                )
                
                startup_embed.add_field(
                    name="Version",
                    value="2.0.0",
                    inline=True
                )
                
                startup_embed.add_field(
                    name="Features",
                    value="• Repository Assessments\n• Beta Transformation\n• Agent Coordination\n• Auto-Scaling",
                    inline=False
                )
                
                await self.channels['coordination'].send(embed=startup_embed)
                self.logger.info("✅ System startup message posted to Discord")
                
        except Exception as e:
            self.logger.error(f"❌ Error posting startup message: {e}")
    
    async def post_agent_update(self, agent_id: str, update_data: Dict[str, Any]):
        """Post agent update to Discord"""
        try:
            # Determine appropriate channel based on update type
            channel_name = self.get_channel_for_update(update_data)
            
            if channel_name and channel_name in self.channels:
                channel = self.channels[channel_name]
                
                # Create update embed
                update_embed = discord.Embed(
                    title=f"🤖 {agent_id} Update",
                    description=update_data.get('description', 'Agent activity update'),
                    color=self.get_color_for_update_type(update_data.get('type', 'info')),
                    timestamp=datetime.utcnow()
                )
                
                # Add fields based on update type
                if update_data.get('type') == 'work_progress':
                    update_embed.add_field(
                        name="Current Activity",
                        value=update_data.get('activity', 'No activity specified'),
                        inline=False
                    )
                    
                    if 'progress' in update_data:
                        update_embed.add_field(
                            name="Progress",
                            value=f"{update_data['progress']}%",
                            inline=True
                        )
                    
                    if 'milestone' in update_data:
                        update_embed.add_field(
                            name="Milestone",
                            value=update_data['milestone'],
                            inline=True
                        )
                
                elif update_data.get('type') == 'project_update':
                    update_embed.add_field(
                        name="Project",
                        value=update_data.get('project_name', 'Unknown project'),
                        inline=True
                    )
                    
                    update_embed.add_field(
                        name="Status",
                        value=update_data.get('status', 'Unknown status'),
                        inline=True
                    )
                
                elif update_data.get('type') == 'coordination':
                    update_embed.add_field(
                        name="Action",
                        value=update_data.get('action', 'No action specified'),
                        inline=False
                    )
                    
                    if 'target_agent' in update_data:
                        update_embed.add_field(
                            name="Target Agent",
                            value=update_data['target_agent'],
                            inline=True
                        )
                
                # Add timestamp
                update_embed.set_footer(text=f"Agent: {agent_id}")
                
                # Post to Discord
                await channel.send(embed=update_embed)
                
                # Update agent status
                self.agent_status[agent_id] = {
                    'name': agent_id,
                    'status': 'ACTIVE',
                    'current_activity': update_data.get('activity', 'No activity'),
                    'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'last_update_data': update_data
                }
                
                self.logger.info(f"✅ Agent update posted to Discord: {agent_id}")
                
        except Exception as e:
            self.logger.error(f"❌ Error posting agent update: {e}")
    
    def get_channel_for_update(self, update_data: Dict[str, Any]) -> str:
        """Determine appropriate Discord channel for update type"""
        update_type = update_data.get('type', 'info')
        
        channel_mapping = {
            'work_progress': 'agent_updates',
            'project_update': 'project_progress',
            'technical_assessment': 'technical',
            'quality_assurance': 'qa',
            'beta_transformation': 'beta_transformation',
            'coordination': 'coordination',
            'community': 'community',
            'user_support': 'user_support'
        }
        
        return channel_mapping.get(update_type, 'coordination')
    
    def get_color_for_update_type(self, update_type: str) -> int:
        """Get Discord embed color for update type"""
        color_mapping = {
            'work_progress': 0x00ff00,      # Green
            'project_update': 0x9932cc,     # Purple
            'technical_assessment': 0x0066ff, # Blue
            'quality_assurance': 0xff6600,   # Orange
            'beta_transformation': 0xff00ff, # Magenta
            'coordination': 0x0099ff,       # Light Blue
            'community': 0x00cc99,          # Teal
            'user_support': 0xffcc00,       # Yellow
            'error': 0xff0000,              # Red
            'warning': 0xffff00,            # Bright Yellow
            'info': 0xcccccc                # Light Gray
        }
        
        return color_mapping.get(update_type, 0xcccccc)
    
    @tasks.loop(minutes=5)
    async def status_update_loop(self):
        """Periodic status update loop"""
        try:
            if self.coordination_active and 'coordination' in self.channels:
                # Create status summary
                status_embed = discord.Embed(
                    title="📊 Auto Mode Status Summary",
                    description="Periodic system status update",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                
                # Add system metrics
                active_agents = len([a for a in self.agent_status.values() if a.get('status') == 'ACTIVE'])
                total_agents = len(self.agent_status)
                
                status_embed.add_field(
                    name="Agent Status",
                    value=f"🟢 Active: {active_agents}/{total_agents}",
                    inline=True
                )
                
                status_embed.add_field(
                    name="Coordination",
                    value="🟢 ACTIVE" if self.coordination_active else "🔴 INACTIVE",
                    inline=True
                )
                
                # Add recent activities
                recent_activities = []
                for agent_id, agent_data in list(self.agent_status.items())[:3]:
                    activity = agent_data.get('current_activity', 'No activity')
                    recent_activities.append(f"• {agent_id}: {activity}")
                
                if recent_activities:
                    status_embed.add_field(
                        name="Recent Activities",
                        value="\n".join(recent_activities),
                        inline=False
                    )
                
                # Post status update
                await self.channels['coordination'].send(embed=status_embed)
                
        except Exception as e:
            self.logger.error(f"❌ Error in status update loop: {e}")
    
    async def start_bot(self):
        """Start the Discord bot"""
        try:
            token = self.config['token']
            
            if token == "YOUR_DISCORD_BOT_TOKEN_HERE":
                self.logger.error("❌ Please update Discord bot token in config/discord_config.json")
                return False
            
            self.logger.info("🚀 Starting Discord bot...")
            await self.bot.start(token)
            
        except Exception as e:
            self.logger.error(f"❌ Error starting Discord bot: {e}")
            return False
    
    def stop_bot(self):
        """Stop the Discord bot"""
        try:
            if self.bot:
                asyncio.create_task(self.bot.close())
                self.logger.info("🛑 Discord bot stopped")
        except Exception as e:
            self.logger.error(f"❌ Error stopping Discord bot: {e}")
    
    def get_bot_status(self) -> Dict[str, Any]:
        """Get Discord bot status"""
        return {
            "bot_initialized": self.bot is not None,
            "channels_available": len(self.channels),
            "agent_status_count": len(self.agent_status),
            "coordination_active": self.coordination_active,
            "config_loaded": bool(self.config)
        }

# Example usage functions
async def post_agent_work_update(discord_system: DiscordIntegrationSystem, agent_id: str, activity: str, progress: int = None, milestone: str = None):
    """Post agent work progress update"""
    update_data = {
        "type": "work_progress",
        "description": f"Agent {agent_id} work progress update",
        "activity": activity,
        "progress": progress,
        "milestone": milestone
    }
    
    await discord_system.post_agent_update(agent_id, update_data)

async def post_project_update(discord_system: DiscordIntegrationSystem, agent_id: str, project_name: str, status: str, description: str):
    """Post project update"""
    update_data = {
        "type": "project_update",
        "description": description,
        "project_name": project_name,
        "status": status
    }
    
    await discord_system.post_agent_update(agent_id, update_data)

async def post_coordination_update(discord_system: DiscordIntegrationSystem, agent_id: str, action: str, target_agent: str = None, description: str = None):
    """Post coordination update"""
    update_data = {
        "type": "coordination",
        "description": description or f"Coordination action: {action}",
        "action": action,
        "target_agent": target_agent
    }
    
    await discord_system.post_agent_update(agent_id, update_data)

def main():
    """Main function for testing Discord integration"""
    print("🚀 DISCORD INTEGRATION SYSTEM")
    print("=" * 50)
    print("🤖 Discord bot for agent updates and coordination")
    print("📊 Real-time work progress tracking")
    print("🔗 Multi-channel communication")
    print("📈 Automated status updates")
    print("=" * 50)
    
    # Create Discord integration system
    discord_system = DiscordIntegrationSystem()
    
    # Check configuration
    if discord_system.config['token'] == "YOUR_DISCORD_BOT_TOKEN_HERE":
        print("❌ Please update Discord bot token in config/discord_config.json")
        print("📝 Instructions:")
        print("1. Create a Discord application at https://discord.com/developers/applications")
        print("2. Create a bot and copy the token")
        print("3. Update config/discord_config.json with your token")
        print("4. Invite the bot to your Discord server")
        return 1
    
    print("✅ Discord configuration loaded")
    print("🤖 Bot ready to start")
    print("📝 Use discord_system.start_bot() to start the bot")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


