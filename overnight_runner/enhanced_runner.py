#!/usr/bin/env python3
"""
Enhanced Overnight Runner with FSM Integration

This runner provides enhanced functionality including:
- FSM orchestration
- Advanced task management
- Configurable paths
- Progress tracking
"""

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

# Ensure package root and src/ are on path for direct script execution
_THIS = Path(__file__).resolve()
sys.path.insert(0, str(_THIS.parents[1]))
sys.path.insert(0, str(_THIS.parents[1] / 'src'))

from src.core.config import get_owner_path, get_repos_root  # type: ignore
from src.services.agent_cell_phone import AgentCellPhone, MsgTag  # type: ignore


class EnhancedRunner:
    """Enhanced runner with FSM integration and configurable paths."""
    
    def __init__(self, 
                 agents: List[str],
                 fsm_enabled: bool = True,
                 repos_root: str = str(get_owner_path())):
        self.agents = agents
        self.fsm_enabled = fsm_enabled
        self.repos_root = repos_root
        self.acp = None  # Will be initialized when needed
        
    def initialize_acp(self, coords_file: str, test_mode: bool = False):
        """Initialize the Agent Cell Phone."""
        try:
            self.acp = AgentCellPhone(coords_file, test_mode=test_mode)
            print(f"✅ ACP initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize ACP: {e}")
            return False
        return True
    
    def run_fsm_cycle(self) -> Dict:
        """Run one FSM cycle and return status."""
        if not self.fsm_enabled:
            return {"error": "FSM not enabled"}
        
        try:
            # Simple FSM cycle for now
            return {
                "updates_processed": 0,
                "status": {"total_tasks": 0, "completed_tasks": 0, "in_progress_tasks": 0}
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def send_agent_message(self, agent: str, message: str, tag: MsgTag = MsgTag.TASK) -> bool:
        """Send a message to a specific agent."""
        if not self.acp:
            print("❌ ACP not initialized")
            return False
        
        try:
            self.acp.send(agent, message, tag)
            print(f"✅ Message sent to {agent}")
            return True
        except Exception as e:
            print(f"❌ Failed to send message to {agent}: {e}")
            return False
    
    def run_continuous_cycle(self, interval_seconds: int = 300, max_cycles: int = None):
        """Run continuous cycles with FSM integration."""
        print(f"🚀 Starting Enhanced Runner with FSM")
        print(f"📁 Repos Root: {self.repos_root}")
        print(f"🤖 Agents: {', '.join(self.agents)}")
        print(f"⚙️  FSM Enabled: {self.fsm_enabled}")
        print(f"⏱️  Cycle Interval: {interval_seconds}s")
        print()
        
        cycle = 0
        try:
            while max_cycles is None or cycle < max_cycles:
                cycle += 1
                print(f"\n🔄 Cycle {cycle}")
                print("=" * 50)
                
                # Run FSM cycle
                if self.fsm_enabled:
                    fsm_result = self.run_fsm_cycle()
                    if "error" in fsm_result:
                        print(f"⚠️  FSM Error: {fsm_result['error']}")
                    else:
                        print(f"✅ FSM: {fsm_result['updates_processed']} updates processed")
                        print(f"📊 Status: {fsm_result['status']}")
                
                # Send status messages to agents
                for agent in self.agents:
                    status_msg = f"🤖 {agent} status check - Cycle {cycle}"
                    self.send_agent_message(agent, status_msg, MsgTag.SYNC)
                    time.sleep(1)  # Small delay between agents
                
                print(f"⏳ Waiting {interval_seconds}s until next cycle...")
                time.sleep(interval_seconds)
                
        except KeyboardInterrupt:
            print(f"\n⏹️  Enhanced Runner stopped by user")
        except Exception as e:
            print(f"\n❌ Enhanced Runner error: {e}")
        finally:
            print(f"🏁 Enhanced Runner completed {cycle} cycles")


def main():
    """Main entry point for enhanced runner."""
    parser = argparse.ArgumentParser(
        description="Enhanced Overnight Runner with FSM Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Core arguments
    parser.add_argument("--agents", nargs="+", required=True, help="List of agent IDs")
    parser.add_argument("--coords-file", default="src/runtime/config/cursor_agent_coords.json", help="Agent coordinates file")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode (no actual mouse/keyboard)")
    
    # FSM arguments
    parser.add_argument("--fsm-enabled", action="store_true", default=True, help="Enable FSM orchestration")
    parser.add_argument("--repos-root", default=str(get_owner_path()), help="Repositories root path")
    
    # Runtime arguments
    parser.add_argument("--interval", type=int, default=300, help="Cycle interval in seconds")
    parser.add_argument("--max-cycles", type=int, help="Maximum number of cycles to run")
    
    args = parser.parse_args()
    
    # Create and run enhanced runner
    runner = EnhancedRunner(
        agents=args.agents,
        fsm_enabled=args.fsm_enabled,
        repos_root=args.repos_root
    )
    
    # Initialize ACP
    if not runner.initialize_acp(args.coords_file, args.test_mode):
        print("❌ Failed to initialize ACP, exiting")
        sys.exit(1)
    
    # Run continuous cycle
    runner.run_continuous_cycle(
        interval_seconds=args.interval,
        max_cycles=args.max_cycles
    )


if __name__ == "__main__":
    main()
