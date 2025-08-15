#!/usr/bin/env python3
"""
Enhanced Response Capture System
================================
Integrates cursor database capture with advanced workflow engine
Provides real-time AI response monitoring and workflow orchestration
"""

import os
import time
import json
import re
import threading
import asyncio
from pathlib import Path
from dataclasses import dataclass
from typing import Optional, Dict, Callable, List, Any
from enum import Enum

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

class CaptureStrategy(Enum):
    """Available capture strategies in priority order"""
    CURSOR_DB = "cursor_db"           # Real-time Cursor state.vscdb monitoring
    EXPORT_CHAT = "export_chat"        # Monitor exported chat files
    COPY_RESPONSE = "copy_response"    # UI automation to copy responses
    FILE = "file"                      # Monitor response.txt files

@dataclass
class EnhancedCaptureConfig:
    """Enhanced configuration for response capture"""
    # Strategy configuration
    primary_strategy: CaptureStrategy = CaptureStrategy.CURSOR_DB
    fallback_strategies: List[CaptureStrategy] = None
    
    # Cursor DB settings
    cursor_db_poll_interval: float = 2.0
    cursor_db_max_age: int = 300  # seconds
    
    # File monitoring
    file_watch_root: str = "agent_workspaces"
    response_filename: str = "response.txt"
    
    # Output routing
    workflow_inbox: str = "agent_workspaces/Agent-5/inbox"  # For workflow engine
    fsm_inbox: str = "runtime/agent_comms/inbox"           # For FSM bridge
    
    # Advanced processing
    enable_conversation_analysis: bool = True
    enable_sentiment_analysis: bool = True
    enable_task_extraction: bool = True

class AIResponse:
    """Enhanced AI response with analysis"""
    def __init__(self, agent: str, text: str, timestamp: float, source: str = "unknown"):
        self.agent = agent
        self.text = text
        self.timestamp = timestamp
        self.source = source
        self.analysis = {}
        
    def analyze(self, config: EnhancedCaptureConfig):
        """Analyze the response content"""
        if config.enable_conversation_analysis:
            self.analysis["conversation"] = self._analyze_conversation()
        
        if config.enable_sentiment_analysis:
            self.analysis["sentiment"] = self._analyze_sentiment()
            
        if config.enable_task_extraction:
            self.analysis["tasks"] = self._extract_tasks()
    
    def _analyze_conversation(self) -> Dict:
        """Analyze conversation patterns"""
        lines = self.text.split('\n')
        return {
            "line_count": len(lines),
            "has_questions": any('?' in line for line in lines),
            "has_commands": any(line.strip().startswith(('-', '*', '•')) for line in lines),
            "has_code": any('```' in line or 'def ' in line or 'class ' in line for line in lines)
        }
    
    def _analyze_sentiment(self) -> Dict:
        """Basic sentiment analysis"""
        positive_words = ['success', 'complete', 'working', 'fixed', 'resolved', 'good', 'great']
        negative_words = ['error', 'fail', 'broken', 'issue', 'problem', 'bad', 'wrong']
        
        text_lower = self.text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        return {
            "positive_score": positive_count,
            "negative_score": negative_count,
            "overall": "positive" if positive_count > negative_count else "negative" if negative_count > positive_count else "neutral"
        }
    
    def _extract_tasks(self) -> List[Dict]:
        """Extract actionable tasks from response"""
        tasks = []
        lines = self.text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line.startswith(('-', '*', '•', '1.', '2.', '3.')):
                task_text = line.lstrip('-*•1234567890. ')
                if task_text:
                    tasks.append({
                        "text": task_text,
                        "type": "task",
                        "priority": "medium"
                    })
        
        return tasks

