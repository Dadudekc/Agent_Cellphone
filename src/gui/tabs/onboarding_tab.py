#!/usr/bin/env python3
"""
Onboarding Manager Tab for Dream.OS GUI
Provides onboarding functionality for managing agent onboarding using modular components
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional
import threading
import time

# Import our modular components
import sys
from pathlib import Path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

try:
    from src.gui.components.onboarding_components import (
        OnboardingProgressWidget, OnboardingStatusWidget, OnboardingLogWidget,
        OnboardingControlsWidget, OnboardingChecklistWidget, OnboardingManager
    )
    from src.gui.components.custom_message_widget import CustomMessageWidget
    from src.gui.components.onboarding_dashboard import OnboardingDashboardWidget
except ImportError as e:
    print(f"Warning: onboarding components not found: {e}")

class OnboardingTab(ttk.Frame):
    """Onboarding Manager Tab for managing agent onboarding using modular components"""
    
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.onboarding_manager = None
        self.components = {}
        self.setup_ui()
        self.initialize_onboarding()
    
    def setup_ui(self):
        """Setup the user interface using modular components"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Onboarding Dashboard
        dashboard_frame = ttk.Frame(self.notebook)
        self.notebook.add(dashboard_frame, text="Dashboard")
        
        self.components['dashboard'] = OnboardingDashboardWidget(dashboard_frame)
        
        # Tab 2: Onboarding Controls
        controls_frame = ttk.Frame(self.notebook)
        self.notebook.add(controls_frame, text="Controls")
        
        # Main container for controls tab
        main_frame = ttk.Frame(controls_frame)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Onboarding controls and custom message
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Controls widget
        self.components['controls'] = OnboardingControlsWidget(
            left_panel, send_callback=self.handle_send_request
        )
        
        # Custom message widget
        self.components['custom_message'] = CustomMessageWidget(
            left_panel, send_callback=self.handle_send_request
        )
        
        # Right panel - Status, progress, and checklist
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Progress widget
        self.components['progress'] = OnboardingProgressWidget(right_panel)
        
        # Status widget
        self.components['status'] = OnboardingStatusWidget(right_panel)
        
        # Checklist widget
        self.components['checklist'] = OnboardingChecklistWidget(right_panel)
        
        # Log widget
        self.components['log'] = OnboardingLogWidget(
            right_panel, clear_callback=self.on_log_clear
        )
        
        # Refresh button
        refresh_frame = ttk.Frame(right_panel)
        refresh_frame.pack(fill=tk.X, pady=(5, 0))
        
        ttk.Button(refresh_frame, text="Refresh Status", 
                  command=self.refresh_status).pack(side=tk.RIGHT)
    
    def initialize_onboarding(self):
        """Initialize the onboarding manager and components"""
        try:
            self.onboarding_manager = OnboardingManager(layout_mode="8-agent", test_mode=True)
            
            # Populate agent dropdown
            agents = self.onboarding_manager.get_available_agents()
            self.components['controls'].set_agents(agents)
            
            # Populate message types
            message_types = [
                "welcome", "system_overview", "communication_protocol",
                "roles_and_responsibilities", "best_practices", "getting_started",
                "troubleshooting", "quick_start"
            ]
            self.components['controls'].set_message_types(message_types)
            
            # Load initial checklist
            self.load_checklist()
            
            self.log_message("Onboarding system initialized successfully")
            self.refresh_status()
            
        except Exception as e:
            self.log_message(f"Error initializing onboarding: {e}", error=True)
    
    def handle_send_request(self, request_type: str, target: str, message_type: str):
        """Handle send requests from components"""
        if not self.onboarding_manager:
            messagebox.showerror("Error", "Onboarding system not initialized")
            return
        
        def send_thread():
            try:
                if request_type == "specific":
                    self.send_specific_message(target, message_type)
                elif request_type == "bulk":
                    if message_type == "onboard_all":
                        self.onboard_all_agents()
                    elif message_type == "send_all":
                        self.send_all_messages_to_agent(target)
                elif request_type == "custom":
                    self.send_custom_message(target, message_type)
                
            except Exception as e:
                self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
        
        threading.Thread(target=send_thread, daemon=True).start()
    
    def send_specific_message(self, target: str, message_type: str):
        """Send a specific onboarding message"""
        try:
            if target == "all":
                # Send to all agents
                agents = self.onboarding_manager.get_available_agents()
                results = {}
                
                for agent in agents:
                    success, result = self.onboarding_manager.send_onboarding_message(agent, message_type)
                    results[agent] = (success, result)
                    time.sleep(1)  # Delay between sends
                
                # Log results
                for agent, (success, result) in results.items():
                    status = "✓" if success else "✗"
                    self.after(0, lambda a=agent, s=status, r=result: 
                             self.log_message(f"{s} {a}: {r}"))
                
            else:
                # Send to specific agent
                success, result = self.onboarding_manager.send_onboarding_message(target, message_type)
                self.after(0, lambda: self.handle_send_result(success, result))
            
            # Refresh status after sending
            self.after(0, self.refresh_status)
            
        except Exception as e:
            self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
    
    def send_all_messages_to_agent(self, target: str):
        """Send all onboarding messages to a specific agent"""
        if target == "all":
            self.after(0, lambda: messagebox.showwarning("Warning", 
                                                        "Please select a specific agent for this operation"))
            return
        
        try:
            # Get all message types and send them
            message_types = [
                "welcome", "system_overview", "communication_protocol",
                "roles_and_responsibilities", "best_practices", "getting_started",
                "troubleshooting", "quick_start"
            ]
            
            results = {}
            for message_type in message_types:
                success, result = self.onboarding_manager.send_onboarding_message(target, message_type)
                results[message_type] = (success, result)
                time.sleep(1)  # Delay between sends
            
            # Log results
            for message_type, (success, result) in results.items():
                status = "✓" if success else "✗"
                self.after(0, lambda mt=message_type, s=status, r=result: 
                         self.log_message(f"{s} {mt}: {r}"))
            
            self.after(0, lambda: messagebox.showinfo("Complete", 
                                                    f"All messages sent to {target}"))
            self.after(0, self.refresh_status)
            
        except Exception as e:
            self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
    
    def onboard_all_agents(self):
        """Onboard all agents"""
        try:
            agents = self.onboarding_manager.get_available_agents()
            results = {}
            
            for agent in agents:
                self.after(0, lambda a=agent: self.log_message(f"Onboarding {a}..."))
                
                agent_result = self.onboarding_manager.onboard_agent(agent)
                results[agent] = agent_result
                
                if "error" in agent_result:
                    self.after(0, lambda a=agent, e=agent_result["error"]: 
                             self.log_message(f"✗ {a}: {e}", error=True))
                else:
                    self.after(0, lambda a=agent: self.log_message(f"✓ {a}: Onboarded successfully"))
                
                time.sleep(2)  # Delay between agents
            
            self.after(0, lambda: messagebox.showinfo("Complete", "All agents onboarded"))
            self.after(0, self.refresh_status)
            
        except Exception as e:
            self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
    
    def send_custom_message(self, target: str, message: str):
        """Send a custom onboarding message"""
        try:
            success, result = self.onboarding_manager.send_onboarding_message(target, "custom", message)
            self.after(0, lambda: self.handle_send_result(success, result))
            self.after(0, self.refresh_status)
            
        except Exception as e:
            self.after(0, lambda: self.handle_send_result(False, f"Error: {e}"))
    
    def handle_send_result(self, success: bool, result: str):
        """Handle the result of sending a message"""
        if success:
            self.log_message(f"✓ {result}")
            messagebox.showinfo("Success", result)
        else:
            self.log_message(f"✗ {result}", error=True)
            messagebox.showerror("Error", result)
    
    def on_log_clear(self):
        """Handle log clear callback"""
        # Additional cleanup if needed
        pass
    
    def log_message(self, message: str, error: bool = False):
        """Add a message to the log"""
        self.components['log'].log_message(message, error)
    
    def load_checklist(self):
        """Load the onboarding checklist"""
        try:
            checklist_data = self.onboarding_manager.get_checklist()
            self.components['checklist'].update_checklist(checklist_data)
        except Exception as e:
            self.log_message(f"Error loading checklist: {e}", error=True)
    
    def refresh_status(self):
        """Refresh the onboarding status"""
        if not self.onboarding_manager:
            self.components['status'].update_status("Onboarding system not initialized")
            return
        
        def status_thread():
            try:
                # Get onboarding progress
                progress = self.onboarding_manager.get_onboarding_progress()
                
                # Update progress bar
                completion = progress.get("completion_percentage", 0)
                self.after(0, lambda: self.components['progress'].update_progress(completion))
                
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
                
                self.after(0, lambda: self.components['status'].update_status(status_text))
                
                # Refresh checklist
                self.after(0, self.load_checklist)
                
            except Exception as e:
                error_text = f"Error getting status: {e}"
                self.after(0, lambda: self.components['status'].update_status(error_text))
        
        threading.Thread(target=status_thread, daemon=True).start()
    
    def get_agent_onboarding_status(self, agent_name: str) -> Dict:
        """Get onboarding status for a specific agent"""
        if not self.onboarding_manager:
            return {"error": "Onboarding system not initialized"}
        
        return self.onboarding_manager.validate_onboarding(agent_name) 