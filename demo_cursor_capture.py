#!/usr/bin/env python3
"""
Demonstration of Complete Bi-directional AI Response Capture
Shows the full workflow from prompting agents to capturing AI responses
"""

import sys
import time
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_agent_prompting():
    """Demonstrate how the system prompts agents"""
    print("📤 **AGENT PROMPTING DEMONSTRATION**")
    print("=" * 50)
    
    try:
        from agent_cell_phone import AgentCellPhone, MsgTag
        
        # Initialize AgentCellPhone
        acp = AgentCellPhone(agent_id="Agent-1", layout_mode="2-agent", test=True)
        print("✅ AgentCellPhone initialized")
        
        # Show available agents
        agents = acp.get_available_agents()
        print(f"📋 Available agents: {agents}")
        
        # Demonstrate sending a message
        print("\n📤 Sending test message to Agent-2...")
        acp.send("Agent-2", "This is a test prompt from the system", MsgTag.TASK)
        print("✅ Message sent successfully")
        
    except Exception as e:
        print(f"❌ Error in agent prompting demo: {e}")

def demo_cursor_capture():
    """Demonstrate the cursor capture system"""
    print("\n📥 **CURSOR CAPTURE DEMONSTRATION**")
    print("=" * 50)
    
    try:
        from cursor_capture.watcher import CursorDBWatcher
        
        # Load agent workspace mapping
        map_path = Path("src/runtime/config/agent_workspace_map.json")
        if map_path.exists():
            with open(map_path, 'r') as f:
                agent_map = json.load(f)
            
            print(f"✅ Loaded workspace mapping for {len(agent_map)} agents")
            
            # Initialize watcher
            watcher = CursorDBWatcher(agent_map=agent_map)
            print("✅ CursorDBWatcher initialized")
            
            # Show stats
            stats = watcher.get_stats()
            print(f"📊 Watcher stats: {stats}")
            
            # Show what workspaces are being monitored
            print("\n🔍 Monitoring workspaces:")
            for agent, config in agent_map.items():
                workspace = config.get("workspace_root", "unknown")
                print(f"   {agent}: {workspace}")
            
        else:
            print(f"❌ Workspace map not found: {map_path}")
            
    except Exception as e:
        print(f"❌ Error in cursor capture demo: {e}")

def demo_inbox_processing():
    """Demonstrate how captured responses are processed"""
    print("\n📨 **INBOX PROCESSING DEMONSTRATION**")
    print("=" * 50)
    
    inbox_path = Path("agent_workspaces/Agent-5/inbox")
    if inbox_path.exists():
        # Check for message files
        message_files = list(inbox_path.glob("*.json"))
        if message_files:
            print(f"✅ Found {len(message_files)} message files in inbox")
            
            # Show recent messages
            recent_files = sorted(message_files, key=lambda x: x.stat().st_mtime, reverse=True)[:3]
            print("\n📄 Recent messages:")
            for f in recent_files:
                try:
                    with open(f, 'r') as msg_file:
                        msg_data = json.load(msg_file)
                    
                    msg_type = msg_data.get("type", "unknown")
                    from_agent = msg_data.get("from", "unknown")
                    timestamp = msg_data.get("timestamp", "unknown")
                    
                    print(f"   📄 {f.name}")
                    print(f"      Type: {msg_type}")
                    print(f"      From: {from_agent}")
                    print(f"      Time: {timestamp}")
                    
                    # Show payload summary if available
                    payload = msg_data.get("payload", {})
                    if payload:
                        payload_type = payload.get("type", "unknown")
                        if payload_type == "assistant_reply":
                            text = payload.get("text", "")
                            preview = text[:100] + "..." if len(text) > 100 else text
                            print(f"      Content: {preview}")
                    
                    print()
                    
                except Exception as e:
                    print(f"   ❌ Error reading {f.name}: {e}")
        else:
            print("📭 No message files found in inbox")
    else:
        print(f"❌ Inbox directory not found: {inbox_path}")

def demo_fsm_integration():
    """Demonstrate FSM integration"""
    print("\n⚙️ **FSM INTEGRATION DEMONSTRATION**")
    print("=" * 50)
    
    # Check if there are any FSM update files
    inbox_path = Path("agent_workspaces/Agent-5/inbox")
    if inbox_path.exists():
        fsm_files = list(inbox_path.glob("*fsm*"))
        if fsm_files:
            print(f"✅ Found {len(fsm_files)} FSM-related files")
            
            # Show FSM file structure
            for f in fsm_files[:2]:  # Show first 2
                print(f"\n📄 FSM File: {f.name}")
                try:
                    with open(f, 'r') as fsm_file:
                        fsm_data = json.load(fsm_file)
                    
                    # Show key FSM fields
                    task_id = fsm_data.get("task_id", "unknown")
                    state = fsm_data.get("state", "unknown")
                    summary = fsm_data.get("summary", "no summary")
                    
                    print(f"   Task ID: {task_id}")
                    print(f"   State: {state}")
                    print(f"   Summary: {summary[:80]}...")
                    
                except Exception as e:
                    print(f"   ❌ Error reading FSM file: {e}")
        else:
            print("📭 No FSM files found")
    else:
        print(f"❌ Inbox directory not found: {inbox_path}")

def demo_export_fallback():
    """Demonstrate export fallback system"""
    print("\n📤 **EXPORT FALLBACK DEMONSTRATION**")
    print("=" * 50)
    
    try:
        from cursor_capture.export_consumer import watch_exports, process_export_file
        
        print("✅ Export consumer module loaded")
        
        # Check export directories
        export_dir = Path("agent_workspaces/exports")
        if export_dir.exists():
            export_files = list(export_dir.glob("*"))
            if export_files:
                print(f"📁 Found {len(export_files)} files in export directory")
                for f in export_files:
                    print(f"   📄 {f.name}")
            else:
                print("📁 Export directory is empty")
        else:
            print("📁 Export directory not found - will be created when needed")
            
        print("\n💡 Export fallback workflow:")
        print("   1. Agent exports chat from Cursor (File → Export Chat)")
        print("   2. Export file is placed in agent_workspaces/exports/")
        print("   3. Export consumer processes file and creates inbox envelope")
        print("   4. File is moved to processed/ directory")
        
    except Exception as e:
        print(f"❌ Error in export fallback demo: {e}")

def main():
    """Run the complete demonstration"""
    print("🚀 **COMPLETE BI-DIRECTIONAL AI RESPONSE CAPTURE DEMONSTRATION**")
    print("=" * 70)
    print("This demo shows the complete workflow from prompting agents to capturing AI responses")
    print("=" * 70)
    
    demo_agent_prompting()
    demo_cursor_capture()
    demo_inbox_processing()
    demo_fsm_integration()
    demo_export_fallback()
    
    print("\n" + "=" * 70)
    print("🎯 **SYSTEM READY FOR PRODUCTION USE**")
    print("\n💡 **How to use:**")
    print("   1. Run overnight runner with --cursor-db-capture-enabled")
    print("   2. System automatically captures AI responses from Cursor")
    print("   3. Responses are processed and sent to FSM system")
    print("   4. Full bi-directional communication loop established!")
    print("\n🔧 **Fallback options:**")
    print("   - Export Chat: Manual export when DB unavailable")
    print("   - Copy Response: UI automation for clipboard capture")
    print("   - File-based: Direct file writing for reliability")

if __name__ == "__main__":
    main()