class EnhancedResponseCapture:
    """Enhanced response capture with multiple strategies and workflow integration"""
    
    def __init__(self, coords: Dict, config: EnhancedCaptureConfig):
        self.coords = coords
        self.config = config
        self._threads: Dict[str, threading.Thread] = {}
        self._stop = threading.Event()
        self._responses: List[AIResponse] = []
        self._response_callbacks: List[Callable[[AIResponse], None]] = []
        
        # Initialize capture strategies
        self._init_strategies()
        
        # Ensure output directories exist
        Path(self.config.workflow_inbox).mkdir(parents=True, exist_ok=True)
        Path(self.config.fsm_inbox).mkdir(parents=True, exist_ok=True)
        
        print(f"[ENHANCED_CAPTURE] Initialized with strategy: {config.primary_strategy.value}")
    
    def _init_strategies(self):
        """Initialize available capture strategies"""
        self.strategies = {}
        
        # Initialize Cursor DB capture if available
        try:
            from ..cursor_capture.watcher import CursorDBWatcher
            self.strategies[CaptureStrategy.CURSOR_DB] = CursorDBWatcher
            print("[ENHANCED_CAPTURE] Cursor DB capture available")
        except ImportError:
            print("[ENHANCED_CAPTURE] Cursor DB capture not available")
        
        # Initialize other strategies
        if pyperclip:
            self.strategies[CaptureStrategy.COPY_RESPONSE] = self._copy_response_capture
            print("[ENHANCED_CAPTURE] Copy response capture available")
        
        if pyautogui and pytesseract:
            self.strategies[CaptureStrategy.COPY_RESPONSE] = self._ocr_capture
            print("[ENHANCED_CAPTURE] OCR capture available")
        
        # File capture is always available
        self.strategies[CaptureStrategy.FILE] = self._file_capture
        print("[ENHANCED_CAPTURE] File capture available")
    
    def add_response_callback(self, callback: Callable[[AIResponse], None]):
        """Add callback for when responses are captured"""
        self._response_callbacks.append(callback)
    
    def start_for(self, agent: str):
        """Start capture for a specific agent"""
        if agent in self._threads:
            return
            
        t = threading.Thread(target=self._run, args=(agent,), daemon=True)
        self._threads[agent] = t
        t.start()
        print(f"[ENHANCED_CAPTURE] Started capture for {agent}")
    
    def stop_all(self):
        """Stop all capture threads"""
        self._stop.set()
        for t in self._threads.values():
            t.join(timeout=1.0)
        print("[ENHANCED_CAPTURE] All capture stopped")
    
    def _run(self, agent: str):
        """Main capture loop for an agent"""
        strategy = self.config.primary_strategy
        
        while not self._stop.is_set():
            response = None
            
            try:
                # Try primary strategy
                if strategy in self.strategies:
                    response = self.strategies[strategy](agent)
                
                # Try fallback strategies if primary fails
                if not response and self.config.fallback_strategies:
                    for fallback in self.config.fallback_strategies:
                        if fallback in self.strategies:
                            response = self.strategies[fallback](agent)
                            if response:
                                break
                
                if response:
                    # Analyze response
                    response.analyze(self.config)
                    
                    # Store response
                    self._responses.append(response)
                    
                    # Route to both outputs
                    self._route_to_workflow(response)
                    self._route_to_fsm(response)
                    
                    # Notify callbacks
                    for callback in self._response_callbacks:
                        try:
                            callback(response)
                        except Exception as e:
                            print(f"[ENHANCED_CAPTURE] Callback error: {e}")
                    
                    print(f"[ENHANCED_CAPTURE] Captured response from {agent}: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"[ENHANCED_CAPTURE] Error in capture loop for {agent}: {e}")
            
            time.sleep(1.0)
    
    def _file_capture(self, agent: str) -> Optional[AIResponse]:
        """Capture from response.txt files"""
        p = Path(self.config.file_watch_root) / agent / self.config.response_filename
        if not p.exists():
            return None
        
        try:
            data = p.read_text(encoding="utf-8").strip()
            if data:
                # Clear file after reading
                p.write_text("", encoding="utf-8")
                return AIResponse(agent, data, time.time(), "file")
        except Exception:
            pass
        return None
    
    def _copy_response_capture(self, agent: str) -> Optional[AIResponse]:
        """Capture from clipboard"""
        if not pyperclip:
            return None
        
        try:
            data = pyperclip.paste()
            if data and len(data.strip()) > 0:
                return AIResponse(agent, data, time.time(), "clipboard")
        except Exception:
            pass
        return None
    
    def _ocr_capture(self, agent: str) -> Optional[AIResponse]:
        """Capture using OCR on output area"""
        if not (pyautogui and pytesseract and Image):
            return None
        
        try:
            # Get agent coordinates
            agent_coords = self.coords.get(agent, {})
            if not agent_coords:
                return None
            
            # Take screenshot and extract text
            # This would need proper coordinate mapping
            return None
        except Exception:
            pass
        return None
    
    def _route_to_workflow(self, response: AIResponse):
        """Route response to workflow engine inbox"""
        try:
            envelope = {
                "type": "ai_response",
                "agent": response.agent,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "ts": int(response.timestamp),
                "payload": {
                    "text": response.text,
                    "source": response.source,
                    "analysis": response.analysis
                }
            }
            
            out_file = Path(self.config.workflow_inbox) / f"response_{int(time.time()*1000)}_{response.agent}.json"
            out_file.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
            
        except Exception as e:
            print(f"[ENHANCED_CAPTURE] Error routing to workflow: {e}")
    
    def _route_to_fsm(self, response: AIResponse):
        """Route response to FSM bridge inbox"""
        try:
            # Parse structured response
            payload = self._parse_structured(response.text)
            
            envelope = {
                "type": "agent_response",
                "agent": response.agent,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "ts": int(response.timestamp),
                "payload": payload
            }
            
            out_file = Path(self.config.fsm_inbox) / f"response_{int(time.time()*1000)}_{response.agent}.json"
            out_file.write_text(json.dumps(envelope, ensure_ascii=False, indent=2), encoding="utf-8")
            
        except Exception as e:
            print(f"[ENHANCED_CAPTURE] Error routing to FSM: {e}")
    
    def _parse_structured(self, text: str) -> Dict:
        """Parse structured agent responses"""
        # Use the existing parsing logic
        STRUCTURE_RX = re.compile(
            r"(?si)"
            r"(?:^|\n)Task:\s*(?P<task>.+?)\s*(?:\n|$)"
            r".*?Actions(?:\s*Taken)?:\s*(?P<actions>(?:- .+?\n?)+)"
            r".*?Commit(?:\s*Message)?:\s*(?P<commit>.+?)\s*(?:\n|$)"
            r".*?Status:\s*(?P<status>.+?)\s*(?:\n|$)"
        )
        
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
    
    def get_responses(self, agent: str = None, since: float = None) -> List[AIResponse]:
        """Get captured responses, optionally filtered by agent and time"""
        responses = self._responses
        
        if agent:
            responses = [r for r in responses if r.agent == agent]
        
        if since:
            responses = [r for r in responses if r.timestamp >= since]
        
        return responses
    
    def is_capture_enabled(self) -> bool:
        """Check if capture is available and working"""
        return len(self.strategies) > 0
