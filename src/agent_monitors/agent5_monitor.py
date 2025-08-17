#!/usr/bin/env python3
"""
Agent-5 Production Monitor
==========================
Real production monitor that:
- Monitors agent responses via file timestamps
- Sends real rescue messages via AgentCellPhone
- Persists state and health metrics
- Integrates with existing response capture pipeline
"""

from __future__ import annotations
import os
import json
import time
import signal
import threading
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

# Real ACP send
from src.services.agent_cell_phone import AgentCellPhone, MsgTag  # type: ignore

# File-lane capture (flows into inbox/FSM you already wired)
try:
    from src.agent_cell_phone.response_capture import ResponseCapture, CaptureConfig  # type: ignore
    HAS_RESPONSE_CAPTURE = True
except ImportError:
    HAS_RESPONSE_CAPTURE = False

# Optional DB lane (only if you've added cursor_capture_v2)
try:
    from src.cursor_capture_v2.watcher import CursorDBWatcher  # type: ignore
    HAS_DB_LANE = True
except Exception:
    HAS_DB_LANE = False

# Runtime directories
RUNTIME = Path("runtime/agent_monitors/agent5")
RUNTIME.mkdir(parents=True, exist_ok=True)
STATE = RUNTIME / "activity.json"
HEALTH = RUNTIME / "health.json"
METRICS = RUNTIME / "metrics.json"
LOG = RUNTIME / "monitor.log"

def _iso() -> str:
    """Get current timestamp in ISO format"""
    return datetime.now(timezone.utc).isoformat()

def _log(msg: str):
    """Write to monitor log"""
    try:
        with LOG.open("a", encoding="utf-8") as f:
            f.write(f"{_iso()} {msg}\n")
    except Exception:
        pass  # Don't fail if logging fails

@dataclass
class MonitorConfig:
    """Configuration for the Agent-5 monitor"""
    agents: List[str]
    stall_threshold_sec: int = 600   # 10 minutes - FIXED: realistic stall threshold
    warn_threshold_sec: int = 480    # 8 minutes - FIXED: warn before stall
    normal_response_time: int = 300  # 5 minutes - FIXED: normal agent response time
    warn_ratio: float = 0.8
    check_every_sec: int = 30        # FIXED: check every 30 seconds instead of 5
    file_watch_root: str = "agent_workspaces"
    file_response_name: str = "response.txt"
    inbox_root: str = "runtime/agent_comms/inbox"
    fsm_enabled: bool = True
    rescue_cooldown_sec: int = 300   # 5 minutes between rescues
    active_grace_sec: int = 300      # 5 minutes before considered idle
    onboarding_grace_period: int = 600  # 10 minutes grace during onboarding
    use_db_lane: bool = False
    workspace_map_path: str = "src/runtime/config/agent_workspace_map.json"
    test_mode: bool = False  # Enable test mode for testing
    
    def __post_init__(self):
        """Apply environment variable overrides after initialization"""
        # Environment variable overrides
        if os.environ.get("AGENT_STALL_SEC"):
            try:
                self.stall_threshold_sec = int(os.environ["AGENT_STALL_SEC"])
            except ValueError:
                pass  # Keep default if invalid
        
        if os.environ.get("AGENT_CHECK_SEC"):
            try:
                self.check_every_sec = int(os.environ["AGENT_CHECK_SEC"])
            except ValueError:
                pass  # Keep default if invalid

