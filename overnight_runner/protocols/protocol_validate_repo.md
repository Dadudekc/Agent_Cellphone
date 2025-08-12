### Protocol: Validate Repo

Goal
- Verify a repository is healthy: README present, TASK_LIST present, validate script passes.

CLI
- Use `../tools/validate-repo.ps1 -Path <repo>`

Steps
1) Run validation script if present; else fail with guidance
2) If missing README/TASK_LIST, create stubs and re-run
3) Emit JSON summary to communications log directory

Guardrails
- Never modify unrelated files; only create minimal docs/scripts needed
- Exit non-zero on failure; include remediation hints





