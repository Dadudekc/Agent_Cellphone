#!/usr/bin/env python3
"""
Inbox Consumer - FSM Bridge
===========================
Consumes agent response envelopes from the inbox and converts them to FSM events
for Agent-5 to process.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any

# Configuration
INBOX = Path("runtime/agent_comms/inbox")
OUTBOX = Path("communications/overnight_YYYYMMDD_/Agent-5/fsm_update_inbox")

def to_fsm_event(envelope: dict) -> dict:
    """Convert agent response envelope to FSM event format"""
    p = envelope.get("payload", {})
    
    if p.get("type") == "agent_report":
        return {
            "event": "AGENT_REPORT",
            "agent": envelope["agent"],
            "task": p.get("task"),
            "actions": p.get("actions", []),
            "commit_message": p.get("commit_message"),
            "status": p.get("status"),
            "raw": p.get("raw"),
            "timestamp": envelope.get("timestamp"),
            "ts": envelope.get("ts")
        }
    
    return {
        "event": "AGENT_FREEFORM",
        "agent": envelope["agent"],
        "summary": p.get("summary"),
        "raw": p.get("raw"),
        "timestamp": envelope.get("timestamp"),
        "ts": envelope.get("ts")
    }

def ensure_outbox():
    """Ensure the outbox directory exists"""
    OUTBOX.mkdir(parents=True, exist_ok=True)

def main():
    """Main processing loop"""
    print(f"Starting inbox consumer...")
    print(f"Watching: {INBOX}")
    print(f"Output: {OUTBOX}")
    
    ensure_outbox()
    
    processed_files = set()
    
    while True:
        try:
            # Process any new JSON files in the inbox
            for f in sorted(INBOX.glob("*.json")):
                if f.name in processed_files:
                    continue
                    
                try:
                    # Read and parse the envelope
                    env = json.loads(f.read_text(encoding="utf-8"))
                    print(f"Processing: {f.name}")
                    
                    # Convert to FSM event
                    ev = to_fsm_event(env)
                    
                    # Write to outbox
                    out_file = OUTBOX / f"fsm_{f.stem}.json"
                    out_file.write_text(
                        json.dumps(ev, ensure_ascii=False, indent=2), 
                        encoding="utf-8"
                    )
                    
                    # Mark as processed and remove from inbox
                    processed_files.add(f.name)
                    f.unlink(missing_ok=True)
                    
                    print(f"  -> {out_file.name} ({ev['event']})")
                    
                except Exception as e:
                    print(f"Error processing {f.name}: {e}")
                    # Move to error folder to avoid infinite retry
                    error_dir = INBOX / "errors"
                    error_dir.mkdir(exist_ok=True)
                    try:
                        f.rename(error_dir / f.name)
                    except:
                        pass
            
            # Clean up old processed file names (keep last 1000)
            if len(processed_files) > 1000:
                processed_files = set(list(processed_files)[-1000:])
                
        except Exception as e:
            print(f"Main loop error: {e}")
            
        time.sleep(0.5)

if __name__ == "__main__":
    main()
