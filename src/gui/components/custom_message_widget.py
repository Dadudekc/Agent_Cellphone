#!/usr/bin/env python3
"""
Custom Message Widget for Onboarding
Provides a reusable widget for sending custom onboarding messages
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional, Callable

class CustomMessageWidget:
    """Reusable custom message widget for onboarding"""
    
    def __init__(self, parent, send_callback: Callable, **kwargs):
        self.parent = parent
        self.send_callback = send_callback
        self.custom_message_text = None
        self.setup_widget(**kwargs)
    
    def setup_widget(self, **kwargs):
        """Setup the custom message widget"""
        frame = ttk.LabelFrame(self.parent, text="Custom Message", padding=5)
        frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.custom_message_text = scrolledtext.ScrolledText(frame, height=6, wrap=tk.WORD)
        self.custom_message_text.pack(fill=tk.BOTH, expand=True)
        
        # Send buttons - Enhanced with chunk and comprehensive options
        send_buttons_frame = ttk.Frame(frame)
        send_buttons_frame.pack(fill=tk.X, pady=(5, 0))
        
        self.send_chunk_btn = ttk.Button(send_buttons_frame, text="📤 Send Chunk", 
                                       command=self.send_chunk_message)
        self.send_chunk_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        self.send_comprehensive_btn = ttk.Button(send_buttons_frame, text="📋 Send Comprehensive", 
                                               command=self.send_comprehensive_message)
        self.send_comprehensive_btn.pack(side=tk.LEFT)
        
        # Help text
        help_label = ttk.Label(frame, text="💡 Chunk: Send in pieces | Comprehensive: Send complete message", 
                              font=("TkDefaultFont", 8))
        help_label.pack(pady=(5, 0))
    
    def set_message_content(self, content: str):
        """Set the message content"""
        self.custom_message_text.delete(1.0, tk.END)
        self.custom_message_text.insert(1.0, content)
    
    def get_message_content(self) -> str:
        """Get the current message content"""
        return self.custom_message_text.get(1.0, tk.END).strip()
    
    def clear_message(self):
        """Clear the message content"""
        self.custom_message_text.delete(1.0, tk.END)
    
    def send_chunk_message(self):
        """Send the custom message in chunks"""
        message = self.get_message_content()
        if message:
            self.send_callback("chunk", "all", message)
        else:
            # Show warning for empty message
            tk.messagebox.showwarning("Warning", "Please enter a message")
    
    def send_comprehensive_message(self):
        """Send the custom message as comprehensive"""
        message = self.get_message_content()
        if message:
            self.send_callback("comprehensive", "all", message)
        else:
            # Show warning for empty message
            tk.messagebox.showwarning("Warning", "Please enter a message")
    
    def get_widget(self):
        """Get the main widget"""
        return self.custom_message_text.master 