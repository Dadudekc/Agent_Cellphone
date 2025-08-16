#!/usr/bin/env python3
"""
FSM Integration Demo
===================
Demonstrates the FSM orchestrator integration with the overnight runner.
"""

import json
import tempfile
import time
from pathlib import Path
import threading

# Import the FSM orchestrator
from src.core.fsm_orchestrator import FSMOrchestrator

def demo_fsm_integration():
    """Demonstrate FSM orchestrator integration"""
    print("🚀 FSM Integration Demo Starting...")
    
    # Create temporary environment
    temp_root = Path(tempfile.mkdtemp(prefix="fsm_integration_demo_"))
    fsm_root = temp_root / "fsm_data"
    inbox_root = temp_root / "runtime/fsm_bridge/outbox"
    outbox_root = temp_root / "communications/overnight_20250815_/Agent-5/verifications"
    
    # Create directory structure
    fsm_root.mkdir(parents=True, exist_ok=True)
    inbox_root.mkdir(parents=True, exist_ok=True)
    outbox_root.mkdir(parents=True, exist_ok=True)
    (fsm_root / "tasks").mkdir(exist_ok=True)
    (fsm_root / "workflows").mkdir(exist_ok=True)
    
    print(f"📁 Created demo environment:")
    print(f"   FSM Root: {fsm_root}")
    print(f"   Inbox: {inbox_root}")
    print(f"   Outbox: {outbox_root}")
    
    try:
        # Initialize FSM Orchestrator (as runner does)
        print("\n🔧 Initializing FSM Orchestrator...")
        orchestrator = FSMOrchestrator(
            fsm_root=fsm_root,
            inbox_root=inbox_root,
            outbox_root=outbox_root
        )
        
        # Start monitoring in background thread (as runner does)
        print("🔄 Starting FSM monitoring in background thread...")
        fsm_thread = threading.Thread(
            target=orchestrator.monitor_inbox,
            kwargs={"poll_interval": 2},
            daemon=True
        )
        fsm_thread.start()
        
        # Wait for monitoring to start
        time.sleep(0.5)
        print(f"✅ FSM monitoring active: {orchestrator.is_monitoring()}")
        
        # Simulate agent responses (as would come from inbox consumer)
        print("\n📨 Simulating agent responses...")
        
        # Agent-1 completes a task
        agent1_update = {
            "event": "AGENT_REPORT",
            "agent": "Agent-1",
            "task": "Wire FSM Bridge Integration",
            "actions": ["Created FSM orchestrator", "Integrated with runner"],
            "commit_message": "feat: integrate FSM orchestrator with overnight runner",
            "status": "Completed - FSM orchestrator successfully integrated",
            "raw": "Task: Wire FSM Bridge Integration\nActions:\n- Created FSM orchestrator in src/core/\n- Added integration tests\n- Wired orchestrator to overnight runner\n- Added FSM-driven message plan\nCommit Message: feat: integrate FSM orchestrator with overnight runner\nStatus: Completed - FSM orchestrator successfully integrated",
            "timestamp": "2025-08-15T22:00:00"
        }
        
        # Agent-2 reports progress
        agent2_update = {
            "event": "AGENT_REPORT",
            "agent": "Agent-2",
            "task": "Add Integration Tests",
            "actions": ["Created test suite", "Added runner integration tests"],
            "commit_message": "test: add FSM runner integration tests",
            "status": "In progress - tests passing, adding more coverage",
            "raw": "Task: Add Integration Tests\nActions:\n- Created test suite for FSM orchestrator\n- Added runner integration tests\n- Tests passing successfully\nCommit Message: test: add FSM runner integration tests\nStatus: In progress - tests passing, adding more coverage",
            "timestamp": "2025-08-15T22:15:00"
        }
        
        # Write updates to inbox
        updates = [agent1_update, agent2_update]
        for i, update in enumerate(updates):
            update_file = inbox_root / f"fsm_update_{i}.json"
            update_file.write_text(json.dumps(update, indent=2), encoding="utf-8")
            print(f"   📝 Created update {i+1}: {update['agent']} - {update['task']}")
        
        # Wait for processing
        print("\n⏳ Waiting for FSM processing...")
        time.sleep(5)
        
        # Check results
        print("\n📊 FSM Processing Results:")
        
        # Check tasks created
        task_files = list((fsm_root / "tasks").glob("*.json"))
        print(f"   📋 Tasks created: {len(task_files)}")
        for task_file in task_files:
            task_data = json.loads(task_file.read_text())
            print(f"      - {task_data['name']} ({task_data['status']})")
        
        # Check verifications emitted
        ver_files = list(outbox_root.glob("verification_*.json"))
        print(f"   ✅ Verifications emitted: {len(ver_files)}")
        for ver_file in ver_files:
            ver_data = json.loads(ver_file.read_text())
            print(f"      - {ver_data['task_id']} by {ver_data['agent']}")
        
        # Get status summary
        status = orchestrator.get_status_summary()
        print(f"\n📈 FSM Status Summary:")
        print(f"   Total tasks: {status['total_tasks']}")
        print(f"   Completed: {status['completed_tasks']}")
        print(f"   In progress: {status['in_progress_tasks']}")
        print(f"   Updates processed: {status['processed_updates']}")
        
        # Stop monitoring
        print("\n🛑 Stopping FSM monitoring...")
        orchestrator.stop_monitoring()
        fsm_thread.join(timeout=2.0)
        print(f"✅ FSM monitoring stopped: {orchestrator.is_monitoring()}")
        
        print("\n🎉 FSM Integration Demo Completed Successfully!")
        print("\n📋 What was demonstrated:")
        print("   ✅ FSM Orchestrator initialization")
        print("   ✅ Background thread monitoring (as runner does)")
        print("   ✅ Agent response processing")
        print("   ✅ Task state management")
        print("   ✅ Verification message emission")
        print("   ✅ Status reporting")
        print("   ✅ Graceful shutdown")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Cleanup
        import shutil
        if temp_root.exists():
            shutil.rmtree(temp_root, ignore_errors=True)
            print(f"\n🧹 Cleaned up demo environment: {temp_root}")

if __name__ == "__main__":
    success = demo_fsm_integration()
    exit(0 if success else 1)
