import os
import time
import json
import re
import threading
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Callable

from ..utils import atomic_write

try:
    import pyperclip
except Exception:
    pyperclip = None

try:
    import pyautogui
except Exception:
    pyautogui = None

try:
    import pytesseract
    from PIL import Image
except Exception:
    pytesseract = None
    Image = None

@dataclass
class CaptureConfig:
    strategy: str
    file_watch_root: str
    file_response_name: str
    clipboard_poll_ms: int
    ocr_tesseract_cmd: Optional[str]
    ocr_lang: str
    ocr_psm: int
    inbox_root: str
    fsm_enabled: bool

STRUCTURE_RX = re.compile(
    r"(?si)"
    r"(?:^|\n)Task:\s*(?P<task>.+?)\s*(?:\n|$)"
    r".*?Actions(?:\s*Taken)?:\s*(?P<actions>(?:- .+?\n?)+)"
    r".*?Commit(?:\s*Message)?:\s*(?P<commit>.+?)\s*(?:\n|$)"
    r".*?Status:\s*(?P<status>.+?)\s*(?:\n|$)"
)

def parse_structured(text: str) -> Dict:
    """Parse structured agent responses into system-readable format"""
    m = STRUCTURE_RX.search(text or "")
    if not m:
        # Fallback: best-effort summary
        head = (text or "").strip().splitlines()[:5]
        return {
            "type": "agent_freeform",
            "summary": " / ".join([s.strip() for s in head if s.strip()]),
            "raw": text
        }
    
    acts = [ln.strip("- ").strip() for ln in m.group("actions").splitlines() if ln.strip().startswith("-")]
    return {
        "type": "agent_report",
        "task": m.group("task").strip(),
        "actions": acts,
        "commit_message": m.group("commit").strip(),
        "status": m.group("status").strip(),
        "raw": text
    }

class ResponseCapture:
    """Captures agent responses using multiple strategies and routes them to the inbox system"""
    
    def __init__(self, coords: Dict, cfg: CaptureConfig, get_output_rect: Callable[[str], Dict]):
        self.coords = coords
        self.cfg = cfg
        self.get_output_rect = get_output_rect
        self._threads: Dict[str, threading.Thread] = {}
        self._stop = threading.Event()
        
        # Configure OCR if available
        if self.cfg.ocr_tesseract_cmd and pytesseract:
            pytesseract.pytesseract.tesseract_cmd = self.cfg.ocr_tesseract_cmd
        
        # Ensure inbox directory exists
        Path(self.cfg.inbox_root).mkdir(parents=True, exist_ok=True)

    def start_for(self, agent: str):
        """Start capture thread for a specific agent"""
        if agent in self._threads:
            return
        t = threading.Thread(target=self._run, args=(agent,), daemon=True)
        self._threads[agent] = t
        t.start()

    def stop_all(self):
        """Stop all capture threads"""
        self._stop.set()
        for t in self._threads.values():
            t.join(timeout=1.0)

    def _run(self, agent: str):
        """Main capture loop for an agent"""
        strat = self.cfg.strategy
        while not self._stop.is_set():
            text = None
            try:
                if strat == "file":
                    text = self._pull_file(agent)
                elif strat == "clipboard":
                    text = self._pull_clipboard()
                elif strat == "ocr":
                    text = self._pull_ocr(agent)
                
                if text:
                    payload = parse_structured(text)
                    self._route(agent, payload)
                    
            except Exception as e:
                # Log error but continue running
                print(f"Error in response capture for {agent}: {e}")
                
            time.sleep(max(self.cfg.clipboard_poll_ms, 300)/1000)

    def _pull_file(self, agent: str) -> Optional[str]:
        """Pull response from agent's response.txt file"""
        p = Path(self.cfg.file_watch_root) / agent / self.cfg.file_response_name
        if not p.exists():
            return None
        
        try:
            data = p.read_text(encoding="utf-8").strip()
            if data:
                # Clear file after reading atomically
                atomic_write(p, "")
                return data
        except Exception:
            return None
        return None

    def _pull_clipboard(self) -> Optional[str]:
        """Pull response from system clipboard"""
        if not pyperclip:
            return None
        
        try:
            data = pyperclip.paste()
            return data if data and len(data.strip()) > 0 else None
        except Exception:
            return None

    def _pull_ocr(self, agent: str) -> Optional[str]:
        """Pull response using OCR on agent's output area"""
        if not (pyautogui and pytesseract and Image):
            return None
        
        try:
            rect = self.get_output_rect(agent)
            if not rect:
                return None
                
            # Take screenshot of output area
            im = pyautogui.screenshot(region=(
                rect["x"], rect["y"], rect["width"], rect["height"]
            ))
            
            # Extract text using OCR
            txt = pytesseract.image_to_string(
                im, 
                lang=self.cfg.ocr_lang, 
                config=f"--psm {self.cfg.ocr_psm}"
            )
            
            return txt.strip() if txt and txt.strip() else None
            
        except Exception:
            return None

    def _route(self, agent: str, payload: Dict):
        """Route captured response to the inbox system"""
        try:
            # Create envelope with metadata
            envelope = {
                "type": "agent_response",
                "from": agent,
                "to": "Agent-5",  # Route to FSM agent
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "agent": agent,
                "ts": int(time.time()),
                "payload": payload
            }
            
            # Write to inbox directory
            out = Path(self.cfg.inbox_root) / f"response_{int(time.time()*1000)}_{agent}.json"
            atomic_write(out, json.dumps(envelope, ensure_ascii=False, indent=2))
            
            print(f"[CAPTURE] Captured response from {agent}: {payload.get('type', 'unknown')}")
            
        except Exception as e:
            print(f"Error routing response from {agent}: {e}")
