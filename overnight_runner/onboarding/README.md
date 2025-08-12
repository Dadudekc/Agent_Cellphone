### Overnight Onboarding Pack

Use this bundle to get new agents productive quickly with the Agent Cell Phone (ACP) and the Overnight Runner.

#### Start here
- Index: `overnight_runner/onboarding/00_INDEX.md`
- New Agent Quickstart: `overnight_runner/onboarding/10_NEW_AGENT_QUICKSTART.md`
- Overnight Runner: `overnight_runner/onboarding/04_OVERNIGHT_RUNNER.md`
- Playbooks: `overnight_runner/onboarding/06_PLAYBOOKS.md`

#### Communication and coordination
- Messaging channels: `overnight_runner/onboarding/03_MESSAGING_CHANNELS.md`
- File inbox listener: `overnight_runner/onboarding/05_FILE_INBOX_LISTENER.md`

#### Protocols and command references
- Protocols index: `overnight_runner/protocols/README.md`
- Validate repo: `overnight_runner/protocols/protocol_validate_repo.md`
- Send sync: `overnight_runner/protocols/protocol_send_sync.md`
- Scan task lists: `overnight_runner/protocols/protocol_scan_tasklists.md`

#### More references
- Calibration: `overnight_runner/onboarding/02_CALIBRATION.md`
- Messaging schemas: `overnight_runner/onboarding/13_MESSAGING_SCHEMAS.md`
- Troubleshooting: `overnight_runner/onboarding/07_TROUBLESHOOTING.md`

#### Overnight Runner quick links
- Runner usage: `overnight_runner/onboarding/04_OVERNIGHT_RUNNER.md`
- Listener (file inbox): `overnight_runner/listener.py`

#### Expectations for autonomous work
- Prefer reuse/refactor across repos; avoid duplication, stubs, or shims
- Use each repo’s `TASK_LIST.md` to choose work and update status
- Commit small, verifiable edits; add tests/build checks when practical
- Use the communications folder (per shift) to leave notes and handoffs

#### Environment assumptions (Cursor + shared workspace)
- Agents are Cursor-based: ACP types directly into each agent’s Cursor window via calibrated coordinates.
- All agents operate on the same repositories and file system (shared workspace). Coordinate through `TASK_LIST.md`, `status.json`, and PRDs to avoid conflicts.
- Prefer the file-inbox channel for silent automation between tools: `agent_workspaces/Agent-N/inbox/`.
- Run commands from `D:\Agent_Cellphone`; project repos typically live under `D:\repositories`.

Run all commands from `D:\Agent_Cellphone` so paths resolve correctly.

[Back to Index](00_INDEX.md)





