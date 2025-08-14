## 🛰️ Agent Directive: PRD Creation Standards Update

**Task:**
Move away from boilerplate PRDs. From now on, every PRD must be hand-crafted per repository.

---

### 📌 Protocol

1. **Manual Inspection**
   - Open the repo locally
   - Read `README.md`, `docs/`, issues/PRs, code structure and comments, designs

2. **Template Reference — Not Copy/Paste**
   Use this as a reference only (adapt order/names; do not leave TBDs):
   - Overview
   - Problem Statement
   - Goals / Non-Goals
   - Target Users
   - Scope
   - Requirements (Functional / Non-Functional)
   - Success Metrics
   - Milestones & Timeline
   - Assumptions
   - Risks & Mitigations
   - Open Questions
   - Appendix

3. **Uniqueness Mandate**
   - No two PRDs should look identical
   - Reflect tech stack, maturity, and real problems

4. **Legacy Content Integration**
   - Extract only relevant, current parts from older PRDs/designs
   - Rephrase to reflect current direction
   - Remove outdated milestones/features

5. **Ownership & Accountability**
   - Sign off at bottom:
     ```
     Prepared by: [Agent Name]
     Last updated: YYYY-MM-DD
     ```
   - Treat as a living document

---

### 📄 Metadata Header
Include at top of `docs/PRD.md`:
```
---
title: [Repo Name] Product Requirements Document
repository: [Repo Path or URL]
owner: [Name or Team]
status: Draft / Active / Deprecated
version: 1.0
last_updated: YYYY-MM-DD
x-standard-prd: v1
---
```

---

### 🗂 PRD Crafting Checklist — Agent Field Guide

1) Pre-Work: Repo Recon
- [ ] Repo inspected
- [ ] README reviewed
- [ ] Docs/issues/designs reviewed

2) Draft the PRD — Structure Guide
- [ ] Sections adapted and filled with real context (no TBDs)

3) Uniqueness Rules
- [ ] PRD reflects stack, maturity, problem context
- [ ] Irrelevant content removed

4) Integrate Legacy Content
- [ ] Relevant content extracted & rewritten
- [ ] Outdated content removed

5) Finalization
- [ ] Metadata header present
- [ ] Signature present
- [ ] Committed to `docs/PRD.md`
- [ ] Pushed to repo

---

### 🛠 Tools (Helper Only)
- `Standardize-PRDs.ps1` ensures a starting file when missing. Final PRD must be hand-crafted before commit.
- `agent_prd_tracker.ps1` creates/updates per-repo tracker at `docs/prd_tracker.json`.
- `agent_prd_master_tracker.ps1` updates global tracker at `D:\repos\runtime\agent_comms\prd_master_tracker.json`.
