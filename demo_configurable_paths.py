#!/usr/bin/env python3
"""
Demonstration: Configurable Paths System

This script demonstrates how easy it is to change where agents focus their work
by simply updating environment variables. No more hardcoded paths!
"""

import os
import sys
from pathlib import Path

# Add src/core to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src" / "core"))

try:
    from config import config, get_repos_root, get_owner_path, get_agent_workspace_path
except ImportError:
    print("❌ Error: Could not import configuration system.")
    print("   Make sure you're running this from the Agent_Cellphone directory.")
    sys.exit(1)


def demo_personal_projects():
    """Demonstrate focusing on personal projects."""
    print("🎯 DEMO: Personal Projects Focus")
    print("=" * 50)
    
    # Set environment for personal projects
    os.environ['REPOS_ROOT'] = 'C:/my-projects'
    os.environ['DEFAULT_OWNER'] = 'MyUsername'
    
    # Reload configuration
    config.update_environment()
    
    # Show results
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print(f"🤖 Agent-1 Workspace: {get_agent_workspace_path('Agent-1')}")
    print(f"📡 Communications: {config.get_path('communications_root')}")
    print()


def demo_company_projects():
    """Demonstrate focusing on company projects."""
    print("🏢 DEMO: Company Projects Focus")
    print("=" * 50)
    
    # Set environment for company projects
    os.environ['REPOS_ROOT'] = 'D:/company-projects'
    os.environ['DEFAULT_OWNER'] = 'CompanyName'
    
    # Reload configuration
    config.update_environment()
    
    # Show results
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print(f"🤖 Agent-1 Workspace: {get_agent_workspace_path('Agent-1')}")
    print(f"📡 Communications: {config.get_path('communications_root')}")
    print()


def demo_cross_platform():
    """Demonstrate cross-platform path support."""
    print("🌍 DEMO: Cross-Platform Paths")
    print("=" * 50)
    
    # Simulate Linux/Mac paths
    os.environ['REPOS_ROOT'] = '/home/user/projects'
    os.environ['DEFAULT_OWNER'] = 'MyName'
    
    # Reload configuration
    config.update_environment()
    
    # Show results
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print(f"🤖 Agent-1 Workspace: {get_agent_workspace_path('Agent-1')}")
    print(f"📡 Communications: {config.get_path('communications_root')}")
    print()


def demo_custom_communications():
    """Demonstrate custom communications location."""
    print("📡 DEMO: Custom Communications Location")
    print("=" * 50)
    
    # Set custom communications path
    os.environ['REPOS_ROOT'] = 'E:/development'
    os.environ['DEFAULT_OWNER'] = 'DevTeam'
    os.environ['COMMUNICATIONS_ROOT'] = 'F:/agent-comms'
    
    # Reload configuration
    config.update_environment()
    
    # Show results
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print(f"🤖 Agent-1 Workspace: {get_agent_workspace_path('Agent-1')}")
    print(f"📡 Communications: {config.get_path('communications_root')}")
    print()


def demo_agent_workspaces():
    """Demonstrate all agent workspace paths."""
    print("🤖 DEMO: All Agent Workspaces")
    print("=" * 50)
    
    # Set a simple configuration
    os.environ['REPOS_ROOT'] = 'G:/projects'
    os.environ['DEFAULT_OWNER'] = 'ProjectTeam'
    
    # Reload configuration
    config.update_environment()
    
    # Show all agent workspaces
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print()
    print("🤖 Agent Workspaces:")
    for agent in ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5']:
        workspace = get_agent_workspace_path(agent)
        print(f"  {agent}: {workspace}")
    print()


def demo_communications_structure():
    """Demonstrate communications directory structure."""
    print("📡 DEMO: Communications Directory Structure")
    print("=" * 50)
    
    # Set configuration
    os.environ['REPOS_ROOT'] = 'H:/work'
    os.environ['DEFAULT_OWNER'] = 'WorkTeam'
    
    # Reload configuration
    config.update_environment()
    
    # Show communications structure
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print()
    print("📡 Communications Structure:")
    print(f"  Base: {config.get_path('communications_root')}")
    print(f"  Signals: {config.get_path('signals_root')}")
    print(f"  Overnight (20241201): {config.get_communications_path('20241201')}")
    print(f"  Agent-1 Comms: {config.get_agent_communications_path('Agent-1', '20241201')}")
    print()


def reset_to_default():
    """Reset configuration to default values."""
    print("🔄 Resetting to Default Configuration")
    print("=" * 50)
    
    # Reset to default
    os.environ['REPOS_ROOT'] = 'D:/repos'
    os.environ['DEFAULT_OWNER'] = 'Dadudekc'
    
    # Clear custom paths
    if 'COMMUNICATIONS_ROOT' in os.environ:
        del os.environ['COMMUNICATIONS_ROOT']
    if 'AGENT_WORKSPACES_ROOT' in os.environ:
        del os.environ['AGENT_WORKSPACES_ROOT']
    
    # Reload configuration
    config.update_environment()
    
    # Show results
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"👤 Owner: {get_owner_path()}")
    print(f"🤖 Agent-1 Workspace: {get_agent_workspace_path('Agent-1')}")
    print(f"📡 Communications: {config.get_path('communications_root')}")
    print()


def main():
    """Run all demonstrations."""
    print("🚀 CONFIGURABLE PATHS SYSTEM DEMONSTRATION")
    print("=" * 60)
    print("This script demonstrates how easy it is to change where agents")
    print("focus their work by simply updating environment variables.")
    print("No more hardcoded paths!")
    print()
    
    # Run demonstrations
    demo_personal_projects()
    demo_company_projects()
    demo_cross_platform()
    demo_custom_communications()
    demo_agent_workspaces()
    demo_communications_structure()
    
    # Reset to default
    reset_to_default()
    
    print("🎉 DEMONSTRATION COMPLETE!")
    print("=" * 60)
    print("💡 Key Benefits:")
    print("  ✅ Zero hardcoded paths")
    print("  ✅ Easy project focus switching")
    print("  ✅ Cross-platform compatibility")
    print("  ✅ Flexible directory structure")
    print("  ✅ Environment-based configuration")
    print()
    print("🔧 To configure your own project focus:")
    print("  python configure_project_focus.py --repos-root 'C:/my-projects' --owner 'MyName'")
    print()
    print("📖 For more information, see: CONFIGURABLE_PATHS_README.md")


if __name__ == "__main__":
    main()
