"""
Central Configuration System for Agent Cellphone

This module provides a centralized way to manage all configurable paths and settings
throughout the system, making it easy for users to customize paths for their projects.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SystemPaths:
    """Centralized system path configuration."""
    
    # Main repository root (e.g., D:/repos, C:/projects, /home/user/projects)
    repos_root: Path
    
    # Communications directory under repos root
    communications_root: Path
    
    # Agent workspaces directory
    agent_workspaces_root: Path
    
    # GitHub configuration file location
    github_config_path: Path
    
    # Signals directory for immediate resume
    signals_root: Path
    
    # Default organization/owner (e.g., "Dadudekc", "YourOrg")
    default_owner: str
    
    def __post_init__(self):
        """Ensure all paths are Path objects."""
        self.repos_root = Path(self.repos_root)
        self.communications_root = Path(self.communications_root)
        self.agent_workspaces_root = Path(self.agent_workspaces_root)
        self.github_config_path = Path(self.github_config_path)
        self.signals_root = Path(self.signals_root)


class ConfigManager:
    """Manages system configuration and provides easy access to paths."""
    
    def __init__(self):
        self._paths: Optional[SystemPaths] = None
        self._env_vars: Dict[str, str] = {}
        self._load_environment()
    
    def _load_environment(self):
        """Load environment variables with sensible defaults."""
        # Load from .env file if it exists (but don't override existing env vars)
        env_file = Path(".env")
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            # Only set if not already in environment
                            if key not in os.environ:
                                os.environ[key] = value.strip()
            except Exception as e:
                print(f"Warning: Could not load .env file: {e}")
        
        # Set default values for key environment variables
        # Environment variables take priority over .env file
        self._env_vars = {
            'REPOS_ROOT': os.getenv('REPOS_ROOT', 'D:/repos'),
            'REPO_DEST': os.getenv('REPO_DEST', 'D:/repos'),
            'AGENT_FILE_ROOT': os.getenv('AGENT_FILE_ROOT', 'D:/repos/Dadudekc'),
            'DEFAULT_OWNER': os.getenv('DEFAULT_OWNER', 'Dadudekc'),
            'COMMUNICATIONS_ROOT': os.getenv('COMMUNICATIONS_ROOT', ''),
            'AGENT_WORKSPACES_ROOT': os.getenv('AGENT_WORKSPACES_ROOT', ''),
        }
    
    @property
    def paths(self) -> SystemPaths:
        """Get or create the system paths configuration."""
        if self._paths is None:
            # Determine repos root (prioritize REPOS_ROOT over REPO_DEST)
            repos_root = self._env_vars['REPOS_ROOT']
            if repos_root == 'D:/repos' and self._env_vars['REPO_DEST'] != 'D:/repos':
                repos_root = self._env_vars['REPO_DEST']
            
            # Determine default owner
            default_owner = self._env_vars['DEFAULT_OWNER']
            
            # Build derived paths
            communications_root = self._env_vars['COMMUNICATIONS_ROOT'] or f"{repos_root}/communications"
            agent_workspaces_root = self._env_vars['AGENT_WORKSPACES_ROOT'] or f"{repos_root}/{default_owner}"
            
            self._paths = SystemPaths(
                repos_root=repos_root,
                communications_root=communications_root,
                agent_workspaces_root=agent_workspaces_root,
                github_config_path=f"{repos_root}/github_config.json",
                signals_root=f"{communications_root}/_signals",
                default_owner=default_owner
            )
        
        return self._paths
    
    def get_path(self, path_type: str) -> Path:
        """Get a specific path by type."""
        paths = self.paths
        
        path_map = {
            'repos_root': paths.repos_root,
            'communications_root': paths.communications_root,
            'agent_workspaces_root': paths.agent_workspaces_root,
            'github_config': paths.github_config_path,
            'signals_root': paths.signals_root,
            'default_owner': paths.default_owner,
        }
        
        if path_type not in path_map:
            raise ValueError(f"Unknown path type: {path_type}")
        
        return path_map[path_type]
    
    def get_owner_path(self, owner: Optional[str] = None) -> Path:
        """Get the path for a specific owner/organization."""
        owner = owner or self.paths.default_owner
        return self.paths.repos_root / owner
    
    def get_agent_workspace_path(self, agent: str, owner: Optional[str] = None) -> Path:
        """Get the workspace path for a specific agent."""
        owner_path = self.get_owner_path(owner)
        return owner_path / agent
    
    def get_communications_path(self, date_suffix: str = "") -> Path:
        """Get the communications path with optional date suffix."""
        base = self.paths.communications_root
        if date_suffix:
            return base / f"overnight_{date_suffix}_"
        return base
    
    def get_agent_communications_path(self, agent: str, date_suffix: str = "") -> Path:
        """Get the communications path for a specific agent."""
        comms_path = self.get_communications_path(date_suffix)
        return comms_path / agent
    
    def update_environment(self, **kwargs):
        """Update environment variables and reload configuration."""
        for key, value in kwargs.items():
            os.environ[key] = str(value)
        
        # Clear cached paths to force reload
        self._paths = None
        self._load_environment()
    
    def print_configuration(self):
        """Print current configuration for debugging."""
        print("🔧 Current System Configuration:")
        print(f"  📁 Repos Root: {self.paths.repos_root}")
        print(f"  📁 Communications Root: {self.paths.communications_root}")
        print(f"  📁 Agent Workspaces Root: {self.paths.agent_workspaces_root}")
        print(f"  📁 GitHub Config: {self.paths.github_config_path}")
        print(f"  📁 Signals Root: {self.paths.signals_root}")
        print(f"  👤 Default Owner: {self.paths.default_owner}")
        print()
        print("🔧 Environment Variables:")
        for key, value in self._env_vars.items():
            print(f"  {key}: {value}")
        print()
        print("🔧 Raw Environment Variables (for debugging):")
        for key in ['REPOS_ROOT', 'REPO_DEST', 'DEFAULT_OWNER', 'AGENT_FILE_ROOT']:
            print(f"  {key}: {os.getenv(key, 'NOT SET')}")


# Global configuration instance
config = ConfigManager()


def get_config() -> ConfigManager:
    """Get the global configuration manager."""
    return config


def get_paths() -> SystemPaths:
    """Get the system paths configuration."""
    return config.paths


def get_repos_root() -> Path:
    """Get the repositories root path."""
    return config.get_path('repos_root')


def get_communications_root() -> Path:
    """Get the communications root path."""
    return config.get_path('communications_root')


def get_agent_workspaces_root() -> Path:
    """Get the agent workspaces root path."""
    return config.get_path('agent_workspaces_root')


def get_github_config_path() -> Path:
    """Get the GitHub configuration file path."""
    return config.get_path('github_config')


def get_signals_root() -> Path:
    """Get the signals root path."""
    return config.get_path('signals_root')


def get_default_owner() -> str:
    """Get the default owner/organization name."""
    return config.get_path('default_owner')


# Convenience functions for common path operations
def get_owner_path(owner: Optional[str] = None) -> Path:
    """Get the path for a specific owner/organization."""
    return config.get_owner_path(owner)


def get_agent_workspace_path(agent: str, owner: Optional[str] = None) -> Path:
    """Get the workspace path for a specific agent."""
    return config.get_agent_workspace_path(agent, owner)


def get_communications_path(date_suffix: str = "") -> Path:
    """Get the communications path with optional date suffix."""
    return config.get_communications_path(date_suffix)


def get_agent_communications_path(agent: str, date_suffix: str = "") -> Path:
    """Get the communications path for a specific agent."""
    return config.get_agent_communications_path(agent, date_suffix)


if __name__ == "__main__":
    # Print current configuration when run directly
    config.print_configuration()