class Agent5Monitor:
    """Production monitor for Agent-5 to track agent responses and send rescues"""
    
    def __init__(self, cfg: MonitorConfig, sender: str = "Agent-5", layout: str = "5-agent", test: bool = False):
        self.cfg = cfg
        self.acp = AgentCellPhone(agent_id=sender, layout_mode=layout, test=test)
        self.capture: Optional[ResponseCapture] = None
        self.db_lane: Optional[CursorDBWatcher] = None
        self.last_activity: Dict[str, float] = {}
        self.last_rescue: Dict[str, float] = {}
        self._stop = threading.Event()
        self._start_time = time.time()

    # ---- lifecycle ----
    def start(self) -> bool:
        """Start the monitor"""
        try:
            self._init_capture()
            self._init_db_lane()
            self._restore_state()

            agents = self.cfg.agents or self.acp.get_available_agents()
            if not agents:
                _log("no agents available; exiting")
                return False

            # Default to "now" to avoid false stalls on boot
            now = time.time()
            for agent in agents:
                self.last_activity.setdefault(agent, now)

            # Start file-lane capture (lets your existing pipeline keep flowing)
            if self.capture:
                for agent in agents:
                    try:
                        self.capture.start_for(agent)
                        _log(f"capture started for {agent}")
                    except Exception as e:
                        _log(f"capture failed for {agent}: {e}")

            # Start monitoring thread
            threading.Thread(target=self._loop, daemon=True).start()
            _log(f"monitor started with {len(agents)} agents")
            return True
            
        except Exception as e:
            _log(f"start failed: {e}")
            return False

    def stop(self):
        """Stop the monitor"""
        self._stop.set()
        try:
            if self.capture:
                self.capture.stop_all()
        except Exception:
            pass
        try:
            if self.db_lane:
                self.db_lane.stop()
        except Exception:
            pass
        self._persist_state()
        self._write_health(False, "stopped")
        _log("monitor stopped")

    # ---- init lanes ----
    def _init_capture(self):
        """Initialize response capture system"""
        if not HAS_RESPONSE_CAPTURE:
            _log("response capture not available")
            return
            
        try:
            cfg = CaptureConfig(
                strategy="file",
                file_watch_root=self.cfg.file_watch_root,
                file_response_name=self.cfg.file_response_name,
                clipboard_poll_ms=500,
                ocr_tesseract_cmd=None,
                ocr_lang="eng",
                ocr_psm=6,
                inbox_root=self.cfg.inbox_root,
                fsm_enabled=self.cfg.fsm_enabled,
            )
            # File lane doesn't need screen rects
            self.capture = ResponseCapture(
                coords={}, 
                cfg=cfg, 
                get_output_rect=lambda a: {"x": 0, "y": 0, "width": 1, "height": 1}
            )
            _log("response capture initialized")
        except Exception as e:
            _log(f"response capture init failed: {e}")

    def _init_db_lane(self):
        """Initialize cursor database monitoring (optional)"""
        if not (self.cfg.use_db_lane and HAS_DB_LANE):
            return
            
        try:
            agent_map = {}
            p = Path(self.cfg.workspace_map_path)
            if p.exists():
                agent_map = json.loads(p.read_text(encoding="utf-8"))
            
            self.db_lane = CursorDBWatcher(agent_map=agent_map)
            threading.Thread(target=self.db_lane.run, daemon=True).start()
            _log("db lane started")
        except Exception as e:
            _log(f"db lane failed: {e}")

    # ---- main loop ----
    def _loop(self):
        """Main monitoring loop"""
        while not self._stop.is_set():
            try:
                self._tick()
            except Exception as e:
                _log(f"tick error: {e}")
            time.sleep(self.cfg.check_every_sec)

    def _tick(self):
        """Single monitoring tick"""
        agents = self.cfg.agents or self.acp.get_available_agents()
        self._update_activity_from_files(agents)

        now = time.time()
        metrics = {"ts": _iso(), "agents": {}}
        
        for agent in agents:
            age = now - self.last_activity.get(agent, 0.0)
            
            # FIXED: Better status determination with realistic timing
            if age < self.cfg.active_grace_sec:
                status = "active"
            elif age < self.cfg.warn_threshold_sec:
                status = "idle"
            elif age < self.cfg.stall_threshold_sec:
                status = "warning"
            else:
                status = "stalled"
                
            metrics["agents"][agent] = {"age_sec": age, "status": status}

            # FIXED: Progressive stall detection with realistic timing
            if age >= self.cfg.stall_threshold_sec:
                # Agent is stalled - send rescue
                self._rescue(agent)
            elif age >= self.cfg.warn_threshold_sec:
                # Agent might be stalling - send warning nudge
                self._send_stall_warning(agent)

        self._write_metrics(metrics)
        self._write_health(True, "running")
        self._persist_state()

    # ---- activity sources ----
    def _update_activity_from_files(self, agents: List[str]):
        """Update activity timestamps from file modification times"""
        root = Path(self.cfg.file_watch_root)
        
        for agent in agents:
            ws = root / agent
            # Prefer state.json; fallback to response.txt
            st = ws / "state.json"
            rt = ws / self.cfg.file_response_name
            mtime = 0.0
            
            try:
                if st.exists():
                    mtime = max(mtime, st.stat().st_mtime)
                if rt.exists():
                    mtime = max(mtime, rt.stat().st_mtime)
            except Exception:
                pass
                
            if mtime:
                # Normalize to seconds and only move forward
                self.last_activity[agent] = max(self.last_activity.get(agent, 0.0), float(mtime))

    # ---- rescue path ----
    def _send_stall_warning(self, agent: str):
        """Send Shift+Backspace nudge for potential stall (before full rescue)"""
        now = time.time()
        
        # Check cooldown to prevent spam
        if (now - self.last_rescue.get(agent, 0.0)) < self.cfg.rescue_cooldown_sec:
            return
            
        try:
            # Send gentle warning with Shift+Backspace nudge
            warning_msg = (
                f"[STALL WARNING] {agent}, you appear to be taking longer than usual to respond.\n"
                f"Sending Shift+Backspace nudge to ensure your terminal is responsive.\n"
                f"Please confirm you are working on your task."
            )
            
            # Use progressive escalation with nudge flag
            if hasattr(self.acp, 'progressive_escalation'):
                self.acp.progressive_escalation(agent, warning_msg, MsgTag.RESCUE)
            else:
                # Fallback to direct send with nudge flag
                self.acp.send(agent, warning_msg, MsgTag.RESCUE, False, True)
            
            self.last_rescue[agent] = now
            _log(f"stall warning sent -> {agent}")
            
        except Exception as e:
            _log(f"stall warning failed -> {agent}: {e}")
    
    def _rescue(self, agent: str):
        """Send rescue message to stalled agent using progressive escalation"""
        now = time.time()
        
        # Check cooldown to prevent spam
        if (now - self.last_rescue.get(agent, 0.0)) < self.cfg.rescue_cooldown_sec:
            return
            
        try:
            # Use progressive escalation for stalled agents
            rescue_msg = (
                f"[RESCUE] {agent}, you appear stalled.\n"
                f"Reply using the Dream.OS block:\n"
                f"Task: <what you're doing>\n"
                f"Actions Taken:\n- ...\n"
                f"Commit Message: <if any>\n"
                f"Status: 🟡 pending or ✅ done"
            )
            
            # Progressive escalation: nudge → rescue message → new chat
            if hasattr(self.acp, 'progressive_escalation'):
                # Use the new progressive escalation system
                self.acp.progressive_escalation(agent, rescue_msg, MsgTag.RESCUE)
            else:
                # Fallback to traditional rescue
                self.acp.send(agent, rescue_msg, MsgTag.RESCUE, new_chat=False)
            
            self.last_rescue[agent] = now
            
            # Optimistic nudge to reduce duplicate rescues until we see file updates
            self.last_activity[agent] = max(self.last_activity.get(agent, 0.0), now)
            _log(f"progressive rescue sent -> {agent}")
            
        except Exception as e:
            _log(f"rescue failed -> {agent}: {e}")

    # ---- state/health/metrics ----
    def _persist_state(self):
        """Persist current state to disk"""
        try:
            STATE.write_text(json.dumps({
                "ts": _iso(),
                "last_activity": self.last_activity,
                "last_rescue": self.last_rescue,
                "config": self.cfg.__dict__,
                "uptime_sec": time.time() - self._start_time
            }, indent=2), encoding="utf-8")
        except Exception as e:
            _log(f"persist error: {e}")

    def _restore_state(self):
        """Restore state from disk"""
        try:
            if STATE.exists():
                data = json.loads(STATE.read_text(encoding="utf-8"))
                self.last_activity.update({k: float(v) for k, v in data.get("last_activity", {}).items()})
                self.last_rescue.update({k: float(v) for k, v in data.get("last_rescue", {}).items()})
                _log("state restored")
        except Exception as e:
            _log(f"restore error: {e}")

    def _write_health(self, ok: bool, note: str):
        """Write health status"""
        try:
            HEALTH.write_text(json.dumps({
                "ok": ok, 
                "note": note, 
                "ts": _iso(),
                "uptime_sec": time.time() - self._start_time
            }, indent=2), encoding="utf-8")
        except Exception as e:
            _log(f"health write error: {e}")

    def _write_metrics(self, data: dict):
        """Write metrics data"""
        try:
            METRICS.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception as e:
            _log(f"metrics write error: {e}")

    def get_status(self) -> dict:
        """Get current monitor status"""
        return {
            "timestamp": _iso(),
            "uptime_sec": time.time() - self._start_time,
            "agents": len(self.last_activity),
            "last_activity": self.last_activity,
            "last_rescue": self.last_rescue,
            "config": self.cfg.__dict__
        }

