#!/usr/bin/env python3
"""
FSM Bridge for Overnight Runner

This module provides a bridge between the overnight runner and the FSM system,
allowing for state management and task orchestration.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

# Ensure package root and src/ are on path for direct script execution
_THIS = Path(__file__).resolve()
sys.path.insert(0, str(_THIS.parents[1]))
sys.path.insert(0, str(_THIS.parents[1] / 'src'))

from src.core.config import get_owner_path, get_repos_root, get_communications_root  # type: ignore


# Use configurable paths instead of hardcoded ones
INBOX_ROOT = get_owner_path()
REPO_ROOT = get_owner_path()


def _P(path_str: str) -> Path:
    """Convert string to Path object."""
    return Path(path_str)


def _write_inbox_message(agent: str, message: Dict[str, Any]) -> bool:
    """Write a message to an agent's inbox."""
    try:
        inbox_dir = INBOX_ROOT / agent / "inbox"
        inbox_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"fsm_message_{timestamp}.json"
        filepath = inbox_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(message, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Message written to {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to write message to {agent} inbox: {e}")
        return False


def _read_inbox_messages(agent: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Read messages from an agent's inbox."""
    try:
        inbox_dir = INBOX_ROOT / agent / "inbox"
        if not inbox_dir.exists():
        return []
        
        messages = []
        for filepath in sorted(inbox_dir.glob("fsm_message_*.json"), reverse=True):
            if len(messages) >= limit:
                break
                
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    message = json.load(f)
                    message['_filepath'] = str(filepath)
                    messages.append(message)
            except Exception as e:
                print(f"⚠️  Failed to read {filepath}: {e}")
                continue
        
        return messages
        
    except Exception as e:
        print(f"❌ Failed to read inbox for {agent}: {e}")
        return []


def _scan_repositories_for_tasks() -> List[Dict[str, Any]]:
    """Scan all repositories for TASK_LIST.md entries and seed queued tasks."""
    tasks = []
    
    if not REPO_ROOT.exists():
        print(f"⚠️  Repository root {REPO_ROOT} does not exist")
    return tasks

    try:
        for repo in sorted(REPO_ROOT.iterdir()):
            if not repo.is_dir() or repo.name.startswith('.'):
                continue
                
            tasklist_file = repo / "TASK_LIST.md"
            if not tasklist_file.exists():
                continue
            
            try:
                # Read TASK_LIST.md and extract tasks
                content = tasklist_file.read_text(encoding='utf-8')
                
                # Simple task extraction (can be enhanced)
                lines = content.split('\n')
                current_task = None
                
                for line in lines:
                    line = line.strip()
                    if line.startswith('## '):
                        if current_task:
                            tasks.append(current_task)
                        
                        current_task = {
                            'repo': repo.name,
                            'title': line[3:],  # Remove '## '
                            'status': 'queued',
                            'created': datetime.now().isoformat(),
                            'filepath': str(tasklist_file)
                        }
                    elif line.startswith('- ') and current_task:
                        if 'description' not in current_task:
                            current_task['description'] = line[2:]  # Remove '- '
                
                if current_task:
                    tasks.append(current_task)
                    
            except Exception as e:
                print(f"⚠️  Failed to process {tasklist_file}: {e}")
                continue
        
        print(f"✅ Scanned {len(tasks)} tasks from repositories")
        return tasks
        
    except Exception as e:
        print(f"❌ Failed to scan repositories: {e}")
        return tasks


def _create_fsm_task(owner: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create an FSM task from task data."""
    return {
        "id": f"task-{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "type": "task",
        "owner": owner,
        "title": task_data.get('title', 'Untitled Task'),
        "description": task_data.get('description', 'No description'),
        "repo": task_data.get('repo', 'unknown'),
        "status": "queued",
        "priority": "medium",
        "created": datetime.now().isoformat(),
        "updated": datetime.now().isoformat(),
        "assignee": None,
        "evidence": [],
        "transitions": [],
        # Helpful context for downstream tools
        "workflow": "default",
        "repo_path": str(get_repos_root() / task_data.get('repo', '')),
        "comm_root_path": str(get_communications_root()),
    }


def process_fsm_update(agent: str, update_data: Dict[str, Any]) -> bool:
    """Process an FSM update from an agent."""
    try:
        # Validate update data
        required_fields = ['task_id', 'state', 'summary']
        for field in required_fields:
            if field not in update_data:
                print(f"❌ Missing required field: {field}")
                return False
        
        # Create FSM task if it doesn't exist
        task_id = update_data['task_id']
        state = update_data['state']
        summary = update_data['summary']
        
        # Write update to agent's inbox for FSM processing
        message = {
            "type": "fsm_update",
            "from": agent,
            "task_id": task_id,
            "state": state,
            "summary": summary,
            "evidence": update_data.get('evidence', []),
            "timestamp": datetime.now().isoformat(),
            "workflow": update_data.get('workflow', 'default')
        }
        
        return _write_inbox_message(agent, message)
        
    except Exception as e:
        print(f"❌ Failed to process FSM update: {e}")
        return False


def get_fsm_status(agent: str) -> Dict[str, Any]:
    """Get FSM status for a specific agent."""
    try:
        # Read recent messages from agent's inbox
        messages = _read_inbox_messages(agent, limit=20)
        
        # Filter for FSM-related messages
        fsm_messages = [msg for msg in messages if msg.get('type') in ['fsm_update', 'fsm_request']]
        
        # Get agent's current state
        state_file = INBOX_ROOT / agent / "state.json"
        current_state = {}
        if state_file.exists():
            try:
                current_state = json.loads(state_file.read_text(encoding='utf-8'))
    except Exception:
        pass
        
        return {
            "agent": agent,
            "current_state": current_state,
            "fsm_messages": fsm_messages,
            "last_update": current_state.get('updated', 'unknown'),
            "status": "active" if fsm_messages else "inactive"
        }
        
    except Exception as e:
        print(f"❌ Failed to get FSM status for {agent}: {e}")
        return {"agent": agent, "error": str(e)}


def seed_fsm_tasks(owner: str) -> List[Dict[str, Any]]:
    """Seed FSM with tasks from repository TASK_LIST.md files."""
    try:
        # Scan repositories for tasks
        repo_tasks = _scan_repositories_for_tasks()
        
        # Convert to FSM tasks
        fsm_tasks = []
        for task_data in repo_tasks:
            fsm_task = _create_fsm_task(owner, task_data)
            fsm_tasks.append(fsm_task)
        
        # Write tasks to FSM inbox
        for task in fsm_tasks:
            message = {
                "type": "fsm_task_seed",
                "task": task,
                "timestamp": datetime.now().isoformat()
            }
            _write_inbox_message("Agent-5", message)  # Send to FSM orchestrator
        
        print(f"✅ Seeded {len(fsm_tasks)} FSM tasks")
        return fsm_tasks
        
    except Exception as e:
        print(f"❌ Failed to seed FSM tasks: {e}")
        return []


def main():
    """Main entry point for testing."""
    print("🔧 FSM Bridge Test")
    print("=" * 50)
    
    # Test configuration
    print(f"📁 INBOX_ROOT: {INBOX_ROOT}")
    print(f"📁 REPO_ROOT: {REPO_ROOT}")
    print(f"📁 Repos Root: {get_repos_root()}")
    print(f"📁 Communications Root: {get_communications_root()}")
    
    # Test task seeding
    print("\n🌱 Testing task seeding...")
    tasks = seed_fsm_tasks("test_user")
    print(f"Seeded {len(tasks)} tasks")
    
    # Test FSM status
    print("\n📊 Testing FSM status...")
    status = get_fsm_status("Agent-1")
    print(f"Agent-1 status: {status.get('status', 'unknown')}")
    
    print("\n✅ FSM Bridge test completed")


if __name__ == "__main__":
    main()
