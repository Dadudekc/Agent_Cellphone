#!/usr/bin/env python3
"""
Personal Jarvis - Standalone AI Assistant
Your personal AI agent that can control Cursor and your entire development environment
"""

import time
import logging
import threading
import subprocess
import os
import sys
from typing import Dict, List, Callable, Optional
from simple_audio_system import SimpleAudioSystem as AudioSystem
from vision_system import VisionSystem
from memory_system import MemorySystem
from conversation_engine import ConversationEngine
from fsm_organizer import FSMOrganizer, TaskPriority, TaskStatus, ProjectStatus, WorkflowType
from dreamvault_integration import DreamVaultIntegration
import pyautogui
import re
import json

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class PersonalJarvis:
    """
    Your personal AI assistant that can control Cursor and your development environment
    """
    
    def __init__(self, name: str = "Jarvis"):
        self.name = name
        self.logger = logging.getLogger(f"PersonalJarvis_{name}")
        
        # Initialize systems
        self.audio = AudioSystem({
            'speech_rate': 150,
            'volume': 0.9,
            'energy_threshold': 4000
        })
        
        self.vision = VisionSystem({
            'capture_frequency': 2.0
        })
        
        # Initialize memory and conversation systems
        self.memory = MemorySystem()
        self.conversation_engine = ConversationEngine(self.memory)
        
        # Initialize FSM Organizer
        self.fsm_organizer = FSMOrganizer()
        
        # Initialize DreamVault Integration
        self.dreamvault = DreamVaultIntegration()
        
        # Agent state
        self.is_active = False
        self.conversation_history = []
        self.current_context = {}
        self.is_in_conversation = False  # Flag to prevent vision interference
        self.vision_alerts_enabled = True  # Flag to control vision alerts
        
        # Voice command patterns
        self.commands = {
            'cursor': [
                r'open cursor',
                r'start cursor',
                r'launch cursor',
                r'close cursor',
                r'stop cursor'
            ],
            'development': [
                r'run (?:the )?tests?',
                r'build (?:the )?project',
                r'install (?:dependencies?|packages?)',
                r'check (?:for )?errors?',
                r'fix (?:the )?bugs?',
                r'commit (?:the )?changes?',
                r'push (?:to )?git',
                r'deploy (?:the )?application'
            ],
            'vision': [
                r'what (?:do you )?see',
                r'analyze (?:the )?screen',
                r'find (?:the )?text (.+)',
                r'click (?:on )?(.+)',
                r'look (?:for )?(.+)'
            ],
            'system': [
                r'stop (?:listening|speaking)',
                r'start (?:listening|speaking)',
                r'change (?:your )?voice',
                r'list (?:available )?voices?',
                r'train (?:voice )?recognition',
                r'enable (?:voice )?recognition',
                r'disable (?:voice )?recognition',
                r'set (?:speech )?rate (.+)',
                r'set (?:volume )?to (.+)',
                r'(?:disable|enable) (?:vision )?alerts?',
                r'toggle (?:vision )?alerts?',
                r'what (?:can you )?do',
                r'help',
                r'exit',
                r'quit',
                r'goodbye'
            ],
            'workflow': [
                r'create (?:new )?project (.+)',
                r'create (?:new )?task (.+)',
                r'create (?:new )?workflow (.+)',
                r'start (?:workflow|project) (.+)',
                r'complete (?:task|workflow) (.+)',
                r'list (?:projects|tasks|workflows)',
                r'show (?:project|task|workflow) (.+)',
                r'get (?:system )?overview',
                r'get (?:project )?progress (.+)',
                r'what (?:are )?my (?:tasks|projects|workflows)',
                r'what (?:is )?next',
                r'what (?:is )?overdue'
            ],
            'dreamvault': [
                r'search (?:my )?conversations? (.+)',
                r'find (?:my )?conversations? (.+)',
                r'get (?:my )?recent (?:conversations?|chats?)',
                r'show (?:my )?product (?:ideas?|concepts?)',
                r'get (?:my )?workflows?',
                r'find (?:my )?abandoned (?:ideas?|concepts?)',
                r'get (?:my )?high (?:value )?insights?',
                r'analyze (?:my )?topic (.+)',
                r'get (?:my )?learning (?:recommendations?|suggestions?)',
                r'suggest (?:actions?|next steps?)',
                r'what (?:are )?my (?:conversations?|chats?) about (.+)',
                r'find (?:similar )?conversations? (.+)'
            ],
            'cursor_control': [
                r'open (?:file|document) (.+)',
                r'create (?:file|document) (.+)',
                r'save (?:file|document)',
                r'search (?:for )?(.+)',
                r'find (?:in )?files? (.+)',
                r'replace (?:text )?(.+) with (.+)',
                r'format (?:code|document)',
                r'run (?:code|script)',
                r'debug (?:code|script)',
                r'build (?:project|solution)',
                r'deploy (?:project|application)'
            ]
        }
        
        # Set up audio callbacks
        self.audio.add_speech_callback(self._handle_voice_command)
        
        # Cursor control
        self.cursor_process = None
        self.cursor_path = self._find_cursor_path()
        
        # Check if we know the user
        user_name = self.memory.get_user_info("name")
        if user_name:
            self.logger.info(f"Welcome back, {user_name}!")
        else:
            self.logger.info("New user detected - ready to learn about you!")
        
        self.logger.info(f"Personal {name} initialized and ready to serve")
    
    def _find_cursor_path(self) -> str:
        """
        Find Cursor installation path
        """
        possible_paths = [
            r"C:\Users\%USERNAME%\AppData\Local\Programs\Cursor\Cursor.exe",
            r"C:\Program Files\Cursor\Cursor.exe",
            r"C:\Program Files (x86)\Cursor\Cursor.exe"
        ]
        
        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                self.logger.info(f"Found Cursor at: {expanded_path}")
                return expanded_path
        
        self.logger.warning("Cursor not found in standard locations")
        return None
    
    def start(self):
        """
        Start Personal Jarvis
        """
        self.logger.info("Starting Personal Jarvis...")
        self.is_active = True
        
        # Start vision monitoring
        self._start_vision_monitoring()
        
        # Start audio listening
        self.audio.start_listening()
        
        # Welcome message
        self.audio.speak(f"Hello! I am {self.name}, your personal AI assistant. I can help you control Cursor and your development environment. What would you like me to do?")
        
        self.logger.info("Personal Jarvis is now active and listening")
    
    def stop(self):
        """
        Stop Personal Jarvis
        """
        self.logger.info("Stopping Personal Jarvis...")
        self.is_active = False
        
        # Stop systems
        self.audio.stop_listening()
        self.audio.stop_speaking()
        
        # Close Cursor if open
        if self.cursor_process:
            self._close_cursor()
        
        # Close memory system
        self.memory.close()
        
        # Close FSM organizer
        self.fsm_organizer.close()
        
        self.logger.info("Personal Jarvis stopped")
    
    def _start_vision_monitoring(self):
        """
        Start vision monitoring in background
        """
        def vision_loop():
            while self.is_active:
                try:
                    # Capture screen
                    screenshot = self.vision.capture_screen()
                    if screenshot is not None:
                        # Analyze screen content
                        analysis = self.vision.analyze_screen_content(screenshot)
                        self.current_context['screen_analysis'] = analysis
                        
                        # Look for important events
                        self._check_for_important_events(analysis)
                    
                    time.sleep(2)  # Check every 2 seconds
                    
                except Exception as e:
                    self.logger.error(f"Vision monitoring error: {e}")
                    time.sleep(5)
        
        vision_thread = threading.Thread(target=vision_loop, daemon=True)
        vision_thread.start()
    
    def _check_for_important_events(self, analysis: Dict):
        """
        Check for important events on screen
        """
        # Don't interrupt if we're in a conversation or if alerts are disabled
        if self.is_in_conversation or not self.vision_alerts_enabled:
            return
            
        text_content = analysis.get('text_content', '').lower()
        
        # More specific error detection to avoid false positives
        error_indicators = [
            'error:',
            'exception:',
            'failed:',
            'traceback:',
            'syntax error',
            'import error',
            'module not found',
            'file not found'
        ]
        
        # Only alert if we find actual error patterns, not just the word "error"
        found_errors = []
        for indicator in error_indicators:
            if indicator in text_content:
                found_errors.append(indicator)
        
        if found_errors:
            # Only speak if we haven't already alerted about this error recently
            current_time = time.time()
            if not hasattr(self, '_last_error_alert') or (current_time - getattr(self, '_last_error_alert', 0)) > 30:
                self.audio.speak("I detected an error on your screen. Would you like me to help fix it?")
                self._last_error_alert = current_time
        
        # Check for test results
        if 'test' in text_content and ('passed' in text_content or 'failed' in text_content):
            if 'passed' in text_content:
                self.audio.speak("Great! Your tests are passing.")
            else:
                self.audio.speak("I see some tests failed. Would you like me to help debug them?")
        
        # Check for build results
        if 'build' in text_content and ('successful' in text_content or 'failed' in text_content):
            if 'successful' in text_content:
                self.audio.speak("Build completed successfully!")
            else:
                self.audio.speak("Build failed. Let me help you fix the issues.")
    
    def _handle_voice_command(self, text: str):
        """
        Process voice commands with intelligent conversation
        """
        self.logger.info(f"Processing command: {text}")
        
        # Set conversation flag to prevent vision interference
        self.is_in_conversation = True
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user_command',
            'text': text,
            'timestamp': time.time()
        })
        
        # First, try to generate an intelligent conversation response
        conversation_response = self.conversation_engine.generate_response(text, self.current_context)
        self.logger.info(f"Generated conversation response: '{conversation_response}'")
        
        # Check if this is a conversation or a command
        if self._is_conversation_only(text):
            # This is just conversation - respond intelligently
            self.logger.info(f"Detected conversation-only input, speaking response...")
            self.audio.speak(conversation_response)
            self.conversation_engine.remember_conversation(text, conversation_response)
            # Reset conversation flag after a short delay
            threading.Timer(3.0, lambda: setattr(self, 'is_in_conversation', False)).start()
            return
        
        # This might be a command - check command types
        command_executed = False
        
        if self._is_cursor_command(text):
            self._execute_cursor_command(text)
            command_executed = True
        elif self._is_development_command(text):
            self._execute_development_command(text)
            command_executed = True
        elif self._is_vision_command(text):
            self._execute_vision_command(text)
            command_executed = True
        elif self._is_system_command(text):
            self._execute_system_command(text)
            command_executed = True
        elif self._is_cursor_control_command(text):
            self._execute_cursor_control_command(text)
            command_executed = True
        elif self._is_workflow_command(text):
            self._execute_workflow_command(text)
            command_executed = True
        elif self._is_dreamvault_command(text):
            self._execute_dreamvault_command(text)
            command_executed = True
        
        # If no command was executed, provide conversation response
        if not command_executed:
            self.audio.speak(conversation_response)
            self.conversation_engine.remember_conversation(text, conversation_response)
        
        # Reset conversation flag after a short delay
        threading.Timer(3.0, lambda: setattr(self, 'is_in_conversation', False)).start()
    
    def _is_cursor_command(self, text: str) -> bool:
        """Check if text contains Cursor-related commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['cursor'])
    
    def _is_development_command(self, text: str) -> bool:
        """Check if text contains development commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['development'])
    
    def _is_vision_command(self, text: str) -> bool:
        """Check if text contains vision commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['vision'])
    
    def _is_system_command(self, text: str) -> bool:
        """Check if text contains system commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['system'])
    
    def _is_cursor_control_command(self, text: str) -> bool:
        """Check if text contains Cursor control commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['cursor_control'])
    
    def _is_workflow_command(self, text: str) -> bool:
        """Check if text contains workflow commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['workflow'])
    
    def _is_dreamvault_command(self, text: str) -> bool:
        """Check if text contains DreamVault commands"""
        return any(re.search(pattern, text.lower()) for pattern in self.commands['dreamvault'])
    
    def _is_conversation_only(self, text: str) -> bool:
        """Check if text is conversation-only (not a command)"""
        conversation_patterns = [
            r'hello|hi|hey|greetings',
            r'how are you|what\'s up',
            r'thank you|thanks',
            r'goodbye|bye|see you',
            r'who are you|what are you',
            r'do you remember|can you remember',
            r'my name is|i am|call me',
            r'i like|i prefer|my favorite',
            r'what can you do|help',
            r'nice to meet you|pleasure',
            r'that\'s interesting|cool|awesome',
            r'i don\'t understand|confused',
            r'what do you mean|explain'
        ]
        
        # If it matches conversation patterns and doesn't contain command words
        is_conversation = any(re.search(pattern, text.lower()) for pattern in conversation_patterns)
        has_command_words = any(word in text.lower() for word in ['open', 'close', 'run', 'start', 'stop', 'find', 'search', 'click', 'save', 'create'])
        
        return is_conversation and not has_command_words
    
    def _execute_cursor_command(self, text: str):
        """Execute Cursor-related commands"""
        text_lower = text.lower()
        
        if re.search(r'open cursor|start cursor|launch cursor', text_lower):
            self._open_cursor()
        elif re.search(r'close cursor|stop cursor', text_lower):
            self._close_cursor()
    
    def _execute_development_command(self, text: str):
        """Execute development commands"""
        text_lower = text.lower()
        
        if re.search(r'run (?:the )?tests?', text_lower):
            self._run_tests()
        elif re.search(r'build (?:the )?project', text_lower):
            self._build_project()
        elif re.search(r'install (?:dependencies?|packages?)', text_lower):
            self._install_dependencies()
        elif re.search(r'check (?:for )?errors?', text_lower):
            self._check_errors()
        elif re.search(r'fix (?:the )?bugs?', text_lower):
            self._fix_bugs()
        elif re.search(r'commit (?:the )?changes?', text_lower):
            self._commit_changes()
        elif re.search(r'push (?:to )?git', text_lower):
            self._push_git()
        elif re.search(r'deploy (?:the )?application', text_lower):
            self._deploy_application()
    
    def _execute_vision_command(self, text: str):
        """Execute vision commands"""
        text_lower = text.lower()
        
        if re.search(r'what (?:do you )?see', text_lower):
            self._describe_what_i_see()
        elif re.search(r'analyze (?:the )?screen', text_lower):
            self._analyze_screen()
        elif re.search(r'find (?:the )?text (.+)', text_lower):
            match = re.search(r'find (?:the )?text (.+)', text_lower)
            if match:
                search_text = match.group(1)
                self._find_text_on_screen(search_text)
        elif re.search(r'click (?:on )?(.+)', text_lower):
            match = re.search(r'click (?:on )?(.+)', text_lower)
            if match:
                click_text = match.group(1)
                self._click_on_text(click_text)
    
    def _execute_system_command(self, text: str):
        """Execute system commands"""
        text_lower = text.lower()
        
        if re.search(r'exit|quit|goodbye', text_lower):
            self.audio.speak(f"Goodbye! {self.name} signing off.")
            self.stop()
        elif re.search(r'help|what (?:can you )?do', text_lower):
            self._provide_help()
        elif re.search(r'change (?:your )?voice', text_lower):
            self._change_voice()
        elif re.search(r'list (?:available )?voices?', text_lower):
            self._list_voices()
        elif re.search(r'train (?:voice )?recognition', text_lower):
            self._train_voice_recognition()
        elif re.search(r'enable (?:voice )?recognition', text_lower):
            self._enable_voice_recognition()
        elif re.search(r'disable (?:voice )?recognition', text_lower):
            self._disable_voice_recognition()
        elif re.search(r'(?:disable|enable) (?:vision )?alerts?', text_lower):
            self._toggle_vision_alerts(text_lower)
        elif re.search(r'toggle (?:vision )?alerts?', text_lower):
            self._toggle_vision_alerts(text_lower)
    
    def _execute_cursor_control_command(self, text: str):
        """Execute Cursor control commands"""
        text_lower = text.lower()
        
        if re.search(r'open (?:file|document) (.+)', text_lower):
            match = re.search(r'open (?:file|document) (.+)', text_lower)
            if match:
                filename = match.group(1)
                self._open_file_in_cursor(filename)
        elif re.search(r'create (?:file|document) (.+)', text_lower):
            match = re.search(r'create (?:file|document) (.+)', text_lower)
            if match:
                filename = match.group(1)
                self._create_file_in_cursor(filename)
        elif re.search(r'save (?:file|document)', text_lower):
            self._save_file_in_cursor()
        elif re.search(r'search (?:for )?(.+)', text_lower):
            match = re.search(r'search (?:for )?(.+)', text_lower)
            if match:
                search_term = match.group(1)
                self._search_in_cursor(search_term)
    
    def _open_cursor(self):
        """Open Cursor editor"""
        if self.cursor_path and os.path.exists(self.cursor_path):
            try:
                self.cursor_process = subprocess.Popen([self.cursor_path])
                self.audio.speak("Opening Cursor editor.")
                time.sleep(3)  # Wait for Cursor to start
            except Exception as e:
                self.logger.error(f"Failed to open Cursor: {e}")
                self.audio.speak("I couldn't open Cursor. Please check if it's installed.")
        else:
            self.audio.speak("I couldn't find Cursor on your system. Please install it first.")
    
    def _close_cursor(self):
        """Close Cursor editor"""
        if self.cursor_process:
            try:
                self.cursor_process.terminate()
                self.cursor_process = None
                self.audio.speak("Closing Cursor editor.")
            except Exception as e:
                self.logger.error(f"Failed to close Cursor: {e}")
        else:
            # Try to close by window title
            try:
                pyautogui.hotkey('alt', 'f4')
                self.audio.speak("Closing Cursor editor.")
            except:
                self.audio.speak("I couldn't close Cursor.")
    
    def _open_file_in_cursor(self, filename: str):
        """Open a file in Cursor"""
        self.audio.speak(f"Opening {filename} in Cursor.")
        pyautogui.hotkey('ctrl', 'o')
        time.sleep(1)
        pyautogui.write(filename)
        pyautogui.press('enter')
    
    def _create_file_in_cursor(self, filename: str):
        """Create a new file in Cursor"""
        self.audio.speak(f"Creating {filename} in Cursor.")
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 's')
        time.sleep(1)
        pyautogui.write(filename)
        pyautogui.press('enter')
    
    def _save_file_in_cursor(self):
        """Save current file in Cursor"""
        self.audio.speak("Saving file in Cursor.")
        pyautogui.hotkey('ctrl', 's')
    
    def _search_in_cursor(self, search_term: str):
        """Search in Cursor"""
        self.audio.speak(f"Searching for {search_term} in Cursor.")
        pyautogui.hotkey('ctrl', 'f')
        time.sleep(1)
        pyautogui.write(search_term)
    
    def _run_tests(self):
        """Run tests"""
        self.audio.speak("Running tests for your project.")
        pyautogui.hotkey('ctrl', 'shift', '`')  # Open terminal
        time.sleep(1)
        pyautogui.write('python -m pytest')
        pyautogui.press('enter')
    
    def _build_project(self):
        """Build project"""
        self.audio.speak("Building your project.")
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('npm run build')
        pyautogui.press('enter')
    
    def _install_dependencies(self):
        """Install dependencies"""
        self.audio.speak("Installing dependencies.")
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('pip install -r requirements.txt')
        pyautogui.press('enter')
    
    def _check_errors(self):
        """Check for errors"""
        self.audio.speak("Checking for errors.")
        analysis = self.current_context.get('screen_analysis', {})
        text_content = analysis.get('text_content', '')
        
        error_patterns = ['error:', 'exception:', 'failed:', 'traceback:']
        found_errors = []
        
        for pattern in error_patterns:
            if pattern in text_content.lower():
                found_errors.append(pattern)
        
        if found_errors:
            self.audio.speak(f"I found {len(found_errors)} potential errors: {', '.join(found_errors)}")
        else:
            self.audio.speak("I don't see any obvious errors in the current view.")
    
    def _fix_bugs(self):
        """Attempt to fix bugs"""
        self.audio.speak("Attempting to fix bugs.")
        analysis = self.current_context.get('screen_analysis', {})
        text_content = analysis.get('text_content', '')
        
        if 'import error' in text_content.lower():
            self.audio.speak("I see an import error. Let me try to install the missing package.")
            self._install_dependencies()
        elif 'syntax error' in text_content.lower():
            self.audio.speak("I see a syntax error. Please check the highlighted line in your editor.")
        else:
            self.audio.speak("I don't see any obvious bugs that I can automatically fix.")
    
    def _commit_changes(self):
        """Commit changes to git"""
        self.audio.speak("Committing your changes to git.")
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('git add .')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write('git commit -m "Auto-commit from Jarvis"')
        pyautogui.press('enter')
    
    def _push_git(self):
        """Push changes to git"""
        self.audio.speak("Pushing changes to git.")
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('git push')
        pyautogui.press('enter')
    
    def _deploy_application(self):
        """Deploy application"""
        self.audio.speak("Deploying your application.")
        # This would depend on the deployment platform
        self.audio.speak("Please specify your deployment platform or I can help you set up automated deployment.")
    
    def _describe_what_i_see(self):
        """Describe what's on screen"""
        analysis = self.current_context.get('screen_analysis', {})
        text_content = analysis.get('text_content', '')
        
        if text_content:
            summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            self.audio.speak(f"I can see: {summary}")
        else:
            self.audio.speak("I can see your screen but I'm not detecting any text content.")
    
    def _analyze_screen(self):
        """Analyze screen content"""
        analysis = self.current_context.get('screen_analysis', {})
        ui_elements = analysis.get('ui_elements', [])
        text_regions = analysis.get('text_regions', [])
        
        self.audio.speak(f"I can see {len(text_regions)} text elements and {len(ui_elements)} UI elements on your screen.")
    
    def _find_text_on_screen(self, search_text: str):
        """Find text on screen"""
        # This would use the vision system to find text
        self.audio.speak(f"Looking for '{search_text}' on your screen.")
        # Implementation would use OCR to find text locations
    
    def _click_on_text(self, text: str):
        """Click on specific text"""
        self.audio.speak(f"Clicking on '{text}'.")
        # Implementation would use vision system to find and click text
    
    def _change_voice(self):
        """Change TTS voice"""
        try:
            # Import and run voice selector
            from voice_selector import list_available_voices, test_voice
            
            voices = list_available_voices()
            if voices:
                self.audio.speak("I'll list the available voices for you.")
                print("\n🎤 Available voices:")
                for i, voice in enumerate(voices):
                    print(f"{i+1}. {voice.name}")
                
                # Test current voice
                self.audio.speak("Testing current voice.")
                test_voice()
                
                self.audio.speak("You can run the voice selector script to change my voice.")
            else:
                self.audio.speak("No voices found. Using default voice.")
                
        except Exception as e:
            self.logger.error(f"Error changing voice: {e}")
            self.audio.speak("Sorry, I couldn't change my voice right now.")
    
    def _list_voices(self):
        """List available voices"""
        try:
            from voice_selector import list_available_voices
            
            voices = list_available_voices()
            if voices:
                self.audio.speak(f"I found {len(voices)} available voices.")
                print(f"\n🎤 Found {len(voices)} voices:")
                for i, voice in enumerate(voices):
                    print(f"{i+1}. {voice.name}")
            else:
                self.audio.speak("No voices found.")
                
        except Exception as e:
            self.logger.error(f"Error listing voices: {e}")
            self.audio.speak("Sorry, I couldn't list the voices.")
    
    def _train_voice_recognition(self):
        """Train voice recognition system"""
        try:
            from voice_recognition import VoiceRecognition
            
            self.audio.speak("I'll help you train voice recognition. This will teach me to recognize your voice.")
            
            # Create voice recognition instance
            voice_recognition = VoiceRecognition("Victor")
            
            # Start training
            voice_recognition.train_voice()
            
            # Enable voice recognition in audio system
            self.audio.voice_recognition_enabled = True
            self.audio.voice_recognition = voice_recognition
            
            self.audio.speak("Voice recognition training completed! I'll now only respond to your voice.")
            
        except Exception as e:
            self.logger.error(f"Error training voice recognition: {e}")
            self.audio.speak("Sorry, I couldn't train voice recognition right now.")
    
    def _enable_voice_recognition(self):
        """Enable voice recognition"""
        try:
            from voice_recognition import VoiceRecognition
            
            # Load existing voice profile
            voice_recognition = VoiceRecognition("Victor")
            status = voice_recognition.get_voice_status()
            
            if status['training_complete']:
                self.audio.voice_recognition_enabled = True
                self.audio.voice_recognition = voice_recognition
                self.audio.speak("Voice recognition enabled. I'll only respond to your voice.")
            else:
                self.audio.speak("Voice recognition not trained yet. Please train it first.")
                
        except Exception as e:
            self.logger.error(f"Error enabling voice recognition: {e}")
            self.audio.speak("Sorry, I couldn't enable voice recognition.")
    
    def _disable_voice_recognition(self):
        """Disable voice recognition"""
        self.audio.voice_recognition_enabled = False
        self.audio.voice_recognition = None
        self.audio.speak("Voice recognition disabled. I'll respond to any voice now.")
    
    def _toggle_vision_alerts(self, text: str):
        """Toggle vision alerts on/off"""
        if 'disable' in text.lower():
            self.vision_alerts_enabled = False
            self.audio.speak("Vision alerts disabled. I won't interrupt you with screen notifications.")
        elif 'enable' in text.lower():
            self.vision_alerts_enabled = True
            self.audio.speak("Vision alerts enabled. I'll notify you of important screen events.")
        else:
            # Toggle
            self.vision_alerts_enabled = not self.vision_alerts_enabled
            status = "enabled" if self.vision_alerts_enabled else "disabled"
            self.audio.speak(f"Vision alerts {status}.")
    
    def _execute_workflow_command(self, text: str):
        """Execute workflow commands"""
        text_lower = text.lower()
        
        if re.search(r'create (?:new )?project (.+)', text_lower):
            match = re.search(r'create (?:new )?project (.+)', text_lower)
            if match:
                project_name = match.group(1)
                self._create_project(project_name)
        elif re.search(r'create (?:new )?task (.+)', text_lower):
            match = re.search(r'create (?:new )?task (.+)', text_lower)
            if match:
                task_name = match.group(1)
                self._create_task(task_name)
        elif re.search(r'create (?:new )?workflow (.+)', text_lower):
            match = re.search(r'create (?:new )?workflow (.+)', text_lower)
            if match:
                workflow_name = match.group(1)
                self._create_workflow(workflow_name)
        elif re.search(r'list (?:projects|tasks|workflows)', text_lower):
            self._list_items(text_lower)
        elif re.search(r'get (?:system )?overview', text_lower):
            self._get_system_overview()
        elif re.search(r'what (?:are )?my (?:tasks|projects|workflows)', text_lower):
            self._get_my_items(text_lower)
        elif re.search(r'what (?:is )?next', text_lower):
            self._get_next_tasks()
        elif re.search(r'what (?:is )?overdue', text_lower):
            self._get_overdue_tasks()
    
    def _create_project(self, name: str):
        """Create a new project"""
        try:
            project_id = self.fsm_organizer.create_project(
                name=name,
                description=f"Project created by {self.name}",
                tags=["jarvis", "auto-created"]
            )
            self.audio.speak(f"Created new project: {name}")
            self.logger.info(f"Created project: {name} ({project_id})")
        except Exception as e:
            self.audio.speak(f"Failed to create project: {str(e)}")
            self.logger.error(f"Project creation error: {e}")
    
    def _create_task(self, name: str):
        """Create a new task"""
        try:
            # Get the most recent project or create a default one
            active_projects = self.fsm_organizer.get_projects_by_status(ProjectStatus.ACTIVE)
            if not active_projects:
                active_projects = self.fsm_organizer.get_projects_by_status(ProjectStatus.PLANNING)
            
            if not active_projects:
                # Create a default project
                project_id = self.fsm_organizer.create_project(
                    name="Default Project",
                    description="Default project for tasks",
                    tags=["default", "jarvis"]
                )
                self.fsm_organizer.update_project_status(project_id, ProjectStatus.ACTIVE)
            else:
                project_id = active_projects[0].id
            
            # Create a default workflow if none exists
            project = self.fsm_organizer.get_project(project_id)
            if not project.workflows:
                workflow_id = self.fsm_organizer.create_workflow(
                    name="Default Workflow",
                    description="Default workflow for tasks",
                    workflow_type=WorkflowType.DEVELOPMENT,
                    project_id=project_id
                )
            else:
                workflow_id = project.workflows[0]
            
            task_id = self.fsm_organizer.create_task(
                name=name,
                description=f"Task created by {self.name}",
                project_id=project_id,
                workflow_id=workflow_id,
                priority=TaskPriority.MEDIUM
            )
            
            self.audio.speak(f"Created new task: {name}")
            self.logger.info(f"Created task: {name} ({task_id})")
        except Exception as e:
            self.audio.speak(f"Failed to create task: {str(e)}")
            self.logger.error(f"Task creation error: {e}")
    
    def _create_workflow(self, name: str):
        """Create a new workflow"""
        try:
            # Get the most recent project or create a default one
            active_projects = self.fsm_organizer.get_projects_by_status(ProjectStatus.ACTIVE)
            if not active_projects:
                active_projects = self.fsm_organizer.get_projects_by_status(ProjectStatus.PLANNING)
            
            if not active_projects:
                # Create a default project
                project_id = self.fsm_organizer.create_project(
                    name="Default Project",
                    description="Default project for workflows",
                    tags=["default", "jarvis"]
                )
                self.fsm_organizer.update_project_status(project_id, ProjectStatus.ACTIVE)
            else:
                project_id = active_projects[0].id
            
            workflow_id = self.fsm_organizer.create_workflow(
                name=name,
                description=f"Workflow created by {self.name}",
                workflow_type=WorkflowType.DEVELOPMENT,
                project_id=project_id
            )
            
            self.audio.speak(f"Created new workflow: {name}")
            self.logger.info(f"Created workflow: {name} ({workflow_id})")
        except Exception as e:
            self.audio.speak(f"Failed to create workflow: {str(e)}")
            self.logger.error(f"Workflow creation error: {e}")
    
    def _list_items(self, text: str):
        """List projects, tasks, or workflows"""
        if 'projects' in text:
            projects = list(self.fsm_organizer.projects.values())
            if projects:
                project_names = [p.name for p in projects[:5]]  # Show first 5
                self.audio.speak(f"You have {len(projects)} projects. Recent ones: {', '.join(project_names)}")
            else:
                self.audio.speak("You don't have any projects yet.")
        elif 'tasks' in text:
            tasks = list(self.fsm_organizer.tasks.values())
            if tasks:
                task_names = [t.name for t in tasks[:5]]  # Show first 5
                self.audio.speak(f"You have {len(tasks)} tasks. Recent ones: {', '.join(task_names)}")
            else:
                self.audio.speak("You don't have any tasks yet.")
        elif 'workflows' in text:
            workflows = list(self.fsm_organizer.workflows.values())
            if workflows:
                workflow_names = [w.name for w in workflows[:5]]  # Show first 5
                self.audio.speak(f"You have {len(workflows)} workflows. Recent ones: {', '.join(workflow_names)}")
            else:
                self.audio.speak("You don't have any workflows yet.")
    
    def _get_system_overview(self):
        """Get system overview"""
        overview = self.fsm_organizer.get_system_overview()
        self.audio.speak(f"System overview: {overview['total_projects']} projects, {overview['total_tasks']} tasks, {overview['total_workflows']} workflows. {overview['in_progress_tasks']} tasks in progress.")
    
    def _get_my_items(self, text: str):
        """Get user's items"""
        if 'tasks' in text:
            pending_tasks = self.fsm_organizer.get_tasks_by_status(TaskStatus.PENDING)
            in_progress_tasks = self.fsm_organizer.get_tasks_by_status(TaskStatus.IN_PROGRESS)
            total_tasks = len(pending_tasks) + len(in_progress_tasks)
            self.audio.speak(f"You have {total_tasks} active tasks: {len(pending_tasks)} pending, {len(in_progress_tasks)} in progress.")
        elif 'projects' in text:
            active_projects = self.fsm_organizer.get_projects_by_status(ProjectStatus.ACTIVE)
            self.audio.speak(f"You have {len(active_projects)} active projects.")
        elif 'workflows' in text:
            active_workflows = self.fsm_organizer.get_active_workflows()
            self.audio.speak(f"You have {len(active_workflows)} active workflows.")
    
    def _get_next_tasks(self):
        """Get next tasks to work on"""
        ready_tasks = self.fsm_organizer.get_ready_tasks()
        if ready_tasks:
            task_names = [t.name for t in ready_tasks[:3]]  # Show first 3
            self.audio.speak(f"Next tasks to work on: {', '.join(task_names)}")
        else:
            self.audio.speak("No tasks are ready to start. All tasks are either completed or have unmet dependencies.")
    
    def _get_overdue_tasks(self):
        """Get overdue tasks"""
        overdue_tasks = self.fsm_organizer.get_overdue_tasks()
        if overdue_tasks:
            task_names = [t.name for t in overdue_tasks[:3]]  # Show first 3
            self.audio.speak(f"Overdue tasks: {', '.join(task_names)}")
        else:
            self.audio.speak("No tasks are overdue.")
    
    def _execute_dreamvault_command(self, text: str):
        """Execute DreamVault commands"""
        text_lower = text.lower()
        
        if not self.dreamvault.available:
            self.audio.speak("DreamVault integration is not available. Please check if the database exists.")
            return
        
        # Search conversations
        if re.search(r'search (?:my )?conversations? (.+)', text_lower):
            match = re.search(r'search (?:my )?conversations? (.+)', text_lower)
            if match:
                query = match.group(1)
                self._search_conversations(query)
        elif re.search(r'find (?:my )?conversations? (.+)', text_lower):
            match = re.search(r'find (?:my )?conversations? (.+)', text_lower)
            if match:
                query = match.group(1)
                self._search_conversations(query)
        # Get recent conversations
        elif re.search(r'get (?:my )?recent (?:conversations?|chats?)', text_lower):
            self._get_recent_conversations()
        # Show product ideas
        elif re.search(r'show (?:my )?product (?:ideas?|concepts?)', text_lower):
            self._get_product_ideas()
        # Get workflows
        elif re.search(r'get (?:my )?workflows?', text_lower):
            self._get_workflows()
        # Find abandoned ideas
        elif re.search(r'find (?:my )?abandoned (?:ideas?|concepts?)', text_lower):
            self._get_abandoned_ideas()
        # Get high value insights
        elif re.search(r'get (?:my )?high (?:value )?insights?', text_lower):
            self._get_high_value_insights()
        # Analyze topic
        elif re.search(r'analyze (?:my )?topic (.+)', text_lower):
            match = re.search(r'analyze (?:my )?topic (.+)', text_lower)
            if match:
                topic = match.group(1)
                self._analyze_topic(topic)
        # Get learning recommendations
        elif re.search(r'get (?:my )?learning (?:recommendations?|suggestions?)', text_lower):
            self._get_learning_recommendations()
        # Suggest actions
        elif re.search(r'suggest (?:actions?|next steps?)', text_lower):
            self._suggest_actions()
        # Find similar conversations
        elif re.search(r'find (?:similar )?conversations? (.+)', text_lower):
            match = re.search(r'find (?:similar )?conversations? (.+)', text_lower)
            if match:
                query = match.group(1)
                self._search_conversations(query)
    
    def _search_conversations(self, query: str):
        """Search conversations in DreamVault"""
        try:
            results = self.dreamvault.search_conversations(query, limit=5)
            if results:
                self.audio.speak(f"Found {len(results)} conversations matching '{query}'. Here are the most relevant ones:")
                for i, conv in enumerate(results[:3], 1):
                    summary = conv['summary'][:100] + "..." if len(conv['summary']) > 100 else conv['summary']
                    self.audio.speak(f"Conversation {i}: {summary}")
            else:
                self.audio.speak(f"No conversations found matching '{query}'.")
        except Exception as e:
            self.audio.speak(f"Error searching conversations: {str(e)}")
    
    def _get_recent_conversations(self):
        """Get recent conversations from DreamVault"""
        try:
            recent = self.dreamvault.get_recent_conversations(days=7, limit=5)
            if recent:
                self.audio.speak(f"You have {len(recent)} recent conversations. Here are the latest ones:")
                for i, conv in enumerate(recent[:3], 1):
                    summary = conv['summary'][:100] + "..." if len(conv['summary']) > 100 else conv['summary']
                    self.audio.speak(f"Recent conversation {i}: {summary}")
            else:
                self.audio.speak("No recent conversations found.")
        except Exception as e:
            self.audio.speak(f"Error getting recent conversations: {str(e)}")
    
    def _get_product_ideas(self):
        """Get product ideas from DreamVault"""
        try:
            ideas = self.dreamvault.get_product_ideas(min_value=5000, limit=5)
            if ideas:
                self.audio.speak(f"Found {len(ideas)} high-value product ideas. Here are the top ones:")
                for i, idea in enumerate(ideas[:3], 1):
                    value = idea['potential_value']
                    self.audio.speak(f"Product idea {i}: Estimated value ${value:,.0f}")
            else:
                self.audio.speak("No high-value product ideas found.")
        except Exception as e:
            self.audio.speak(f"Error getting product ideas: {str(e)}")
    
    def _get_workflows(self):
        """Get workflows from DreamVault"""
        try:
            workflows = self.dreamvault.get_workflows(limit=5)
            if workflows:
                self.audio.speak(f"Found {len(workflows)} workflows. Here are the most valuable ones:")
                for i, workflow in enumerate(workflows[:3], 1):
                    value = workflow['potential_value']
                    self.audio.speak(f"Workflow {i}: Estimated value ${value:,.0f}")
            else:
                self.audio.speak("No workflows found.")
        except Exception as e:
            self.audio.speak(f"Error getting workflows: {str(e)}")
    
    def _get_abandoned_ideas(self):
        """Get abandoned ideas from DreamVault"""
        try:
            abandoned = self.dreamvault.get_abandoned_ideas(min_value=5000, limit=5)
            if abandoned:
                self.audio.speak(f"Found {len(abandoned)} abandoned ideas that could be resurrected. Here are the top ones:")
                for i, idea in enumerate(abandoned[:3], 1):
                    value = idea['potential_value']
                    self.audio.speak(f"Abandoned idea {i}: Potential value ${value:,.0f}")
            else:
                self.audio.speak("No high-value abandoned ideas found.")
        except Exception as e:
            self.audio.speak(f"Error getting abandoned ideas: {str(e)}")
    
    def _get_high_value_insights(self):
        """Get high value insights from DreamVault"""
        try:
            insights = self.dreamvault.get_high_value_insights(min_value=10000)
            if insights:
                total_value = insights.get('total_value', 0)
                total_conversations = insights.get('total_conversations', 0)
                avg_value = insights.get('avg_value', 0)
                self.audio.speak(f"High-value insights: {total_conversations} conversations with total value ${total_value:,.0f}, average ${avg_value:,.0f} per conversation.")
            else:
                self.audio.speak("No high-value insights found.")
        except Exception as e:
            self.audio.speak(f"Error getting high value insights: {str(e)}")
    
    def _analyze_topic(self, topic: str):
        """Analyze a specific topic from DreamVault"""
        try:
            insights = self.dreamvault.get_topic_insights(topic, limit=5)
            if insights:
                self.audio.speak(f"Found {len(insights)} conversations about '{topic}'. Here are the key insights:")
                for i, insight in enumerate(insights[:3], 1):
                    summary = insight['summary'][:100] + "..." if len(insight['summary']) > 100 else insight['summary']
                    self.audio.speak(f"Insight {i}: {summary}")
            else:
                self.audio.speak(f"No conversations found about '{topic}'.")
        except Exception as e:
            self.audio.speak(f"Error analyzing topic: {str(e)}")
    
    def _get_learning_recommendations(self):
        """Get learning recommendations from DreamVault"""
        try:
            recommendations = self.dreamvault.get_learning_recommendations()
            if recommendations:
                topic_patterns = recommendations.get('topic_patterns', [])
                valuable_insights = recommendations.get('valuable_insights', [])
                
                if topic_patterns:
                    self.audio.speak(f"Based on your conversation patterns, here are your most common topics:")
                    for i, pattern in enumerate(topic_patterns[:3], 1):
                        topics = pattern['topics']
                        frequency = pattern['frequency']
                        self.audio.speak(f"Topic pattern {i}: {', '.join(topics[:3])} (mentioned {frequency} times)")
                
                if valuable_insights:
                    self.audio.speak("Here are your most valuable insights:")
                    for i, insight in enumerate(valuable_insights[:2], 1):
                        value = insight['value']
                        self.audio.speak(f"Valuable insight {i}: Estimated value ${value:,.0f}")
            else:
                self.audio.speak("No learning recommendations available.")
        except Exception as e:
            self.audio.speak(f"Error getting learning recommendations: {str(e)}")
    
    def _suggest_actions(self):
        """Suggest actions based on current context and DreamVault history"""
        try:
            # Use current context to suggest actions
            current_context = " ".join([str(v) for v in self.current_context.values()])
            suggestions = self.dreamvault.suggest_actions_based_on_history(current_context)
            
            if suggestions:
                self.audio.speak(f"Based on your conversation history, here are some suggested actions:")
                for i, suggestion in enumerate(suggestions[:3], 1):
                    action = suggestion['action']
                    priority = suggestion['priority']
                    self.audio.speak(f"Suggested action {i}: {action} (priority: {priority})")
            else:
                self.audio.speak("No specific actions suggested based on your history.")
        except Exception as e:
            self.audio.speak(f"Error suggesting actions: {str(e)}")
    
    def _provide_help(self):
        """Provide help about available commands"""
        help_text = f"""
        I am {self.name}, your personal AI assistant. Here are some things I can do:
        
        Cursor Control:
        - Open Cursor
        - Close Cursor
        - Open file [filename]
        - Create file [filename]
        - Save file
        - Search for [text]
        
        Development:
        - Run tests
        - Build project
        - Install dependencies
        - Check for errors
        - Fix bugs
        - Commit changes
        - Push to git
        - Deploy application
        
        Vision:
        - What do you see
        - Analyze screen
        - Find text [text]
        - Click on [text]
        
        Workflow Management:
        - Create new project [name]
        - Create new task [name]
        - Create new workflow [name]
        - List projects/tasks/workflows
        - Get system overview
        - What are my tasks/projects/workflows
        - What is next
        - What is overdue
        
        DreamVault:
        - Search my conversations [query]
        - Show my product ideas
        - Get my workflows
        - Find my abandoned ideas
        - Get my learning recommendations
        - Suggest actions
        
        System:
        - Help
        - Change voice
        - List voices
        - Train voice recognition
        - Enable/Disable voice recognition
        - Enable/Disable vision alerts
        - Exit/Quit
        """
        
        self.audio.speak(f"I can help you control Cursor, manage your development workflow, analyze your screen, and access your DreamVault data. I can also manage projects, tasks, and workflows using my FSM organizer. Try saying 'open cursor', 'search my conversations', or 'create new project' to get started.")

def main():
    """
    Main function to start Personal Jarvis
    """
    print("🚀 Personal Jarvis - Your AI Assistant")
    print("=" * 50)
    
    # Create Personal Jarvis
    jarvis = PersonalJarvis("Jarvis")
    
    try:
        # Start Jarvis
        jarvis.start()
        
        print("🎤🎧👁️ Personal Jarvis is now active!")
        print("You can now talk to your personal AI assistant.")
        print("Try saying:")
        print("• 'Open Cursor'")
        print("• 'What do you see'")
        print("• 'Help'")
        print("• 'Exit' to quit")
        
        # Keep running
        while jarvis.is_active:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Stopping Personal Jarvis...")
    finally:
        jarvis.stop()
        print("✅ Personal Jarvis stopped.")

if __name__ == "__main__":
    main() 