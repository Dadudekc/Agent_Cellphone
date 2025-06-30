import os, json, datetime, shutil

def onboard_agent():
    agent_id = input("Enter new agent ID (e.g., Agent-3): ").strip()
    base = os.path.join(os.getcwd(), "agent_workspaces", agent_id)
    if os.path.exists(base):
        print("Agent workspace already exists!")
        return
    # Copy template
    shutil.copytree("workspace_template", base)
    # Patch status.json
    status_path = os.path.join(base, "status.json")
    with open(status_path, "r", encoding="utf-8") as f:
        status = json.load(f)
    status["agent_id"] = agent_id
    status["last_updated"] = datetime.datetime.utcnow().isoformat() + "Z"
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(status, f, indent=2)
    print(f"Workspace for {agent_id} created at {base}")
    print("Next: Review the onboarding checklist in your workspace.")

if __name__ == "__main__":
    onboard_agent() 