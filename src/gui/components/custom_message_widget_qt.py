#!/usr/bin/env python3
"""
PyQt5 Custom Message Widget for Onboarding
Provides a reusable widget for sending custom onboarding messages
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel, QPushButton, QTextEdit, QGroupBox
from PyQt5.QtCore import Qt, pyqtSignal
from typing import Optional, Callable

class CustomMessageWidget(QWidget):
    """Reusable custom message widget for onboarding"""
    
    send_custom_message = pyqtSignal(str, str)  # target, message
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_message_text = None
        self.setup_widget()
    
    def setup_widget(self):
        """Setup the custom message widget"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        container = QFrame()
        container.setObjectName("customMessageContainer")
        container.setStyleSheet("""
            #customMessageContainer {
                background-color: #2C3E50;
                border-radius: 8px;
                border: 2px solid #34495E;
            }
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(8)
        
        # Title
        title_label = QLabel("Custom Message")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: white;
                padding: 5px;
            }
        """)
        container_layout.addWidget(title_label)
        
        # Message text area
        self.custom_message_text = QTextEdit()
        self.custom_message_text.setStyleSheet("""
            QTextEdit {
                background-color: #34495E;
                border: 1px solid #2C3E50;
                border-radius: 5px;
                color: #BDC3C7;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.custom_message_text.setMaximumHeight(120)
        container_layout.addWidget(self.custom_message_text)
        
        # Send buttons - Enhanced with chunk and comprehensive options
        send_buttons_layout = QHBoxLayout()
        
        self.send_chunk_btn = QPushButton("📤 Send Chunk")
        self.send_chunk_btn.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C;
                border-radius: 5px;
                color: white;
                padding: 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        self.send_chunk_btn.clicked.connect(self.send_chunk_message_clicked)
        send_buttons_layout.addWidget(self.send_chunk_btn)
        
        self.send_comprehensive_btn = QPushButton("📋 Send Comprehensive")
        self.send_comprehensive_btn.setStyleSheet("""
            QPushButton {
                background-color: #27AE60;
                border-radius: 5px;
                color: white;
                padding: 8px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.send_comprehensive_btn.clicked.connect(self.send_comprehensive_message_clicked)
        send_buttons_layout.addWidget(self.send_comprehensive_btn)
        
        container_layout.addLayout(send_buttons_layout)
        
        # Help text
        help_label = QLabel("💡 Chunk: Send in pieces | Comprehensive: Send complete message")
        help_label.setStyleSheet("""
            QLabel {
                color: #BDC3C7;
                font-size: 9px;
                padding: 2px;
            }
        """)
        help_label.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(help_label)
        
        layout.addWidget(container)
    
    def set_message_content(self, content: str):
        """Set the message content"""
        self.custom_message_text.setPlainText(content)
    
    def get_message_content(self) -> str:
        """Get the current message content"""
        return self.custom_message_text.toPlainText().strip()
    
    def clear_message(self):
        """Clear the message content"""
        self.custom_message_text.clear()
    
    def send_chunk_message_clicked(self):
        """Handle chunk send button click"""
        message = self.get_message_content()
        if message:
            self.send_custom_message.emit("chunk", message)
        else:
            # Show warning for empty message - this would need to be handled by parent
            pass
    
    def send_comprehensive_message_clicked(self):
        """Handle comprehensive send button click"""
        message = self.get_message_content()
        if message:
            self.send_custom_message.emit("comprehensive", message)
        else:
            # Show warning for empty message - this would need to be handled by parent
            pass 