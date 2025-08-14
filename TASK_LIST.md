## TASK LIST — Jarvis Enhancement

Project: `Jarvis Enhancement`
Workflow: `Development Workflow` (state: IN_PROGRESS)

### Tasks (FSM-driven)

- [x] Design FSM Structure (state: DONE)
  - Description: Design the FSM structure for workflow management
  - Priority: HIGH
  - Deliverable: `docs/FSM_STRUCTURE.md`
  - Evidence: Document authored; lints clean

- [ ] Implement FSM Logic (state: PENDING)
  - Description: Implement the FSM logic and state transitions
  - Priority: HIGH
  - Depends on: Design FSM Structure

- [ ] Test FSM System (state: PENDING)
  - Description: Test the FSM system with various scenarios
  - Priority: MEDIUM
  - Depends on: Implement FSM Logic

### Current Focus

- Implement FSM Logic → Wire transitions and guards into orchestrator/overnight runner.
  - Evidence target: smoke/unit tests validating transitions and evidence emission.
  - Next small step: Confirm transition names and guard keys in code, add minimal test scaffolding.



