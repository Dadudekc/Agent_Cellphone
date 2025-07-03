#!/usr/bin/env python3
"""
Modular Onboarding Components for Dream.OS GUI
Provides reusable onboarding UI components that work with both tkinter and PyQt5
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Dict, List, Optional, Callable
import threading
import time
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from agent_workspaces.onboarding.onboarding_manager import OnboardingManager
except ImportError:
    print("Warning: OnboardingManager not found")

class OnboardingProgressWidget:
    """Reusable progress widget for onboarding status"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.progress_var = tk.DoubleVar()
        self.progress_bar = None
        self.progress_label = None
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the progress widget"""
        frame = ttk.LabelFrame(self.parent, text="Onboarding Progress", padding=5)
        frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_bar = ttk.Progressbar(frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = ttk.Label(frame, text="0% Complete")
        self.progress_label.pack()
    
    def update_progress(self, percentage: float):
        """Update progress display"""
        self.progress_var.set(percentage)
        self.progress_label.config(text=f"{percentage:.1f}% Complete")
    
    def get_widget(self):
        """Get the main widget"""
        return self.progress_bar.master

class OnboardingStatusWidget:
    """Reusable status widget for agent onboarding status"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.status_text = None
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the status widget"""
        frame = ttk.LabelFrame(self.parent, text="Agent Status", padding=5)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(frame, height=8, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
    
    def update_status(self, status_text: str):
        """Update status display"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, status_text)
    
    def get_widget(self):
        """Get the main widget"""
        return self.status_text.master

