### 4‑Agent Onboarding Sequence (Captain + Crew)

[Back to Index](00_INDEX.md)

Objective: Facilitate autonomous development across the same codebase with one captain validating and coordinating.

Roles
- Captain (Agent‑3 by default): plans, assigns, validates outcomes, posts summaries/handoffs
- Crew (Agents 1, 2, 4): choose work from repo `TASK_LIST.md`, execute, coordinate with peers

Sequence
1) Captain kickoff (visible ACP)
   - Send `[CAPTAIN]` kickoff to self
   - Broadcast `[COORDINATE]` collab norms (no duplication/stubs; reuse/refactor; use `TASK_LIST.md`; log to comms folder)
   - Start inbox listener with devlog broadcasting (Discord):
     ```powershell
     python overnight_runner/listener.py --agent Agent-5 --env-file .env --devlog-embed --devlog-username "Agent Devlog"
     ```
2) Assignments (visible ACP)
   - Send `[TASK]` per agent with 1–2 repos each; reference comms folder for logs/handoffs
3) Start cadence (runner)
   - 5‑minute autonomous‑dev plan: cycles `[RESUME]`, `[TASK]`, `[COORDINATE]`, `[SYNC]`, `[VERIFY]`
   - Cycle targets: Agents 1, 2, 4 (captain gets kickoff only) or include captain as needed
4) Crew flow (per agent)
   - Open assigned repo `TASK_LIST.md`, choose high‑leverage item, update status as you work
   - Prefer reuse/refactor vs adding new code; avoid duplicates and shims
   - Commit small, verifiable edits; add tests/build steps
   - Prompt another agent for a quick sanity check when needed; incorporate feedback
5) Validation
   - Captain sends `[VERIFY]` checks; reviews tests/build; requests evidence or staged diffs
   - If blocked by permissions, stage diffs and summarize impact + next steps in comms folder
   - Post validation broadcast to Discord (optional):
     ```powershell
     ./overnight_runner/tools/devlog_after_validate.ps1 -RepoPath D:\repositories\<repo>
     ```
6) Handoffs
   - At cadence or shift end, captain posts `[SYNC]` summary: changed, open TODO, next verifiable action
   - All agents log notes/handoffs in the per‑shift comms folder

Messaging channels
- Visible ACP: `src/agent_cell_phone.py` (requires calibrated 4‑agent coords)
- Silent inbox: `overnight_runner/listener.py` + drop JSON in `agent_workspaces/Agent-N/inbox`

Start commands
- See `10_NEW_AGENT_QUICKSTART.md` and `04_OVERNIGHT_RUNNER.md` for copy‑paste commands
- See `../protocols/DEVLOG_BROADCASTER.md` for devlog setup, testing, and examples



[Back to Index](00_INDEX.md)












