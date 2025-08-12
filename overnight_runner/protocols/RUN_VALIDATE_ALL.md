### Protocol: Validate All Repositories

When to use
- Start of shift; before runner; before handoff.

Steps
1) Run the tool:
```powershell
./overnight_runner/tools/run_validate_all.ps1 -WriteSummary
```
2) If any repo fails, open its `TASK_LIST.md`, create a quick fix, and re‑run.





