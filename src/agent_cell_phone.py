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
import argparse, json, logging, sys, time, threading
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
import queue

try:
    import pyautogui  # mechanical control
except ImportError:
    pyautogui = None                          # tolerates headless tests

# ──────────────────────────── config paths
REPO_ROOT   = Path(__file__).resolve().parent    # Current directory
CONFIG_DIR  = REPO_ROOT / "runtime" / "config"
COORD_FILE  = CONFIG_DIR / "cursor_agent_coords.json"
MODE_FILE   = CONFIG_DIR / "templates" / "agent_modes.json"

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
    """Deterministic messenger for Cursor agents with inter-agent communication."""

    # public API ─────────────────────────
    def __init__(self, agent_id: str = "Agent-1", layout_mode: str = "2-agent", test: bool = False) -> None:
        self._agent_id = self._fmt_id(agent_id)
        self._layout_mode = layout_mode
        self._all_coords = self._load_json(COORD_FILE, "coordinates")
        self._coords = self._all_coords.get(layout_mode, {})
        self._modes  = self._load_json(MODE_FILE,  "mode templates")["modes"]
        self._cursor = _TestCursor() if test or pyautogui is None else _Cursor()
        
        # Communication system
        self._message_queue = queue.Queue()
        self._conversation_history: List[AgentMessage] = []
        self._message_handlers: Dict[str, Callable[[AgentMessage], None]] = {}
        self._listening = False
        self._listener_thread: Optional[threading.Thread] = None
        
        if not self._coords:
            log.error("No coordinates found for layout mode: %s", layout_mode)
            log.info("Available modes: %s", list(self._all_coords.keys()))
            sys.exit(1)
            
        log.debug("AgentCellPhone ready for %s (test=%s, layout=%s)", self._agent_id, test, layout_mode)

    def send(self, agent: str, message: str, tag: MsgTag = MsgTag.NORMAL) -> None:
        """Send a single line to a specific agent."""
        agent = self._fmt_id(agent)
        if agent not in self._coords:
            log.error("Agent %s not found in %s mode", agent, self._layout_mode)
            return
        
        # Create message object
        msg = AgentMessage(self._agent_id, agent, message, tag)
        self._conversation_history.append(msg)
        
        loc   = self._coords[agent]["input_box"]
        text  = f"{tag.value} {message}".strip()
        print(f"[SEND] {agent} at ({loc['x']}, {loc['y']}): {text}")
        self._cursor.move_click(loc["x"], loc["y"])
        self._cursor.type(text)
        self._cursor.enter()
        log.info("→ %s %s", agent, text[:80])

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

    # private helpers ────────────────────
    def _listen_loop(self) -> None:
        """Main listening loop for incoming messages."""
        while self._listening:
            try:
                # Simulate checking for incoming messages
                # In a real implementation, this would monitor the agent's input/output
                time.sleep(0.1)
                
                # For demo purposes, we'll simulate incoming messages after a delay
                if not hasattr(self, '_demo_messages_sent'):
                    self._demo_messages_sent = True
                    # Simulate some incoming messages after a delay
                    threading.Timer(2.0, self._simulate_incoming_messages).start()
                    
            except Exception as e:
                log.error("Error in listen loop: %s", e)

    def _simulate_incoming_messages(self) -> None:
        """Simulate incoming messages for demo purposes."""
        if self._agent_id == "Agent-1":
            # Agent-1 receives responses from Agent-3 and Agent-4
            self._handle_incoming_message(AgentMessage("Agent-3", self._agent_id, "I'll create the GUI components. What API endpoints do you need?", MsgTag.REPLY))
            time.sleep(1)
            self._handle_incoming_message(AgentMessage("Agent-4", self._agent_id, "I'll handle the integration layer. Ready to connect API and GUI.", MsgTag.REPLY))
        elif self._agent_id == "Agent-3":
            # Agent-3 receives from Agent-1 and Agent-4
            self._handle_incoming_message(AgentMessage("Agent-1", self._agent_id, "API endpoints ready: GET/POST/PUT/DELETE /resume. Please integrate into GUI.", MsgTag.COORDINATE))
            time.sleep(1)
            self._handle_incoming_message(AgentMessage("Agent-4", self._agent_id, "Integration utilities ready. I'll provide data binding for your GUI.", MsgTag.REPLY))
        elif self._agent_id == "Agent-4":
            # Agent-4 receives from Agent-1 and Agent-3
            self._handle_incoming_message(AgentMessage("Agent-1", self._agent_id, "API validation endpoints added. Ready for integration testing.", MsgTag.REPLY))
            time.sleep(1)
            self._handle_incoming_message(AgentMessage("Agent-3", self._agent_id, "GUI components created: ResumeForm, ResumeList, ResumeView. Ready for API binding.", MsgTag.REPLY))

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

# ──────────────────────────── cursor abstraction
class _Cursor:
    def move_click(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y); pyautogui.click()

    def type(self, text: str) -> None:
        pyautogui.typewrite(text, interval=0)

    def enter(self) -> None:
        pyautogui.press("enter")

class _TestCursor(_Cursor):
    """Headless stub – records actions instead of executing."""
    def __init__(self) -> None: self.record: List[str]=[]
    def move_click(self,x:int,y:int)->None: self.record.append(f"move({x},{y})+click")
    def type(self,t:str)->None: self.record.append(f"type({t})")
    def enter(self)->None: self.record.append("enter")

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
            acp.send(args.agent, args.msg, MsgTag[args.tag.upper()])
        else:
            acp.broadcast(args.msg, MsgTag[args.tag.upper()])
    else:
        p.print_help()

if __name__ == "__main__":
    _cli() 