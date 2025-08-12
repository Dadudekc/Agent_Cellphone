### Protocol: Send Sync Message

Goal
- Send a structured sync/task/ack JSON to an agent inbox.

CLI
- Use `../tools/send-sync.ps1 -To Agent-3 -Type sync -Topic "..." -Summary "..." -PayloadPath optional.json`

Steps
1) Locate inbox path for the agent
2) Build JSON with required fields per `13_MESSAGING_SCHEMAS.md`
3) Write file and log the path to communications directory

Guardrails
- Do not overwrite existing files; use timestamped names
- Validate required fields before write





