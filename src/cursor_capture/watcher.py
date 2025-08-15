from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, List
from .db_reader import read_assistant_messages

# Configuration
INBOX = Path("agent_workspaces/Agent-5/inbox")
SEEN_DIR = Path("agent_workspaces/Agent-5/inbox/.seen")
INBOX.mkdir(parents=True, exist_ok=True)
SEEN_DIR.mkdir(parents=True, exist_ok=True)

class CursorDBWatcher:
    """Watches Cursor databases for new AI assistant messages and emits envelopes"""
    
    def __init__(self, agent_map: Dict[str, dict], poll_s: float = 1.0):
        self.agent_map = agent_map
        self.poll_s = poll_s
        self._running = False
        self._stats = {
            "total_messages": 0,
            "agents_seen": set(),
            "last_check": None
        }

    def _load_seen(self, agent: str) -> set[str]:
        """Load the set of seen message signatures for an agent"""
        p = SEEN_DIR / f"{agent}.json"
        if p.exists():
            try: 
                return set(json.loads(p.read_text(encoding="utf-8")))
            except Exception: 
                return set()
        return set()

    def _save_seen(self, agent: str, sigs: set[str]):
        """Save the set of seen message signatures for an agent"""
        (SEEN_DIR / f"{agent}.json").write_text(json.dumps(sorted(sigs)), encoding="utf-8")

    def get_stats(self) -> Dict:
        """Get current watcher statistics"""
        return {
            "total_messages": self._stats["total_messages"],
            "agents_seen": list(self._stats["agents_seen"]),
            "last_check": self._stats["last_check"],
            "running": self._running,
            "poll_interval": self.poll_s
        }

    def run(self):
        """Main watcher loop"""
        self._running = True
        print(f"[CURSOR_WATCHER] Started watching {len(self.agent_map)} agents")
        
        while self._running:
            try:
                self._check_all_agents()
                time.sleep(self.poll_s)
            except Exception as e:
                print(f"[CURSOR_WATCHER] Error in main loop: {e}")
                time.sleep(self.poll_s)

    def _check_all_agents(self):
        """Check all agents for new messages"""
        self._stats["last_check"] = time.time()
        
        for agent, meta in self.agent_map.items():
            ws = meta.get("workspace_root")
            if not ws: 
                continue
                
            try:
                seen = self._load_seen(agent)
                msgs = read_assistant_messages(ws, seen)
                
                if not msgs: 
                    continue
                    
                print(f"[CURSOR_WATCHER] Found {len(msgs)} new messages from {agent}")
                
                for m in msgs:
                    seen.add(m["sig"])
                    self._stats["total_messages"] += 1
                    self._stats["agents_seen"].add(agent)
                    
                    # Create envelope
                    env = {
                        "type": "assistant_reply",
                        "from": agent,
                        "to": "Agent-5",
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "agent": agent,
                        "ts": m.get("ts", int(time.time())),
                        "payload": {
                            "type": "assistant_reply",
                            "text": m["text"],
                            "message_id": m.get("id"),
                            "role": m.get("role", "assistant")
                        }
                    }
                    
                    # Write to inbox
                    out = INBOX / f"assistant_{int(time.time()*1000)}_{agent}.json"
                    out.write_text(json.dumps(env, ensure_ascii=False, indent=2), encoding="utf-8")
                    
                    print(f"[CURSOR_WATCHER] Captured AI response from {agent}: {len(m['text'])} chars")
                
                # Save updated seen signatures
                self._save_seen(agent, seen)
                
            except Exception as e:
                print(f"[CURSOR_WATCHER] Error processing {agent}: {e}")

    def stop(self): 
        """Stop the watcher"""
        self._running = False
        print("[CURSOR_WATCHER] Stopped")

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()
