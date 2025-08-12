### Protocol: Commit, Push, and Notify

When to use
- After making real, verifiable edits (no stubs), with validation/tests passing.

Steps
1) Validate repo and run tests if present
```powershell
./overnight_runner/tools/run_validate_all.ps1 -ReposRoot <repo_parent> -WriteSummary
```
2) Commit and push changes
```powershell
./overnight_runner/tools/git_commit_push.ps1 -RepoPath D:\repositories\<repo> -Message "feat: concise summary" -Branch feat/short-name -CreateBranch
```
3) Optional: open PR (requires GitHub CLI `gh` authenticated)
```powershell
./overnight_runner/tools/git_commit_push.ps1 -RepoPath D:\repositories\<repo> -OpenPR -PRTitle "feat: concise summary" -PRBody "Why, what, how tested"
```
4) Send devlog notification to Discord
```powershell
$env:DISCORD_WEBHOOK_URL = '<webhook>'
./overnight_runner/tools/devlog_notify_from_repo.ps1 -RepoPath D:\repositories\<repo> -Validated -Pushed -Extra "nightly run"
```

Notes
- Follow `16_GIT_WORKFLOW.md` for branch/commit conventions.
- Keep diffs small and cohesive; include validation evidence in PR body.




