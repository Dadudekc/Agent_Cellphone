#!/usr/bin/env python3
"""
Dream.OS Demo GUI
A comprehensive showcase of the Dream.OS autonomous agent system
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import json
import os
import sys
import threading
import time
from datetime import datetime

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DreamOSDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Dream.OS Demo - Autonomous Agent System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 24, 'bold'), foreground='#00ff88')
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#ffffff')
        self.style.configure('Demo.TButton', font=('Arial', 12, 'bold'), padding=10)
        
        self.setup_ui()
        self.demo_running = False
        
    def setup_ui(self):
        """Setup the main UI components"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = ttk.Label(main_frame, text="DREAM.OS DEMO", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        subtitle_label = ttk.Label(main_frame, text="Autonomous Agent System Showcase", 
                                 style='Header.TLabel')
        subtitle_label.pack(pady=(0, 30))
        
        # Control buttons frame
        button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        button_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Demo buttons
        self.start_demo_btn = ttk.Button(button_frame, text="🚀 Start Full Demo", 
                                       command=self.start_full_demo, style='Demo.TButton')
        self.start_demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_demo_btn = ttk.Button(button_frame, text="⏹️ Stop Demo", 
                                      command=self.stop_demo, style='Demo.TButton', state='disabled')
        self.stop_demo_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_btn = ttk.Button(button_frame, text="🗑️ Clear Output", 
                                  command=self.clear_output, style='Demo.TButton')
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Feature buttons
        self.coord_btn = ttk.Button(button_frame, text="🗺️ Coordinate Mapping", 
                                  command=self.show_coordinate_mapping, style='Demo.TButton')
        self.coord_btn.pack(side=tk.LEFT, padx=(20, 0))
        
        # Progress frame
        progress_frame = tk.Frame(main_frame, bg='#1a1a1a')
        progress_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.progress_label = ttk.Label(progress_frame, text="Ready to start demo...", 
                                      style='Header.TLabel')
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=400)
        self.progress_bar.pack(pady=(10, 0))
        
        # Output area
        output_frame = tk.Frame(main_frame, bg='#1a1a1a')
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        output_label = ttk.Label(output_frame, text="Demo Output:", style='Header.TLabel')
        output_label.pack(anchor=tk.W, pady=(0, 10))
        
        # Create text widget with custom colors
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=20,
            bg='#2a2a2a',
            fg='#00ff88',
            font=('Consolas', 10),
            insertbackground='#00ff88'
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_label = ttk.Label(main_frame, text="Status: Ready", style='Header.TLabel')
        self.status_label.pack(pady=(10, 0))
        
    def log(self, message, level="INFO"):
        """Add a message to the output with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        color_map = {
            "INFO": "#00ff88",
            "SUCCESS": "#00ff00", 
            "WARNING": "#ffff00",
            "ERROR": "#ff0000",
            "HEADER": "#00ffff"
        }
        
        color = color_map.get(level, "#00ff88")
        
        # Insert with color
        self.output_text.insert(tk.END, f"[{timestamp}] {message}\n")
        
        # Apply color to the last line
        last_line_start = self.output_text.index("end-2c linestart")
        last_line_end = self.output_text.index("end-1c")
        self.output_text.tag_add(level, last_line_start, last_line_end)
        self.output_text.tag_config(level, foreground=color)
        
        self.output_text.see(tk.END)
        self.root.update()
        
    def clear_output(self):
        """Clear the output text area"""
        self.output_text.delete(1.0, tk.END)
        self.log("Output cleared", "INFO")
        
    def update_progress(self, value, text):
        """Update progress bar and label"""
        self.progress_bar['value'] = value
        self.progress_label.config(text=text)
        self.root.update()
        
    def start_full_demo(self):
        """Start the full Dream.OS demo in a separate thread"""
        if self.demo_running:
            return
            
        self.demo_running = True
        self.start_demo_btn.config(state='disabled')
        self.stop_demo_btn.config(state='normal')
        
        # Start demo in separate thread
        demo_thread = threading.Thread(target=self.run_demo_sequence)
        demo_thread.daemon = True
        demo_thread.start()
        
    def stop_demo(self):
        """Stop the running demo"""
        self.demo_running = False
        self.start_demo_btn.config(state='normal')
        self.stop_demo_btn.config(state='disabled')
        self.log("Demo stopped by user", "WARNING")
        self.update_progress(0, "Demo stopped")
        
    def run_demo_sequence(self):
        """Run the complete demo sequence"""
        try:
            self.log("=" * 60, "HEADER")
            self.log("DREAM.OS AUTONOMOUS AGENT SYSTEM DEMO", "HEADER")
            self.log("=" * 60, "HEADER")
            self.log("", "INFO")
            
            # Demo sections
            sections = [
                ("System Overview", self.demo_system_overview),
                ("Agent Status Check", self.demo_agent_status),
                ("Inter-Agent Communication", self.demo_communication),
                ("Task Management", self.demo_task_management),
                ("Onboarding System", self.demo_onboarding),
                ("Document Generation", self.demo_document_generation),
                ("Performance Monitoring", self.demo_performance),
                ("System Controls", self.demo_system_controls)
            ]
            
            total_sections = len(sections)
            
            for i, (section_name, section_func) in enumerate(sections):
                if not self.demo_running:
                    break
                    
                progress = (i / total_sections) * 100
                self.update_progress(progress, f"Running: {section_name}")
                
                self.log(f"", "INFO")
                self.log(f"🎯 SECTION {i+1}/{total_sections}: {section_name.upper()}", "HEADER")
                self.log(f"", "INFO")
                
                try:
                    section_func()
                    self.log(f"✅ {section_name} completed successfully", "SUCCESS")
                except Exception as e:
                    self.log(f"❌ {section_name} failed: {str(e)}", "ERROR")
                
                if not self.demo_running:
                    break
                    
                time.sleep(1)  # Brief pause between sections
            
            if self.demo_running:
                self.update_progress(100, "Demo completed successfully!")
                self.log("", "INFO")
                self.log("🎉 DREAM.OS DEMO COMPLETED SUCCESSFULLY!", "SUCCESS")
                self.log("All features have been demonstrated.", "INFO")
                
        except Exception as e:
            self.log(f"Demo failed with error: {str(e)}", "ERROR")
        finally:
            self.demo_running = False
            self.start_demo_btn.config(state='normal')
            self.stop_demo_btn.config(state='disabled')
            
    def demo_system_overview(self):
        """Demonstrate system overview"""
        self.log("📋 SYSTEM OVERVIEW", "HEADER")
        self.log("Dream.OS is an autonomous agent system with the following capabilities:", "INFO")
        
        features = [
            "🤖 Multi-agent coordination and communication",
            "📊 Real-time status monitoring and reporting", 
            "📝 Automated task management and execution",
            "🎓 Comprehensive onboarding system",
            "📄 Document generation and template management",
            "⚡ Performance monitoring and optimization",
            "🔧 System controls and configuration management",
            "🌐 Inter-agent messaging and collaboration"
        ]
        
        for feature in features:
            self.log(f"  {feature}", "INFO")
            time.sleep(0.3)
            
        self.log("", "INFO")
        self.log("System architecture supports scalable agent deployment", "INFO")
        self.log("with autonomous decision-making capabilities.", "INFO")
        
    def demo_agent_status(self):
        """Demonstrate agent status checking"""
        self.log("🔍 AGENT STATUS CHECK", "HEADER")
        
        # Check if agent workspaces exist
        agent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_workspaces")
        
        if os.path.exists(agent_dir):
            agents = [d for d in os.listdir(agent_dir) if d.startswith("Agent-")]
            self.log(f"Found {len(agents)} agent workspaces: {', '.join(agents)}", "SUCCESS")
            
            # Check Agent-1 status
            agent1_status_file = os.path.join(agent_dir, "Agent-1", "status.json")
            if os.path.exists(agent1_status_file):
                try:
                    with open(agent1_status_file, 'r') as f:
                        status = json.load(f)
                    
                    self.log(f"Agent-1 Status: {status.get('status', 'unknown')}", "INFO")
                    self.log(f"Current Task: {status.get('current_task', 'none')}", "INFO")
                    self.log(f"Tasks Completed: {status.get('performance_metrics', {}).get('tasks_completed', 0)}", "INFO")
                    self.log(f"Onboarding: {status.get('onboarding', {}).get('status', 'unknown')}", "INFO")
                    
                except Exception as e:
                    self.log(f"Error reading Agent-1 status: {str(e)}", "ERROR")
            else:
                self.log("Agent-1 status file not found", "WARNING")
        else:
            self.log("Agent workspaces directory not found", "WARNING")
            
    def demo_communication(self):
        """Demonstrate inter-agent communication"""
        self.log("💬 INTER-AGENT COMMUNICATION", "HEADER")
        
        # Check message files
        agent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_workspaces")
        
        if os.path.exists(agent_dir):
            # Check inbox/outbox for messages
            for agent in ["Agent-1", "Agent-2"]:
                agent_path = os.path.join(agent_dir, agent)
                if os.path.exists(agent_path):
                    inbox_path = os.path.join(agent_path, "inbox")
                    outbox_path = os.path.join(agent_path, "outbox")
                    
                    inbox_count = len([f for f in os.listdir(inbox_path) if f.endswith('.json')]) if os.path.exists(inbox_path) else 0
                    outbox_count = len([f for f in os.listdir(outbox_path) if f.endswith('.json')]) if os.path.exists(outbox_path) else 0
                    
                    self.log(f"{agent}: {inbox_count} messages received, {outbox_count} messages sent", "INFO")
                    
        self.log("Communication system enables real-time message exchange", "INFO")
        self.log("between agents with structured JSON format.", "INFO")
        
    def demo_task_management(self):
        """Demonstrate task management"""
        self.log("📋 TASK MANAGEMENT", "HEADER")
        
        # Check task files
        agent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_workspaces")
        
        if os.path.exists(agent_dir):
            for agent in ["Agent-1", "Agent-2"]:
                agent_path = os.path.join(agent_dir, agent)
                if os.path.exists(agent_path):
                    task_list_file = os.path.join(agent_path, "task_list.json")
                    if os.path.exists(task_list_file):
                        try:
                            with open(task_list_file, 'r') as f:
                                tasks = json.load(f)
                            
                            task_count = len(tasks.get('tasks', []))
                            self.log(f"{agent}: {task_count} tasks in queue", "INFO")
                            
                        except Exception as e:
                            self.log(f"Error reading {agent} tasks: {str(e)}", "ERROR")
                            
        self.log("Task management system supports:", "INFO")
        self.log("  • Task creation and assignment", "INFO")
        self.log("  • Priority-based scheduling", "INFO")
        self.log("  • Progress tracking and reporting", "INFO")
        self.log("  • Autonomous task execution", "INFO")
        
    def demo_onboarding(self):
        """Demonstrate onboarding system"""
        self.log("🎓 ONBOARDING SYSTEM", "HEADER")
        
        onboarding_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_workspaces", "onboarding")
        
        if os.path.exists(onboarding_dir):
            onboarding_files = os.listdir(onboarding_dir)
            self.log(f"Onboarding directory contains {len(onboarding_files)} files", "INFO")
            
            # Check for key onboarding files
            key_files = [
                "ONBOARDING_GUIDE.md",
                "CORE_PROTOCOLS.md", 
                "DEVELOPMENT_STANDARDS.md",
                "onboarding_manager.py"
            ]
            
            for file in key_files:
                if os.path.exists(os.path.join(onboarding_dir, file)):
                    self.log(f"✅ {file} - Available", "SUCCESS")
                else:
                    self.log(f"❌ {file} - Missing", "WARNING")
                    
        self.log("Onboarding system provides:", "INFO")
        self.log("  • Step-by-step agent initialization", "INFO")
        self.log("  • Protocol training and verification", "INFO")
        self.log("  • Role assignment and responsibility training", "INFO")
        self.log("  • Development standards and best practices", "INFO")
        
    def demo_document_generation(self):
        """Demonstrate document generation"""
        self.log("📄 DOCUMENT GENERATION", "HEADER")
        
        docs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "docs")
        
        if os.path.exists(docs_dir):
            doc_files = [f for f in os.listdir(docs_dir) if f.endswith('.md')]
            self.log(f"Documentation directory contains {len(doc_files)} markdown files", "INFO")
            
            # Show some key documents
            key_docs = [
                "RESUME_TEMPLATE_USAGE_GUIDE.md",
                "INTER_AGENT_COMMUNICATION_GUIDE.md",
                "PROJECT_ROADMAP.md",
                "SYSTEM_ARCHITECT_RESUME_TEMPLATE.md"
            ]
            
            for doc in key_docs:
                if os.path.exists(os.path.join(docs_dir, doc)):
                    self.log(f"📋 {doc} - Available", "SUCCESS")
                else:
                    self.log(f"❌ {doc} - Missing", "WARNING")
                    
        self.log("Document generation system supports:", "INFO")
        self.log("  • Resume templates and conversion guides", "INFO")
        self.log("  • Technical documentation", "INFO")
        self.log("  • Project specifications and requirements", "INFO")
        self.log("  • User guides and tutorials", "INFO")
        
    def demo_performance(self):
        """Demonstrate performance monitoring"""
        self.log("📊 PERFORMANCE MONITORING", "HEADER")
        
        # Check agent performance metrics
        agent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "agent_workspaces")
        
        if os.path.exists(agent_dir):
            for agent in ["Agent-1", "Agent-2"]:
                status_file = os.path.join(agent_dir, agent, "status.json")
                if os.path.exists(status_file):
                    try:
                        with open(status_file, 'r') as f:
                            status = json.load(f)
                        
                        metrics = status.get('performance_metrics', {})
                        self.log(f"{agent} Performance:", "INFO")
                        self.log(f"  • Tasks Completed: {metrics.get('tasks_completed', 0)}", "INFO")
                        self.log(f"  • Success Rate: {metrics.get('success_rate', 0)}%", "INFO")
                        self.log(f"  • Messages Sent: {metrics.get('messages_sent', 0)}", "INFO")
                        self.log(f"  • Uptime: {metrics.get('uptime_hours', 0)} hours", "INFO")
                        
                    except Exception as e:
                        self.log(f"Error reading {agent} performance: {str(e)}", "ERROR")
                        
        self.log("Performance monitoring tracks:", "INFO")
        self.log("  • Task completion rates and success metrics", "INFO")
        self.log("  • Response times and system uptime", "INFO")
        self.log("  • Communication patterns and message volumes", "INFO")
        self.log("  • Error rates and system health", "INFO")
        
    def demo_system_controls(self):
        """Demonstrate system controls"""
        self.log("🔧 SYSTEM CONTROLS", "HEADER")
        
        # Check for system control files
        config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config")
        
        if os.path.exists(config_dir):
            config_files = os.listdir(config_dir)
            self.log(f"Configuration directory contains {len(config_files)} items", "INFO")
            
            # Check for key config files
            key_configs = [
                "system/system_config.json",
                "agents/agent_roles.json",
                "agents/agent_coordinates.json"
            ]
            
            for config in key_configs:
                config_path = os.path.join(config_dir, config)
                if os.path.exists(config_path):
                    self.log(f"⚙️ {config} - Available", "SUCCESS")
                else:
                    self.log(f"❌ {config} - Missing", "WARNING")
                    
        self.log("System controls provide:", "INFO")
        self.log("  • Agent role and capability configuration", "INFO")
        self.log("  • System-wide settings and parameters", "INFO")
        self.log("  • Communication protocol configuration", "INFO")
        self.log("  • Performance tuning and optimization", "INFO")

    def show_coordinate_mapping(self):
        """Show coordinate mapping for 2-agent mode"""
        self.log("🗺️ COORDINATE MAPPING (2-Agent Mode)", "HEADER")
        try:
            # Try to load coordinates from the config file
            coord_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                      "src", "runtime", "config", "cursor_agent_coords.json")
            if os.path.exists(coord_path):
                with open(coord_path, 'r', encoding='utf-8') as f:
                    coords = json.load(f)
                # Show only Agent-1 and Agent-2 from 2-agent layout
                if "2-agent" in coords:
                    agents_2 = coords["2-agent"]
                    for agent in ["Agent-1", "Agent-2"]:
                        if agent in agents_2:
                            c = agents_2[agent]["input_box"]
                            self.log(f"{agent} (2-agent layout): x={c['x']}, y={c['y']}", "INFO")
                        else:
                            self.log(f"{agent}: No coordinates found in 2-agent layout", "WARNING")
                else:
                    self.log("2-agent layout not found in config", "ERROR")
            else:
                self.log("Coordinate config file not found!", "ERROR")
        except Exception as e:
            self.log(f"Error loading coordinates: {e}", "ERROR")

def main():
    """Main function to run the Dream.OS demo GUI"""
    root = tk.Tk()
    app = DreamOSDemo(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main() 