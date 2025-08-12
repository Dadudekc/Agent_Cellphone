### Code Standards

Formatting and linting
- Python: black, ruff, mypy (where types exist)
- Node: prettier, eslint, tsconfig for TS

Pre-commit
- Run format + lint before commit; block on errors

Naming and clarity
- Prefer descriptive names; avoid 1–2 char vars
- Small functions, early returns, handle errors first

File size limits
- Logic files: hard limit 350 LOC (including imports but excluding license header)
- GUI logic files: hard limit 500 LOC
- If you hit limits, split by responsibility (SRP) and extract classes/modules

Paradigm and structure
- Object‑oriented first: model the domain with classes and clear responsibilities
- Prefer composition over inheritance; inject dependencies explicitly
- Public APIs fully typed; avoid global state

No stubs or placeholders in production
- Do not leave TODO stubs, mock implementations, or placeholder returns in app/library code
- Implement complete behavior with retries, timeouts, and error handling where appropriate
- Tests may use test doubles (mocks/fakes) but production code must be real and autonomous

Autonomous by default
- Assume no human will “come back later”; make features complete, resilient, and self‑healing
- Provide sane defaults, `.env.example`, validation scripts, and clear errors with remediation hints



[Back to Index](00_INDEX.md)
