#!/usr/bin/env python3
"""
Onboarding Integration for GUI
=============================
Provides onboarding status loading and management for GUI components.
"""

import json
from pathlib import Path
from typing import Dict
from datetime import datetime

class OnboardingIntegration:
    """Handles onboarding status integration with GUI components."""
    
    def __init__(self):
        self.agent_workspaces_path = Path("agent_workspaces")
    
    def get_agent_onboarding_status(self, agent_id: str) -> Dict:
        """Get onboarding status for a specific agent."""
        status_file = self.agent_workspaces_path / agent_id / "status.json"
        
        if not status_file.exists():
            return {
                "agent_id": agent_id,
                "status": "unknown",
                "progress": 0,
                "error": "Status file not found"
            }
        
        try:
            with open(status_file, 'r') as f:
                status_data = json.load(f)
            
            onboarding = status_data.get("onboarding", {})
            return {
                "agent_id": agent_id,
                "status": onboarding.get("status", "not_started"),
                "progress": onboarding.get("progress", 0),
                "completed_steps": onboarding.get("completed_steps", []),
                "current_step": onboarding.get("current_step"),
                "start_date": onboarding.get("start_date"),
                "completion_date": onboarding.get("completion_date"),
                "verification_passed": onboarding.get("verification_passed", False),
                "checklist": onboarding.get("checklist", {})
            }
            
        except Exception as e:
            return {
                "agent_id": agent_id,
                "status": "error",
                "progress": 0,
                "error": f"Error reading status: {e}"
            }
    
    def get_all_agents_onboarding_status(self) -> Dict[str, Dict]:
        """Get onboarding status for all agents."""
        results = {}
        
        if not self.agent_workspaces_path.exists():
            return results
        
        agent_dirs = [d for d in self.agent_workspaces_path.iterdir() 
                     if d.is_dir() and d.name.startswith("Agent-")]
        
        for agent_dir in agent_dirs:
            agent_id = agent_dir.name
            results[agent_id] = self.get_agent_onboarding_status(agent_id)
        
        return results
    
    def update_agent_onboarding_progress(self, agent_id: str, step: str, completed: bool = True) -> bool:
        """Update onboarding progress for a specific agent."""
        status_file = self.agent_workspaces_path / agent_id / "status.json"
        
        if not status_file.exists():
            return False
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            if "onboarding" not in status:
                status["onboarding"] = {
                    "status": "not_started",
                    "progress": 0,
                    "completed_steps": [],
                    "current_step": None,
                    "start_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "completion_date": None,
                    "verification_passed": False,
                    "checklist": {
                        "quick_start_completed": False,
                        "core_protocols_reviewed": False,
                        "status_reporting_implemented": False,
                        "first_communication_test": False,
                        "role_responsibilities_understood": False,
                        "development_standards_reviewed": False,
                        "tools_environment_setup": False,
                        "onboarding_verification_passed": False
                    }
                }
            
            onboarding = status["onboarding"]
            
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
    
    def get_onboarding_summary(self) -> Dict:
        """Get a summary of all agents' onboarding status."""
        all_statuses = self.get_all_agents_onboarding_status()
        
        summary = {
            "total_agents": len(all_statuses),
            "completed": 0,
            "in_progress": 0,
            "not_started": 0,
            "error": 0,
            "average_progress": 0,
            "agents": {}
        }
        
        total_progress = 0
        
        for agent_id, status in all_statuses.items():
            agent_status = status.get("status", "unknown")
            progress = status.get("progress", 0)
            
            summary["agents"][agent_id] = {
                "status": agent_status,
                "progress": progress
            }
            
            if agent_status == "completed":
                summary["completed"] += 1
            elif agent_status == "in_progress":
                summary["in_progress"] += 1
            elif agent_status == "not_started":
                summary["not_started"] += 1
            elif agent_status == "error":
                summary["error"] += 1
            
            total_progress += progress
        
        if summary["total_agents"] > 0:
            summary["average_progress"] = int(total_progress / summary["total_agents"])
        
        return summary
    
    def format_onboarding_status_for_display(self, status: Dict) -> str:
        """Format onboarding status for GUI display."""
        if "error" in status:
            return f"❌ Error: {status['error']}"
        
        status_text = status.get("status", "unknown").replace("_", " ").title()
        progress = status.get("progress", 0)
        
        if progress == 100:
            return f"✅ {status_text} (100%)"
        elif progress > 50:
            return f"🟡 {status_text} ({progress}%)"
        elif progress > 0:
            return f"🟠 {status_text} ({progress}%)"
        else:
            return f"⚫ {status_text} (0%)"

# Global instance for easy access
onboarding_integration = OnboardingIntegration() 