def main():
    """Main entry point"""
    # Get available agents
    acp = AgentCellPhone(agent_id="Agent-5", layout_mode="5-agent", test=False)
    agents = acp.get_available_agents()
    
    # Load configuration from environment
    cfg = MonitorConfig(
        agents=agents,
        stall_threshold_sec=int(os.environ.get("AGENT_STALL_SEC", "600")),      # FIXED: 10 minutes
        warn_threshold_sec=int(os.environ.get("AGENT_WARN_SEC", "480")),        # FIXED: 8 minutes
        normal_response_time=int(os.environ.get("AGENT_RESPONSE_SEC", "300")),  # FIXED: 5 minutes
        warn_ratio=float(os.environ.get("AGENT_WARN_RATIO", "0.8")),
        check_every_sec=int(os.environ.get("AGENT_CHECK_SEC", "30")),           # FIXED: 30 seconds
        file_watch_root=os.environ.get("AGENT_FILE_ROOT", "agent_workspaces"),
        file_response_name=os.environ.get("AGENT_FILE_NAME", "response.txt"),
        inbox_root=os.environ.get("AGENT_INBOX_ROOT", "runtime/agent_comms/inbox"),
        fsm_enabled=os.environ.get("AGENT_FSM_ENABLED", "1") == "1",
        rescue_cooldown_sec=int(os.environ.get("AGENT_RESCUE_COOLDOWN_SEC", "300")),
        active_grace_sec=int(os.environ.get("AGENT_ACTIVE_GRACE_SEC", "300")),
        onboarding_grace_period=int(os.environ.get("AGENT_ONBOARDING_SEC", "600")),  # FIXED: 10 minutes
        use_db_lane=os.environ.get("AGENT_USE_DB_LANE", "0") == "1",
        workspace_map_path=os.environ.get("AGENT_WORKSPACE_MAP", "src/runtime/config/agent_workspace_map.json"),
    )
    
    # Create and start monitor
    mon = Agent5Monitor(cfg)
    
    # Setup signal handlers
    def _sig(signum, frame):
        _log(f"received signal {signum}")
        mon.stop()
    
    signal.signal(signal.SIGINT, _sig)
    signal.signal(signal.SIGTERM, _sig)
    
    # Start monitor
    ok = mon.start()
    if not ok:
        return 2
    
    try:
        # Keep main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        mon.stop()
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
