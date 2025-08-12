### Protocol: Scan TASK_LISTs

Goal
- Inventory repos with `TASK_LIST.md`, rank quick wins, and emit a prioritized plan.

CLI
- Use `../tools/scan-tasklists.ps1 -Root D:\repositories -Out D:\repositories\communications\overnight_YYYYMMDD_`

Steps
1) Find all `TASK_LIST.md` under the root
2) Summarize per repo: quickstart present, validate present, last updated
3) Output CSV/JSON and captain summary note

Guardrails
- Respect `.gitignore` where applicable; do not modify repos





