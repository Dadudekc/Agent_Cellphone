#!/usr/bin/env python3
"""
Test script for standardizing agent status files
"""

import json
import os
from pathlib import Path
from datetime import datetime

def load_status_template():
    """Load the standardized status template."""
    template_file = Path("agent_workspaces/onboarding/status_template.json")
    try:
        with open(template_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading status template: {e}")
        return {}

def standardize_agent_status(agent_id: str) -> bool:
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
        
        # Load template
        template = load_status_template()
        if not template:
            return False
        
        # Create new standardized status
        new_status = template.copy()
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

def standardize_all_agents():
    """Standardize status.json for all agents."""
    print("🔧 Standardizing all agent status files...")
    
    agent_dirs = [d for d in Path("agent_workspaces").iterdir() 
                 if d.is_dir() and d.name.startswith("Agent-")]
    
    results = {}
    for agent_dir in agent_dirs:
        agent_id = agent_dir.name
        results[agent_id] = standardize_agent_status(agent_id)
    
    print("\n📊 Standardization Results:")
    for agent, success in results.items():
        print(f"  {agent}: {'✅' if success else '❌'}")
    
    return results

if __name__ == "__main__":
    standardize_all_agents()
