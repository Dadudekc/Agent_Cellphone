### Protocols

Operational playbooks for recurring hurdles and the tools that unblock autonomous workflows.

- Use these when an agent hits a blocker.
- Each protocol references concrete tools in `../tools`.

Purpose: Document standardized responses to recurring hurdles and the automation tools that resolve them.

Layout
- `*.md`: Human-readable protocol docs with steps, guardrails, and links
- `../tools/*`: CLI scripts used by protocols

Index
- `protocol_validate_repo.md` – run repo validation and summarize
- `protocol_send_sync.md` – compose and send sync JSON to an agent inbox
- `protocol_scan_tasklists.md` – inventory repos with TASK_LIST.md and plan quick wins
- `DEVLOG_BROADCASTER.md` – configure and use the Discord devlog broadcaster (listener + repo tools)


