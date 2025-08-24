import os, json, asyncio, logging, time, re, platform
from pathlib import Path
from typing import Dict, Tuple, Optional

import discord
import pyautogui
import pyperclip
from dotenv import load_dotenv

try:
    import pygetwindow as gw
except Exception:
    gw = None

# ─────────────────────────────────────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
load_dotenv(BASE / ".env", override=True)

DRY_RUN = os.getenv("DRY_RUN", "false").lower() == "true"
TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
GUILD_ID_ENV = os.getenv("GUILD_ID", "").strip()

CONFIG_PATH = BASE / "config.json"
EXAMPLE_CONFIG_PATH = BASE / "config.example.json"
LOG_DIR = BASE / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(LOG_DIR / "discord_router.log", encoding="utf-8"),
        logging.StreamHandler()
    ],
)
log = logging.getLogger("router")

if not CONFIG_PATH.exists() and EXAMPLE_CONFIG_PATH.exists():
    CONFIG_PATH.write_text(EXAMPLE_CONFIG_PATH.read_text(), encoding="utf-8")
    log.info("No config.json found. Seeded from config.example.json")

config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

CHANNEL_WHITELIST = set(config.get("channel_whitelist", []))
ROLE_WHITELIST = set(r.lower() for r in config.get("role_whitelist", []))
PRESS_ENTER = bool(config.get("press_enter_after_typing", True))
TYPING_MODE = config.get("typing_mode", "paste")  # "paste" or "type"
TYPING_DELAY_MS = int(config.get("typing_delay_ms", 0))
AGENTS: Dict[str, Dict] = config.get("agents", {})

if not TOKEN:
    raise SystemExit("DISCORD_BOT_TOKEN missing. Put it in .env")

pyautogui.FAILSAFE = True  # move mouse to top-left to abort

# ─────────────────────────────────────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────────────────────────────────────
def save_config():
    CONFIG_PATH.write_text(json.dumps(config, indent=2), encoding="utf-8")
    log.info("config.json updated")

def get_agent(agent: str) -> Optional[Dict]:
    return AGENTS.get(agent)

def set_coords(agent: str, x: int, y: int):
    AGENTS.setdefault(agent, {}).setdefault("coords", {})["chat_input"] = [x, y]
    config["agents"] = AGENTS
    save_config()

def set_window(agent: str, title_substr: str):
    AGENTS.setdefault(agent, {})["window_title"] = title_substr
    config["agents"] = AGENTS
    save_config()

def bring_to_front(title_substr: str) -> bool:
    if not gw or not title_substr:
        return False
    try:
        wins = gw.getWindowsWithTitle(title_substr)
        if not wins:
            return False
        win = wins[0]
        # Best-effort activate across OSes
        win.activate()
        time.sleep(0.2)
        return True
    except Exception as e:
        log.warning(f"bring_to_front failed: {e}")
        return False

async def type_to_gui(text: str, coords: Tuple[int, int], press_enter: bool):
    x, y = coords
    log.info(f"Clicking at {coords} DRY_RUN={DRY_RUN}")
    if not DRY_RUN:
        pyautogui.click(x, y)
        time.sleep(0.05)
        if TYPING_MODE == "paste":
            pyperclip.copy(text)
            # Most editors accept Ctrl/Cmd+V
            if platform.system() == "Darwin":
                pyautogui.hotkey("command", "v")
            else:
                pyautogui.hotkey("ctrl", "v")
        else:
            pyautogui.typewrite(text, interval=(TYPING_DELAY_MS / 1000.0))
        if press_enter:
            pyautogui.press("enter")

# ─────────────────────────────────────────────────────────────────────────────
# Discord Client
# ─────────────────────────────────────────────────────────────────────────────
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

client = discord.Client(intents=intents)
action_queue: "asyncio.Queue[Tuple[discord.Message, str, str]]" = asyncio.Queue()

AGENT_CMD = re.compile(r"^!(agent)\s+(\S+)\s+(.+)$", re.IGNORECASE)
COORDS_CMD = re.compile(r"^!(coords)\s+(\S+)\s+(\d+)\s+(\d+)$", re.IGNORECASE)
BIND_CMD = re.compile(r"^!(bind|bind_window)\s+(\S+)\s+(.+)$", re.IGNORECASE)
FOCUS_CMD = re.compile(r"^!(focus)\s+(\S+)$", re.IGNORECASE)
LIST_CMD = re.compile(r"^!(agents|list_agents)$", re.IGNORECASE)
PING_CMD = re.compile(r"^!(ping)$", re.IGNORECASE)
MODE_CMD = re.compile(r"^!(mode)\s+(paste|type)$", re.IGNORECASE)
ENTER_CMD = re.compile(r"^!(enter)\s+(on|off)$", re.IGNORECASE)
DRY_CMD = re.compile(r"^!(dry)\s+(on|off)$", re.IGNORECASE)

def author_allowed(member: discord.Member) -> bool:
    if not ROLE_WHITELIST:
        return True
    roles = {r.name.lower() for r in member.roles}
    return bool(roles & ROLE_WHITELIST)

