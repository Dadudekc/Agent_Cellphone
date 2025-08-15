#!/usr/bin/env python3
"""
Inbox Consumer - Bridges agent responses to FSM system
Processes captured agent responses and converts them to FSM events
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

# Configuration
INBOX_ROOT = Path("agent_workspaces/Agent-5/inbox")
OUTBOX_ROOT = Path("communications/overnight_YYYYMMDD_/Agent-5/fsm_update_inbox")

def ensure_outbox():
    """Ensure the outbox directory exists"""
    OUTBOX_ROOT.mkdir(parents=True, exist_ok=True)

def to_fsm_event(envelope: dict) -> dict:
    """Convert captured response envelope to FSM event format"""
    p = envelope.get("payload", {})
    
    if p.get("type") == "agent_report":
        return {
            "type": "fsm_update",
            "from": envelope.get("from", "unknown"),
            "to": "Agent-5",
            "timestamp": envelope.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%S")),
            "task_id": p.get("task", "unknown_task"),
            "state": "completed" if p.get("status", "").lower() in ["done", "completed", "finished"] else "in_progress",
            "summary": p.get("summary", p.get("commit_message", "Task completed")),
            "evidence": p.get("actions", []),
            "raw": p.get("raw", "")
        }
    
    # Fallback for freeform responses
    return {
        "type": "note",
        "from": envelope.get("from", "unknown"),
        "to": "Agent-5",
        "timestamp": envelope.get("timestamp", time.strftime("%Y-%m-%dT%H:%M:%S")),
        "summary": p.get("summary", "Agent response captured"),
        "raw": p.get("raw", "")
    }

def process_inbox():
    """Process all files in the inbox directory"""
    if not INBOX_ROOT.exists():
        return
    
    for f in sorted(INBOX_ROOT.glob("*.json")):
        try:
            # Read and parse the envelope
            env = json.loads(f.read_text(encoding="utf-8"))
            
            # Convert to FSM event format
            ev = to_fsm_event(env)
            
            # Write to outbox
            out = OUTBOX_ROOT / f.name
            out.write_text(json.dumps(ev, ensure_ascii=False, indent=2), encoding="utf-8")
            
            # Remove processed file
            f.unlink(missing_ok=True)
            
            print(f"[INBOX_CONSUMER] Processed {f.name} -> {ev.get('type', 'unknown')}")
            
        except Exception as e:
            print(f"Error processing {f.name}: {e}")

def main():
    """Main loop for processing inbox files"""
    print("Inbox Consumer starting...")
    print(f"Watching: {INBOX_ROOT}")
    print(f"Output: {OUTBOX_ROOT}")
    
    ensure_outbox()
    
    try:
        while True:
            process_inbox()
            time.sleep(0.5)  # Poll every 500ms
    except KeyboardInterrupt:
        print("\nInbox Consumer stopped")

if __name__ == "__main__":
    main()
