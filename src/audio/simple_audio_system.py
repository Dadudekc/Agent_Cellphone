#!/usr/bin/env python3
"""
Simple Audio System - Working version without complex threading
"""
import speech_recognition as sr
import pyttsx3
import threading
import time
import logging
import json
import os
from typing import Dict, Callable

class SimpleAudioSystem:
    """
    Simplified audio system that actually works
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Audio state
        self.is_listening = False
        self.is_speaking = False
        
        # Callbacks
        self.speech_callbacks = []
        
        # Voice recognition
        self.voice_recognition_enabled = self.config.get('voice_recognition_enabled', False)
        self.voice_recognition = None
        if self.voice_recognition_enabled:
            try:
                from voice_recognition import VoiceRecognition
                self.voice_recognition = VoiceRecognition("Victor")
                self.logger.info("Voice recognition enabled")
            except Exception as e:
                self.logger.warning(f"Voice recognition not available: {e}")
        
        # Load voice configuration
        self._load_voice_config()
        
        # Configure TTS
        self._configure_tts()
        
        # Configure speech recognition
        self._configure_speech_recognition()
    
    def _load_voice_config(self):
        """Load voice configuration from file"""
        try:
            if os.path.exists('voice_config.json'):
                with open('voice_config.json', 'r') as f:
                    voice_config = json.load(f)
                    self.config['voice_config'] = voice_config
                    self.logger.info(f"Loaded voice config: {voice_config.get('voice_name', 'Unknown')}")
        except Exception as e:
            self.logger.warning(f"Could not load voice config: {e}")
    
    def _configure_tts(self):
        """Configure text-to-speech settings"""
        try:
            # We'll create TTS engines as needed
            self.logger.info("TTS system ready")
        except Exception as e:
            self.logger.error(f"TTS configuration failed: {e}")
    
    def _configure_speech_recognition(self):
        """Configure speech recognition settings"""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Set recognition parameters
            self.recognizer.energy_threshold = self.config.get('energy_threshold', 4000)
            self.recognizer.dynamic_energy_threshold = self.config.get('dynamic_energy_threshold', True)
            self.recognizer.pause_threshold = self.config.get('pause_threshold', 0.8)
            
            self.logger.info("Speech recognition configured successfully")
            
        except Exception as e:
            self.logger.error(f"Speech recognition configuration failed: {e}")
    
    def start_listening(self, callback: Callable = None):
        """Start continuous speech recognition"""
        if self.is_listening:
            self.logger.warning("Already listening")
            return
        
        if callback:
            self.speech_callbacks.append(callback)
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
        self.logger.info("Started listening for speech")
    
    def stop_listening(self):
        """Stop speech recognition"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        self.logger.info("Stopped listening")
    
    def _listen_loop(self):
        """Main listening loop"""
        while self.is_listening:
            try:
                with self.microphone as source:
                    self.logger.debug("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(audio)
                    if text.strip():
                        # Voice recognition check
                        voice_authorized = True
                        confidence = 0.0
                        
                        if self.voice_recognition_enabled and self.voice_recognition:
                            try:
                                voice_authorized, confidence = self.voice_recognition.recognize_voice(audio)
                                if not voice_authorized:
                                    self.logger.warning(f"Voice not authorized (confidence: {confidence:.2f})")
                                    continue
                                else:
                                    self.logger.info(f"Voice authorized (confidence: {confidence:.2f})")
                            except Exception as e:
                                self.logger.error(f"Voice recognition error: {e}")
                        
                        self.logger.info(f"Recognized: {text}")
                        
                        # Trigger callbacks
                        for callback in self.speech_callbacks:
                            try:
                                callback(text)
                            except Exception as e:
                                self.logger.error(f"Speech callback error: {e}")
                
                except sr.UnknownValueError:
                    self.logger.debug("Speech not recognized")
                except sr.RequestError as e:
                    self.logger.error(f"Speech recognition service error: {e}")
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                self.logger.error(f"Listening error: {e}")
                time.sleep(1)
    
    def speak(self, text: str, priority: bool = False):
        """Convert text to speech - SIMPLE VERSION"""
        self.logger.info(f"Speaking: {text}")
        
        try:
            # Create a fresh TTS engine for each speech
            engine = pyttsx3.init()
            engine.setProperty('rate', self.config.get('speech_rate', 150))
            engine.setProperty('volume', self.config.get('volume', 0.9))
            
            # Load voice preference if available
            voice_config = self.config.get('voice_config')
            if voice_config and 'voice_id' in voice_config:
                try:
                    engine.setProperty('voice', voice_config['voice_id'])
                    self.logger.info(f"Using voice: {voice_config.get('voice_name', 'Custom')}")
                except Exception as e:
                    self.logger.warning(f"Could not set voice: {e}")
            
            # Speak the text
            engine.say(text)
            engine.runAndWait()
            
            # Clean up
            engine.stop()
            
            self.logger.info(f"Successfully spoke: {text}")
            
        except Exception as e:
            self.logger.error(f"TTS error: {e}")
    
    def stop_speaking(self):
        """Stop current speech"""
        self.logger.info("Stopped speaking")
    
    def add_speech_callback(self, callback: Callable):
        """Add callback for speech recognition events"""
        self.speech_callbacks.append(callback)

# Test the simple audio system
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    audio = SimpleAudioSystem({
        'speech_rate': 150,
        'volume': 0.9,
        'energy_threshold': 4000
    })
    
    def on_speech(text):
        print(f"🎤 Heard: {text}")
        
        # Simple responses
        if "hello" in text.lower():
            audio.speak("Hello! How can I help you?")
        elif "test" in text.lower():
            audio.speak("This is a test response from the simple audio system.")
        elif "stop" in text.lower():
            audio.speak("Goodbye!")
            audio.stop_listening()
    
    # Add speech callback
    audio.add_speech_callback(on_speech)
    
    # Test speaking
    print("Testing simple TTS...")
    audio.speak("Hello Victor, this is the simple audio system.")
    time.sleep(2)
    audio.speak("This is test message number two.")
    time.sleep(2)
    audio.speak("And this is test message number three.")
    time.sleep(2)
    
    print("🎧 Did you hear all 3 messages? If yes, the simple system works!")
    
    # Start listening
    audio.start_listening()
    
    try:
        print("🎧 Listening for speech... (say 'stop' to exit)")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping audio system...")
    finally:
        audio.stop_listening() 