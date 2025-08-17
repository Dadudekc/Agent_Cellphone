#!/usr/bin/env python3
"""
Test script for Cursor AI Response Capture System
Tests the database reading and message extraction functionality
"""

import json
from pathlib import Path


def test_cursor_watcher_outputs_no_partial_files(tmp_path, monkeypatch):
    """Ensure CursorDBWatcher writes files atomically without leaving partial files."""
    from src.cursor_capture import watcher as watcher_mod
    from src.cursor_capture.watcher import CursorDBWatcher

    inbox = tmp_path / "inbox"
    seen_dir = tmp_path / ".seen"
    inbox.mkdir()
    seen_dir.mkdir()

    monkeypatch.setattr(watcher_mod, "INBOX", inbox)
    monkeypatch.setattr(watcher_mod, "SEEN_DIR", seen_dir)

    def fake_read_assistant_messages(ws, seen):
        return [{"sig": "1", "text": "hi", "ts": 1}]

    monkeypatch.setattr(watcher_mod, "read_assistant_messages", fake_read_assistant_messages)

    w = CursorDBWatcher({"Agent-1": {"workspace_root": "dummy"}})
    w._check_all_agents()

    files = list(inbox.glob("assistant_*.json"))
    assert len(files) == 1, "expected one output file"
    json.loads(files[0].read_text())
    assert not list(inbox.glob("*.tmp")), "temporary file should not remain"

def test_cursor_storage_path():
    """Test finding the Cursor workspace storage directory"""
    print("🧪 Testing Cursor workspace storage path...")
    
    try:
        from src.cursor_capture.db_reader import cursor_workspace_storage
        storage_path = cursor_workspace_storage()
        print(f"✅ Cursor storage path: {storage_path}")
        
        if storage_path.exists():
            print(f"✅ Storage directory exists")
            # List some workspace directories
            workspace_dirs = list(storage_path.glob("*"))[:5]
            print(f"✅ Found {len(workspace_dirs)} workspace directories")
            for d in workspace_dirs:
                print(f"   📁 {d.name}")
        else:
            print("❌ Storage directory does not exist")
            
    except Exception as e:
        print(f"❌ Error finding storage path: {e}")

def test_workspace_mapping():
    """Test agent workspace mapping configuration"""
    print("\n🧪 Testing agent workspace mapping...")
    
    map_path = Path("src/runtime/config/agent_workspace_map.json")
    if map_path.exists():
        try:
            with open(map_path, 'r') as f:
                mapping = json.load(f)
            print(f"✅ Agent workspace map loaded: {len(mapping)} agents")
            
            for agent, config in mapping.items():
                workspace = config.get("workspace_root", "unknown")
                print(f"   {agent}: {workspace}")
                
        except Exception as e:
            print(f"❌ Error loading workspace map: {e}")
    else:
        print(f"❌ Workspace map not found: {map_path}")

def test_database_finding():
    """Test finding state.vscdb files for workspaces"""
    print("\n🧪 Testing database finding...")
    
    try:
        from src.cursor_capture.db_reader import find_state_db_for_workspace
        
        # Test with a sample workspace path
        test_workspace = "D:/repos/project-A"
        db_path = find_state_db_for_workspace(test_workspace)
        
        if db_path:
            print(f"✅ Found database for {test_workspace}: {db_path}")
        else:
            print(f"⚠️  No database found for {test_workspace}")
            print("   This is normal if the workspace hasn't been opened in Cursor")
            
    except Exception as e:
        print(f"❌ Error finding database: {e}")

def test_message_extraction():
    """Test message extraction from sample data"""
    print("\n🧪 Testing message extraction...")
    
    try:
        from src.cursor_capture.db_reader import extract_messages
        
        # Test with sample chat data
        sample_data = {
            "chats": [
                {
                    "messages": [
                        {"role": "user", "content": "Hello, can you help me?"},
                        {"role": "assistant", "content": "Of course! I'd be happy to help you with your question."},
                        {"role": "user", "content": "Great, thanks!"}
                    ]
                }
            ]
        }
        
        messages = extract_messages(json.dumps(sample_data))
        print(f"✅ Extracted {len(messages)} messages from sample data")
        
        for msg in messages:
            print(f"   {msg['role']}: {msg['text'][:50]}...")
            
    except Exception as e:
        print(f"❌ Error extracting messages: {e}")

def test_agent_workspace_finding():
    """Test finding agent workspaces"""
    print("\n🧪 Testing agent workspace finding...")
    
    try:
        from src.cursor_capture.db_reader import find_agent_workspaces
        
        workspaces = find_agent_workspaces()
        print(f"✅ Found {len(workspaces)} agent workspaces")
        
        for agent, workspace in workspaces.items():
            print(f"   {agent}: {workspace}")
            
    except Exception as e:
        print(f"❌ Error finding agent workspaces: {e}")

def test_full_workflow():
    """Test the complete workflow from workspace to messages"""
    print("\n🧪 Testing complete workflow...")
    
    try:
        from src.cursor_capture.db_reader import cursor_workspace_storage, find_agent_workspaces, extract_messages
        
        # Get storage path
        storage_path = cursor_workspace_storage()
        print(f"✅ Storage path: {storage_path}")
        
        # Find agent workspaces
        agent_workspaces = find_agent_workspaces()
        print(f"✅ Agent workspaces: {len(agent_workspaces)} found")
        
        # Test with first available workspace
        if agent_workspaces:
            first_agent = list(agent_workspaces.keys())[0]
            workspace_path = agent_workspaces[first_agent]
            print(f"✅ Testing with workspace: {workspace_path}")
            
            # Try to extract messages
            try:
                messages = extract_messages(workspace_path)
                print(f"✅ Extracted {len(messages)} messages from {first_agent}")
            except Exception as e:
                print(f"⚠️  Could not extract messages (may need Cursor to be open): {e}")
        else:
            print("⚠️  No agent workspaces found to test")
            
    except Exception as e:
        print(f"❌ Error in full workflow test: {e}")

if __name__ == "__main__":
    print("🧪 Running Cursor Capture System Tests\n")
    print("=" * 50)
    
    test_cursor_storage_path()
    test_workspace_mapping()
    test_database_finding()
    test_message_extraction()
    test_agent_workspace_finding()
    test_full_workflow()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
