"""
Project Focus Manager - Dynamic Configuration for Agent Project Assignments

This module provides a flexible, user-configurable system for managing which projects
agents focus on, eliminating hardcoded project assignments and improving scalability.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class Project:
    """Project configuration data structure"""
    name: str
    category: str
    priority: int
    description: str
    repository_path: str
    active: bool

@dataclass
class AgentAssignment:
    """Agent project assignment data structure"""
    primary_projects: List[str]
    secondary_projects: List[str]
    max_projects: int
    focus_area: str

class ProjectFocusManager:
    """
    Manages dynamic project focus configuration for agents.
    
    Allows users to easily modify which projects agents work on without
    changing code or restarting the system.
    """
    
    def __init__(self, config_path: str = "config/agents/project_focus.json"):
        self.config_path = Path(config_path)
        self.config = {}
        self.projects: Dict[str, Project] = {}
        self.agent_assignments: Dict[str, AgentAssignment] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load configuration from JSON file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                self._parse_config()
                logger.info(f"Loaded project focus configuration from {self.config_path}")
            else:
                logger.warning(f"Project focus config not found at {self.config_path}")
                self._create_default_config()
        except Exception as e:
            logger.error(f"Error loading project focus config: {e}")
            self._create_default_config()
    
    def _parse_config(self) -> None:
        """Parse loaded configuration into structured objects"""
        try:
            # Parse projects
            for project_data in self.config.get("project_focus_config", {}).get("available_projects", []):
                project = Project(
                    name=project_data["name"],
                    category=project_data["category"],
                    priority=project_data["priority"],
                    description=project_data["description"],
                    repository_path=project_data["repository_path"],
                    active=project_data["active"]
                )
                self.projects[project.name] = project
            
            # Parse agent assignments
            for agent_id, assignment_data in self.config.get("project_focus_config", {}).get("agent_project_assignments", {}).items():
                assignment = AgentAssignment(
                    primary_projects=assignment_data["primary_projects"],
                    secondary_projects=assignment_data["secondary_projects"],
                    max_projects=assignment_data["max_projects"],
                    focus_area=assignment_data["focus_area"]
                )
                self.agent_assignments[agent_id] = assignment
                
        except Exception as e:
            logger.error(f"Error parsing project focus config: {e}")
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create default configuration if none exists"""
        self.config = {
            "project_focus_config": {
                "description": "Default project focus configuration",
                "version": "1.0",
                "last_updated": datetime.now().isoformat(),
                "available_projects": [
                    {
                        "name": "default_project",
                        "category": "general",
                        "priority": 1,
                        "description": "Default project for testing",
                        "repository_path": "repos/default",
                        "active": True
                    }
                ],
                "agent_project_assignments": {
                    "Agent-1": {
                        "primary_projects": ["default_project"],
                        "secondary_projects": [],
                        "max_projects": 1,
                        "focus_area": "general"
                    }
                }
            }
        }
        self._parse_config()
        self.save_config()
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        try:
            self.config["project_focus_config"]["last_updated"] = datetime.now().isoformat()
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved project focus configuration to {self.config_path}")
        except Exception as e:
            logger.error(f"Error saving project focus config: {e}")
    
    def get_agent_projects(self, agent_id: str) -> List[str]:
        """Get all projects assigned to a specific agent"""
        if agent_id not in self.agent_assignments:
            return []
        
        assignment = self.agent_assignments[agent_id]
        all_projects = assignment.primary_projects + assignment.secondary_projects
        return [p for p in all_projects if p in self.projects and self.projects[p].active]
    
    def get_agent_primary_projects(self, agent_id: str) -> List[str]:
        """Get primary projects for a specific agent"""
        if agent_id not in self.agent_assignments:
            return []
        
        assignment = self.agent_assignments[agent_id]
        return [p for p in assignment.primary_projects if p in self.projects and self.projects[p].active]
    
    def get_project_info(self, project_name: str) -> Optional[Project]:
        """Get information about a specific project"""
        return self.projects.get(project_name)
    
    def get_projects_by_category(self, category: str) -> List[Project]:
        """Get all projects in a specific category"""
        return [p for p in self.projects.values() if p.category == category and p.active]
    
    def get_agents_for_project(self, project_name: str) -> List[str]:
        """Get all agents assigned to a specific project"""
        agents = []
        for agent_id, assignment in self.agent_assignments.items():
            if project_name in assignment.primary_projects or project_name in assignment.secondary_projects:
                agents.append(agent_id)
        return agents
    
    def add_project(self, name: str, category: str, priority: int, description: str, 
                   repository_path: str, active: bool = True) -> bool:
        """Add a new project to the configuration"""
        try:
            if name in self.projects:
                logger.warning(f"Project {name} already exists")
                return False
            
            project = Project(name, category, priority, description, repository_path, active)
            self.projects[name] = project
            
            # Add to config
            self.config["project_focus_config"]["available_projects"].append({
                "name": name,
                "category": category,
                "priority": priority,
                "description": description,
                "repository_path": repository_path,
                "active": active
            })
            
            self.save_config()
            logger.info(f"Added new project: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding project {name}: {e}")
            return False
    
    def remove_project(self, name: str) -> bool:
        """Remove a project from the configuration"""
        try:
            if name not in self.projects:
                logger.warning(f"Project {name} not found")
                return False
            
            # Remove from projects
            del self.projects[name]
            
            # Remove from config
            projects_list = self.config["project_focus_config"]["available_projects"]
            self.config["project_focus_config"]["available_projects"] = [
                p for p in projects_list if p["name"] != name
            ]
            
            # Remove from agent assignments
            for agent_id, assignment in self.agent_assignments.items():
                assignment.primary_projects = [p for p in assignment.primary_projects if p != name]
                assignment.secondary_projects = [p for p in assignment.secondary_projects if p != name]
            
            self.save_config()
            logger.info(f"Removed project: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Error removing project {name}: {e}")
            return False
    
    def assign_project_to_agent(self, project_name: str, agent_id: str, 
                               is_primary: bool = True) -> bool:
        """Assign a project to an agent"""
        try:
            if project_name not in self.projects:
                logger.warning(f"Project {project_name} not found")
                return False
            
            if agent_id not in self.agent_assignments:
                logger.warning(f"Agent {agent_id} not found")
                return False
            
            assignment = self.agent_assignments[agent_id]
            
            # Check if agent can handle more projects
            current_total = len(assignment.primary_projects) + len(assignment.secondary_projects)
            if current_total >= assignment.max_projects:
                logger.warning(f"Agent {agent_id} already at max project capacity")
                return False
            
            # Remove from other lists first
            assignment.primary_projects = [p for p in assignment.primary_projects if p != project_name]
            assignment.secondary_projects = [p for p in assignment.secondary_projects if p != project_name]
            
            # Add to appropriate list
            if is_primary:
                assignment.primary_projects.append(project_name)
            else:
                assignment.secondary_projects.append(project_name)
            
            # Update config
            for agent_data in self.config["project_focus_config"]["agent_project_assignments"][agent_id]:
                if agent_data == agent_id:
                    self.config["project_focus_config"]["agent_project_assignments"][agent_id] = {
                        "primary_projects": assignment.primary_projects,
                        "secondary_projects": assignment.secondary_projects,
                        "max_projects": assignment.max_projects,
                        "focus_area": assignment.focus_area
                    }
                    break
            
            self.save_config()
            logger.info(f"Assigned project {project_name} to agent {agent_id} as {'primary' if is_primary else 'secondary'}")
            return True
            
        except Exception as e:
            logger.error(f"Error assigning project {project_name} to agent {agent_id}: {e}")
            return False
    
    def get_project_priority_order(self) -> List[str]:
        """Get projects ordered by priority (highest first)"""
        sorted_projects = sorted(
            self.projects.values(), 
            key=lambda x: x.priority
        )
        return [p.name for p in sorted_projects if p.active]
    
    def get_agent_workload(self, agent_id: str) -> Dict[str, Any]:
        """Get workload information for a specific agent"""
        if agent_id not in self.agent_assignments:
            return {"error": "Agent not found"}
        
        assignment = self.agent_assignments[agent_id]
        current_load = len(assignment.primary_projects) + len(assignment.secondary_projects)
        
        return {
            "agent_id": agent_id,
            "current_load": current_load,
            "max_capacity": assignment.max_projects,
            "utilization_percent": (current_load / assignment.max_projects) * 100,
            "primary_projects": assignment.primary_projects,
            "secondary_projects": assignment.secondary_projects,
            "focus_area": assignment.focus_area
        }
    
    def get_system_overview(self) -> Dict[str, Any]:
        """Get overview of entire system configuration"""
        return {
            "total_projects": len(self.projects),
            "active_projects": len([p for p in self.projects.values() if p.active]),
            "total_agents": len(self.agent_assignments),
            "project_categories": list(set(p.category for p in self.projects.values())),
            "agent_workloads": {
                agent_id: self.get_agent_workload(agent_id) 
                for agent_id in self.agent_assignments.keys()
            }
        }
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        logger.info("Reloading project focus configuration")
        self.load_config()
    
    def export_config(self, export_path: str) -> bool:
        """Export current configuration to a file"""
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            logger.info(f"Exported configuration to {export_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")
            return False
