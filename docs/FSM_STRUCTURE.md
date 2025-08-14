# Agent Cell Phone – FSM Structure

This document defines the minimal finite-state machine (FSM) used to coordinate task execution, evidence capture, and reporting across the Agent Cell Phone platform.

## Goals

- Provide an explicit, auditable lifecycle for tasks and workflows
- Enable small, cohesive steps with verifiable evidence after each transition
- Support guard conditions for safety, retries, and approvals

## Core States

- IDLE: System is initialized, not yet assigned work
- READY: System health and configuration validated; ready to accept a task
- EXECUTING_TASK: Running the current atomic step; producing artifacts/evidence
- AWAITING_APPROVAL: Paused pending human or agent approval/verification
- BLOCKED: Waiting on dependency, external prerequisite, or rate limit
- ERROR: Recoverable error encountered; subject to retry policy
- COMPLETE: Task finished with acceptance criteria satisfied

## Events (external/internal)

- task_received: New task arrived (inbox or API)
- validate_passed / validate_failed: Environment/repo checks
- step_passed / step_failed: Execution result of a small step
- evidence_captured: Logs/tests/build artifacts stored
- approval_granted / approval_denied: Human/agent gate result
- dependency_ready: Unblocked signal from an external prerequisite
- timeout / rate_limited: Operational limits reached
- reset_requested: Reset to READY for the next task

## Transitions

- IDLE → READY on validate_passed
- READY → EXECUTING_TASK on task_received [guard: has_valid_task]
- EXECUTING_TASK → AWAITING_APPROVAL on step_passed [guard: approval_required]
- EXECUTING_TASK → ERROR on step_failed [guard: retries_remaining]
- EXECUTING_TASK → BLOCKED on timeout or rate_limited
- AWAITING_APPROVAL → EXECUTING_TASK on approval_denied (revise)
- AWAITING_APPROVAL → COMPLETE on approval_granted
- BLOCKED → EXECUTING_TASK on dependency_ready
- ERROR → EXECUTING_TASK on step_retry [guard: retries_remaining]
- Any → READY on reset_requested

## Guards (examples)

- has_valid_task: Payload adheres to schema; acceptance criteria provided
- approval_required: Current step’s policy requires human/agent approval
- retries_remaining: Remaining attempts > 0 within backoff policy
- evidence_attached: Artifacts (logs, tests, diffs) persisted to evidence store

## Actions (side effects)

- run_validation: Repo/setup validation (e.g., PowerShell validate.ps1)
- execute_step: Perform the minimal cohesive change or operation
- run_tests: Execute unit/integration tests; capture summaries
- capture_evidence: Persist outputs under communications/overnight_YYYYMMDD_/Agent-5/
- post_fsm_update: Send JSON status to Agent-5 inbox with task_id, state, summary, evidence
- notify: Signal ACP/UI with concise status and next step

## Minimal Sequence (happy path)

1) IDLE → READY (run_validation)
2) READY → EXECUTING_TASK (task_received, has_valid_task)
3) EXECUTING_TASK (execute_step → run_tests → capture_evidence)
4) EXECUTING_TASK → AWAITING_APPROVAL (step_passed, approval_required)
5) AWAITING_APPROVAL → COMPLETE (approval_granted → post_fsm_update)

## Error and Recovery

- On step_failed: record diagnostics, decrement retries, transition to ERROR; attempt step_retry with backoff
- On BLOCKED: persist reason and poll/subscribe for dependency_ready to resume
- On validation failure: remain in IDLE; surface actionable diagnostics

## Next Step

Confirm canonical transition names and guard condition keys in code (e.g., orchestrator and overnight runner), and wire a thin adapter that emits evidence consistently to the Agent-5 inbox.

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



