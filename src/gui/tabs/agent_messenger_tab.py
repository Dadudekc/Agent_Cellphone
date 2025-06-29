#!/usr/bin/env python3
"""
Agent Messenger Tab for Dream.OS GUI
Provides messaging functionality for communicating with agents
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
    from src.gui.utils.messaging_utils import MessagingUtils
except ImportError:
    print("Warning: messaging_utils not found")

class AgentMessengerTab(ttk.Frame):
    """Agent Messenger Tab for sending messages and commands to agents"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.messaging_utils = None
        self.setup_ui()
        self.initialize_messaging()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Message composition
        left_panel = ttk.LabelFrame(main_frame, text="Message Composition", padding=10)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Target selection
        target_frame = ttk.Frame(left_panel)
        target_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(target_frame, text="Target:").pack(side=tk.LEFT)
        self.target_var = tk.StringVar(value="all")
        self.target_combo = ttk.Combobox(target_frame, textvariable=self.target_var, state="readonly")
        self.target_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Message type selection
        type_frame = ttk.Frame(left_panel)
        type_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(type_frame, text="Type:").pack(side=tk.LEFT)
        self.type_var = tk.StringVar(value="message")
        type_combo = ttk.Combobox(type_frame, textvariable=self.type_var, 
                                 values=["message", "command"], state="readonly")
        type_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        type_combo.bind("<<ComboboxSelected>>", self.on_type_change)
        
        # Message tag selection
        tag_frame = ttk.Frame(left_panel)
        tag_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(tag_frame, text="Tag:").pack(side=tk.LEFT)
        self.tag_var = tk.StringVar(value="NORMAL")
        self.tag_combo = ttk.Combobox(tag_frame, textvariable=self.tag_var, state="readonly")
        self.tag_combo.pack(side=tk.LEFT, padx=(5, 0), fill=tk.X, expand=True)
        
        # Message content
        content_frame = ttk.LabelFrame(left_panel, text="Message Content", padding=5)
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.message_text = scrolledtext.ScrolledText(content_frame, height=8, wrap=tk.WORD)
        self.message_text.pack(fill=tk.BOTH, expand=True)
        
        # Quick message buttons
        quick_frame = ttk.LabelFrame(left_panel, text="Quick Messages", padding=5)
        quick_frame.pack(fill=tk.X, pady=(0, 10))
        
        quick_buttons = [
            ("Ping", "ping"),
            ("Status", "status"),
            ("Resume", "resume"),
            ("Sync", "sync"),
            ("Verify", "verify")
        ]
        
        for i, (text, command) in enumerate(quick_buttons):
            btn = ttk.Button(quick_frame, text=text, 
                           command=lambda cmd=command: self.send_quick_command(cmd))
            btn.grid(row=i//3, column=i%3, padx=2, pady=2, sticky="ew")
        
        # Send button
        send_frame = ttk.Frame(left_panel)
        send_frame.pack(fill=tk.X)
        
        self.send_button = ttk.Button(send_frame, text="Send Message", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(send_frame, text="Clear", command=self.clear_message)
        self.clear_button.pack(side=tk.LEFT)
        
        # Right panel - Status and logs
        right_panel = ttk.LabelFrame(main_frame, text="Status & Logs", padding=10)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Status display
        status_frame = ttk.LabelFrame(right_panel, text="System Status", padding=5)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_text = scrolledtext.ScrolledText(status_frame, height=6, wrap=tk.WORD)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Log display
        log_frame = ttk.LabelFrame(right_panel, text="Message Log", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Log controls
        log_controls = ttk.Frame(right_panel)
        log_controls.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(log_controls, text="Clear Log", command=self.clear_log).pack(side=tk.LEFT)
        ttk.Button(log_controls, text="Refresh Status", command=self.refresh_status).pack(side=tk.RIGHT)
    
    def initialize_messaging(self):
        """Initialize the messaging utilities"""
        try:
            self.messaging_utils = MessagingUtils(layout_mode="8-agent", test_mode=True)
            
            # Populate target dropdown
            agents = self.messaging_utils.get_available_agents()
            self.target_combo['values'] = ["all"] + agents
            
            # Populate tag dropdown
            tags = self.messaging_utils.get_available_tags()
            self.tag_combo['values'] = tags
            
            self.log_message("Messaging system initialized successfully")
            self.refresh_status()
            
        except Exception as e:
            self.log_message(f"Error initializing messaging: {e}", error=True)
    
    def on_type_change(self, event=None):
        """Handle message type change"""
        if self.type_var.get() == "command":
            # Show available commands
            commands = self.messaging_utils.get_available_commands() if self.messaging_utils else []
            self.message_text.delete(1.0, tk.END)
            self.message_text.insert(1.0, "Available commands:\n" + "\n".join(commands))
        else:
            # Clear for regular message
            self.message_text.delete(1.0, tk.END)
    
    def send_message(self):
        """Send the composed message"""
        if not self.messaging_utils:
            messagebox.showerror("Error", "Messaging system not initialized")
            return
        
        target = self.target_var.get()
        message_type = self.type_var.get()
        tag = self.tag_var.get()
        content = self.message_text.get(1.0, tk.END).strip()
        
        if not content:
            messagebox.showwarning("Warning", "Please enter a message")
            return
        
        # Validate target
        valid, error_msg = self.messaging_utils.validate_target(target)
        if not valid:
            messagebox.showerror("Error", error_msg)
            return
        
        # Send message in background thread
        def send_thread():
            try:
                if message_type == "command":
                    success, result = self.messaging_utils.send_command(target, content)
                else:
                    success, result = self.messaging_utils.send_message(target, content, tag)
                
                # Update UI in main thread
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
    
    def send_quick_command(self, command: str):
        """Send a quick command"""
        if not self.messaging_utils:
            messagebox.showerror("Error", "Messaging system not initialized")
            return
        
        target = self.target_var.get()
        
        def send_thread():
            try:
                success, result = self.messaging_utils.send_command(target, command)
                self.after(0, lambda: self.handle_send_result(success, result))
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def clear_message(self):
        """Clear the message text"""
        self.message_text.delete(1.0, tk.END)
    
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
        """Refresh the system status"""
        if not self.messaging_utils:
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, "Messaging system not initialized")
            return
        
        def status_thread():
            try:
                status = self.messaging_utils.get_system_status()
                
                # Format status for display
                status_text = "System Status:\n"
                status_text += "=" * 50 + "\n"
                
                if "error" in status:
                    status_text += f"Error: {status['error']}\n"
                else:
                    status_text += f"Layout Mode: {status.get('layout_mode', 'Unknown')}\n"
                    status_text += f"Available Agents: {len(status.get('available_agents', []))}\n"
                    status_text += f"Available Layouts: {len(status.get('available_layouts', []))}\n"
                    status_text += f"Timestamp: {status.get('timestamp', 'Unknown')}\n"
                
                self.after(0, lambda: self.update_status_display(status_text))
                
            except Exception as e:
                error_text = f"Error getting status: {e}"
                self.after(0, lambda: self.update_status_display(error_text))
        
        threading.Thread(target=status_thread, daemon=True).start()
    
    def update_status_display(self, status_text: str):
        """Update the status display"""
        self.status_text.delete(1.0, tk.END)
        self.status_text.insert(1.0, status_text)
    
    def test_connectivity(self):
        """Test connectivity to all agents"""
        if not self.messaging_utils:
            messagebox.showerror("Error", "Messaging system not initialized")
            return
        
        def test_thread():
            try:
                results = self.messaging_utils.test_connectivity()
                
                # Format results
                result_text = "Connectivity Test Results:\n"
                result_text += "=" * 50 + "\n"
                
                for agent, result in results.items():
                    status = "✓" if result['success'] else "✗"
                    result_text += f"{status} {agent}: {result['message']}\n"
                
                self.after(0, lambda: self.log_message(result_text))
                
            except Exception as e:
                self.after(0, lambda: self.log_message(f"Error testing connectivity: {e}", error=True))
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def get_agent_info(self, agent_name: str) -> Dict:
        """Get information about a specific agent"""
        if not self.messaging_utils:
            return {"error": "Messaging system not initialized"}
        
        return self.messaging_utils.get_agent_info(agent_name)
    
    def switch_layout_mode(self, new_layout: str):
        """Switch to a different layout mode"""
        if not self.messaging_utils:
            messagebox.showerror("Error", "Messaging system not initialized")
            return
        
        def switch_thread():
            try:
                success, result = self.messaging_utils.switch_layout_mode(new_layout)
                self.after(0, lambda: self.handle_send_result(success, result))
                
                if success:
                    # Refresh the UI
                    self.after(0, self.initialize_messaging)
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=switch_thread, daemon=True).start()
    
    def toggle_test_mode(self):
        """Toggle between test and live mode"""
        if not self.messaging_utils:
            messagebox.showerror("Error", "Messaging system not initialized")
            return
        
        def toggle_thread():
            try:
                success, result = self.messaging_utils.toggle_test_mode()
                self.after(0, lambda: self.handle_send_result(success, result))
                
                if success:
                    # Refresh the UI
                    self.after(0, self.initialize_messaging)
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=toggle_thread, daemon=True).start() 