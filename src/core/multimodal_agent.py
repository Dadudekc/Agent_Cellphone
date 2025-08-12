#!/usr/bin/env python3
"""
Multimodal Agent - Complete AI Assistant
Combines vision, audio, and interaction capabilities for full voice-controlled development
"""

import time
import logging
import threading
from typing import Dict, List, Callable, Optional
from agent_vision_integration import VisionEnabledAgent
from audio_system import AudioSystem
import pyautogui
import re

class MultimodalAgent(VisionEnabledAgent):
    """
    Complete multimodal AI agent with vision, hearing, and voice capabilities
    Can see your screen, hear your voice, and respond with speech
    """
    
    def __init__(self, agent_id: str = "multimodal_assistant", config: Dict = None):
        super().__init__(agent_id, config)
        self.logger = logging.getLogger(f"MultimodalAgent_{agent_id}")
        
        # Initialize audio system
        audio_config = config.get('audio_config', {}) if config else {}
        self.audio = AudioSystem(audio_config)
        
        # Voice command patterns
        self.voice_commands = {
            'development': [
                r'run (?:the )?tests?',
                r'build (?:the )?project',
                r'install (?:dependencies?|packages?)',
                r'check (?:for )?errors?',
                r'fix (?:the )?bugs?',
                r'deploy (?:the )?application',
                r'commit (?:the )?changes?',
                r'push (?:to )?git'
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
                r'set (?:speech )?rate (.+)',
                r'set (?:volume )?to (.+)',
                r'what (?:can you )?do',
                r'help'
            ]
        }
        
        # Development automation commands
        self.dev_automation = {
            'run_tests': self._run_tests,
            'build_project': self._build_project,
            'install_dependencies': self._install_dependencies,
            'check_errors': self._check_errors,
            'fix_bugs': self._fix_bugs,
            'deploy_app': self._deploy_application,
            'commit_changes': self._commit_changes,
            'push_git': self._push_git
        }
        
        # Set up audio callbacks
        self.audio.add_speech_callback(self._handle_voice_command)
        
        # Agent state
        self.is_voice_enabled = True
        self.conversation_history = []
        
        self.logger.info("Multimodal agent initialized with vision and audio capabilities")
    
    def start_multimodal_session(self):
        """
        Start complete multimodal session with vision and audio
        """
        self.logger.info("Starting multimodal session")
        
        # Start vision monitoring
        self.start_vision()
        
        # Start audio listening
        self.audio.start_listening()
        
        # Welcome message
        self.audio.speak("Hello! I'm your multimodal AI assistant. I can see your screen, hear your voice, and help with your development tasks. What would you like me to do?")
        
        self.logger.info("Multimodal session started - agent can now see and hear")
    
    def stop_multimodal_session(self):
        """
        Stop multimodal session
        """
        self.logger.info("Stopping multimodal session")
        
        # Stop vision
        self.stop_vision()
        
        # Stop audio
        self.audio.stop_listening()
        self.audio.stop_speaking()
        
        self.logger.info("Multimodal session stopped")
    
    def _handle_voice_command(self, text: str):
        """
        Process voice commands and execute appropriate actions
        """
        self.logger.info(f"Processing voice command: {text}")
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user_speech',
            'text': text,
            'timestamp': time.time()
        })
        
        # Check for development commands
        if self._is_development_command(text):
            self._execute_development_command(text)
            return
        
        # Check for vision commands
        if self._is_vision_command(text):
            self._execute_vision_command(text)
            return
        
        # Check for system commands
        if self._is_system_command(text):
            self._execute_system_command(text)
            return
        
        # Default response
        self.audio.speak("I heard your command but I'm not sure how to handle it. Try saying 'help' to see what I can do.")
    
    def _is_development_command(self, text: str) -> bool:
        """
        Check if text contains development-related commands
        """
        text_lower = text.lower()
        for pattern in self.voice_commands['development']:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def _is_vision_command(self, text: str) -> bool:
        """
        Check if text contains vision-related commands
        """
        text_lower = text.lower()
        for pattern in self.voice_commands['vision']:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def _is_system_command(self, text: str) -> bool:
        """
        Check if text contains system-related commands
        """
        text_lower = text.lower()
        for pattern in self.voice_commands['system']:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def _execute_development_command(self, text: str):
        """
        Execute development-related voice commands
        """
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
        elif re.search(r'deploy (?:the )?application', text_lower):
            self._deploy_application()
        elif re.search(r'commit (?:the )?changes?', text_lower):
            self._commit_changes()
        elif re.search(r'push (?:to )?git', text_lower):
            self._push_git()
    
    def _execute_vision_command(self, text: str):
        """
        Execute vision-related voice commands
        """
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
        elif re.search(r'look (?:for )?(.+)', text_lower):
            match = re.search(r'look (?:for )?(.+)', text_lower)
            if match:
                search_text = match.group(1)
                self._look_for_text(search_text)
    
    def _execute_system_command(self, text: str):
        """
        Execute system-related voice commands
        """
        text_lower = text.lower()
        
        if re.search(r'stop (?:listening|speaking)', text_lower):
            if 'listening' in text_lower:
                self.audio.stop_listening()
                self.audio.speak("I've stopped listening for voice commands.")
            else:
                self.audio.stop_speaking()
                self.audio.speak("I've stopped speaking.")
        elif re.search(r'start (?:listening|speaking)', text_lower):
            if 'listening' in text_lower:
                self.audio.start_listening()
                self.audio.speak("I'm now listening for voice commands.")
            else:
                self.audio.speak("I'm ready to speak.")
        elif re.search(r'change (?:your )?voice', text_lower):
            self._change_voice()
        elif re.search(r'set (?:speech )?rate (.+)', text_lower):
            match = re.search(r'set (?:speech )?rate (.+)', text_lower)
            if match:
                rate_text = match.group(1)
                self._set_speech_rate(rate_text)
        elif re.search(r'set (?:volume )?to (.+)', text_lower):
            match = re.search(r'set (?:volume )?to (.+)', text_lower)
            if match:
                volume_text = match.group(1)
                self._set_volume(volume_text)
        elif re.search(r'what (?:can you )?do', text_lower) or re.search(r'help', text_lower):
            self._provide_help()
    
    def _run_tests(self):
        """
        Run tests based on current project
        """
        self.audio.speak("Running tests for your project.")
        
        # Get current vision data to understand project type
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '').lower()
        
        if 'python' in text_content or '.py' in text_content:
            # Python project
            pyautogui.hotkey('ctrl', 'shift', '`')  # Open terminal
            time.sleep(1)
            pyautogui.write('python -m pytest')
            pyautogui.press('enter')
            self.audio.speak("Running Python tests with pytest.")
        elif 'npm' in text_content or 'package.json' in text_content:
            # Node.js project
            pyautogui.hotkey('ctrl', 'shift', '`')
            time.sleep(1)
            pyautogui.write('npm test')
            pyautogui.press('enter')
            self.audio.speak("Running Node.js tests.")
        else:
            self.audio.speak("I can see your project but I'm not sure what type of tests to run. Please specify the testing framework.")
    
    def _build_project(self):
        """
        Build the current project
        """
        self.audio.speak("Building your project.")
        
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '').lower()
        
        if 'package.json' in text_content:
            pyautogui.hotkey('ctrl', 'shift', '`')
            time.sleep(1)
            pyautogui.write('npm run build')
            pyautogui.press('enter')
            self.audio.speak("Building Node.js project.")
        elif 'requirements.txt' in text_content:
            pyautogui.hotkey('ctrl', 'shift', '`')
            time.sleep(1)
            pyautogui.write('python setup.py build')
            pyautogui.press('enter')
            self.audio.speak("Building Python project.")
        else:
            self.audio.speak("I can see your project but I'm not sure how to build it. Please specify the build command.")
    
    def _install_dependencies(self):
        """
        Install project dependencies
        """
        self.audio.speak("Installing dependencies.")
        
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '').lower()
        
        if 'requirements.txt' in text_content:
            pyautogui.hotkey('ctrl', 'shift', '`')
            time.sleep(1)
            pyautogui.write('pip install -r requirements.txt')
            pyautogui.press('enter')
            self.audio.speak("Installing Python dependencies.")
        elif 'package.json' in text_content:
            pyautogui.hotkey('ctrl', 'shift', '`')
            time.sleep(1)
            pyautogui.write('npm install')
            pyautogui.press('enter')
            self.audio.speak("Installing Node.js dependencies.")
        else:
            self.audio.speak("I can see your project but I'm not sure what dependencies to install.")
    
    def _check_errors(self):
        """
        Check for errors in the current view
        """
        self.audio.speak("Checking for errors.")
        
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '')
        
        # Look for common error patterns
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
        """
        Attempt to fix common bugs
        """
        self.audio.speak("Attempting to fix bugs.")
        
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '')
        
        # Look for common issues and suggest fixes
        if 'import error' in text_content.lower():
            self.audio.speak("I see an import error. Let me try to install the missing package.")
            self._install_dependencies()
        elif 'syntax error' in text_content.lower():
            self.audio.speak("I see a syntax error. Please check the highlighted line in your editor.")
        else:
            self.audio.speak("I don't see any obvious bugs that I can automatically fix.")
    
    def _deploy_application(self):
        """
        Deploy the application
        """
        self.audio.speak("Deploying your application.")
        
        # This would depend on the deployment platform
        self.audio.speak("Please specify your deployment platform or I can help you set up automated deployment.")
    
    def _commit_changes(self):
        """
        Commit changes to git
        """
        self.audio.speak("Committing your changes to git.")
        
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('git add .')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write('git commit -m "Auto-commit from voice command"')
        pyautogui.press('enter')
        self.audio.speak("Changes committed successfully.")
    
    def _push_git(self):
        """
        Push changes to git
        """
        self.audio.speak("Pushing changes to git.")
        
        pyautogui.hotkey('ctrl', 'shift', '`')
        time.sleep(1)
        pyautogui.write('git push')
        pyautogui.press('enter')
        self.audio.speak("Changes pushed to remote repository.")
    
    def _describe_what_i_see(self):
        """
        Describe what the agent sees on screen
        """
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '')
        
        if text_content:
            # Summarize what's visible
            summary = text_content[:200] + "..." if len(text_content) > 200 else text_content
            self.audio.speak(f"I can see: {summary}")
        else:
            self.audio.speak("I can see your screen but I'm not detecting any text content.")
    
    def _analyze_screen(self):
        """
        Analyze the current screen content
        """
        vision_data = self.get_vision_data()
        text_content = vision_data.get('text_content', '')
        ui_elements = vision_data.get('ui_elements', [])
        text_regions = vision_data.get('text_regions', [])
        
        self.audio.speak(f"I can see {len(text_regions)} text elements and {len(ui_elements)} UI elements on your screen.")
        
        if text_content:
            # Look for specific content types
            if 'error' in text_content.lower():
                self.audio.speak("I notice there are error messages visible.")
            if 'test' in text_content.lower():
                self.audio.speak("I can see test-related content.")
            if 'build' in text_content.lower():
                self.audio.speak("I can see build-related information.")
    
    def _find_text_on_screen(self, search_text: str):
        """
        Find specific text on screen
        """
        matches = self.vision_integration.find_text_on_screen(search_text)
        
        if matches:
            self.audio.speak(f"I found {len(matches)} instances of '{search_text}' on your screen.")
        else:
            self.audio.speak(f"I couldn't find '{search_text}' on your screen.")
    
    def _click_on_text(self, text: str):
        """
        Click on specific text
        """
        success = self.vision_integration.click_on_text(text)
        
        if success:
            self.audio.speak(f"I clicked on '{text}'.")
        else:
            self.audio.speak(f"I couldn't find '{text}' to click on.")
    
    def _look_for_text(self, text: str):
        """
        Look for text and describe what's found
        """
        matches = self.vision_integration.find_text_on_screen(text)
        
        if matches:
            self.audio.speak(f"I found '{text}' in {len(matches)} locations on your screen.")
        else:
            self.audio.speak(f"I don't see '{text}' anywhere on your screen.")
    
    def _change_voice(self):
        """
        Change the TTS voice
        """
        voices = self.audio.get_available_voices()
        
        if len(voices) > 1:
            # Switch to next voice
            current_voice = self.audio.tts_engine.getProperty('voice')
            current_index = 0
            
            for i, voice in enumerate(voices):
                if voice['id'] == current_voice:
                    current_index = i
                    break
            
            next_index = (current_index + 1) % len(voices)
            new_voice = voices[next_index]
            
            self.audio.change_voice(new_voice['id'])
            self.audio.speak(f"I've changed my voice to {new_voice['name']}.")
        else:
            self.audio.speak("I only have one voice available.")
    
    def _set_speech_rate(self, rate_text: str):
        """
        Set speech rate based on voice command
        """
        try:
            # Parse rate from text
            if 'slow' in rate_text:
                rate = 100
            elif 'fast' in rate_text:
                rate = 200
            elif 'normal' in rate_text:
                rate = 150
            else:
                # Try to extract number
                import re
                numbers = re.findall(r'\d+', rate_text)
                if numbers:
                    rate = int(numbers[0])
                else:
                    rate = 150
            
            self.audio.set_speech_rate(rate)
            self.audio.speak(f"I've set my speech rate to {rate} words per minute.")
        except:
            self.audio.speak("I couldn't understand the speech rate you specified. Try saying 'slow', 'normal', or 'fast'.")
    
    def _set_volume(self, volume_text: str):
        """
        Set volume based on voice command
        """
        try:
            if 'mute' in volume_text or 'off' in volume_text:
                volume = 0.0
            elif 'low' in volume_text:
                volume = 0.3
            elif 'high' in volume_text or 'loud' in volume_text:
                volume = 1.0
            elif 'normal' in volume_text:
                volume = 0.7
            else:
                # Try to extract percentage
                import re
                numbers = re.findall(r'\d+', volume_text)
                if numbers:
                    volume = min(100, int(numbers[0])) / 100.0
                else:
                    volume = 0.7
            
            self.audio.set_volume(volume)
            self.audio.speak(f"I've set my volume to {int(volume * 100)} percent.")
        except:
            self.audio.speak("I couldn't understand the volume level you specified. Try saying 'mute', 'low', 'normal', or 'high'.")
    
    def _provide_help(self):
        """
        Provide help about available commands
        """
        help_text = """
        I can help you with many tasks. Here are some things you can say:
        
        Development commands:
        - Run tests
        - Build project
        - Install dependencies
        - Check for errors
        - Fix bugs
        - Deploy application
        - Commit changes
        - Push to git
        
        Vision commands:
        - What do you see
        - Analyze screen
        - Find text [text to find]
        - Click on [text]
        - Look for [text]
        
        System commands:
        - Stop listening
        - Start listening
        - Change voice
        - Set speech rate [slow/normal/fast]
        - Set volume to [low/normal/high]
        - Help
        """
        
        self.audio.speak("I can help you with development tasks, screen analysis, and system controls. Try saying 'run tests' or 'what do you see' to get started.")

# Example usage
if __name__ == "__main__":
    # Create multimodal agent
    config = {
        'audio_config': {
            'speech_rate': 150,
            'volume': 0.9,
            'energy_threshold': 4000
        }
    }
    
    agent = MultimodalAgent("assistant", config)
    
    # Start multimodal session
    agent.start_multimodal_session()
    
    try:
        print("🎤🎧👁️ Multimodal agent is running!")
        print("Say 'help' to see available commands")
        print("Say 'stop listening' to exit")
        
        # Keep running
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nStopping multimodal agent...")
    finally:
        agent.stop_multimodal_session() 