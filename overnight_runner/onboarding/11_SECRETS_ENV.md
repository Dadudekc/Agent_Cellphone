### Secrets and Environment

GitHub token
- Prefer Git Credential Manager or `git -c http.extraHeader="Authorization: Bearer $env:GITHUB_TOKEN"` over embedding tokens in URLs
- Scopes: for cloning, grant repo read access; for pushing, repo write
- Avoid pasting tokens into logs; prefer Credential Manager when possible

Cloning tool
```powershell
python overnight_runner/tools/github_clone_tool.py --user <github-username> --token $env:GITHUB_TOKEN --dest D:/repos
```

Safety notes
- Avoid token-in-URL clone syntax; it can leak via process list/history
- Never commit tokens; do not add to comms logs

- Use `.env` in each repo root; never commit real secrets.
- Provide `.env.example` with key names and placeholders.
- Standard keys:
  - `API_KEY`, `API_TIMEOUT`, `LOG_LEVEL`
  - Repo-specific keys live in that repo’s README.
- Rotation: change keys monthly or on incident; document owner.
- Storage: local `.env`; shared secrets via your password manager.
- Loading:
  - Python: `python-dotenv` or repo util (e.g., `shared.utils.config`)
  - Node: `dotenv`



[Back to Index](00_INDEX.md)


