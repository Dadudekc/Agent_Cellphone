#!/usr/bin/env python3
"""
Export Consumer - Fallback for when Cursor DB isn't accessible
Processes exported chat files (.json/.md) and converts them to inbox envelopes
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
EXPORT_WATCH_DIR = Path("agent_workspaces/exports")
INBOX = Path("agent_workspaces/Agent-5/inbox")
PROCESSED_DIR = Path("agent_workspaces/exports/processed")

# Ensure directories exist
EXPORT_WATCH_DIR.mkdir(parents=True, exist_ok=True)
INBOX.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def parse_exported_chat(file_path: Path) -> List[Dict]:
    """Parse an exported chat file and extract AI assistant messages"""
    messages = []
    
    try:
        if file_path.suffix.lower() == '.json':
            # JSON export format
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle different export formats
            if isinstance(data, list):
                # Direct messages array
                for msg in data:
                    if msg.get('role') == 'assistant':
                        messages.append({
                            'text': msg.get('content', ''),
                            'timestamp': msg.get('timestamp'),
                            'id': msg.get('id')
                        })
            elif isinstance(data, dict):
                # Nested structure
                chats = data.get('chats', [])
                for chat in chats:
                    msgs = chat.get('messages', [])
                    for msg in msgs:
                        if msg.get('role') == 'assistant':
                            messages.append({
                                'text': msg.get('content', ''),
                                'timestamp': msg.get('timestamp'),
                                'id': msg.get('id')
                            })
        
        elif file_path.suffix.lower() == '.md':
            # Markdown export format
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple markdown parsing - look for AI responses
            lines = content.split('\n')
            current_role = None
            current_text = []
            
            for line in lines:
                if line.startswith('**Assistant:**'):
                    # Save previous message if it was from assistant
                    if current_role == 'assistant' and current_text:
                        messages.append({
                            'text': '\n'.join(current_text).strip(),
                            'timestamp': int(time.time()),
                            'id': f"md_{len(messages)}"
                        })
                    
                    current_role = 'assistant'
                    current_text = [line.replace('**Assistant:**', '').strip()]
                elif line.startswith('**User:**'):
                    current_role = 'user'
                    current_text = []
                elif current_role == 'assistant' and line.strip():
                    current_text.append(line)
            
            # Don't forget the last message
            if current_role == 'assistant' and current_text:
                messages.append({
                    'text': '\n'.join(current_text).strip(),
                    'timestamp': int(time.time()),
                    'id': f"md_{len(messages)}"
                })
    
    except Exception as e:
        print(f"Error parsing {file_path}: {e}")
    
    return messages

def process_export_file(file_path: Path, agent_name: str = "unknown") -> bool:
    """Process a single export file and create inbox envelopes"""
    try:
        messages = parse_exported_chat(file_path)
        
        if not messages:
            print(f"No AI messages found in {file_path}")
            return False
        
        print(f"Found {len(messages)} AI messages in {file_path}")
        
        for i, msg in enumerate(messages):
            if not msg['text'].strip():
                continue
            
            # Create envelope
            envelope = {
                "type": "assistant_reply",
                "from": agent_name,
                "to": "Agent-5",
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "agent": agent_name,
                "ts": msg.get('timestamp', int(time.time())),
                "payload": {
                    "type": "assistant_reply",
                    "text": msg['text'],
                    "message_id": msg.get('id'),
                    "role": "assistant",
                    "source": "export_file",
                    "file": file_path.name
                }
            }
            
            # Write to inbox
            out_file = INBOX / f"export_{int(time.time()*1000)}_{agent_name}_{i}.json"
            out_file.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
            
            print(f"Created envelope: {out_file.name}")
        
        return True
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def watch_exports(agent_map: Dict[str, dict], poll_seconds: float = 5.0):
    """Watch export directory for new files and process them"""
    print(f"[EXPORT_WATCHER] Watching {EXPORT_WATCH_DIR} for new export files")
    
    processed_files = set()
    
    try:
        while True:
            # Look for new export files
            for file_path in EXPORT_WATCH_DIR.glob("*"):
                if file_path.is_file() and file_path not in processed_files:
                    # Try to determine agent from filename or content
                    agent_name = "unknown"
                    
                    # Check if filename contains agent info
                    for agent in agent_map.keys():
                        if agent.lower() in file_path.name.lower():
                            agent_name = agent
                            break
                    
                    # Process the file
                    if process_export_file(file_path, agent_name):
                        processed_files.add(file_path)
                        
                        # Move to processed directory
                        processed_path = PROCESSED_DIR / file_path.name
                        try:
                            file_path.rename(processed_path)
                            print(f"Moved {file_path.name} to processed")
                        except Exception as e:
                            print(f"Could not move {file_path.name}: {e}")
            
            time.sleep(poll_seconds)
            
    except KeyboardInterrupt:
        print("\n[EXPORT_WATCHER] Stopped by user")
    except Exception as e:
        print(f"[EXPORT_WATCHER] Error: {e}")

if __name__ == "__main__":
    # Test with sample agent map
    test_agent_map = {
        "Agent-1": {"workspace_root": "D:/repos/project-A"},
        "Agent-2": {"workspace_root": "D:/repos/project-B"}
    }
    
    watch_exports(test_agent_map)
