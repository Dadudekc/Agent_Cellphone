### CI and Testing Policy

Minimum checks
- Run `validate.ps1` on Windows runners
- Run language tests (pytest, node test) with coverage summary

Artifacts
- Save logs on failure; upload junit/coverage if available

Fast feedback
- Keep a smoke test path (< 1 min) separate from full suite


Minimal GitHub Actions (Windows) example
```yaml
name: CI
on: [push, pull_request]
jobs:
  validate:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Run repo validation
        run: pwsh -NoLogo -NoProfile -File ./validate.ps1
      - name: Run local smoke tests
        run: pwsh -NoLogo -NoProfile -File ./tests/smoke/run_smoke.ps1
```



[Back to Index](00_INDEX.md)

