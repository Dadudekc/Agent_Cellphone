## FSM Structure — Jarvis Enhancement

States:
- PLANNING
- IN_PROGRESS
- BLOCKED
- REVIEW
- DONE

Events:
- START
- SUBTASK_COMPLETE
- REQUEST_REVIEW
- APPROVE
- REJECT
- UNBLOCK

Transitions:
- PLANNING --START--> IN_PROGRESS
- IN_PROGRESS --SUBTASK_COMPLETE--> REVIEW
- REVIEW --APPROVE--> DONE
- REVIEW --REJECT--> IN_PROGRESS
- IN_PROGRESS --BLOCKED--> BLOCKED
- BLOCKED --UNBLOCK--> IN_PROGRESS

Guards/Notes:
- Only progress when evidence or tests exist
- Prefer small, verifiable edits with unit tests

Transition Names (finalized):
- start: PLANNING --START--> IN_PROGRESS
- submit_subtask: IN_PROGRESS --SUBTASK_COMPLETE--> REVIEW
- approve: REVIEW --APPROVE--> DONE
- request_changes: REVIEW --REJECT--> IN_PROGRESS
- block: IN_PROGRESS --BLOCKED--> BLOCKED
- unblock: BLOCKED --UNBLOCK--> IN_PROGRESS

Guard Conditions (finalized):
- EVIDENCE_PRESENT: Transition to REVIEW or DONE requires linked evidence (e.g., updated docs or passing tests/build logs).
- SMALL_VERIFIABLE: Each transition represents a small, atomic edit that can be independently verified.
- NO_DUPLICATION: Changes must reuse existing structures and avoid duplicate logic/docs.
- TESTABLE: For code-path transitions, a smoke test or unit test must exist or be updated to cover the change.



