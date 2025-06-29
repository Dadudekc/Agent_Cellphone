#!/usr/bin/env python3
"""
Onboarding Manager Tab for Dream.OS GUI
Provides onboarding functionality for managing agent onboarding
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, List, Optional
import threading
import time

# Import our utilities
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from src.gui.utils.onboarding_utils import OnboardingUtils
except ImportError:
    print("Warning: onboarding_utils not found")

class OnboardingTab(ttk.Frame):
    """Onboarding Manager Tab for managing agent onboarding"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.onboarding_utils = None
        self.setup_ui()
        self.initialize_onboarding()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Onboarding controls
        left_panel = ttk.LabelFrame(main_frame, text="Onboarding Controls", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Agent selection
        agent_frame = ttk.Frame(left_panel)
        agent_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(agent_frame, text="Target Agent:").pack(side=tk.LEFT)
        self.agent_var = tk.StringVar(value="all")
        self.agent_combo = ttk.Combobox(agent_frame, textvariable=self.agent_var, state="readonly")
        self.agent_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Message type selection
        message_frame = ttk.Frame(left_panel)
        message_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(message_frame, text="Message Type:").pack(side=tk.LEFT)
        self.message_type_var = tk.StringVar(value="welcome")
        self.message_type_combo = ttk.Combobox(message_frame, textvariable=self.message_type_var, 
                                              state="readonly")
        self.message_type_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        self.message_type_combo.bind("<<ComboboxSelected>>", self.on_message_type_change)
        
        # Quick onboarding buttons
        quick_frame = ttk.LabelFrame(left_panel, text="Quick Onboarding", padding=5)
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
        bulk_frame = ttk.LabelFrame(left_panel, text="Bulk Operations", padding=5)
        bulk_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(bulk_frame, text="Onboard All Agents", 
                  command=self.onboard_all_agents).pack(fill=tk.X, pady=2)
        ttk.Button(bulk_frame, text="Send All Messages to Agent", 
                  command=self.send_all_messages_to_agent).pack(fill=tk.X, pady=2)
        
        # Custom message
        custom_frame = ttk.LabelFrame(left_panel, text="Custom Message", padding=5)
        custom_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.custom_message_text = scrolledtext.ScrolledText(custom_frame, height=6, wrap=tk.WORD)
        self.custom_message_text.pack(fill=tk.BOTH, expand=True)
        
        ttk.Button(custom_frame, text="Send Custom Message", 
                  command=self.send_custom_message).pack(fill=tk.X, pady=(5, 0))
        
        # Right panel - Status and progress
        right_panel = ttk.LabelFrame(main_frame, text="Onboarding Status", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Progress display
        progress_frame = ttk.LabelFrame(right_panel, text="Onboarding Progress", padding=5)
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 5))
        
        self.progress_label = ttk.Label(progress_frame, text="0% Complete")
        self.progress_label.pack()
        
        # Status display
        status_frame = ttk.LabelFrame(right_panel, text="Agent Status", padding=5)
        status_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=8, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Log display
        log_frame = ttk.LabelFrame(right_panel, text="Onboarding Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(right_panel)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(log_controls, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Refresh Status", command=self.refresh_status).pack(side=tk.RIGHT)
    
    def initialize_onboarding(self):
        """Initialize the onboarding utilities"""
        try:
            self.onboarding_utils = OnboardingUtils(layout_mode="8-agent", test_mode=True)
            
            # Populate agent dropdown
            agents = self.onboarding_utils.acp.get_available_agents() if self.onboarding_utils.acp else []
            self.agent_combo['values'] = ["all"] + agents
            
            # Populate message type dropdown
            messages = self.onboarding_utils.get_onboarding_messages()
            self.message_type_combo['values'] = list(messages.keys())
            
            self.log_message("Onboarding system initialized successfully")
            self.refresh_status()
            
        except Exception as e:
            self.log_message(f"Error initializing onboarding: {e}", error=True)
    
    def on_message_type_change(self, event=None):
        """Handle message type change"""
        message_type = self.message_type_var.get()
        if self.onboarding_utils:
            messages = self.onboarding_utils.get_onboarding_messages()
            if message_type in messages:
                self.custom_message_text.delete(1.0, tk.END)
                self.custom_message_text.insert(1.0, messages[message_type])
    
    def send_specific_message(self, message_type: str):
        """Send a specific onboarding message"""
        if not self.onboarding_utils:
            messagebox.showerror("Error", "Onboarding system not initialized")
            return
        
        target = self.agent_var.get()
        
        def send_thread():
            try:
                if target == "all":
                    # Send to all agents
                    agents = self.onboarding_utils.acp.get_available_agents()
                    results = {}
                    
                    for agent in agents:
                        success, result = self.onboarding_utils.send_onboarding_message(agent, message_type)
                        results[agent] = (success, result)
                        time.sleep(1)  # Delay between sends
                    
                    # Log results
                    for agent, (success, result) in results.items():
                        status = "✓" if success else "✗"
                        self.after(0, lambda a=agent, s=status, r=result: 
                                 self.log_message(f"{s} {a}: {r}"))
                    
                else:
                    # Send to specific agent
                    success, result = self.onboarding_utils.send_onboarding_message(target, message_type)
                    self.after(0, lambda: self.handle_send_result(success, result))
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def send_all_messages_to_agent(self):
        """Send all onboarding messages to a specific agent"""
        if not self.onboarding_utils:
            messagebox.showerror("Error", "Onboarding system not initialized")
            return
        
        target = self.agent_var.get()
        if target == "all":
            messagebox.showwarning("Warning", "Please select a specific agent for this operation")
            return
        
        def send_thread():
            try:
                results = self.onboarding_utils.send_all_onboarding_messages(target)
                
                # Log results
                for message_type, (success, result) in results.items():
                    status = "✓" if success else "✗"
                    self.after(0, lambda mt=message_type, s=status, r=result: 
                             self.log_message(f"{s} {mt}: {r}"))
                
                self.after(0, lambda: messagebox.showinfo("Complete", 
                                                        f"All messages sent to {target}"))
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def onboard_all_agents(self):
        """Onboard all agents"""
        if not self.onboarding_utils:
            messagebox.showerror("Error", "Onboarding system not initialized")
            return
        
        def onboard_thread():
            try:
                results = self.onboarding_utils.onboard_all_agents()
                
                # Log results
                for agent, agent_results in results.items():
                    self.after(0, lambda a=agent: self.log_message(f"Onboarding {a}..."))
                    
                    for message_type, (success, result) in agent_results.items():
                        status = "✓" if success else "✗"
                        self.after(0, lambda mt=message_type, s=status, r=result: 
                                 self.log_message(f"  {s} {mt}: {r}"))
                
                self.after(0, lambda: messagebox.showinfo("Complete", "All agents onboarded"))
                self.after(0, self.refresh_status)
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=onboard_thread, daemon=True).start()
    
    def send_custom_message(self):
        """Send a custom onboarding message"""
        if not self.onboarding_utils:
            messagebox.showerror("Error", "Onboarding system not initialized")
            return
        
        target = self.agent_var.get()
        message = self.custom_message_text.get(1.0, tk.END).strip()
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message")
            return
        
        def send_thread():
            try:
                success, result = self.onboarding_utils.send_custom_onboarding_message(target, message)
                self.after(0, lambda: self.handle_send_result(success, result))
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def handle_send_result(self, success: bool, result: str):
        """Handle the result of sending a message"""
        if success:
            self.log_message(f"✓ {result}")
            messagebox.showinfo("Success", result)
        else:
            self.log_message(f"✗ {result}", error=True)
            messagebox.showerror("Error", result)
    
    def clear_log(self):
        """Clear the log display"""
        self.log_text.delete(1.0, tk.END)
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log"""
        timestamp = time.strftime("%H:%M:%S")
        prefix = "ERROR" if error else "INFO"
        log_entry = f"[{timestamp}] {prefix}: {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
    
    def refresh_status(self):
        """Refresh the onboarding status"""
        if not self.onboarding_utils:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, "Onboarding system not initialized")
            return
        
        def status_thread():
            try:
                # Get onboarding progress
                progress = self.onboarding_utils.get_onboarding_progress()
                
                # Update progress bar
                completion = progress.get("completion_percentage", 0)
                self.after(0, lambda: self.progress_var.set(completion))
                self.after(0, lambda: self.progress_label.config(text=f"{completion:.1f}% Complete"))
                
                # Update status display
                status_text = "Onboarding Status:\n"
                status_text += "=" * 50 + "\n"
                
                if "error" in progress:
                    status_text += f"Error: {progress['error']}\n"
                else:
                    status_text += f"Total Agents: {progress.get('total_agents', 0)}\n"
                    status_text += f"Completed: {progress.get('completed_agents', 0)}\n"
                    status_text += f"Completion: {completion:.1f}%\n\n"
                    
                    # Agent details
                    agent_details = progress.get("agent_details", {})
                    for agent, details in agent_details.items():
                        if "error" in details:
                            status_text += f"✗ {agent}: {details['error']}\n"
                        else:
                            complete = "✓" if details.get("complete", False) else "✗"
                            status_text += f"{complete} {agent}\n"
                
                self.after(0, lambda: self.update_status_display(status_text))
                
            except Exception as e:
                error_text = f"Error getting status: {e}"
                self.after(0, lambda: self.update_status_display(error_text))
        
        threading.Thread(target=status_thread, daemon=True).start()
    
    def update_status_display(self, status_text: str):
        """Update the status display"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, status_text)
    
    def get_agent_onboarding_status(self, agent_name: str) -> Dict:
        """Get onboarding status for a specific agent"""
        if not self.onboarding_utils:
            return {"error": "Onboarding system not initialized"}
        
        return self.onboarding_utils.get_onboarding_status(agent_name)
    
    def validate_agent_onboarding(self, agent_name: str) -> Dict:
        """Validate onboarding completion for a specific agent"""
        if not self.onboarding_utils:
            return {"error": "Onboarding system not initialized"}
        
        return self.onboarding_utils.validate_onboarding_completion(agent_name) 