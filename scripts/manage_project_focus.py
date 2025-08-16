#!/usr/bin/env python3
"""
Project Focus Management Script

A user-friendly command-line interface for managing which projects your agents focus on.
This eliminates the need to manually edit JSON configuration files.

Usage:
    python manage_project_focus.py [command] [options]

Commands:
    list                    - List all projects and agent assignments
    add-project            - Add a new project
    remove-project         - Remove a project
    assign                 - Assign a project to an agent
    unassign               - Remove a project from an agent
    set-priority           - Set project priority
    agent-workload         - Show agent workload information
    system-overview        - Show system overview
    export                 - Export configuration to file
    reload                 - Reload configuration from file
    help                   - Show this help message

Examples:
    python manage_project_focus.py list
    python manage_project_focus.py add-project "MyNewProject" "web_development" 2 "A new web project" "repos/myproject"
    python manage_project_focus.py assign "MyNewProject" "Agent-1" --primary
    python manage_project_focus.py set-priority "MyNewProject" 1
"""

import sys
import argparse
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.project_focus_manager import ProjectFocusManager
except ImportError as e:
    print(f"Error importing ProjectFocusManager: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def print_banner():
    """Print a nice banner for the script"""
    print("=" * 60)
    print("🤖 AGENT PROJECT FOCUS MANAGER")
    print("=" * 60)
    print("Manage which projects your agents work on dynamically!")
    print()

def list_projects(manager: ProjectFocusManager):
    """List all projects and their assignments"""
    print("📋 PROJECT OVERVIEW")
    print("-" * 40)
    
    # Get system overview
    overview = manager.get_system_overview()
    
    print(f"Total Projects: {overview['total_projects']}")
    print(f"Active Projects: {overview['active_projects']}")
    print(f"Total Agents: {overview['total_agents']}")
    print()
    
    # List all projects
    print("📁 PROJECTS:")
    for project_name in manager.get_project_priority_order():
        project = manager.get_project_info(project_name)
        if project:
            agents = manager.get_agents_for_project(project_name)
            status = "🟢 ACTIVE" if project.active else "🔴 INACTIVE"
            print(f"  {status} {project.name} (Priority: {project.priority})")
            print(f"    Category: {project.category}")
            print(f"    Description: {project.description}")
            print(f"    Repository: {project.repository_path}")
            print(f"    Assigned Agents: {', '.join(agents) if agents else 'None'}")
            print()
    
    # List agent workloads
    print("👥 AGENT WORKLOADS:")
    for agent_id in overview['agent_workloads']:
        workload = overview['agent_workloads'][agent_id]
        if 'error' not in workload:
            utilization = workload['utilization_percent']
            status_icon = "🟢" if utilization < 80 else "🟡" if utilization < 100 else "🔴"
            print(f"  {status_icon} {agent_id}: {workload['current_load']}/{workload['max_capacity']} projects ({utilization:.1f}% utilization)")
            print(f"    Primary: {', '.join(workload['primary_projects']) if workload['primary_projects'] else 'None'}")
            print(f"    Secondary: {', '.join(workload['secondary_projects']) if workload['secondary_projects'] else 'None'}")
            print()

def add_project(manager: ProjectFocusManager, args):
    """Add a new project"""
    print(f"➕ ADDING NEW PROJECT: {args.name}")
    print("-" * 40)
    
    success = manager.add_project(
        name=args.name,
        category=args.category,
        priority=args.priority,
        description=args.description,
        repository_path=args.repository_path,
        active=args.active
    )
    
    if success:
        print(f"✅ Successfully added project '{args.name}'")
        print(f"   Category: {args.category}")
        print(f"   Priority: {args.priority}")
        print(f"   Repository: {args.repository_path}")
        print(f"   Active: {args.active}")
    else:
        print(f"❌ Failed to add project '{args.name}'")
        print("   Check the logs for more details")

def remove_project(manager: ProjectFocusManager, args):
    """Remove a project"""
    print(f"🗑️  REMOVING PROJECT: {args.name}")
    print("-" * 40)
    
    # Confirm removal
    confirm = input(f"Are you sure you want to remove project '{args.name}'? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Project removal cancelled")
        return
    
    success = manager.remove_project(args.name)
    
    if success:
        print(f"✅ Successfully removed project '{args.name}'")
    else:
        print(f"❌ Failed to remove project '{args.name}'")
        print("   Check the logs for more details")

def assign_project(manager: ProjectFocusManager, args):
    """Assign a project to an agent"""
    print(f"🔗 ASSIGNING PROJECT: {args.project} → {args.agent}")
    print("-" * 40)
    
    assignment_type = "primary" if args.primary else "secondary"
    success = manager.assign_project_to_agent(
        project_name=args.project,
        agent_id=args.agent,
        is_primary=args.primary
    )
    
    if success:
        print(f"✅ Successfully assigned '{args.project}' to '{args.agent}' as {assignment_type}")
    else:
        print(f"❌ Failed to assign '{args.project}' to '{args.agent}'")
        print("   Check the logs for more details")

def set_priority(manager: ProjectFocusManager, args):
    """Set project priority"""
    print(f"🎯 SETTING PRIORITY: {args.project} → {args.priority}")
    print("-" * 40)
    
    # This would require adding a method to ProjectFocusManager
    print("⚠️  Priority setting not yet implemented in ProjectFocusManager")
    print("   You can manually edit the config file for now")

def show_agent_workload(manager: ProjectFocusManager, args):
    """Show agent workload information"""
    if args.agent:
        print(f"👤 AGENT WORKLOAD: {args.agent}")
        print("-" * 40)
        workload = manager.get_agent_workload(args.agent)
        
        if 'error' in workload:
            print(f"❌ {workload['error']}")
        else:
            utilization = workload['utilization_percent']
            status_icon = "🟢" if utilization < 80 else "🟡" if utilization < 100 else "🔴"
            print(f"Status: {status_icon} {utilization:.1f}% utilization")
            print(f"Current Load: {workload['current_load']}/{workload['max_capacity']} projects")
            print(f"Focus Area: {workload['focus_area']}")
            print(f"Primary Projects: {', '.join(workload['primary_projects']) if workload['primary_projects'] else 'None'}")
            print(f"Secondary Projects: {', '.join(workload['secondary_projects']) if workload['secondary_projects'] else 'None'}")
    else:
        print("👥 ALL AGENT WORKLOADS:")
        print("-" * 40)
        overview = manager.get_system_overview()
        
        for agent_id, workload in overview['agent_workloads'].items():
            if 'error' not in workload:
                utilization = workload['utilization_percent']
                status_icon = "🟢" if utilization < 80 else "🟡" if utilization < 100 else "🔴"
                print(f"  {status_icon} {agent_id}: {workload['current_load']}/{workload['max_capacity']} projects ({utilization:.1f}% utilization)")

def show_system_overview(manager: ProjectFocusManager):
    """Show system overview"""
    print("🏗️  SYSTEM OVERVIEW")
    print("-" * 40)
    
    overview = manager.get_system_overview()
    
    print(f"Total Projects: {overview['total_projects']}")
    print(f"Active Projects: {overview['active_projects']}")
    print(f"Total Agents: {overview['total_agents']}")
    print(f"Project Categories: {', '.join(overview['project_categories'])}")
    print()
    
    print("Agent Utilization:")
    for agent_id, workload in overview['agent_workloads'].items():
        if 'error' not in workload:
            utilization = workload['utilization_percent']
            status_icon = "🟢" if utilization < 80 else "🟡" if utilization < 100 else "🔴"
            print(f"  {status_icon} {agent_id}: {utilization:.1f}%")

def export_config(manager: ProjectFocusManager, args):
    """Export configuration to file"""
    print(f"💾 EXPORTING CONFIGURATION TO: {args.file}")
    print("-" * 40)
    
    success = manager.export_config(args.file)
    
    if success:
        print(f"✅ Successfully exported configuration to '{args.file}'")
    else:
        print(f"❌ Failed to export configuration to '{args.file}'")

def reload_config(manager: ProjectFocusManager):
    """Reload configuration from file"""
    print("🔄 RELOADING CONFIGURATION")
    print("-" * 40)
    
    manager.reload_config()
    print("✅ Configuration reloaded successfully")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description="Manage agent project focus configurations dynamically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    subparsers.add_parser('list', help='List all projects and agent assignments')
    
    # Add project command
    add_parser = subparsers.add_parser('add-project', help='Add a new project')
    add_parser.add_argument('name', help='Project name')
    add_parser.add_argument('category', help='Project category')
    add_parser.add_argument('priority', type=int, help='Project priority (1=highest, 5=lowest)')
    add_parser.add_argument('description', help='Project description')
    add_parser.add_argument('repository_path', help='Repository path')
    add_parser.add_argument('--active', action='store_true', default=True, help='Set project as active')
    
    # Remove project command
    remove_parser = subparsers.add_parser('remove-project', help='Remove a project')
    remove_parser.add_argument('name', help='Project name to remove')
    
    # Assign command
    assign_parser = subparsers.add_parser('assign', help='Assign a project to an agent')
    assign_parser.add_argument('project', help='Project name')
    assign_parser.add_argument('agent', help='Agent ID')
    assign_parser.add_argument('--primary', action='store_true', help='Assign as primary project')
    
    # Set priority command
    priority_parser = subparsers.add_parser('set-priority', help='Set project priority')
    priority_parser.add_argument('project', help='Project name')
    priority_parser.add_argument('priority', type=int, help='New priority (1=highest, 5=lowest)')
    
    # Agent workload command
    workload_parser = subparsers.add_parser('agent-workload', help='Show agent workload information')
    workload_parser.add_argument('--agent', help='Specific agent ID (optional)')
    
    # System overview command
    subparsers.add_parser('system-overview', help='Show system overview')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export configuration to file')
    export_parser.add_argument('file', help='Export file path')
    
    # Reload command
    subparsers.add_parser('reload', help='Reload configuration from file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        # Initialize project focus manager
        manager = ProjectFocusManager()
        
        print_banner()
        
        # Execute command
        if args.command == 'list':
            list_projects(manager)
        elif args.command == 'add-project':
            add_project(manager, args)
        elif args.command == 'remove-project':
            remove_project(manager, args)
        elif args.command == 'assign':
            assign_project(manager, args)
        elif args.command == 'set-priority':
            set_priority(manager, args)
        elif args.command == 'agent-workload':
            show_agent_workload(manager, args)
        elif args.command == 'system-overview':
            show_system_overview(manager)
        elif args.command == 'export':
            export_config(manager, args)
        elif args.command == 'reload':
            reload_config(manager)
        else:
            print(f"Unknown command: {args.command}")
            parser.print_help()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Check the logs for more details")
        sys.exit(1)

if __name__ == "__main__":
    main()
