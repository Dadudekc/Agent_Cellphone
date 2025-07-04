#!/usr/bin/env python3
"""
Status Standardizer for Dream.OS Agents
Standardizes agent status.json files to the new comprehensive format
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class StatusStandardizer:
    """Utility for standardizing agent status files"""
    
    def __init__(self, agent_workspaces_dir: str = "agent_workspaces"):
        self.agent_workspaces_dir = Path(agent_workspaces_dir)
        self.template_path = self.agent_workspaces_dir / "onboarding" / "status_template.json"
        self.template = self.load_template()
    
    def load_template(self) -> Dict[str, Any]:
        """Load the status template"""
        try:
            with open(self.template_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading template: {e}")
            return self.get_default_template()
    
    def get_default_template(self) -> Dict[str, Any]:
        """Get default template if file loading fails"""
        return {
            "agent_id": "AGENT_ID",
            "status": "offline",
            "current_task": "none",
            "message": "Agent initialized",
            "last_updated": "TIMESTAMP",
            "workspace_path": "WORKSPACE_PATH",
            "repo_root": "REPO_ROOT",
            "shared_tools": "SHARED_TOOLS_PATH",
            "onboarding": {
                "status": "pending",
                "started_at": None,
                "completed_at": None,
                "progress": 0.0,
                "checklist": {
                    "welcome_message": False,
                    "system_overview": False,
                    "communication_protocol": False,
                    "roles_and_responsibilities": False,
                    "best_practices": False,
                    "getting_started": False,
                    "troubleshooting": False,
                    "quick_start": False,
                    "status_update": False,
                    "repository_push": False
                },
                "documents_read": [],
                "verification_passed": False,
                "notes": ""
            },
            "capabilities": {
                "autonomous_mode": False,
                "communication_enabled": True,
                "file_operations": True,
                "task_execution": True,
                "status_reporting": True
            },
            "performance": {
                "tasks_completed": 0,
                "messages_sent": 0,
                "messages_received": 0,
                "uptime_hours": 0.0,
                "last_activity": None
            },
            "health": {
                "status": "healthy",
                "last_health_check": None,
                "errors": [],
                "warnings": []
            }
        }
    
    def get_agent_directories(self) -> list[Path]:
        """Get list of agent directories"""
        agent_dirs = []
        for item in self.agent_workspaces_dir.iterdir():
            if item.is_dir() and item.name.startswith("Agent-"):
                agent_dirs.append(item)
        return sorted(agent_dirs)
    
    def load_current_status(self, agent_dir: Path) -> Optional[Dict[str, Any]]:
        """Load current status.json for an agent"""
        status_file = agent_dir / "status.json"
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading status for {agent_dir.name}: {e}")
        return None
    
    def migrate_status(self, current_status: Dict[str, Any], agent_dir: Path) -> Dict[str, Any]:
        """Migrate current status to new format"""
        new_status = self.template.copy()
        
        # Basic agent info
        new_status["agent_id"] = current_status.get("agent_id", agent_dir.name)
        new_status["status"] = current_status.get("status", "offline")
        new_status["current_task"] = current_status.get("current_task", "none")
        new_status["message"] = current_status.get("message", "Agent initialized")
        new_status["last_updated"] = current_status.get("last_updated", datetime.now().isoformat())
        
        # Paths
        new_status["workspace_path"] = str(agent_dir.absolute())
        new_status["repo_root"] = str(self.agent_workspaces_dir.parent.absolute())
        new_status["shared_tools"] = str(self.agent_workspaces_dir / "shared_tools")
        
        # Migrate onboarding data if it exists
        if "onboarding" in current_status:
            old_onboarding = current_status["onboarding"]
            new_status["onboarding"]["status"] = old_onboarding.get("status", "pending")
            new_status["onboarding"]["started_at"] = old_onboarding.get("start_date")
            new_status["onboarding"]["completed_at"] = old_onboarding.get("completion_date")
            new_status["onboarding"]["progress"] = old_onboarding.get("progress", 0.0)
            
            # Migrate checklist
            if "checklist" in old_onboarding:
                old_checklist = old_onboarding["checklist"]
                new_checklist = new_status["onboarding"]["checklist"]
                
                # Map old checklist items to new ones
                mapping = {
                    "quick_start_completed": "quick_start",
                    "core_protocols_reviewed": "communication_protocol",
                    "status_reporting_implemented": "status_update",
                    "role_responsibilities_understood": "roles_and_responsibilities",
                    "development_standards_reviewed": "best_practices",
                    "tools_environment_setup": "getting_started"
                }
                
                for old_key, new_key in mapping.items():
                    if old_key in old_checklist:
                        new_checklist[new_key] = old_checklist[old_key]
            
            new_status["onboarding"]["verification_passed"] = old_onboarding.get("verification_passed", False)
            new_status["onboarding"]["notes"] = old_onboarding.get("notes", "")
        
        # Migrate capabilities if they exist
        if "capabilities" in current_status:
            old_capabilities = current_status["capabilities"]
            if isinstance(old_capabilities, list):
                # Old format was a list
                new_status["capabilities"]["autonomous_mode"] = "autonomous_mode" in old_capabilities
                new_status["capabilities"]["communication_enabled"] = "message_handling" in old_capabilities
                new_status["capabilities"]["file_operations"] = "file_operations" in old_capabilities
                new_status["capabilities"]["task_execution"] = "task_execution" in old_capabilities
                new_status["capabilities"]["status_reporting"] = "status_reporting" in old_capabilities
            elif isinstance(old_capabilities, dict):
                # New format already
                new_status["capabilities"].update(old_capabilities)
        
        # Migrate performance metrics if they exist
        if "performance_metrics" in current_status:
            old_performance = current_status["performance_metrics"]
            new_status["performance"]["tasks_completed"] = old_performance.get("tasks_completed", 0)
            new_status["performance"]["uptime_hours"] = old_performance.get("uptime_hours", 0.0)
            new_status["performance"]["last_activity"] = old_performance.get("last_response_time")
        
        return new_status
    
    def standardize_agent(self, agent_dir: Path) -> bool:
        """Standardize status for a single agent"""
        try:
            current_status = self.load_current_status(agent_dir)
            if current_status is None:
                # Create new status file
                new_status = self.template.copy()
                new_status["agent_id"] = agent_dir.name
                new_status["last_updated"] = datetime.now().isoformat()
                new_status["workspace_path"] = str(agent_dir.absolute())
                new_status["repo_root"] = str(self.agent_workspaces_dir.parent.absolute())
                new_status["shared_tools"] = str(self.agent_workspaces_dir / "shared_tools")
            else:
                # Migrate existing status
                new_status = self.migrate_status(current_status, agent_dir)
            
            # Save new status
            status_file = agent_dir / "status.json"
            with open(status_file, 'w') as f:
                json.dump(new_status, f, indent=2)
            
            print(f"✓ Standardized status for {agent_dir.name}")
            return True
            
        except Exception as e:
            print(f"✗ Error standardizing {agent_dir.name}: {e}")
            return False
    
    def standardize_all_agents(self) -> Dict[str, bool]:
        """Standardize status for all agents"""
        results = {}
        agent_dirs = self.get_agent_directories()
        
        print(f"Standardizing status for {len(agent_dirs)} agents...")
        
        for agent_dir in agent_dirs:
            results[agent_dir.name] = self.standardize_agent(agent_dir)
        
        return results
    
    def validate_status(self, agent_dir: Path) -> Dict[str, Any]:
        """Validate agent status format"""
        status_file = agent_dir / "status.json"
        if not status_file.exists():
            return {"valid": False, "error": "Status file not found"}
        
        try:
            with open(status_file, 'r') as f:
                status = json.load(f)
            
            # Check required fields
            required_fields = ["agent_id", "status", "current_task", "message", "last_updated", "onboarding"]
            missing_fields = [field for field in required_fields if field not in status]
            
            if missing_fields:
                return {"valid": False, "error": f"Missing required fields: {missing_fields}"}
            
            # Check onboarding structure
            if "onboarding" in status:
                onboarding = status["onboarding"]
                required_onboarding_fields = ["status", "progress", "checklist"]
                missing_onboarding = [field for field in required_onboarding_fields if field not in onboarding]
                
                if missing_onboarding:
                    return {"valid": False, "error": f"Missing onboarding fields: {missing_onboarding}"}
            
            return {"valid": True, "status": status}
            
        except Exception as e:
            return {"valid": False, "error": f"JSON parsing error: {e}"}
    
    def validate_all_agents(self) -> Dict[str, Dict[str, Any]]:
        """Validate all agent status files"""
        results = {}
        agent_dirs = self.get_agent_directories()
        
        for agent_dir in agent_dirs:
            results[agent_dir.name] = self.validate_status(agent_dir)
        
        return results

def main():
    """Main function to run status standardization"""
    standardizer = StatusStandardizer()
    
    print("=== Dream.OS Agent Status Standardization ===")
    
    # Standardize all agents
    results = standardizer.standardize_all_agents()
    
    # Validate results
    validation_results = standardizer.validate_all_agents()
    
    print("\n=== Standardization Results ===")
    for agent, success in results.items():
        status = "✓" if success else "✗"
        print(f"{status} {agent}")
    
    print("\n=== Validation Results ===")
    for agent, validation in validation_results.items():
        status = "✓" if validation["valid"] else "✗"
        print(f"{status} {agent}: {validation.get('error', 'Valid')}")
    
    # Summary
    successful = sum(1 for success in results.values() if success)
    valid = sum(1 for validation in validation_results.values() if validation["valid"])
    total = len(results)
    
    print(f"\n=== Summary ===")
    print(f"Standardized: {successful}/{total} agents")
    print(f"Validated: {valid}/{total} agents")
    
    if successful == total and valid == total:
        print("🎉 All agents successfully standardized and validated!")
    else:
        print("⚠️  Some agents need attention. Check the results above.")

if __name__ == "__main__":
    main() 