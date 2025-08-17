#!/usr/bin/env python3
"""
🔍 BUTTON FUNCTIONALITY TEST - Debug script for Ultimate Command Center
=====================================================================
This script tests basic PyQt5 button functionality to identify the issue.
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import Qt

class ButtonTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🔍 Button Functionality Test")
        self.setGeometry(200, 200, 400, 300)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        
        # Test label
        test_label = QLabel("Testing Button Functionality")
        test_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(test_label)
        
        # Test button 1 - Simple callback
        self.test_btn1 = QPushButton("Test Button 1 - Simple Callback")
        self.test_btn1.clicked.connect(self.test_callback1)
        layout.addWidget(self.test_btn1)
        
        # Test button 2 - Method reference
        self.test_btn2 = QPushButton("Test Button 2 - Method Reference")
        self.test_btn2.clicked.connect(self.test_callback2)
        layout.addWidget(self.test_btn2)
        
        # Test button 3 - Lambda function
        self.test_btn3 = QPushButton("Test Button 3 - Lambda Function")
        self.test_btn3.clicked.connect(lambda: self.test_callback3("Lambda called!"))
        layout.addWidget(self.test_btn3)
        
        # Test button 4 - Direct function
        self.test_btn4 = QPushButton("Test Button 4 - Direct Function")
        self.test_btn4.clicked.connect(lambda: print("Direct function called!"))
        layout.addWidget(self.test_btn4)
        
        # Status label
        self.status_label = QLabel("Status: Ready")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        central_widget.setLayout(layout)
        
        # Counter for callbacks
        self.callback_count = 0
    
    def test_callback1(self):
        """Test callback method 1."""
        self.callback_count += 1
        self.status_label.setText(f"Status: Callback 1 called! Count: {self.callback_count}")
        print(f"✅ Callback 1 executed! Count: {self.callback_count}")
    
    def test_callback2(self):
        """Test callback method 2."""
        self.callback_count += 1
        self.status_label.setText(f"Status: Callback 2 called! Count: {self.callback_count}")
        print(f"✅ Callback 2 executed! Count: {self.callback_count}")
    
    def test_callback3(self, message):
        """Test callback method 3 with parameter."""
        self.callback_count += 1
        self.status_label.setText(f"Status: {message} Count: {self.callback_count}")
        print(f"✅ Callback 3 executed! {message} Count: {self.callback_count}")

def main():
    """Main entry point for button test."""
    print("🚀 Starting Button Functionality Test...")
    
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Button Functionality Test")
    app.setApplicationVersion("1.0")
    
    # Create and show the test window
    window = ButtonTestWindow()
    window.show()
    
    print("✅ Test window created and shown")
    print("🔍 Click the buttons to test functionality")
    print("📝 Check console for callback execution messages")
    
    # Start the event loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

