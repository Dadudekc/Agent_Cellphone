import asyncio, logging, json, time
from pathlib import Path
from typing import AsyncGenerator, Dict, Any

log = logging.getLogger("prd")

class PRDWatcher:
    """Watches for new PRDs and converts them to project roadmaps."""
    
    def __init__(self, prd_dir: Path):
        self.prd_dir = prd_dir
        self.prd_dir.mkdir(exist_ok=True)
        self.processed_files = set()
    
    async def stream(self) -> AsyncGenerator[Dict[str, Any], None]:
        """Stream new PRDs as they appear."""
        log.info("📋 PRD watcher monitoring %s", self.prd_dir)
        
        while True:
            try:
                # Check for new PRD files
                for prd_file in self.prd_dir.glob("*.json"):
                    if prd_file.name not in self.processed_files:
                        log.info("📄 Found new PRD: %s", prd_file.name)
                        
                        # Parse PRD
                        prd_data = self._parse_prd(prd_file)
                        if prd_data:
                            self.processed_files.add(prd_file.name)
                            yield prd_data
                
                await asyncio.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                log.error("❌ PRD watcher error: %s", e)
                await asyncio.sleep(30)
    
    def _parse_prd(self, prd_file: Path) -> Dict[str, Any]:
        """Parse a PRD file into structured data."""
        try:
            prd_data = json.loads(prd_file.read_text())
            
            # Validate required fields
            required_fields = ["name", "description", "requirements"]
            for field in required_fields:
                if field not in prd_data:
                    log.error("❌ PRD missing required field: %s", field)
                    return None
            
            # Add metadata
            prd_data["file_path"] = str(prd_file)
            prd_data["created_at"] = time.strftime('%Y-%m-%d %H:%M:%S')
            prd_data["status"] = "new"
            
            log.info("✅ Parsed PRD: %s", prd_data["name"])
            return prd_data
            
        except json.JSONDecodeError as e:
            log.error("❌ Invalid JSON in PRD %s: %s", prd_file.name, e)
            return None
        except Exception as e:
            log.error("❌ Error parsing PRD %s: %s", prd_file.name, e)
            return None
    
    def create_sample_prd(self, name: str = "sample_project"):
        """Create a sample PRD for testing."""
        sample_prd = {
            "name": "Autonomous Agent Development Platform",
            "description": "A platform for autonomous AI agents to collaborate on software development projects",
            "requirements": [
                "Multi-agent coordination system",
                "Git-based workflow management",
                "Training document system",
                "Project management tools",
                "Real-time communication",
                "Task assignment and tracking",
                "Code review automation",
                "Deployment pipeline"
            ],
            "features": [
                "Agent workspace management",
                "Sprint planning and tracking",
                "Training material distribution",
                "Code quality monitoring",
                "Performance metrics",
                "Integration with development tools"
            ],
            "constraints": [
                "Must work with existing git repositories",
                "Support multiple programming languages",
                "Real-time collaboration",
                "Scalable architecture",
                "Security and access control"
            ],
            "timeline_days": 60,
            "priority": "high",
            "estimated_effort": "medium"
        }
        
        prd_file = self.prd_dir / f"{name}.json"
        prd_file.write_text(json.dumps(sample_prd, indent=2))
        log.info("📄 Created sample PRD: %s", prd_file)
        return prd_file 