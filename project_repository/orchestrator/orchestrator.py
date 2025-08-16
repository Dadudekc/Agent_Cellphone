import asyncio, logging, json, time
from pathlib import Path
from .prd_watcher import PRDWatcher
from .task_router import TaskRouter
from core.workspace_manager import WorkspaceManager
from core.branch_manager import BranchManager
from core.agent_loop import run_agent_loop
from core.captain_loop import run_captain_loop

log = logging.getLogger("orchestrator")

class Orchestrator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.ws_mgr = WorkspaceManager(repo_root, Path("D:/repos/Dadudekc"))
        self.branch_mgr = BranchManager(repo_root)
        self.prd_watch = PRDWatcher(repo_root / "PRDs")
        self.router = TaskRouter()
        self.agent_tasks = []
        self.is_running = False

    async def start(self):
        """Start the orchestrator"""
        self.is_running = True
        log.info("🚀 Dream.OS Orchestrator starting...")
        
        try:
            # Start background tasks
            asyncio.create_task(self.prd_loop())
            asyncio.create_task(self.captain_loop())
            await self.agent_bootstrap()
            
            # Main orchestrator loop
            while self.is_running:
                await self._orchestrator_cycle()
                await asyncio.sleep(60)  # Check every minute
                
        except Exception as e:
            log.error("❌ Orchestrator error: %s", e)
        finally:
            self.is_running = False

    async def agent_bootstrap(self):
        """Bootstrap all agents"""
        log.info("🤖 Bootstrapping agents...")
        
        for i in range(1, 9):  # 8 agents
            agent_id = f"Agent-{i}"
            try:
                # Prepare workspace and branch
                ws = self.ws_mgr.prepare(agent_id)
                
                # Start agent loop
                asyncio.create_task(run_agent_loop(agent_id, ws, self.router))
                
                log.info("✅ Bootstrapped %s", agent_id)
                
            except Exception as e:
                log.error("❌ Failed to bootstrap %s: %s", agent_id, e)

    async def prd_loop(self):
        """Process PRDs and create tasks"""
        log.info("📋 Starting PRD processing loop")
        
        try:
            async for prd_data in self.prd_watch.stream():
                log.info("📄 Processing PRD: %s", prd_data["name"])
                
                # Convert PRD to tasks
                tasks = self.router.ingest_prd(prd_data)
                
                # Dispatch tasks
                self.router.dispatch_tasks(tasks)
                
                log.info("✅ PRD processed into %d tasks", len(tasks))
                
        except Exception as e:
            log.error("❌ PRD loop error: %s", e)

    async def captain_loop(self):
        """Run the captain supervision loop"""
        log.info("👨‍✈️ Starting captain supervision loop")
        
        try:
            await run_captain_loop(self.branch_mgr)
        except Exception as e:
            log.error("❌ Captain loop error: %s", e)

    async def _orchestrator_cycle(self):
        """Main orchestrator cycle - monitoring and coordination"""
        try:
            # Get system status
            status = self.router.get_system_status()
            
            # Log status periodically
            if int(time.time()) % 300 == 0:  # Every 5 minutes
                log.info("📊 System Status:")
                log.info("   Tasks: %d total, %d pending, %d assigned, %d completed (%.1f%%)",
                        status["tasks"]["total"],
                        status["tasks"]["pending"],
                        status["tasks"]["assigned"],
                        status["tasks"]["completed"],
                        status["tasks"]["completion_rate"])
                log.info("   Agents: %d total, %d active", 
                        status["agents"]["total"],
                        status["agents"]["active"])
            
            # Check for system health issues
            if status["tasks"]["pending"] > 10 and status["agents"]["active"] == 0:
                log.warning("⚠️ High task backlog with no active agents")
            
        except Exception as e:
            log.error("❌ Orchestrator cycle error: %s", e)

    def stop(self):
        """Stop the orchestrator"""
        self.is_running = False
        log.info("🛑 Orchestrator stopping...")

    def get_status(self) -> dict:
        """Get current orchestrator status"""
        return {
            "running": self.is_running,
            "system": self.router.get_system_status(),
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }

    def create_sample_prd(self):
        """Create a sample PRD for testing"""
        return self.prd_watch.create_sample_prd("autonomous_platform") 