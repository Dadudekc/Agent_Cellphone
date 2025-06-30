"""Utility to ensure each agent status.json contains standard fields.
Run: python scripts/update_agent_status.py
"""
import json, os, datetime, glob

BASE = os.path.join(os.getcwd(), "agent_workspaces")
AGENTS = sorted([d for d in os.listdir(BASE) if d.startswith("Agent-")])

def ensure_status(path:str, agent_id:str):
    default = {
        "agent_id": agent_id,
        "status": "offline" if agent_id!="Agent-1" else "ready",
        "current_task": "none",
        "last_updated": datetime.datetime.utcnow().isoformat()+"Z"
    }
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}
    else:
        data = {}
    data.update(default)
    data["last_updated"] = datetime.datetime.utcnow().isoformat()+"Z"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def main():
    for agent in AGENTS:
        status_path = os.path.join(BASE, agent, "status.json")
        ensure_status(status_path, agent)
    print(f"Updated status for {len(AGENTS)} agents.")

if __name__ == "__main__":
    main() 