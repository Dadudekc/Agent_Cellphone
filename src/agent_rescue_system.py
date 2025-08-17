#!/usr/bin/env python3
"""
Agent-1 Rescue System
Prevents stalls and maintains continuous operation with Discord updates
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.continuous_worker import start_agent_continuous_work, stop_agent_continuous_work
from core.agent_monitor import update_agent_activity
from services.discord_service import post_discord_update

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler('logs/agent_rescue_system.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("AgentRescueSystem")

class AgentRescueSystem:
    """Main system for keeping Agent-1 active and monitored"""
    
    def __init__(self):
        self.is_running = False
        self.start_time = None
        
    async def start(self):
        """Start the rescue system"""
        self.is_running = True
        self.start_time = datetime.now()
        
        logger.info("🚀 Starting Agent-1 Rescue System")
        logger.info(f"Start time: {self.start_time}")
        
        # Send startup message to Discord
        try:
            await post_discord_update(
                "🚀 Agent-1 Rescue System started - Continuous monitoring and work active",
                "Agent-1"
            )
        except Exception as e:
            logger.error(f"Failed to send startup Discord message: {e}")
        
        # Start continuous work loop
        try:
            await start_agent_continuous_work()
        except Exception as e:
            logger.error(f"Error in continuous work loop: {e}")
            await self._handle_critical_error(e)
            
    async def _handle_critical_error(self, error: Exception):
        """Handle critical errors and attempt recovery"""
        logger.critical(f"Critical error in rescue system: {error}")
        
        try:
            await post_discord_update(
                f"❌ CRITICAL ERROR in Agent-1 Rescue System: {str(error)}",
                "ErrorMonitor"
            )
        except Exception as e:
            logger.error(f"Failed to send error Discord message: {e}")
            
        # Attempt to restart after delay
        await asyncio.sleep(60)
        if self.is_running:
            logger.info("Attempting to restart rescue system...")
            await self.start()
            
    def stop(self):
        """Stop the rescue system"""
        self.is_running = False
        stop_agent_continuous_work()
        
        if self.start_time:
            runtime = datetime.now() - self.start_time
            logger.info(f"🛑 Agent-1 Rescue System stopped. Runtime: {runtime}")
        
    async def health_check(self):
        """Periodic health check and activity update"""
        while self.is_running:
            try:
                # Update agent activity
                update_agent_activity()
                
                # Log health status
                runtime = datetime.now() - self.start_time if self.start_time else timedelta(0)
                logger.info(f"Health check - System running for {runtime}")
                
                # Wait for next health check
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in health check: {e}")
                await asyncio.sleep(60)

async def main():
    """Main entry point"""
    rescue_system = AgentRescueSystem()
    
    # Setup signal handlers
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        rescue_system.stop()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        # Start rescue system
        await rescue_system.start()
        
        # Start health check in background
        health_task = asyncio.create_task(rescue_system.health_check())
        
        # Keep main loop running
        while rescue_system.is_running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Received keyboard interrupt, shutting down...")
    except Exception as e:
        logger.critical(f"Unexpected error in main: {e}")
    finally:
        rescue_system.stop()
        logger.info("Agent-1 Rescue System shutdown complete")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Failed to start rescue system: {e}")
        sys.exit(1)



