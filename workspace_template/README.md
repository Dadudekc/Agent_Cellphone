# Agent Workspace Template

Welcome! This is a template for a new Dream.OS agent workspace.

## Included Files
- `status.json` – Your live status file (update after every action!)
- `notes.md` – Your personal notes or scratchpad
- `task_list.json` – (Optional) List of assigned or completed tasks
- `onboarding/` – Onboarding checklist and docs (read these first!)

## First Steps
1. Review the onboarding checklist in `onboarding/ONBOARDING_CHECKLIST.md`
2. Implement the `update_status` helper in your agent code
3. Update `status.json` after every action, state change, or message
4. Use the `message` field to communicate with the user
5. Test your status reporting in the Dream.OS UI

---
*This file is copied into every new agent workspace by the onboarding script.* 