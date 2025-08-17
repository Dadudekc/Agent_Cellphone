import time
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
import aiohttp

class AgentStallDetector:
    """Detects when agents stall and sends rescue messages"""
    
    def __init__(self, agent_id: str, check_interval: int = 300):
        self.agent_id = agent_id
        self.check_interval = check_interval  # 5 minutes default
        self.last_activity = datetime.now()
        self.stall_threshold = 600  # 10 minutes
        self.rescue_messages_sent = []
        self.is_monitoring = False
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"AgentMonitor-{agent_id}")
        
    def update_activity(self):
        """Update last activity timestamp"""
        self.last_activity = datetime.now()
        self.logger.info(f"Activity updated: {self.last_activity}")
        
    def is_stalled(self) -> bool:
        """Check if agent has stalled"""
        time_since_activity = (datetime.now() - self.last_activity).total_seconds()
        return time_since_activity > self.stall_threshold
        
    async def send_rescue_message(self, message: str):
        """Send rescue message to Discord and other channels"""
        timestamp = datetime.now().isoformat()
        rescue_data = {
            "agent_id": self.agent_id,
            "timestamp": timestamp,
            "message": message,
            "stall_duration": (datetime.now() - self.last_activity).total_seconds()
        }
        
        # Log rescue message
        self.logger.warning(f"RESCUE MESSAGE SENT: {message}")
        self.rescue_messages_sent.append(rescue_data)
        
        # Send to Discord (placeholder for actual Discord integration)
        await self._post_to_discord(rescue_data)
        
        # Save to rescue log
        self._save_rescue_log(rescue_data)
        
    async def _post_to_discord(self, rescue_data: Dict):
        """Post rescue message to Discord"""
        try:
            # Discord webhook integration would go here
            webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
            message = f"🚨 **AGENT STALL DETECTED** 🚨\n"
            message += f"**Agent**: {rescue_data['agent_id']}\n"
            message += f"**Stall Duration**: {rescue_data['stall_duration']:.0f}s\n"
            message += f"**Message**: {rescue_data['message']}\n"
            message += f"**Time**: {rescue_data['timestamp']}"
            
            # For now, just log the message
            self.logger.info(f"Discord message prepared: {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to post to Discord: {e}")
            
    def _save_rescue_log(self, rescue_data: Dict):
        """Save rescue message to log file"""
        try:
            log_file = f"logs/rescue_messages_{self.agent_id}.json"
            with open(log_file, 'a') as f:
                f.write(json.dumps(rescue_data) + '\n')
        except Exception as e:
            self.logger.error(f"Failed to save rescue log: {e}")
            
    async def start_monitoring(self):
        """Start continuous monitoring"""
        self.is_monitoring = True
        self.logger.info(f"Starting stall monitoring for {self.agent_id}")
        
        while self.is_monitoring:
            if self.is_stalled():
                await self.send_rescue_message(
                    f"Agent {self.agent_id} appears stalled. "
                    f"Last activity: {self.last_activity.isoformat()}"
                )
            
            # Wait before next check
            await asyncio.sleep(self.check_interval)
            
    def stop_monitoring(self):
        """Stop monitoring"""
        self.is_monitoring = False
        self.logger.info(f"Stopped monitoring for {self.agent_id}")

class ContinuousWorkTracker:
    """Tracks continuous work and posts updates"""
    
    def __init__(self, agent_id: str, update_interval: int = 1800):  # 30 minutes
        self.agent_id = agent_id
        self.update_interval = update_interval
        self.work_sessions = []
        self.current_session = None
        
    def start_work_session(self, task_description: str):
        """Start a new work session"""
        self.current_session = {
            "start_time": datetime.now(),
            "task": task_description,
            "updates": []
        }
        self.logger.info(f"Started work session: {task_description}")
        
    def add_update(self, update: str):
        """Add work update"""
        if self.current_session:
            timestamp = datetime.now()
            self.current_session["updates"].append({
                "timestamp": timestamp.isoformat(),
                "update": update
            })
            self.logger.info(f"Work update: {update}")
            
    def end_work_session(self):
        """End current work session"""
        if self.current_session:
            self.current_session["end_time"] = datetime.now()
            self.work_sessions.append(self.current_session)
            self.logger.info(f"Ended work session: {self.current_session['task']}")
            self.current_session = None
            
    async def post_work_update(self, update: str):
        """Post work update to Discord"""
        try:
            message = f"🔄 **WORK UPDATE - {self.agent_id}**\n"
            message += f"**Task**: {self.current_session['task'] if self.current_session else 'No active task'}\n"
            message += f"**Update**: {update}\n"
            message += f"**Time**: {datetime.now().isoformat()}"
            
            # For now, just log the message
            self.logger.info(f"Discord work update prepared: {message}")
            
        except Exception as e:
            self.logger.error(f"Failed to post work update: {e}")

# Global instances for Agent-1
stall_detector = AgentStallDetector("Agent-1")
work_tracker = ContinuousWorkTracker("Agent-1")

def update_agent_activity():
    """Call this function to update agent activity"""
    stall_detector.update_activity()

def start_agent_monitoring():
    """Start the monitoring system"""
    asyncio.create_task(stall_detector.start_monitoring())

def log_work_update(update: str):
    """Log a work update"""
    work_tracker.add_update(update)
    update_agent_activity()  # This also updates activity timestamp



