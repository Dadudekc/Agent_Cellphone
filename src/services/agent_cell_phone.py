#!/usr/bin/env python3
"""
Agent Cell Phone – inter-agent messaging layer for Dream.OS Cursor instances
---------------------------------------------------------------------------
• Deterministic (no human-like delays)
• Supports 2 / 4 / 8-agent screen layouts
• CLI or API usage
• Agent-to-agent communication
"""

from __future__ import annotations
import argparse, json, logging, sys, time, threading, os
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import queue

try:
    import pyautogui  # mechanical control
    # Allow disabling failsafe via environment for controlled broadcasts
    try:
        if os.environ.get("ACP_DISABLE_FAILSAFE", "0").strip() not in ("0", "", "false", "False"):
            pyautogui.FAILSAFE = False
    except Exception:
        pass
except Exception:  # pragma: no cover - depends on system display
    pyautogui = None  # tolerate headless or missing dependencies

# Response capture integration
try:
    import yaml
    # Try to import response_capture
    try:
        import sys
        response_capture_path = str(Path(__file__).parent.parent / "agent_cell_phone")
        sys.path.insert(0, response_capture_path)
        from response_capture import ResponseCapture, CaptureConfig
    except ImportError:
        ResponseCapture = None
        CaptureConfig = None
except ImportError:
    ResponseCapture = None
    CaptureConfig = None
    yaml = None

# ──────────────────────────── config paths
REPO_ROOT   = Path(__file__).resolve().parent.parent.parent    # Go up to project root (from src/services/)
CONFIG_DIR  = REPO_ROOT / "runtime" / "config"
COORD_FILE  = REPO_ROOT / "runtime" / "agent_comms" / "cursor_agent_coords.json"
# Mode configuration now lives in runtime/config to support autonomous pipelines
MODE_FILE   = CONFIG_DIR / "modes_runtime.json"
CAPTURE_CONFIG_FILE = CONFIG_DIR / "agent_capture.yaml"

# ──────────────────────────── logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)7s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger("agent_cell_phone")

# ──────────────────────────── helper enums
class MsgTag(str, Enum):
    NORMAL  = ""
    RESUME  = "[RESUME]"
    SYNC    = "[SYNC]"
    VERIFY  = "[VERIFY]"
    REPAIR  = "[REPAIR]"
    BACKUP  = "[BACKUP]"
    RESTORE = "[RESTORE]"
    CLEANUP = "[CLEANUP]"
    CAPTAIN = "[CAPTAIN]"
    TASK    = "[TASK]"
    INTEGRATE = "[INTEGRATE]"
    REPLY   = "[REPLY]"
    COORDINATE = "[COORDINATE]"
    ONBOARDING = "[ONBOARDING]"
    RESCUE  = "[RESCUE]"

# ──────────────────────────── message structure
class AgentMessage:
    """Structure for agent messages"""
    def __init__(self, from_agent: str, to_agent: str, content: str, tag: MsgTag = MsgTag.NORMAL, timestamp: Optional[datetime] = None):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.content = content
        self.tag = tag
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self) -> str:
        return f"{self.from_agent} → {self.to_agent}: {self.tag.value} {self.content}"

