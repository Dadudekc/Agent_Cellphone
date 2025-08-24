# Discord → Agent Cell Phone Router

Routes Discord messages into your agent GUIs via PyAutoGUI.
- Window focusing (best-effort) via pygetwindow
- Coordinate targeting for chat input
- Safe paste or keystroke typing
- Queue-based dispatch to avoid overlap
- Role + channel gating
- Live ops commands

## Install
```
cd agent_cellphone/discord_router
python -m venv .venv && . .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env && cp config.example.json config.json
# put DISCORD_BOT_TOKEN in .env
```

## Run
```
python discord_router.py
```

## Live Ops Commands (in whitelisted channels)
- `!ping` → health check
- `!agents` → list configured agents
- `!coords agent-5 400 600` → set chat_input coords
- `!bind agent-5 Cursor - Agent 5` → bind window substring
- `!focus agent-5` → bring to front
- `!mode paste|type` → paste (default) or keystroke typing
- `!enter on|off` → toggle pressing Enter after typing
- `!dry on|off` → dry-run toggle

## Routing Patterns
- `!agent agent-5 do the thing` → explicit
- Post in `#agent-5` channel → implicit
- `agent-5: do the thing` → prefix form

## Notes
- Enable **Message Content Intent** in Discord Developer Portal.
- Coordinates are absolute to the machine running this bot.
- Use DRY_RUN to test without clicking/typing.
