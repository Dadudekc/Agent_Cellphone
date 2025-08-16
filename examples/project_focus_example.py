#!/usr/bin/env python3
"""
Project Focus Manager Example

This script demonstrates how to use the ProjectFocusManager programmatically
to manage agent project assignments dynamically.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from core.project_focus_manager import ProjectFocusManager
except ImportError as e:
    print(f"Error importing ProjectFocusManager: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)

def main():
    """Demonstrate ProjectFocusManager functionality"""
    print("🚀 Project Focus Manager Example")
    print("=" * 50)
    
    # Initialize the manager
    print("\n1. Initializing ProjectFocusManager...")
    manager = ProjectFocusManager()
    print("✅ Manager initialized successfully")
    
    # Show current system overview
    print("\n2. Current System Overview:")
    overview = manager.get_system_overview()
    print(f"   Total Projects: {overview['total_projects']}")
    print(f"   Active Projects: {overview['active_projects']}")
    print(f"   Total Agents: {overview['total_agents']}")
    
    # List all projects
    print("\n3. Available Projects:")
    for project_name in manager.get_project_priority_order():
        project = manager.get_project_info(project_name)
        if project:
            status = "🟢 ACTIVE" if project.active else "🔴 INACTIVE"
            print(f"   {status} {project.name} (Priority: {project.priority})")
            print(f"     Category: {project.category}")
            print(f"     Description: {project.description}")
    
    # Show agent workloads
    print("\n4. Agent Workloads:")
    for agent_id in overview['agent_workloads']:
        workload = overview['agent_workloads'][agent_id]
        if 'error' not in workload:
            utilization = workload['utilization_percent']
            status_icon = "🟢" if utilization < 80 else "🟡" if utilization < 100 else "🔴"
            print(f"   {status_icon} {agent_id}: {workload['current_load']}/{workload['max_capacity']} projects ({utilization:.1f}% utilization)")
    
    # Demonstrate adding a new project
    print("\n5. Adding a New Project...")
    new_project_name = "ExampleProject"
    
    # Check if project already exists
    if manager.get_project_info(new_project_name):
        print(f"   Project '{new_project_name}' already exists, removing it first...")
        manager.remove_project(new_project_name)
    
    # Add new project
    success = manager.add_project(
        name=new_project_name,
        category="example",
        priority=3,
        description="An example project for demonstration",
        repository_path="examples/example_project",
        active=True
    )
    
    if success:
        print(f"   ✅ Successfully added project '{new_project_name}'")
    else:
        print(f"   ❌ Failed to add project '{new_project_name}'")
        return
    
    # Demonstrate assigning project to agent
    print("\n6. Assigning Project to Agent...")
    agent_id = "Agent-1"
    
    # Check current agent workload
    workload = manager.get_agent_workload(agent_id)
    if 'error' not in workload:
        print(f"   Current workload for {agent_id}: {workload['current_load']}/{workload['max_capacity']} projects")
        
        # Assign project as secondary
        success = manager.assign_project_to_agent(
            project_name=new_project_name,
            agent_id=agent_id,
            is_primary=False
        )
        
        if success:
            print(f"   ✅ Successfully assigned '{new_project_name}' to '{agent_id}' as secondary project")
        else:
            print(f"   ❌ Failed to assign '{new_project_name}' to '{agent_id}'")
    
    # Show updated agent workload
    print("\n7. Updated Agent Workload:")
    updated_workload = manager.get_agent_workload(agent_id)
    if 'error' not in updated_workload:
        print(f"   {agent_id} workload: {updated_workload['current_load']}/{updated_workload['max_capacity']} projects")
        print(f"   Primary: {', '.join(updated_workload['primary_projects']) if updated_workload['primary_projects'] else 'None'}")
        print(f"   Secondary: {', '.join(updated_workload['secondary_projects']) if updated_workload['secondary_projects'] else 'None'}")
    
    # Demonstrate project queries
    print("\n8. Project Queries:")
    
    # Get agents for the new project
    agents_for_project = manager.get_agents_for_project(new_project_name)
    print(f"   Agents working on '{new_project_name}': {', '.join(agents_for_project) if agents_for_project else 'None'}")
    
    # Get projects by category
    example_projects = manager.get_projects_by_category("example")
    print(f"   Projects in 'example' category: {[p.name for p in example_projects]}")
    
    # Get agent projects
    agent_projects = manager.get_agent_projects(agent_id)
    print(f"   All projects for {agent_id}: {', '.join(agent_projects) if agent_projects else 'None'}")
    
    # Clean up - remove the example project
    print("\n9. Cleaning Up...")
    success = manager.remove_project(new_project_name)
    if success:
        print(f"   ✅ Successfully removed example project '{new_project_name}'")
    else:
        print(f"   ❌ Failed to remove example project '{new_project_name}'")
    
    # Show final system overview
    print("\n10. Final System Overview:")
    final_overview = manager.get_system_overview()
    print(f"   Total Projects: {final_overview['total_projects']}")
    print(f"   Active Projects: {final_overview['active_projects']}")
    
    print("\n🎉 Example completed successfully!")
    print("\n💡 Key Takeaways:")
    print("   • ProjectFocusManager provides a clean API for managing agent assignments")
    print("   • Changes are automatically saved to configuration files")
    print("   • The system gracefully handles errors and provides fallbacks")
    print("   • You can easily integrate this into your existing agent coordination code")

def demonstrate_error_handling():
    """Demonstrate error handling capabilities"""
    print("\n🔧 Error Handling Demonstration:")
    print("-" * 40)
    
    try:
        # Try to get workload for non-existent agent
        manager = ProjectFocusManager()
        workload = manager.get_agent_workload("NonExistentAgent")
        
        if 'error' in workload:
            print(f"   ✅ Gracefully handled non-existent agent: {workload['error']}")
        else:
            print("   ❌ Expected error for non-existent agent")
        
        # Try to get non-existent project
        project = manager.get_project_info("NonExistentProject")
        if project is None:
            print("   ✅ Gracefully handled non-existent project: returned None")
        else:
            print("   ❌ Expected None for non-existent project")
            
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

if __name__ == "__main__":
    try:
        main()
        demonstrate_error_handling()
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc()
