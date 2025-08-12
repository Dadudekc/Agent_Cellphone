### Validation and Health Checks

Standard contract
- Each repo provides `validate.ps1` at repo root.
- Must exit 0 on success, non‑zero on failure; print “Validation succeeded.” on pass.

CI usage
- Step 1: run `validate.ps1`
- Step 2: run unit tests if present

Common failures
- Missing `README.md` or `TASK_LIST.md`
- Env not loaded (.env missing); provide `.env.example`
- Dependency not installed: prefer stubs or mock in unit tests



[Back to Index](00_INDEX.md)



