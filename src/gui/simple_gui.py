#!/usr/bin/env python3
"""
Simple GUI for Dream.OS Cell Phone
==================================
A lightweight Tkinter-based GUI for agent communication.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
import sys
import threading
import time
from datetime import datetime
from typing import Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from utils.coordinate_finder import CoordinateFinder
    from framework.agent_autonomy_framework import AgentAutonomyFramework
except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you're running from the project root directory")

class SimpleCellPhoneGUI:
    """Simple Tkinter GUI for Dream.OS Cell Phone."""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Dream.OS Cell Phone - Simple GUI")
        self.root.geometry("800x600")
        
        # Initialize components
        self.coordinate_finder = CoordinateFinder()
        self.framework = AgentAutonomyFramework()
        
        # GUI state
        self.selected_agent = tk.StringVar()
        self.message_text = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        
        self.setup_ui()
        self.load_agents()
    
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📱 Dream.OS Cell Phone", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Agent selection
        ttk.Label(main_frame, text="Select Agent:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.agent_combo = ttk.Combobox(main_frame, textvariable=self.selected_agent, 
                                       state="readonly", width=20)
        self.agent_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        self.agent_combo.bind("<<ComboboxSelected>>", self.on_agent_selected)
        
        # Broadcast button
        broadcast_btn = ttk.Button(main_frame, text="📢 Broadcast to All", 
                                  command=self.broadcast_message)
        broadcast_btn.grid(row=1, column=2, padx=(10, 0), pady=5)
        
        # Message input
        ttk.Label(main_frame, text="Message:").grid(row=2, column=0, sticky=tk.W, pady=5)
        message_entry = ttk.Entry(main_frame, textvariable=self.message_text, width=50)
        message_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 0), pady=5)
        message_entry.bind("<Return>", self.send_message)
        
        # Send button
        send_btn = ttk.Button(main_frame, text="📤 Send", command=self.send_message)
        send_btn.grid(row=2, column=2, padx=(10, 0), pady=5)
        
        # Log area
        ttk.Label(main_frame, text="Message Log:").grid(row=3, column=0, sticky=(tk.W, tk.N), pady=(20, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=15, width=70)
        self.log_text.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Status bar
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_text)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=6, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(control_frame, text="🔄 Refresh", command=self.refresh).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🧹 Clear Log", command=self.clear_log).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="⚙️ Settings", command=self.show_settings).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="❌ Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
    
    def load_agents(self):
        """Load available agents into the combo box."""
        try:
            # Get coordinates for all agents
            coords = self.coordinate_finder.get_all_coordinates()
            agent_ids = list(coords.keys())
            
            if agent_ids:
                self.agent_combo['values'] = agent_ids
                self.selected_agent.set(agent_ids[0])
                self.log_message("System", f"Loaded {len(agent_ids)} agents")
            else:
                self.log_message("System", "No agents found")
                
        except Exception as e:
            self.log_message("Error", f"Failed to load agents: {e}")
    
    def on_agent_selected(self, event=None):
        """Handle agent selection."""
        agent = self.selected_agent.get()
        if agent:
            coords = self.coordinate_finder.get_coordinates(agent)
            if coords:
                self.status_text.set(f"Selected: {agent} at ({coords[0]}, {coords[1]})")
            else:
                self.status_text.set(f"Selected: {agent} (no coordinates)")
    
    def send_message(self, event=None):
        """Send message to selected agent."""
        agent = self.selected_agent.get()
        message = self.message_text.get().strip()
        
        if not agent:
            messagebox.showerror("Error", "Please select an agent")
            return
        
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        try:
            # Simulate sending message (replace with actual implementation)
            coords = self.coordinate_finder.get_coordinates(agent)
            if coords:
                self.log_message(agent, f"Message sent: {message}")
                self.status_text.set(f"Message sent to {agent}")
                
                # Clear message input
                self.message_text.set("")
                
                # Simulate agent response
                self.simulate_agent_response(agent, message)
            else:
                messagebox.showerror("Error", f"No coordinates found for {agent}")
                
        except Exception as e:
            self.log_message("Error", f"Failed to send message: {e}")
    
    def broadcast_message(self):
        """Broadcast message to all agents."""
        message = self.message_text.get().strip()
        
        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return
        
        try:
            coords = self.coordinate_finder.get_all_coordinates()
            if coords:
                self.log_message("Broadcast", f"Broadcasting: {message}")
                self.status_text.set(f"Broadcast sent to {len(coords)} agents")
                
                # Clear message input
                self.message_text.set("")
                
                # Simulate responses from all agents
                for agent_id in coords.keys():
                    self.simulate_agent_response(agent_id, message)
            else:
                messagebox.showerror("Error", "No agents available for broadcast")
                
        except Exception as e:
            self.log_message("Error", f"Failed to broadcast message: {e}")
    
    def simulate_agent_response(self, agent_id: str, message: str):
        """Simulate a response from an agent."""
        def delayed_response():
            time.sleep(1)  # Simulate processing time
            response = f"Received: {message}"
            self.log_message(agent_id, response)
        
        # Run in separate thread to avoid blocking GUI
        threading.Thread(target=delayed_response, daemon=True).start()
    
    def log_message(self, sender: str, message: str):
        """Add message to log."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {sender}: {message}\n"
        
        # Add to log text widget
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Also print to console for debugging
        print(log_entry.strip())
    
    def refresh(self):
        """Refresh the GUI."""
        self.load_agents()
        self.status_text.set("Refreshed")
        self.log_message("System", "GUI refreshed")
    
    def clear_log(self):
        """Clear the message log."""
        self.log_text.delete(1.0, tk.END)
        self.log_message("System", "Log cleared")
    
    def show_settings(self):
        """Show settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings content
        ttk.Label(settings_window, text="Settings", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Coordinate info
        coords = self.coordinate_finder.get_layout_info()
        info_text = f"Total Agents: {coords['total_agents']}\n"
        info_text += f"Config Path: {coords['config_path']}\n"
        info_text += f"Bounds: {coords['bounds']}"
        
        ttk.Label(settings_window, text=info_text, justify=tk.LEFT).pack(pady=10)
        
        # Close button
        ttk.Button(settings_window, text="Close", command=settings_window.destroy).pack(pady=10)

def main():
    """Main function."""
    root = tk.Tk()
    app = SimpleCellPhoneGUI(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\nGUI closed by user")

if __name__ == "__main__":
    main() 