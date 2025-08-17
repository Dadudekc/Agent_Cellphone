import aiohttp
import json
import logging
from datetime import datetime
from typing import Dict, Optional
import asyncio

class DiscordService:
    """Handles Discord webhook integration for agent updates"""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or "YOUR_DISCORD_WEBHOOK_URL"
        self.logger = logging.getLogger("DiscordService")
        self.session = None
        
    async def initialize(self):
        """Initialize HTTP session"""
        if not self.session:
            self.session = aiohttp.ClientSession()
            
    async def cleanup(self):
        """Cleanup HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None
            
    async def post_message(self, message: str, username: str = "Agent-1", avatar_url: Optional[str] = None):
        """Post message to Discord webhook"""
        try:
            await self.initialize()
            
            payload = {
                "content": message,
                "username": username,
                "avatar_url": avatar_url
            }
            
            async with self.session.post(self.webhook_url, json=payload) as response:
                if response.status == 204:
                    self.logger.info("Message posted to Discord successfully")
                    return True
                else:
                    self.logger.error(f"Failed to post to Discord: {response.status}")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Error posting to Discord: {e}")
            return False
            
    async def post_rescue_message(self, agent_id: str, stall_duration: float, last_activity: str):
        """Post rescue message for stalled agent"""
        message = f"🚨 **AGENT STALL DETECTED** 🚨\n"
        message += f"**Agent**: {agent_id}\n"
        message += f"**Stall Duration**: {stall_duration:.0f}s\n"
        message += f"**Last Activity**: {last_activity}\n"
        message += f"**Time**: {datetime.now().isoformat()}\n"
        message += f"**Action Required**: Manual intervention needed"
        
        return await self.post_message(message, username="AgentMonitor")
        
    async def post_work_update(self, agent_id: str, task: str, update: str):
        """Post work update message"""
        message = f"🔄 **WORK UPDATE - {agent_id}**\n"
        message += f"**Task**: {task}\n"
        message += f"**Update**: {update}\n"
        message += f"**Time**: {datetime.now().isoformat()}"
        
        return await self.post_message(message, username=agent_id)
        
    async def post_task_completion(self, agent_id: str, task: str, duration: float):
        """Post task completion message"""
        message = f"✅ **TASK COMPLETED - {agent_id}**\n"
        message += f"**Task**: {task}\n"
        message += f"**Duration**: {duration:.0f}s\n"
        message += f"**Time**: {datetime.now().isoformat()}"
        
        return await self.post_message(message, username=agent_id)
        
    async def post_error_message(self, agent_id: str, error: str, context: str = ""):
        """Post error message"""
        message = f"❌ **ERROR - {agent_id}**\n"
        message += f"**Error**: {error}\n"
        if context:
            message += f"**Context**: {context}\n"
        message += f"**Time**: {datetime.now().isoformat()}"
        
        return await self.post_message(message, username="ErrorMonitor")

# Global Discord service instance
discord_service = DiscordService()

async def post_discord_update(message: str, username: str = "Agent-1"):
    """Convenience function to post Discord updates"""
    return await discord_service.post_message(message, username)

async def post_discord_rescue(agent_id: str, stall_duration: float, last_activity: str):
    """Convenience function to post rescue messages"""
    return await discord_service.post_rescue_message(agent_id, stall_duration, last_activity)



