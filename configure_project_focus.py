#!/usr/bin/env python3
"""
Configure Project Focus Script

This script demonstrates how easy it is to change where agents focus their work
by simply setting environment variables. No more hardcoded paths!

Usage Examples:
    # Focus on your personal projects
    python configure_project_focus.py --repos-root "C:/my-projects" --owner "MyName"
    
    # Focus on company projects
    python configure_project_focus.py --repos-root "D:/company-projects" --owner "CompanyName"
    
    # Focus on a different drive
    python configure_project_focus.py --repos-root "E:/development" --owner "DevTeam"
    
    # Just show current configuration
    python configure_project_focus.py --show
"""

import argparse
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


def show_current_config():
    """Display the current configuration."""
    print("🔧 Current Project Focus Configuration:")
    print("=" * 50)
    config.print_configuration()
    
    print("\n📋 Example Agent Workspace Paths:")
    print(f"  Agent-1: {get_agent_workspace_path('Agent-1')}")
    print(f"  Agent-2: {get_agent_workspace_path('Agent-2')}")
    print(f"  Agent-3: {get_agent_workspace_path('Agent-3')}")
    print(f"  Agent-4: {get_agent_workspace_path('Agent-4')}")
    print(f"  Agent-5: {get_agent_workspace_path('Agent-5')}")


def update_config(repos_root: str, owner: str, communications_root: str = None, agent_workspaces_root: str = None):
    """Update the configuration with new values."""
    print(f"🔄 Updating Project Focus Configuration...")
    print(f"  📁 Repos Root: {repos_root}")
    print(f"  👤 Owner: {owner}")
    if communications_root:
        print(f"  📁 Communications Root: {communications_root}")
    if agent_workspaces_root:
        print(f"  📁 Agent Workspaces Root: {agent_workspaces_root}")
    
    # Update environment variables
    os.environ['REPOS_ROOT'] = repos_root
    os.environ['DEFAULT_OWNER'] = owner
    
    if communications_root:
        os.environ['COMMUNICATIONS_ROOT'] = communications_root
    if agent_workspaces_root:
        os.environ['AGENT_WORKSPACES_ROOT'] = agent_workspaces_root
    
    # Reload configuration
    config.update_environment()
    
    print("\n✅ Configuration Updated Successfully!")
    print("=" * 50)
    show_current_config()
    
    print(f"\n💡 To make this permanent, add these to your .env file:")
    print(f"   REPOS_ROOT={repos_root}")
    print(f"   DEFAULT_OWNER={owner}")
    if communications_root:
        print(f"   COMMUNICATIONS_ROOT={communications_root}")
    if agent_workspaces_root:
        print(f"   AGENT_WORKSPACES_ROOT={agent_workspaces_root}")


def main():
    parser = argparse.ArgumentParser(
        description="Configure where agents focus their work",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Focus on personal projects
  python configure_project_focus.py --repos-root "C:/my-projects" --owner "MyName"
  
  # Focus on company projects with custom communications
  python configure_project_focus.py --repos-root "D:/company-projects" --owner "CompanyName" --communications "D:/company-projects/comms"
  
  # Just show current configuration
  python configure_project_focus.py --show
        """
    )
    
    parser.add_argument(
        '--repos-root',
        help='Root directory for all repositories (e.g., "C:/projects", "D:/repos")'
    )
    parser.add_argument(
        '--owner',
        help='Default organization/owner name (e.g., "MyName", "CompanyName")'
    )
    parser.add_argument(
        '--communications',
        help='Custom communications root (optional, defaults to REPOS_ROOT/communications)'
    )
    parser.add_argument(
        '--agent-workspaces',
        help='Custom agent workspaces root (optional, defaults to REPOS_ROOT/owner)'
    )
    parser.add_argument(
        '--show',
        action='store_true',
        help='Show current configuration without making changes'
    )
    
    args = parser.parse_args()
    
    if args.show:
        show_current_config()
        return
    
    if not args.repos_root or not args.owner:
        print("❌ Error: --repos-root and --owner are required (unless using --show)")
        print("   Use --help for usage information")
        sys.exit(1)
    
    # Validate paths
    repos_path = Path(args.repos_root)
    if not repos_path.exists():
        print(f"⚠️  Warning: Repos root directory '{repos_path}' does not exist.")
        print("   The directory will be created when needed.")
    
    # Update configuration
    update_config(
        repos_root=args.repos_root,
        owner=args.owner,
        communications_root=args.communications,
        agent_workspaces_root=args.agent_workspaces
    )


if __name__ == "__main__":
    main()
