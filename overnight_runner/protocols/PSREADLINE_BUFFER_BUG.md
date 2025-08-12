### Protocol: PSReadLine Buffer/Render Exceptions in PowerShell 7

Symptoms
- `System.ArgumentOutOfRangeException` or `IndexOutOfRangeException` from PSReadLine during long one‑liners.

Resolution
- Always pass `-NoLogo -NoProfile` and avoid interactive editing in automation.
- Prefer here‑strings or scripts over very long inline commands.
- If unavoidable, redirect to files and execute (`.ps1`).

Tooling
- See `tools/ps_invoke.ps1` for a safe invocation wrapper.





