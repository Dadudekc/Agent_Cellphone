from __future__ import annotations
import os
import json
import sqlite3
import hashlib
import time
import re
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

# Cross-platform Cursor workspaceStorage
def cursor_workspace_storage() -> Path:
    """Get the Cursor workspace storage directory for the current platform"""
    if os.name == "nt":  # Windows
        return Path(os.environ["APPDATA"]) / "Cursor" / "User" / "workspaceStorage"
    home = Path.home()
    if (home / "Library").exists():  # macOS
        return home / "Library" / "Application Support" / "Cursor" / "User" / "workspaceStorage"
    return home / ".config" / "Cursor" / "User" / "workspaceStorage"  # Linux

def find_state_db_for_workspace(workspace_root: str) -> Path | None:
    """Find the state.vscdb file for a specific workspace"""
    root = cursor_workspace_storage()
    if not root.exists():
        return None
        
    # Each hash dir has state.vscdb + workspace.json containing folder path
    for d in root.glob("*"):
        state_db = d / "state.vscdb"
        meta = d / "workspace.json"
        if state_db.is_file() and meta.is_file():
            try:
                m = json.loads(meta.read_text(encoding="utf-8"))
                if m.get("folder") == workspace_root:
                    return state_db
            except Exception:
                continue
    return None

# Known keys that store chat JSON (varies across Cursor versions)
CHAT_KEYS = (
    "workbench.panel.aichat.view.aichat.chatdata",
    "aichat.chatView.state",
    "cursor.chat.view.state",
    "aiService.prompts"  # historical, sometimes holds threads
)

# Pattern-based fallback for finding chat keys
KEY_LIKE_PATTERNS = (
    "%aichat%chat%", "%cursor%chat%", "%ai%chat%", "%chatdata%", "%chat.view%"
)

def _query_items(conn: sqlite3.Connection) -> Iterable[Tuple[str, str]]:
    """Query the database for chat-related items"""
    # Try exact keys first
    cur = conn.cursor()
    q_marks = ",".join(["?"]*len(CHAT_KEYS))
    cur.execute(f"SELECT [key], value FROM ItemTable WHERE [key] IN ({q_marks})", CHAT_KEYS)
    for k, v in cur.fetchall():
        yield k, v
    
    # Fallback to LIKE scan for pattern matching
    for pat in KEY_LIKE_PATTERNS:
        cur.execute("SELECT [key], value FROM ItemTable WHERE [key] LIKE ?", (pat,))
        for k, v in cur.fetchall():
            yield k, v

def extract_messages(value: str) -> List[Dict]:
    """
    Normalize Cursor chat JSON into a list of {id, role, text, ts}.
    Schemas vary; we best-effort parse common shapes.
    """
    out = []
    try:
        data = json.loads(value)
    except Exception:
        return out

    def push(role, text, ts=None, mid=None):
        """Helper to add a message to the output"""
        if not (text and text.strip()): 
            return
        rid = mid or hashlib.sha1(f"{role}|{text}".encode("utf-8")).hexdigest()[:16]
        out.append({
            "id": rid, 
            "role": role, 
            "text": text.strip(), 
            "ts": ts or int(time.time())
        })

    # Common shapes:
    # 1) {"chats":[{"messages":[{"role":"assistant"|"user","content":"..."}]}]}
    chats = data.get("chats") if isinstance(data, dict) else None
    if isinstance(chats, list):
        for tab in chats:
            msgs = tab.get("messages") or tab.get("msgs")
            if isinstance(msgs, list):
                for m in msgs:
                    role = m.get("role") or m.get("sender") or "assistant"
                    text = m.get("content") or m.get("text") or m.get("message")
                    ts = m.get("timestamp") or m.get("ts")
                    push(role, text, ts, m.get("id"))
    
    # 2) Direct messages array
    elif isinstance(data, list):
        for m in data:
            if not isinstance(m, dict): 
                continue
            role = m.get("role") or m.get("sender") or "assistant"
            text = m.get("content") or m.get("text")
            push(role, text, m.get("ts"), m.get("id"))
    
    # 3) Nested state objects containing 'chat' or 'messages'
    elif isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, list) and k.lower().startswith(("chat", "messages")):
                for m in v:
                    if not isinstance(m, dict): 
                        continue
                    push(
                        m.get("role", "assistant"), 
                        m.get("content") or m.get("text"), 
                        m.get("ts"), 
                        m.get("id")
                    )
    
    return out

def read_assistant_messages(workspace_root: str, seen: set[str]) -> List[Dict]:
    """
    Returns only new ASSISTANT messages for a workspace (dedup by hash).
    """
    db = find_state_db_for_workspace(workspace_root)
    if not db:
        return []
    
    # Open read-only; SQLite URI
    try:
        conn = sqlite3.connect(f"file:{db.as_posix()}?mode=ro", uri=True)
    except Exception:
        return []
    
    try:
        new = []
        for _, value in _query_items(conn):
            for m in extract_messages(value):
                if m["role"].lower() not in ("assistant", "ai", "system-assistant"): 
                    continue
                sig = hashlib.sha1(m["text"].encode("utf-8")).hexdigest()
                if sig in seen: 
                    continue
                m["sig"] = sig
                new.append(m)
        return new
    finally:
        conn.close()
