### Protocol: Task State and End State Tracking

Goal
- Ensure each agent records task lifecycle and end state so we know when to validate and push.

States
- `assigned` → `in_progress` → `complete` → `validated` → `pushed`
- Branches: record branch name when starting work.
- End state: short phrase describing the objective (e.g., "README+validate added", "APIClient tests passing").

Tools
```powershell
# Mark a task started
./overnight_runner/tools/task_state_manager.ps1 -Agent Agent-4 -TaskId basic-bot-quickstart -RepoPath D:\repositories\basic-bot -Branch feat/quickstart -EndState "README+validate added" -Status in_progress

# After validation passes
./overnight_runner/tools/task_state_manager.ps1 -Agent Agent-4 -TaskId basic-bot-quickstart -Status validated

# After push
./overnight_runner/tools/task_state_manager.ps1 -Agent Agent-4 -TaskId basic-bot-quickstart -Status pushed
```

Where stored
- `agent_workspaces/Agent-X/task_state.json`

Review
- Captain reviews task_state.json across agents to decide which tasks are ready to push or need follow‑ups.




