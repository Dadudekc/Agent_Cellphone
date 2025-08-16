#!/usr/bin/env python3
"""
Repository Activity Monitor for Enhanced FSM
===========================================
Tracks actual agent work in repositories to provide contextual guidance.
"""

import os
import time
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class RepositoryContext:
    """Context of what an agent is working on"""
    current_repo: Optional[str] = None
    last_modified: Optional[float] = None
    recent_commits: List[str] = None
    file_changes: List[str] = None
    task_progress: Dict[str, any] = None
    blockers: List[str] = None
    
    def __post_init__(self):
        if self.recent_commits is None:
            self.recent_commits = []
        if self.file_changes is None:
            self.file_changes = []
        if self.task_progress is None:
            self.task_progress = {}
        if self.blockers is None:
            self.blockers = []

class RepositoryActivityMonitor:
    """Monitors repository activity to understand agent work context"""
    
    def __init__(self, repos_root: str = "D:/repos/Dadudekc"):
        self.repos_root = Path(repos_root)
        # Import here to avoid circular imports
        try:
            from src.core.project_focus_manager import ProjectFocusManager
            self.project_manager = ProjectFocusManager()
            self.use_dynamic_config = True
        except ImportError:
            # Fallback to hardcoded config if import fails
            self.project_manager = None
            self.use_dynamic_config = False
            self.agent_repos = {
                "Agent-1": ["AI_Debugger_Assistant", "DigitalDreamscape", "FreeRideInvestor", "Hive-Mind", "MeT"],
                "Agent-2": ["Auto_Blogger", "Dream.os", "FreeWork", "IT_help_desk", "NewSims4ModProject"],
                "Agent-3": ["DaDudeKC-Website", "DreamVault", "FreerideinvestorWebsite", "LSTMmodel_trainer"],
                "Agent-4": ["DaDudekC", "FocusForge", "HCshinobi", "MLRobotmaker", "SWARM"],
                "Agent-5": ["CAPTAIN"]  # Special role
            }
        
        self.cache = {}
        self.cache_ttl = 60  # 1 minute cache
    
    def get_agent_work_context(self, agent: str) -> RepositoryContext:
        """Get comprehensive work context for an agent"""
        cache_key = f"{agent}_{int(time.time() // self.cache_ttl)}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        context = RepositoryContext()
        
        if agent == "Agent-5":
            # Captain doesn't work on repos directly
            context.current_repo = "coordination"
            context.task_progress = {"role": "CAPTAIN", "status": "coordinating"}
            self.cache[cache_key] = context
            return context
        
        # Get agent repositories dynamically or fallback to hardcoded
        agent_repos = self._get_agent_repositories(agent)
        
        # Find which repo the agent is actively working on
        most_active_repo = None
        most_recent_activity = 0
        
        for repo in agent_repos:
            repo_path = self.repos_root / repo
            if not repo_path.exists():
                continue
                
            activity_level = self._get_repo_activity_level(repo_path)
            if activity_level > most_recent_activity:
                most_recent_activity = activity_level
                most_active_repo = repo
        
        if most_active_repo:
            context.current_repo = most_active_repo
            context.last_modified = most_recent_activity
            
            # Get detailed context for the active repo
            repo_path = self.repos_root / most_active_repo
            context.recent_commits = self._get_recent_commits(repo_path)
            context.file_changes = self._get_recent_file_changes(repo_path)
            context.task_progress = self._get_task_progress(repo_path)
            context.blockers = self._detect_blockers(repo_path)
        
        self.cache[cache_key] = context
        return context
    
    def _get_agent_repositories(self, agent: str) -> List[str]:
        """Get repositories assigned to an agent, using dynamic config if available"""
        if self.use_dynamic_config and self.project_manager:
            try:
                # Get projects from project manager
                projects = self.project_manager.get_agent_projects(agent)
                # Convert project names to repository paths
                repos = []
                for project_name in projects:
                    project_info = self.project_manager.get_project_info(project_name)
                    if project_info and project_info.repository_path:
                        # Extract just the repository name from the path
                        repo_name = project_info.repository_path.split('/')[-1]
                        repos.append(repo_name)
                return repos if repos else []
            except Exception as e:
                logger.warning(f"Error getting dynamic agent repositories for {agent}: {e}")
                # Fallback to hardcoded config
        
        # Fallback to hardcoded configuration
        if hasattr(self, 'agent_repos') and agent in self.agent_repos:
            return self.agent_repos[agent]
        
        return []
    
    def _get_repo_activity_level(self, repo_path: Path) -> float:
        """Get activity level based on file modifications and git activity"""
        try:
            # Check git log for recent commits
            git_activity = self._get_git_last_commit_time(repo_path)
            
            # Check file modifications
            file_activity = self._get_latest_file_modification(repo_path)
            
            # Return most recent activity
            return max(git_activity or 0, file_activity or 0)
        except Exception:
            return 0
    
    def _get_git_last_commit_time(self, repo_path: Path) -> Optional[float]:
        """Get timestamp of last git commit"""
        try:
            result = subprocess.run(
                ["git", "log", "-1", "--format=%ct"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0 and result.stdout.strip():
                return float(result.stdout.strip())
        except Exception:
            pass
        return None
    
    def _get_latest_file_modification(self, repo_path: Path) -> Optional[float]:
        """Get timestamp of most recent file modification"""
        try:
            latest_time = 0
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and not file_path.name.startswith('.'):
                    mtime = file_path.stat().st_mtime
                    latest_time = max(latest_time, mtime)
            return latest_time if latest_time > 0 else None
        except Exception:
            return None
    
    def _get_recent_commits(self, repo_path: Path) -> List[str]:
        """Get recent commit messages"""
        try:
            result = subprocess.run(
                ["git", "log", "--oneline", "-5"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            pass
        return []
    
    def _get_recent_file_changes(self, repo_path: Path) -> List[str]:
        """Get recently modified files"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=repo_path,
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                files = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        status, filename = line[:2], line[3:]
                        files.append(f"{status}: {filename}")
                return files
        except Exception:
            pass
        return []
    
    def _get_task_progress(self, repo_path: Path) -> Dict[str, any]:
        """Extract task progress from repository"""
        progress = {}
        
        # Look for common progress indicators
        progress_files = ["TASK_LIST.md", "README.md", "CHANGELOG.md", "TODO.md"]
        
        for file_name in progress_files:
            file_path = repo_path / file_name
            if file_path.exists():
                try:
                    content = file_path.read_text(encoding='utf-8', errors='ignore')
                    progress[file_name] = {
                        "exists": True,
                        "last_modified": file_path.stat().st_mtime,
                        "size": len(content)
                    }
                except Exception:
                    progress[file_name] = {"exists": True, "error": "unreadable"}
        
        return progress
    
    def _detect_blockers(self, repo_path: Path) -> List[str]:
        """Detect potential blockers in repository"""
        blockers = []
        
        # Check for common blocker indicators
        blocker_indicators = [
            ("requirements.txt", "missing dependencies"),
            ("tests/", "missing tests"),
            ("docs/", "missing documentation"),
            (".gitignore", "git configuration issues")
        ]
        
        for indicator, description in blocker_indicators:
            indicator_path = repo_path / indicator
            if not indicator_path.exists():
                blockers.append(f"{description}: {indicator}")
        
        return blockers
    
    def get_all_agents_context(self) -> Dict[str, RepositoryContext]:
        """Get work context for all agents"""
        return {
            agent: self.get_agent_work_context(agent)
            for agent in self.agent_repos.keys()
        }
    
    def get_coordination_summary(self) -> Dict[str, any]:
        """Get summary for coordination purposes"""
        all_contexts = self.get_all_agents_context()
        
        summary = {
            "timestamp": time.time(),
            "agents": {},
            "overall_progress": {
                "active_agents": 0,
                "stalled_agents": 0,
                "completed_repos": 0
            }
        }
        
        for agent, context in all_contexts.items():
            if agent == "Agent-5":
                continue
                
            status = "active" if context.current_repo else "idle"
            if context.current_repo:
                summary["overall_progress"]["active_agents"] += 1
            else:
                summary["overall_progress"]["stalled_agents"] += 1
            
            summary["agents"][agent] = {
                "status": status,
                "current_repo": context.current_repo,
                "last_activity": context.last_modified,
                "has_progress": bool(context.task_progress),
                "blockers": context.blockers
            }
        
        return summary