# ──────────────────────────── core class
class AgentCellPhone:
    """Deterministic messenger for Cursor agents with inter-agent communication and PyAutoGUI queue integration."""

    # public API ─────────────────────────
    def __init__(self, agent_id: str = "Agent-1", layout_mode: str = "2-agent", test: bool = False) -> None:
        self._agent_id = self._fmt_id(agent_id)
        self._layout_mode = layout_mode
        self._all_coords = self._load_json(COORD_FILE, "coordinates")
        self._coords = self._all_coords.get(layout_mode, {})
        self._modes  = self._load_json(MODE_FILE,  "mode templates")["modes"]
        self._cursor = _TestCursor() if test or pyautogui is None else _Cursor()
        # Default send behavior: enable Ctrl+T new-chat flow when env var is set
        self._default_new_chat = os.environ.get("ACP_DEFAULT_NEW_CHAT", "0").strip() not in ("0", "", "false", "False")
        # Throttle new-chat openings (Ctrl+T) per agent to reduce system load
        # Set via env var ACP_NEW_CHAT_INTERVAL_SEC (e.g., 1800 for 30 minutes). 0 disables throttling.
        try:
            self._new_chat_interval_sec = int(os.environ.get("ACP_NEW_CHAT_INTERVAL_SEC", "0") or 0)
        except Exception:
            self._new_chat_interval_sec = 0
        self._last_new_chat_ts: Dict[str, float] = {}
        # Cap how many new chats (Ctrl+T) we open per agent in a run (-1 for unlimited)
        try:
            self._max_new_chats_per_agent = int(os.environ.get("ACP_MAX_NEW_CHATS_PER_AGENT", "6") or 6)
        except Exception:
            self._max_new_chats_per_agent = 6
        self._new_chat_count: Dict[str, int] = {}
        # Auto-onboard pointer to be included in the same message (no chunking)
        self._auto_onboard_enabled = os.environ.get("ACP_AUTO_ONBOARD", "1").strip() not in ("0", "", "false", "False")
        self._onboard_style = os.environ.get("ACP_ONBOARD_STYLE", "simple").strip().lower()
        # Message verbosity for the single-message onboarding prefix: 'extensive' | 'simple'
        self._msg_verbosity = os.environ.get("ACP_MESSAGE_VERBOSITY", "extensive").strip().lower()
        self._single_message = os.environ.get("ACP_SINGLE_MESSAGE", "1").strip() not in ("0", "", "false", "False")
        self._onboarded_agents: set[str] = set()
        
        # Communication system
        self._message_queue = queue.Queue()
        self._conversation_history: List[AgentMessage] = []
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}
        self._listening = False
        self._listener_thread: Optional[threading.Thread] = None
        
        # PyAutoGUI Queue Integration
        self._pyautogui_queue = None
        self._queue_enabled = os.environ.get("ACP_QUEUE_ENABLED", "1").strip() not in ("0", "", "false", "False")
        self._queue_priority = int(os.environ.get("ACP_QUEUE_PRIORITY", "1") or 1)
        self._queue_timeout = float(os.environ.get("ACP_QUEUE_TIMEOUT", "30.0") or 30.0)
        
        # Response capture system
        self._response_capture: Optional[ResponseCapture] = None
        if ResponseCapture and yaml and CAPTURE_CONFIG_FILE.exists():
            try:
                cfg = yaml.safe_load(CAPTURE_CONFIG_FILE.read_text(encoding="utf-8"))
                self._response_capture = ResponseCapture(
                    coords=self._coords,
                    cfg=CaptureConfig(
                        strategy=cfg.get("default_strategy", "file"),
                        file_watch_root=cfg.get("file", {}).get("watch_root", "agent_workspaces"),
                        file_response_name=cfg.get("file", {}).get("response_filename", "response.txt"),
                        clipboard_poll_ms=int(cfg.get("clipboard", {}).get("poll_ms", 500)),
                        ocr_tesseract_cmd=cfg.get("ocr", {}).get("tesseract_cmd"),
                        ocr_lang=cfg.get("ocr", {}).get("lang", "eng"),
                        ocr_psm=int(cfg.get("ocr", {}).get("psm", 6)),
                        inbox_root=cfg.get("routing", {}).get("inbox_root", "agent_workspaces/Agent-5/inbox"),
                        fsm_enabled=bool(cfg.get("routing", {}).get("agent5_fsm_bridge_enabled", True)),
                    ),
                    get_output_rect=lambda agent: self._coords.get(agent, {}).get("output_area")
                )
                log.info("Response capture initialized with strategy: %s", cfg.get("default_strategy", "file"))
            except Exception as e:
                log.warning("Failed to initialize response capture: %s", e)
                self._response_capture = None
        
        if not self._coords:
            log.error("No coordinates found for layout mode: %s", layout_mode)
            log.info("Available modes: %s", list(self._all_coords.keys()))
            sys.exit(1)
            
        log.debug("AgentCellPhone ready for %s (test=%s, layout=%s, queue=%s)", 
                 self._agent_id, test, layout_mode, self._queue_enabled)

    def set_pyautogui_queue(self, queue_instance) -> None:
        """Set the PyAutoGUI queue instance for coordinated messaging."""
        self._pyautogui_queue = queue_instance
        log.info("PyAutoGUI queue integration enabled for %s", self._agent_id)

    def send(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL, new_chat: bool = False, nudge_stalled: bool = False, use_queue: bool = None) -> None:
        """Send a single line to a specific agent with optional PyAutoGUI queue integration.

        When new_chat is True, the cursor focuses a stable location and triggers Ctrl+T
        to open a new chat before sending to the input box.
        
        When nudge_stalled is True, attempts to nudge the agent with Shift+Backspace
        before sending the message to wake up stalled terminals.
        
        When use_queue is True (or queue is enabled globally), messages are sent through
        the PyAutoGUI queue system to prevent conflicts.
        """
        agent = self._fmt_id(agent)
        if agent not in self._coords:
            log.error("Agent %s not found in %s mode", agent, self._layout_mode)
            return
        
        # Determine if we should use the queue
        should_use_queue = use_queue if use_queue is not None else self._queue_enabled
        
        # Create message object
        msg = AgentMessage(self._agent_id, agent, message, tag)
        self._conversation_history.append(msg)
        
        # If queue is enabled and available, use it
        if should_use_queue and self._pyautogui_queue:
            log.info("→ %s QUEUED MESSAGE: %s", agent, message[:80])
            if self._pyautogui_queue.queue_message(agent, message, self._queue_priority):
                log.info("→ %s Message queued successfully", agent)
                return
            else:
                log.warning("→ %s Queue failed, falling back to direct send", agent)
        
        # Fallback to direct sending (original behavior)
        self._send_direct(agent, message, tag, new_chat, nudge_stalled)

    def _send_direct(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL, new_chat: bool = False, nudge_stalled: bool = False) -> None:
        """Direct send implementation (original behavior)."""
        agent = self._fmt_id(agent)
        
        # Determine target locations
        starter_loc = self._coords[agent].get("starter_location_box") or self._coords[agent].get("input_box")
        input_loc = self._coords[agent].get("input_box") or starter_loc

        # Progressive escalation for stalled agents
        if nudge_stalled:
            # Step 1: Try subtle nudge with Shift+Backspace
            if input_loc:
                self._cursor.move_click(input_loc["x"], input_loc["y"])
                time.sleep(0.3)
                self._cursor.hotkey("shift", "backspace")
                time.sleep(0.2)
                log.info("→ %s NUDGE (Shift+Backspace) to wake up stalled terminal", agent)

        # Respect default new-chat if requested via environment, but allow caller override to keep most sends inline
        # Default behavior remains environment-driven unless explicitly set by caller

        # Apply per-agent throttling for new-chat openings
        if new_chat:
            # Enforce per-agent max cap first
            if self._max_new_chats_per_agent >= 0 and self._new_chat_count.get(agent, 0) >= self._max_new_chats_per_agent:
                new_chat = False
            # Apply interval throttle
        if new_chat and self._new_chat_interval_sec > 0:
            now_ts = time.time()
            last_ts = self._last_new_chat_ts.get(agent, 0.0)
            elapsed = now_ts - last_ts
            if elapsed < float(self._new_chat_interval_sec):
                # Suppress new-chat; fall back to typing in the existing input area
                remaining = int(self._new_chat_interval_sec - elapsed)
                log.debug("Suppressing new-chat for %s due to throttle (%ds remaining)", agent, max(0, remaining))
                new_chat = False
            else:
                # Record this new-chat timestamp
                self._last_new_chat_ts[agent] = now_ts

        # Preferred sequence when opening a new chat:
        # 1) Click starter location to bring the interface into focus
        # 2) Wait briefly for UI to settle
        # 3) Open new chat (Ctrl+T)
        # 4) Type at starter location and send
        if new_chat and (starter_loc or input_loc):
            # Focus the interface at the starter location when available; otherwise fall back to input
            target_loc = starter_loc or input_loc
            if target_loc:
                self._cursor.move_click(target_loc["x"], target_loc["y"])
                time.sleep(0.8)
                self._cursor.hotkey("ctrl", "t")
                time.sleep(0.6)
                # Increment per-agent new-chat count
                self._new_chat_count[agent] = self._new_chat_count.get(agent, 0) + 1
        
        # Final target for typing: starter (if present) when new_chat, otherwise input box
        target = (starter_loc if new_chat and starter_loc else input_loc)

        # Build a single consolidated message if onboarding pointer is enabled
        composed_text = f"{tag.value} {message}".strip()
        if new_chat and self._auto_onboard_enabled and agent not in self._onboarded_agents and self._single_message:
            pointer = self._compose_onboarding_message(agent)
            if pointer:
                composed_text = f"{pointer}\n\n{composed_text}".strip()
                self._onboarded_agents.add(agent)

        print(f"[SEND] {agent} at ({target['x']}, {target['y']}): {composed_text[:120]}{('...' if len(composed_text)>120 else '')}")
        
        # Ensure input area is ready to prevent premature sending
        self._ensure_input_ready(target)
        
        # Type using improved buffering system
        self._type_with_shift_enter(composed_text)
        
        # Final delay before sending to ensure all input is buffered
        time.sleep(0.3)
        
        # Now send the complete message
        self._cursor.enter()
        log.info("→ %s %s", agent, composed_text[:80])

    def reply(self, to_agent: str, message: str, tag: MsgTag = MsgTag.REPLY) -> None:
        """Send a reply to a specific agent."""
        self.send(to_agent, message, tag)

    def broadcast(self, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send the same message to every configured agent."""
        for agent in sorted(self._coords):
            if agent != self._agent_id:  # Don't send to self
                self.send(agent, message, tag)

    def coordinate(self, agents: List[str], message: str) -> None:
        """Send a coordination message to multiple specific agents."""
        for agent in agents:
            if agent != self._agent_id:  # Don't send to self
                self.send(agent, message, MsgTag.COORDINATE)

    def exec_mode(self, agent: str, mode_key: str, **kw) -> None:
        """Fill a mode template then send."""
        tmpl = self._modes[mode_key]["prompt_template"]
        self.send(agent, tmpl.format(agent_id=agent, **kw), MsgTag[mode_key.upper()])

    def start_listening(self) -> None:
        """Start listening for incoming messages."""
        if self._listening:
            return
        
        self._listening = True
        self._listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._listener_thread.start()
        log.info("Started listening for messages as %s", self._agent_id)

    def stop_listening(self) -> None:
        """Stop listening for incoming messages."""
        self._listening = False
        if self._listener_thread:
            self._listener_thread.join(timeout=1)
        log.info("Stopped listening for messages")

    def register_handler(self, message_type: str, handler: Callable[[AgentMessage], None]) -> None:
        """Register a message handler for specific message types."""
        self._message_handlers[message_type] = handler

    def get_conversation_history(self) -> List[AgentMessage]:
        """Get the conversation history."""
        return self._conversation_history.copy()

    def get_available_agents(self) -> List[str]:
        """Get list of available agents in current layout mode."""
        return list(self._coords.keys())

    def get_layout_mode(self) -> str:
        """Get current layout mode."""
        return self._layout_mode

    def get_available_layouts(self) -> List[str]:
        """Get list of available layout modes."""
        return list(self._all_coords.keys())

    def get_agent_id(self) -> str:
        """Get the current agent ID."""
        return self._agent_id

    def send_queued(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL, priority: int = None, timeout: float = None) -> bool:
        """Send a message through the PyAutoGUI queue system.
        
        Args:
            agent: Target agent
            message: Message content
            tag: Message tag
            priority: Queue priority (lower = higher priority)
            timeout: Maximum wait time for queue processing
            
        Returns:
            True if message was queued successfully, False otherwise
        """
        if not self._pyautogui_queue:
            log.warning("PyAutoGUI queue not available, falling back to direct send")
            self.send(agent, message, tag)
            return False
        
        priority = priority if priority is not None else self._queue_priority
        timeout = timeout if timeout is not None else self._queue_timeout
        
        try:
            # Add message to queue
            if self._pyautogui_queue.queue_message(agent, message, priority):
                log.info("→ %s Message queued with priority %d: %s", agent, priority, message[:80])
                return True
            else:
                log.error("→ %s Failed to queue message", agent)
                return False
        except Exception as e:
            log.error("→ %s Queue error: %s", agent, e)
            return False

    def get_queue_status(self) -> Dict[str, any]:
        """Get the current PyAutoGUI queue status."""
        if self._pyautogui_queue:
            return self._pyautogui_queue.get_queue_status()
        else:
            return {
                "queue_size": 0,
                "processing": False,
                "agent_locks": {},
                "queue_available": False
            }

    def wait_for_queue_clear(self, timeout: float = None) -> bool:
        """Wait for the PyAutoGUI queue to clear.
        
        Args:
            timeout: Maximum wait time in seconds
            
        Returns:
            True if queue cleared within timeout, False otherwise
        """
        if not self._pyautogui_queue:
            return True  # No queue to wait for
        
        timeout = timeout if timeout is not None else self._queue_timeout
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            status = self._pyautogui_queue.get_queue_status()
            if status["queue_size"] == 0:
                log.info("Queue cleared successfully")
                return True
            time.sleep(0.1)
        
        log.warning("Queue clear timeout after %.1f seconds", timeout)
        return False

    def clear_queue(self) -> bool:
        """Clear the PyAutoGUI message queue.

        Returns:
            True if queue was cleared, False otherwise
        """
        if not self._pyautogui_queue:
            return False

        try:
            result = self._pyautogui_queue.clear_queue()
            if result:
                log.info("PyAutoGUI queue cleared")
            else:
                log.warning("PyAutoGUI queue clear failed")
            return result
        except Exception as e:
            log.error("Queue clear error: %s", e)
            return False

    # private helpers ────────────────────
    def _listen_loop(self) -> None:
        """Main listening loop for incoming messages.

        Polls the response capture inbox (if configured) and the agent's
        filesystem inbox for JSON envelopes. Each new envelope is parsed and
        dispatched via `_handle_incoming_message`.
        """
        # Allow tests to override inbox directories
        if hasattr(self, "_inbox_override"):
            inbox_dirs = [Path(p) for p in self._inbox_override]
        else:
            inbox_dirs: List[Path] = []
            if self._response_capture:
                try:
                    inbox_dirs.append(Path(self._response_capture.cfg.inbox_root))
                except Exception:
                    pass
            inbox_dirs.append(REPO_ROOT / "agent_workspaces" / self._agent_id / "inbox")

        seen: set[Path] = set()
        while self._listening:
            for inbox in inbox_dirs:
                try:
                    if not inbox.exists():
                        continue
                    for msg_file in sorted(inbox.glob("*.json")):
                        if msg_file in seen:
                            continue
                        try:
                            envelope = json.loads(msg_file.read_text(encoding="utf-8"))
                        except Exception as e:
                            log.error("Failed to read envelope %s: %s", msg_file, e)
                            seen.add(msg_file)
                            continue

                        from_agent = self._fmt_id(envelope.get("from", ""))
                        to_agent = self._fmt_id(envelope.get("to", self._agent_id))
                        if to_agent != self._agent_id:
                            seen.add(msg_file)
                            continue

                        content = (
                            envelope.get("summary")
                            or envelope.get("content")
                            or envelope.get("message")
                            or json.dumps(envelope.get("payload", {}))
                        )
                        tag_str = str(envelope.get("type", "")).upper()
                        tag = MsgTag[tag_str] if tag_str in MsgTag.__members__ else MsgTag.NORMAL

                        self._handle_incoming_message(
                            AgentMessage(from_agent, to_agent, content, tag)
                        )
                        seen.add(msg_file)
                        try:
                            msg_file.unlink()
                        except Exception:
                            pass
                except Exception as e:
                    log.error("Error processing inbox %s: %s", inbox, e)

            time.sleep(0.5)

    def _handle_incoming_message(self, message: AgentMessage) -> None:
        """Handle an incoming message."""
        self._conversation_history.append(message)
        print(f"[RECEIVE] {message}")
        
        # Call registered handlers
        if message.tag.value in self._message_handlers:
            try:
                self._message_handlers[message.tag.value](message)
            except Exception as e:
                log.error("Error in message handler: %s", e)
        
        # Default handling based on message type
        if message.tag == MsgTag.COORDINATE:
            self._handle_coordination_message(message)
        elif message.tag == MsgTag.REPLY:
            self._handle_reply_message(message)

    def _handle_coordination_message(self, message: AgentMessage) -> None:
        """Handle coordination messages."""
        print(f"[COORDINATE] {self._agent_id} processing coordination from {message.from_agent}")
        # Auto-reply to coordination messages
        if "API" in message.content and "GUI" in message.content:
            self.reply(message.from_agent, "Understood. I'll coordinate with the team on API-GUI integration.")

    def _handle_reply_message(self, message: AgentMessage) -> None:
        """Handle reply messages."""
        print(f"[REPLY] {self._agent_id} processing reply from {message.from_agent}")
        # Auto-acknowledge replies
        if "ready" in message.content.lower():
            self.reply(message.from_agent, "Acknowledged. Ready to proceed with next phase.")

    def _load_json(self, path: Path, label: str) -> Dict[str, Any]:
        try:
            with open(path, "r", encoding="utf-8") as fp:
                return json.load(fp)
        except Exception as e:
            log.error("Cannot load %s file %s: %s", label, path, e)
            sys.exit(1)

    @staticmethod
    def _fmt_id(agent: str) -> str:
        return agent if agent.startswith("Agent-") else f"Agent-{agent}"

    # ──────────────────────────── onboarding helper
    def _ensure_input_ready(self, target_loc: dict) -> None:
        """Ensure the input area is ready to receive text without premature sending.
        
        This method performs several checks to prevent the terminal from sending
        messages before the complete input is ready.
        """
        # Click to focus the input area
        self._cursor.move_click(target_loc["x"], target_loc["y"])
        time.sleep(0.3)  # Wait for focus
        
        # Clear any existing partial input that might cause issues
        try:
            self._cursor.hotkey("ctrl", "a")  # Select all
            time.sleep(0.1)
            self._cursor.hotkey("backspace")  # Clear
            time.sleep(0.2)
        except:
            # If Ctrl+A fails, just clear with backspace
            for _ in range(10):  # Clear up to 10 characters
                self._cursor.hotkey("backspace")
                time.sleep(0.05)
        
        # Additional delay to ensure input area is stable
        time.sleep(0.3)

    def _type_with_shift_enter(self, text: str) -> None:
        """Type the given text with proper input buffering to prevent premature sending.
        
        This method ensures the complete message is typed before any Enter key is pressed,
        preventing the system from sending prompts early due to terminal input buffering issues.
        """
        # Normalize line endings
        normalized = text.replace("\r\n", "\n").replace("\r", "\n")
        
        # Split into lines but don't send until complete
        lines = normalized.split("\n")
        
        for idx, line in enumerate(lines):
            if line:
                # Type the line content
                self._cursor.type(line)
                time.sleep(0.05)  # Small delay between characters for stability
            
            # For multi-line messages, use proper line breaks that don't send
            if idx < len(lines) - 1:
                # Use Ctrl+Shift+Enter or just Enter depending on the application
                # This prevents premature sending while maintaining readability
                try:
                    # Try Ctrl+Shift+Enter first (more reliable for preventing send)
                    self._cursor.hotkey("ctrl", "shift", "enter")
                except:
                    # Fallback to regular Enter with longer delay
                    self._cursor.hotkey("enter")
                    time.sleep(0.1)  # Longer delay to ensure input is buffered
                
                time.sleep(0.1)  # Additional delay for UI stability
        
        # Final delay to ensure all input is properly buffered
        time.sleep(0.2)

    def _compose_onboarding_message(self, agent: str) -> str:
        """Create a single-shot onboarding + FSM primer block for a newly opened chat.

        When ACP_MESSAGE_VERBOSITY=extensive (default), produce a detailed but single-message
        briefing. Still returns a single string to be sent with exactly one Enter.
        """
        role_hint = {
            "Agent-1": "Coordinator & PM",
            "Agent-2": "Tech Architect",
            "Agent-3": "Data/Analytics",
            "Agent-4": "DevOps/Infra",
            "Agent-5": "AI/ML Engineer",
            "Agent-6": "Frontend/UI",
            "Agent-7": "Backend/API",
            "Agent-8": "QA/Testing",
        }.get(agent, "Team Member")

        bullet = "• " if self._onboard_style != "ascii" else "* "

        # Extensive single-message briefing
        if self._msg_verbosity == "extensive":
            if agent == "Agent-5":
                return (
                    "CAPTAIN BRIEFING — Agent-5\n"
                    "Context: ACP (visible typing) + file inbox (silent JSON). You own coordination, contracts, and verification gates.\n"
                    f"Start here: agent_workspaces/onboarding/README.md; then CORE_PROTOCOLS.md; DEVELOPMENT_STANDARDS.md.\n"
                    "Operating model:\n"
                    f"{bullet}Contracts come from repos' TASK_LIST.md → convert to machine tasks → assign via FSM (Agent-5 orchestrator).\n"
                    f"{bullet}Anti-duplication: search first; prefer reuse/refactor across repos.\n"
                    f"{bullet}Quality: ship small, verifiable edits with tests/build evidence.\n"
                    "Captain duties:\n"
                    f"{bullet}Seed/adjust contracts; throttle to small batches; prevent duplication across repos.\n"
                    f"{bullet}Assign via FSM (round‑robin/open tasks). Require acceptance criteria and evidence links.\n"
                    f"{bullet}Enforce verify gates; if blocked by perms, stage diffs and request review.\n"
                    f"{bullet}Monitor Agent-5/state.json and contracts.json; keep comms in D:/repos/communications/overnight_YYYYMMDD_/Agent-5.\n"
                    "FSM loop:\n"
                    f"{bullet}Each cadence, trigger fsm_request; agents check inbox, execute, and send fsm_update (task_id, state, summary, evidence).\n"
                    f"{bullet}When verified, issue next task; maintain momentum; minimize context switching."
                )
            else:
                return (
                    f"WELCOME {agent} — {role_hint}\n"
                    "Context: ACP types into Cursor; file inbox carries structured JSON. Work from D:/repos.\n"
                    f"Start here: agent_workspaces/onboarding/README.md → role docs → DEVELOPMENT_STANDARDS.md → CORE_PROTOCOLS.md.\n"
                    "Norms:\n"
                    f"{bullet}Reuse/refactor; avoid duplication and stubs; keep edits small and cohesive.\n"
                    f"{bullet}Provide tests/build evidence; write concise commit messages.\n"
                    "Channels:\n"
                    f"{bullet}ACP: motivational nudges and coordination.\n"
                    f"{bullet}Inbox: task/sync/verify messages with task_id/state/evidence (durable/auditable).\n"
                    "Action now:\n"
                    f"{bullet}Open your assigned repo’s TASK_LIST.md, select the highest‑leverage contract, execute to acceptance criteria.\n"
                    f"{bullet}Send fsm_update to Agent-5 inbox with task_id, state, summary, and evidence (tests/build output). If blocked, summarize and propose next steps."
                )

        # Simple/succinct single-paragraph pointer
        lines: list[str] = []
        if agent == "Agent-5":
            lines.append(
                "Captain: start here agent_workspaces/onboarding/README.md; coordinate contracts from TASK_LIST.md; use FSM to assign small,"
                " evidence-backed tasks; enforce verify gates; keep comms under D:/repos/communications/overnight_YYYYMMDD_/Agent-5."
                " Trigger fsm_request each cadence and nudge agents to maintain momentum."
            )
        else:
            lines.append(
                f"Start here agent_workspaces/onboarding/README.md ({role_hint}). Norms: reuse/refactor, no duplication, small verifiable edits"
                " with tests/build. Channels: ACP nudges; inbox {task/sync/verify} with task_id/state/evidence. Action: open your repo’s"
                " TASK_LIST.md, pick one contract, execute, then inbox update with evidence."
            )
        return " ".join(lines).strip()

    # Response capture methods
    def start_capture_for_agents(self, agents: List[str]) -> None:
        """Start response capture for specified agents"""
        if not self._response_capture:
            log.warning("Response capture not available")
            return
        
        for agent in agents:
            if agent in self._coords:
                self._response_capture.start_for(agent)
                log.info("Started response capture for %s", agent)
            else:
                log.warning("Agent %s not found in layout %s", agent, self._layout_mode)

    def stop_capture(self) -> None:
        """Stop all response capture threads"""
        if self._response_capture:
            self._response_capture.stop_all()
            log.info("Stopped all response capture threads")

    def is_capture_enabled(self) -> bool:
        """Check if response capture is available and enabled"""
        return self._response_capture is not None

    def nudge_agent(self, agent: str, nudge_type: str = "subtle") -> None:
        """Nudge a stalled agent using different escalation strategies.
        
        Args:
            agent: Target agent to nudge
            nudge_type: Type of nudge - "subtle", "moderate", or "aggressive"
        """
        agent = self._fmt_id(agent)
        if agent not in self._coords:
            log.error("Agent %s not found in %s mode", agent, self._layout_mode)
            return
        
        input_loc = self._coords[agent].get("input_box")
        if not input_loc:
            log.error("No input location found for agent %s", agent)
            return
        
        log.info("→ %s NUDGE (%s) to wake up stalled terminal", agent, nudge_type.upper())
        
        if nudge_type == "subtle":
            # Subtle nudge: Shift+Backspace to clear any partial input
            self._cursor.move_click(input_loc["x"], input_loc["y"])
            time.sleep(0.3)
            self._cursor.hotkey("shift", "backspace")
            time.sleep(0.2)
            
        elif nudge_type == "moderate":
            # Moderate nudge: Clear input area and add a small delay
            self._cursor.move_click(input_loc["x"], input_loc["y"])
            time.sleep(0.3)
            self._cursor.hotkey("ctrl", "a")  # Select all
            time.sleep(0.1)
            self._cursor.hotkey("backspace")  # Clear
            time.sleep(0.2)
            
        elif nudge_type == "aggressive":
            # Aggressive nudge: Clear and add a visual indicator
            self._cursor.move_click(input_loc["x"], input_loc["y"])
            time.sleep(0.3)
            self._cursor.hotkey("ctrl", "a")  # Select all
            time.sleep(0.1)
            self._cursor.hotkey("backspace")  # Clear
            time.sleep(0.2)
            # Type a subtle wake-up character
            self._cursor.type(".")
            time.sleep(0.1)
            self._cursor.hotkey("backspace")  # Remove it
            time.sleep(0.2)
        
        log.info("→ %s NUDGE completed (%s)", agent, nudge_type)

    def progressive_escalation(self, agent: str, message: str, tag: MsgTag = MsgTag.RESCUE) -> None:
        """Progressive escalation strategy for stalled agents.
        
        This method implements a three-tier approach:
        1. Subtle nudge (Shift+Backspace)
        2. Rescue message in existing chat
        3. New chat if all else fails
        """
        agent = self._fmt_id(agent)
        if agent not in self._coords:
            log.error("Agent %s not found in %s mode", agent, self._layout_mode)
            return
        
        log.info("→ %s PROGRESSIVE ESCALATION starting", agent)
        
        # Step 1: Try subtle nudge
        try:
            self.nudge_agent(agent, "subtle")
            time.sleep(1.0)  # Wait for potential response
        except Exception as e:
            log.warning("Subtle nudge failed for %s: %s", agent, e)
        
        # Step 2: Send rescue message in existing chat
        try:
            self.send(agent, message, tag, new_chat=False, nudge_stalled=False)
            time.sleep(2.0)  # Wait for potential response
        except Exception as e:
            log.warning("Rescue message failed for %s: %s", agent, e)
        
        # Step 3: Escalate to new chat if needed
        try:
            log.info("→ %s Escalating to new chat", agent)
            self.send(agent, message, tag, new_chat=True, nudge_stalled=False)
        except Exception as e:
            log.error("New chat escalation failed for %s: %s", agent, e)
        
        log.info("→ %s PROGRESSIVE ESCALATION completed", agent)

# ──────────────────────────── cursor abstraction
class _Cursor:
    def move_click(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y); pyautogui.click()

    def type(self, text: str) -> None:
        pyautogui.typewrite(text, interval=0)

    def enter(self) -> None:
        pyautogui.press("enter")

    def hotkey(self, *keys: str) -> None:
        pyautogui.hotkey(*keys)

class _TestCursor(_Cursor):
    """Headless stub – records actions instead of executing."""
    def __init__(self) -> None: self.record: List[str]=[]
    def move_click(self,x:int,y:int)->None: self.record.append(f"move({x},{y})+click")
    def type(self,t:str)->None: self.record.append(f"type({t})")
    def enter(self)->None: self.record.append("enter")
    def hotkey(self, *keys: str) -> None: self.record.append(f"hotkey({','.join(keys)})")

# ──────────────────────────── CLI
def _cli() -> None:
    p = argparse.ArgumentParser("agent_cell_phone")
    p.add_argument("-a","--agent", help="target Agent-N  (omit for broadcast)")
    p.add_argument("-m","--msg",   help="message text")
    p.add_argument("-t","--tag",   default="normal",
                   choices=[e.name.lower() for e in MsgTag], help="message tag")
    p.add_argument("--mode", help="send predefined mode template key (overrides --msg)")
    p.add_argument("--layout", default="2-agent", help="layout mode (2-agent, 4-agent, 8-agent)")
    p.add_argument("--test", action="store_true", help="dry-run / headless")
    p.add_argument("--new-chat", action="store_true", help="press Ctrl+T at starter location before sending")
    p.add_argument("--list-layouts", action="store_true", help="list available layout modes")
    p.add_argument("--list-agents", action="store_true", help="list available agents in current layout")
    args = p.parse_args()

    # Handle list commands first
    if args.list_layouts:
        try:
            all_coords = json.load(open(COORD_FILE, "r"))
            print("Available layout modes:")
            for mode in all_coords.keys():
                agent_count = len(all_coords[mode])
                print(f"  {mode} ({agent_count} agents)")
        except Exception as e:
            print(f"Error loading layouts: {e}")
        return

    acp = AgentCellPhone(layout_mode=args.layout, test=args.test)

    if args.list_agents:
        agents = acp.get_available_agents()
        print(f"Available agents in {args.layout} mode:")
        for agent in agents:
            print(f"  {agent}")
        return

    if args.mode:
        target = args.agent or sys.exit("mode requires --agent")
        acp.exec_mode(acp._fmt_id(target), args.mode)
    elif args.msg:
        if args.agent:
            acp.send(args.agent, args.msg, MsgTag[args.tag.upper()], new_chat=args.new_chat)
        else:
            # Broadcast with new-chat is not supported uniformly; send per agent behaves the same
            acp.broadcast(args.msg, MsgTag[args.tag.upper()])
    else:
        p.print_help()

if __name__ == "__main__":
    _cli() 