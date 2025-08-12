### Git Workflow (Minimal)

Standard flow
```powershell
git checkout -b chore/agent-update-YYYYMMDD
git status
git add -A
git commit -m "feat: small, verifiable improvement (scope)"
git push -u origin chore/agent-update-YYYYMMDD
```

If push is blocked (no permissions)
```powershell
git diff > D:\repositories\communications\overnight_YYYYMMDD_\agent_patch.diff
```

Branch naming
- `feat/`, `fix/`, `chore/` prefixes; keep scope short

Commit messages
- Imperative, concise, include why + impact when relevant

### Git Workflow (conventions)

Branches
- `main`: stable
- `feat/*`, `fix/*`, `docs/*`, `chore/*`

Commits
- Conventional commits: `feat: ...`, `fix: ...`, `docs: ...`, `chore: ...`

PR checklist
- CI green, small diff, clear description, links to `TASK_LIST.md`



[Back to Index](00_INDEX.md)