class OnboardingLogWidget:
    """Reusable log widget for onboarding operations"""
    
    def __init__(self, parent, clear_callback: Optional[Callable] = None, **kwargs):
        self.parent = parent
        self.log_text = None
        self.clear_callback = clear_callback
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the log widget"""
        frame = ttk.LabelFrame(self.parent, text="Onboarding Log", padding=5)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(frame, height=6, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(frame)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(log_controls, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = "ERROR" if error else "INFO"
        log_entry = f"[{timestamp}] {prefix}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
        if self.clear_callback:
            self.clear_callback()
    
    def get_widget(self):
        """Get the main widget"""
        return self.log_text.master

class OnboardingControlsWidget:
    """Reusable controls widget for onboarding operations"""
    
    def __init__(self, parent, send_callback: Callable, **kwargs):
        self.parent = parent
        self.send_callback = send_callback
        self.agent_var = tk.StringVar(value="all")
        self.message_type_var = tk.StringVar(value="welcome")
        self.agent_combo = None
        self.message_type_combo = None
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the controls widget"""
        frame = ttk.LabelFrame(self.parent, text="Onboarding Controls", padding=10)
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Agent selection
        agent_frame = ttk.Frame(frame)
        agent_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(agent_frame, text="Target Agent:").pack(side=tk.LEFT)
        self.agent_combo = ttk.Combobox(agent_frame, textvariable=self.agent_var, state="readonly")
        self.agent_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Message type selection
        message_frame = ttk.Frame(frame)
        message_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(message_frame, text="Message Type:").pack(side=tk.LEFT)
        self.message_type_combo = ttk.Combobox(message_frame, textvariable=self.message_type_var, 
                                              state="readonly")
        self.message_type_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        self.message_type_combo.bind("<<ComboboxSelected>>", self.on_message_type_change)
        
        # Quick onboarding buttons
        quick_frame = ttk.LabelFrame(frame, text="Quick Onboarding", padding=5)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        quick_buttons = [
            ("Send Welcome", "welcome"),
            ("System Overview", "system_overview"),
            ("Communication Protocol", "communication_protocol"),
            ("Roles & Responsibilities", "roles_and_responsibilities"),
            ("Best Practices", "best_practices"),
            ("Getting Started", "getting_started"),
            ("Troubleshooting", "troubleshooting"),
            ("Quick Start", "quick_start")
        ]
        
        for i, (text, msg_type) in enumerate(quick_buttons):
            btn = ttk.Button(quick_frame, text=text, 
                           command=lambda mt=msg_type: self.send_specific_message(mt))
            btn.grid(row=i//2, column=i%2, padx=2, pady=2, sticky="ew")
        
        # Bulk operations
        bulk_frame = ttk.LabelFrame(frame, text="Bulk Operations", padding=5)
        bulk_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(bulk_frame, text="Onboard All Agents", 
                  command=self.onboard_all_agents).pack(fill=tk.X, pady=2)
        ttk.Button(bulk_frame, text="Send All Messages to Agent", 
                  command=self.send_all_messages_to_agent).pack(fill=tk.X, pady=2)
    
    def on_message_type_change(self, event=None):
        """Handle message type change"""
        message_type = self.message_type_var.get()
        # This will be handled by the parent component
    
    def send_specific_message(self, message_type: str):
        """Send a specific onboarding message"""
        target = self.agent_var.get()
        self.send_callback("specific", target, message_type)
    
    def onboard_all_agents(self):
        """Onboard all agents"""
        self.send_callback("bulk", "all", "onboard_all")
    
    def send_all_messages_to_agent(self):
        """Send all messages to a specific agent"""
        target = self.agent_var.get()
        self.send_callback("bulk", target, "send_all")
    
    def set_agents(self, agents: List[str]):
        """Set available agents"""
        self.agent_combo['values'] = ["all"] + agents
    
    def set_message_types(self, message_types: List[str]):
        """Set available message types"""
        self.message_type_combo['values'] = message_types
    
    def get_widget(self):
        """Get the main widget"""
        return self.parent

class OnboardingChecklistWidget:
    """Reusable checklist widget for onboarding progress tracking"""
    
    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.checklist_tree = None
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the checklist widget"""
        frame = ttk.LabelFrame(self.parent, text="Onboarding Checklist", padding=5)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create treeview for checklist
        columns = ("Status", "Document", "Description")
        self.checklist_tree = ttk.Treeview(frame, columns=columns, show="tree headings", height=8)
        
        # Configure columns
        self.checklist_tree.heading("#0", text="✓")
        self.checklist_tree.column("#0", width=30, minwidth=30)
        
        for col in columns:
            self.checklist_tree.heading(col, text=col)
            self.checklist_tree.column(col, width=100, minwidth=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.checklist_tree.yview)
        self.checklist_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack widgets
        self.checklist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_checklist(self, checklist_data: List[Dict]):
        """Update the checklist with new data"""
        # Clear existing items
        for item in self.checklist_tree.get_children():
            self.checklist_tree.delete(item)
        
        # Add new items
        for item_data in checklist_data:
            status = "✓" if item_data.get("completed", False) else "✗"
            document = item_data.get("document", "")
            description = item_data.get("description", "")
            
            self.checklist_tree.insert("", "end", text=status, 
                                     values=(status, document, description))
    
    def get_widget(self):
        """Get the main widget"""
        return self.checklist_tree.master

class OnboardingManager:
    """Enhanced onboarding manager that integrates with the GUI components"""
    
    def __init__(self, layout_mode: str = "8-agent", test_mode: bool = True):
        """Initialize the enhanced onboarding manager"""
        self.layout_mode = layout_mode
        self.test_mode = test_mode
        self.manager = None
        self.initialize_manager()
    
    def initialize_manager(self):
        """Initialize the onboarding manager"""
        try:
            self.manager = OnboardingManager(layout_mode=self.layout_mode, test_mode=self.test_mode)
            return True
        except Exception as e:
            print(f"Error initializing OnboardingManager: {e}")
            return False
    
    def get_available_agents(self) -> List[str]:
        """Get list of available agents"""
        if not self.manager:
            return []
        
        try:
            return self.manager.get_available_agents()
        except Exception as e:
            print(f"Error getting available agents: {e}")
            return []
    
    def get_onboarding_documents(self) -> List[Dict]:
        """Get list of onboarding documents"""
        if not self.manager:
            return []
        
        try:
            return self.manager.get_onboarding_documents()
        except Exception as e:
            print(f"Error getting onboarding documents: {e}")
            return []
    
    def get_checklist(self) -> List[Dict]:
        """Get onboarding checklist"""
        if not self.manager:
            return []
        
        try:
            return self.manager.get_checklist()
        except Exception as e:
            print(f"Error getting checklist: {e}")
            return []
    
    def send_onboarding_message(self, target: str, message_type: str) -> tuple[bool, str]:
        """Send onboarding message"""
        if not self.manager:
            return False, "Manager not initialized"
        
        try:
            return self.manager.send_onboarding_message(target, message_type)
        except Exception as e:
            return False, f"Error: {e}"
    
    def onboard_agent(self, agent_name: str) -> Dict:
        """Onboard a specific agent"""
        if not self.manager:
            return {"error": "Manager not initialized"}
        
        try:
            return self.manager.onboard_agent(agent_name)
        except Exception as e:
            return {"error": f"Error: {e}"}
    
    def get_onboarding_progress(self) -> Dict:
        """Get overall onboarding progress"""
        if not self.manager:
            return {"error": "Manager not initialized"}
        
        try:
            return self.manager.get_onboarding_progress()
        except Exception as e:
            return {"error": f"Error: {e}"}
    
    def validate_onboarding(self, agent_name: str) -> Dict:
        """Validate onboarding completion"""
        if not self.manager:
            return {"error": "Manager not initialized"}
        
        try:
            return self.manager.validate_onboarding(agent_name)
        except Exception as e:
            return {"error": f"Error: {e}"} 