@client.event
def on_ready():
    guilds = ", ".join(f"{g.name}({g.id})" for g in client.guilds)
    log.info(f"Logged in as {client.user} | Guilds: {guilds}")
    if GUILD_ID_ENV:
        if not any(str(g.id) == GUILD_ID_ENV for g in client.guilds):
            log.warning("Configured GUILD_ID not found in bot's guilds")
    client.loop.create_task(worker())

async def worker():
    while True:
        message, agent, payload = await action_queue.get()
        try:
            await dispatch_to_agent(message, agent, payload)
        except Exception as e:
            log.exception("Dispatch error")
            try:
                await message.add_reaction("❌")
                await message.reply(f"Dispatch error: {e}")
            except:  # noqa
                pass
        finally:
            action_queue.task_done()

async def dispatch_to_agent(message: discord.Message, agent: str, payload: str):
    info = get_agent(agent)
    if not info:
        await message.add_reaction("❓")
        await message.reply(f"Unknown agent `{agent}`")
        return

    coords = tuple(info.get("coords", {}).get("chat_input", ()))
    if not coords or len(coords) != 2:
        await message.add_reaction("📍")
        await message.reply(f"No coords for `{agent}`. Set with `!coords {agent} x y`")
        return

    title = info.get("window_title", "")
    focused = bring_to_front(title) if title else False
    log.info(f"Routing → {agent} | focused={focused} | text len={len(payload)}")

    await type_to_gui(payload, coords, PRESS_ENTER)
    await message.add_reaction("✅")

# ─────────────────────────────────────────────────────────────────────────────
# Router
# ─────────────────────────────────────────────────────────────────────────────
@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return
    if not isinstance(message.channel, (discord.TextChannel, discord.Thread)):
        return

    # Channel security
    if CHANNEL_WHITELIST and message.channel.name not in CHANNEL_WHITELIST:
        return

    # Role security
    if isinstance(message.author, discord.Member) and not author_allowed(message.author):
        await message.add_reaction("🚫")
        return

    content = message.content.strip()

    # Control commands
    for pat in (PING_CMD, LIST_CMD, MODE_CMD, ENTER_CMD, DRY_CMD, COORDS_CMD, BIND_CMD, FOCUS_CMD):
        m = pat.match(content)
        if m:
            cmd = m.group(1).lower()
            if cmd == "ping":
                await message.reply("pong")
                return
            if cmd in ("agents", "list_agents"):
                names = ", ".join(sorted(AGENTS.keys()) or ["<none>"])
                await message.reply(f"Agents: {names}")
                return
            if cmd == "mode":
                global TYPING_MODE
                TYPING_MODE = m.group(2)
                config["typing_mode"] = TYPING_MODE
                save_config()
                await message.reply(f"Typing mode set to `{TYPING_MODE}`")
                return
            if cmd == "enter":
                global PRESS_ENTER
                PRESS_ENTER = (m.group(2).lower() == "on")
                config["press_enter_after_typing"] = PRESS_ENTER
                save_config()
                await message.reply(f"Press Enter after typing: `{PRESS_ENTER}`")
                return
            if cmd == "dry":
                global DRY_RUN
                DRY_RUN = (m.group(2).lower() == "on")
                os.environ["DRY_RUN"] = "true" if DRY_RUN else "false"
                await message.reply(f"DRY_RUN: `{DRY_RUN}`")
                return
            if cmd == "coords":
                agent, x, y = m.group(2), int(m.group(3)), int(m.group(4))
                set_coords(agent, x, y)
                await message.reply(f"Coords set for `{agent}` → ({x},{y})")
                return
            if cmd in ("bind", "bind_window"):
                agent, title = m.group(2), m.group(3).strip()
                set_window(agent, title)
                await message.reply(f"Window bound for `{agent}` → '{title}'")
                return
            if cmd == "focus":
                agent = m.group(2)
                info = get_agent(agent)
                if not info or not info.get("window_title"):
                    await message.reply(f"No window set for `{agent}`")
                    return
                ok = bring_to_front(info["window_title"])
                await message.reply(f"Focus `{agent}`: {ok}")
                return

    # Direct routing patterns:
    # 1) !agent <agent-name> <text>
    m = AGENT_CMD.match(content)
    if m:
        agent, payload = m.group(2), m.group(3)
        await action_queue.put((message, agent, payload))
        await message.add_reaction("📨")
        return

    # 2) Channel name equals agent key → route whole message body
    ch_name = message.channel.name
    if ch_name in AGENTS:
        await action_queue.put((message, ch_name, content))
        await message.add_reaction("📨")
        return

    # 3) agent tag prefix: agent-5: do this thing
    pref = re.match(r"^(\S+):\s+(.+)$", content)
    if pref and pref.group(1) in AGENTS:
        agent, payload = pref.group(1), pref.group(2)
        await action_queue.put((message, agent, payload))
        await message.add_reaction("📨")
        return

# ─────────────────────────────────────────────────────────────────────────────
# Entry
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    client.run(TOKEN)
