import os
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

ONBOARDING_ROOT = Path(__file__).parent
CHECKLIST_STATE_FILE = ONBOARDING_ROOT / "onboarding_checklist_state.json"
STATUS_TEMPLATE_FILE = ONBOARDING_ROOT / "status_template.json"

EXCLUDE_DIRS = {"logs", "temp", "__pycache__"}
INCLUDE_EXTS = {".md", ".py"}

class OnboardingManager:
    def __init__(self, root_dir: Optional[Path] = None):
        self.root_dir = Path(root_dir) if root_dir else ONBOARDING_ROOT
        self.docs = self.discover_onboarding_docs()
        self.checklist = self.generate_checklist()
        self.state = self.load_state()
        self.status_template = self.load_status_template()

    def load_status_template(self) -> Dict:
        """Load the standardized status template."""
        try:
            with open(STATUS_TEMPLATE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading status template: {e}")
            return {}

    def standardize_agent_status(self, agent_id: str) -> bool:
        """Standardize an agent's status.json file to the new format."""
        agent_workspace = Path(f"agent_workspaces/{agent_id}")
        status_file = agent_workspace / "status.json"
        
        if not status_file.exists():
            print(f"Status file not found for {agent_id}")
            return False
        
        try:
            # Load current status
            with open(status_file, 'r') as f:
                current_status = json.load(f)
            
            # Create new standardized status
            new_status = self.status_template.copy()
            new_status["agent_id"] = agent_id
            
            # Preserve existing data where possible
            if "status" in current_status:
                new_status["status"] = current_status["status"]
            if "current_task" in current_status:
                new_status["current_task"] = current_status["current_task"]
            if "last_update" in current_status:
                new_status["last_update"] = current_status["last_update"]
            elif "last_updated" in current_status:
                new_status["last_update"] = current_status["last_updated"]
            
            # Initialize onboarding if not present
            if "onboarding" not in current_status:
                new_status["onboarding"]["status"] = "not_started"
                new_status["onboarding"]["start_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save standardized status
            with open(status_file, 'w') as f:
                json.dump(new_status, f, indent=2)
            
            print(f"✅ Standardized status for {agent_id}")
            return True
            
        except Exception as e:
            print(f"❌ Error standardizing status for {agent_id}: {e}")
            return False

    def standardize_all_agents(self) -> Dict[str, bool]:
        """Standardize status.json for all agents."""
        results = {}
        agent_dirs = [d for d in Path("agent_workspaces").iterdir() 
                     if d.is_dir() and d.name.startswith("Agent-")]
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            results[agent_id] = self.standardize_agent_status(agent_id)
        
        return results

    def get_agent_onboarding_status(self, agent_id: str) -> Dict:
        """Get onboarding status for a specific agent."""
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if not status_file.exists():
            return {"error": "Status file not found"}
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            onboarding = status.get("onboarding", {})
            return {
                "agent_id": agent_id,
                "status": onboarding.get("status", "unknown"),
                "progress": onboarding.get("progress", 0),
                "completed_steps": onboarding.get("completed_steps", []),
                "current_step": onboarding.get("current_step"),
                "start_date": onboarding.get("start_date"),
                "completion_date": onboarding.get("completion_date"),
                "verification_passed": onboarding.get("verification_passed", False),
                "checklist": onboarding.get("checklist", {})
            }
        except Exception as e:
            return {"error": f"Error reading status: {e}"}

    def update_agent_onboarding_progress(self, agent_id: str, step: str, completed: bool = True) -> bool:
        """Update onboarding progress for a specific agent."""
        status_file = Path(f"agent_workspaces/{agent_id}/status.json")
        
        if not status_file.exists():
            return False
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            if "onboarding" not in status:
                status["onboarding"] = self.status_template["onboarding"].copy()
            
            onboarding = status["onboarding"]
            
            # Update checklist
            if "checklist" not in onboarding:
                onboarding["checklist"] = self.status_template["onboarding"]["checklist"].copy()
            
            # Map step names to checklist items
            step_mapping = {
                "quick_start": "quick_start_completed",
                "core_protocols": "core_protocols_reviewed",
                "status_reporting": "status_reporting_implemented",
                "communication_test": "first_communication_test",
                "role_responsibilities": "role_responsibilities_understood",
                "development_standards": "development_standards_reviewed",
                "tools_setup": "tools_environment_setup",
                "verification": "onboarding_verification_passed"
            }
            
            checklist_item = step_mapping.get(step, step)
            onboarding["checklist"][checklist_item] = completed
            
            # Update completed steps list
            if completed and step not in onboarding.get("completed_steps", []):
                if "completed_steps" not in onboarding:
                    onboarding["completed_steps"] = []
                onboarding["completed_steps"].append(step)
            
            # Calculate progress
            total_steps = len(onboarding["checklist"])
            completed_steps = sum(1 for v in onboarding["checklist"].values() if v)
            onboarding["progress"] = int((completed_steps / total_steps) * 100)
            
            # Update status
            if onboarding["progress"] == 100:
                onboarding["status"] = "completed"
                onboarding["completion_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            elif onboarding["progress"] > 0:
                onboarding["status"] = "in_progress"
            else:
                onboarding["status"] = "not_started"
            
            # Update last_update
            status["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save updated status
            with open(status_file, 'w') as f:
                json.dump(status, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"❌ Error updating onboarding progress for {agent_id}: {e}")
            return False

    def verify_onboarding_completion(self, agent_id: str) -> Dict:
        """Verify that an agent has completed onboarding requirements."""
        status = self.get_agent_onboarding_status(agent_id)
        
        if "error" in status:
            return status
        
        checklist = status.get("checklist", {})
        verification_results = {
            "agent_id": agent_id,
            "overall_passed": True,
            "details": {},
            "missing_items": []
        }
        
        # Check each requirement
        for item, completed in checklist.items():
            verification_results["details"][item] = completed
            if not completed:
                verification_results["overall_passed"] = False
                verification_results["missing_items"].append(item)
        
        # Update verification status
        self.update_agent_onboarding_progress(agent_id, "verification", verification_results["overall_passed"])
        
        return verification_results

    def get_all_agents_onboarding_status(self) -> Dict[str, Dict]:
        """Get onboarding status for all agents."""
        results = {}
        agent_dirs = [d for d in Path("agent_workspaces").iterdir() 
                     if d.is_dir() and d.name.startswith("Agent-")]
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            results[agent_id] = self.get_agent_onboarding_status(agent_id)
        
        return results

    def discover_onboarding_docs(self) -> List[Dict]:
        """Recursively find all .md and .py docs in onboarding directory."""
        docs = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            # Exclude certain directories
            dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext in INCLUDE_EXTS:
                    fpath = Path(dirpath) / fname
                    docs.append({
                        "path": str(fpath.relative_to(self.root_dir)),
                        "name": fname,
                        "ext": ext,
                        "type": "script" if ext == ".py" else "doc"
                    })
        return sorted(docs, key=lambda d: d["path"])

    def generate_checklist(self) -> List[Dict]:
        """Generate checklist items from discovered docs."""
        checklist = []
        for doc in self.docs:
            item = {
                "path": doc["path"],
                "name": doc["name"],
                "type": doc["type"],
                "completed": False
            }
            checklist.append(item)
        return checklist

    def load_state(self) -> Dict:
        if CHECKLIST_STATE_FILE.exists():
            try:
                with open(CHECKLIST_STATE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        # Default state: all incomplete
        return {item["path"]: False for item in self.checklist}

    def save_state(self):
        with open(CHECKLIST_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, indent=2)

    def mark_item_complete(self, doc_path: str):
        self.state[doc_path] = True
        self.save_state()

    def get_checklist(self) -> List[Dict]:
        """Return checklist with completion status."""
        for item in self.checklist:
            item["completed"] = self.state.get(item["path"], False)
        return self.checklist

    def get_progress(self) -> Dict:
        total = len(self.checklist)
        completed = sum(1 for item in self.get_checklist() if item["completed"])
        percent = (completed / total * 100) if total else 0
        outstanding = [item for item in self.get_checklist() if not item["completed"]]
        return {
            "total": total,
            "completed": completed,
            "percent": percent,
            "outstanding": outstanding
        }

    def reset_checklist(self):
        self.state = {item["path"]: False for item in self.checklist}
        self.save_state()

# Example usage (for testing):
if __name__ == "__main__":
    mgr = OnboardingManager()
    
    print("🔧 Standardizing all agent status files...")
    results = mgr.standardize_all_agents()
    for agent, success in results.items():
        print(f"  {agent}: {'✅' if success else '❌'}")
    
    print("\n📊 Onboarding status for all agents:")
    statuses = mgr.get_all_agents_onboarding_status()
    for agent, status in statuses.items():
        if "error" not in status:
            progress = status.get("progress", 0)
            status_text = status.get("status", "unknown")
            print(f"  {agent}: {progress}% ({status_text})")
        else:
            print(f"  {agent}: {status['error']}") 