#!/usr/bin/env python3
"""
Test script for Cursor AI Response Capture System
Tests the database reading and message extraction functionality
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_cursor_storage_path():
    """Test finding the Cursor workspace storage directory"""
    print("🧪 Testing Cursor workspace storage path...")
    
    try:
        from cursor_capture.db_reader import cursor_workspace_storage
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
        from cursor_capture.db_reader import find_state_db_for_workspace
        
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
        from cursor_capture.db_reader import extract_messages
        
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

def test_watcher_initialization():
    """Test CursorDBWatcher initialization"""
    print("\n🧪 Testing CursorDBWatcher initialization...")
    
    try:
        from cursor_capture.watcher import CursorDBWatcher
        
        # Test with sample agent map
        test_agent_map = {
            "Agent-1": {"workspace_root": "D:/repos/project-A"},
            "Agent-2": {"workspace_root": "D:/repos/project-B"}
        }
        
        watcher = CursorDBWatcher(agent_map=test_agent_map)
        print("✅ CursorDBWatcher initialized successfully")
        
        # Test stats
        stats = watcher.get_stats()
        print(f"✅ Watcher stats: {stats}")
        
    except Exception as e:
        print(f"❌ Error initializing watcher: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing Cursor AI Response Capture System")
    print("=" * 60)
    
    test_cursor_storage_path()
    test_workspace_mapping()
    test_database_finding()
    test_message_extraction()
    test_watcher_initialization()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("\n💡 To test with real data:")
    print("   1. Open a workspace in Cursor")
    print("   2. Have a chat conversation")
    print("   3. Run the overnight runner with --cursor-db-capture-enabled")

if __name__ == "__main__":
    main()
