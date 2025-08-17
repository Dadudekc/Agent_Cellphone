import asyncio
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import random

from .agent_monitor import update_agent_activity, log_work_update, start_agent_monitoring
from services.discord_service import post_discord_update, post_discord_rescue

class ContinuousWorker:
    """Keeps Agent-1 continuously working and posting updates"""
    
    def __init__(self, agent_id: str = "Agent-1"):
        self.agent_id = agent_id
        self.is_running = False
        self.work_interval = 300  # 5 minutes between work updates
        self.discord_interval = 1800  # 30 minutes between Discord posts
        self.last_discord_update = datetime.now()
        self.work_tasks = self._initialize_work_tasks()
        self.current_task_index = 0
        self.work_sessions = []
        self.current_session = None
        
        # Setup logging
        self.logger = logging.getLogger(f"ContinuousWorker-{agent_id}")
        
    def _initialize_work_tasks(self) -> List[Dict]:
        """Initialize list of work tasks to cycle through"""
        return [
            {
                "name": "System Coordination",
                "description": "Coordinate system-wide activities and agent communications",
                "actions": [
                    "Review agent status and task assignments",
                    "Coordinate cross-agent dependencies",
                    "Monitor system health and performance",
                    "Update project timelines and milestones"
                ]
            },
            {
                "name": "Project Management",
                "description": "Manage active projects and task assignments",
                "actions": [
                    "Review project progress and blockers",
                    "Assign new tasks to available agents",
                    "Update project status and documentation",
                    "Coordinate with stakeholders and team members"
                ]
            },
            {
                "name": "Communication Management",
                "description": "Manage internal and external communications",
                "actions": [
                    "Monitor communication channels",
                    "Facilitate agent-to-agent communications",
                    "Update external stakeholders",
                    "Maintain communication protocols"
                ]
            },
            {
                "name": "System Monitoring",
                "description": "Monitor system health and performance",
                "actions": [
                    "Check system resource usage",
                    "Monitor agent performance metrics",
                    "Identify potential issues and bottlenecks",
                    "Update system status and health reports"
                ]
            },
            {
                "name": "Task Coordination",
                "description": "Coordinate task execution and dependencies",
                "actions": [
                    "Review task dependencies and blockers",
                    "Coordinate task handoffs between agents",
                    "Update task status and progress",
                    "Resolve task conflicts and issues"
                ]
            }
        ]
        
    async def start_continuous_work(self):
        """Start the continuous work loop"""
        self.is_running = True
        self.logger.info(f"Starting continuous work loop for {self.agent_id}")
        
        # Start stall monitoring
        start_agent_monitoring()
        
        # Start work loop
        while self.is_running:
            try:
                # Update agent activity
                update_agent_activity()
                
                # Perform current work task
                await self._perform_work_task()
                
                # Post Discord update if interval has passed
                await self._check_discord_update()
                
                # Wait before next work cycle
                await asyncio.sleep(self.work_interval)
                
            except Exception as e:
                self.logger.error(f"Error in continuous work loop: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
                
    async def _perform_work_task(self):
        """Perform the current work task"""
        if not self.work_tasks:
            return
            
        current_task = self.work_tasks[self.current_task_index]
        self.logger.info(f"Performing work task: {current_task['name']}")
        
        # Log work update
        log_work_update(f"Working on: {current_task['description']}")
        
        # Simulate work actions
        for action in current_task['actions']:
            self.logger.info(f"Action: {action}")
            log_work_update(f"Completed: {action}")
            await asyncio.sleep(2)  # Simulate work time
            
        # Move to next task
        self.current_task_index = (self.current_task_index + 1) % len(self.work_tasks)
        
    async def _check_discord_update(self):
        """Check if it's time to post a Discord update"""
        now = datetime.now()
        if (now - self.last_discord_update).total_seconds() >= self.discord_interval:
            await self._post_discord_update()
            self.last_discord_update = now
            
    async def _post_discord_update(self):
        """Post work update to Discord"""
        try:
            current_task = self.work_tasks[self.current_task_index]
            update_message = f"Currently working on: {current_task['name']} - {current_task['description']}"
            
            await post_discord_update(update_message, self.agent_id)
            self.logger.info("Posted Discord update successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to post Discord update: {e}")
            
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
            
    def stop_continuous_work(self):
        """Stop the continuous work loop"""
        self.is_running = False
        self.logger.info(f"Stopped continuous work loop for {self.agent_id}")
        
    async def cleanup(self):
        """Cleanup resources"""
        try:
            from services.discord_service import discord_service
            await discord_service.cleanup()
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
        
    async def emergency_rescue(self, reason: str):
        """Send emergency rescue message"""
        try:
            await post_discord_rescue(
                self.agent_id,
                time.time(),
                f"Emergency rescue triggered: {reason}"
            )
            self.logger.warning(f"Emergency rescue message sent: {reason}")
        except Exception as e:
            self.logger.error(f"Failed to send emergency rescue: {e}")

# Global continuous worker instance
continuous_worker = ContinuousWorker("Agent-1")

async def start_agent_continuous_work():
    """Start Agent-1's continuous work loop"""
    await continuous_worker.start_continuous_work()
    
def stop_agent_continuous_work():
    """Stop Agent-1's continuous work loop"""
    continuous_worker.stop_continuous_work()
    
async def trigger_emergency_rescue(reason: str):
    """Trigger emergency rescue for Agent-1"""
    await continuous_worker.emergency_rescue(reason)
