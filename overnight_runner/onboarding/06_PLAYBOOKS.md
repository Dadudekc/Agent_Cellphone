### Playbooks

[Back to Index](00_INDEX.md)

Quiet kickstart (immediate one cycle)
```powershell
python overnight_runner/runner.py --layout 4-agent --agents Agent-1,Agent-2,Agent-3,Agent-4 \
  --iterations 1 --interval-sec 300 --sender Agent-3 --plan autonomous-dev \
  --initial-wait-sec 0 --phase-wait-sec 0 --stagger-ms 1200 --jitter-ms 400
```

Captain shift (standard)
```powershell
python overnight_runner/runner.py --layout 4-agent --captain Agent-3 --resume-agents Agent-1,Agent-2,Agent-4 \
  --duration-min 480 --interval-sec 300 --sender Agent-3 --plan autonomous-dev
```

Broadcast coordination update
```powershell
python src/agent_cell_phone.py --layout 4-agent --msg "Captain update: use each repo's TASK_LIST.md to choose work and update status; log notes/handoffs to D:\\repositories\\communications\\overnight_YYYYMMDD_." --tag coordinate
```

TASK_LIST.md template snippet
```md
# Task List

- [ ] Short task title – why it matters (owner: @agent, started: 2025‑08‑11)
  - Status: planned | in‑progress | blocked | done
  - Next step: one verifiable action
  - Evidence: link to commit/PR/test
```




[Back to Index](00_INDEX.md)
