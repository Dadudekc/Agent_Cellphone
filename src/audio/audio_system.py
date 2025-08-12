import speech_recognition as sr
import pyttsx3
import threading
import time
import queue
import logging
from typing import Dict, List, Callable, Optional
import json
import os

class AudioSystem:
    """
    Audio system for AI agents to "hear" and "speak"
    Provides speech recognition and text-to-speech capabilities
    """
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        
        # Audio state
        self.is_listening = False
        self.is_speaking = False
        self.audio_queue = queue.Queue()
        self.speech_queue = queue.Queue()
        
        # Threads
        self.listen_thread = None
        self.speak_thread = None
        
        # Callbacks
        self.speech_callbacks = []
        self.audio_callbacks = []
        
        # Configure TTS
        self._configure_tts()
        
        # Configure speech recognition
        self._configure_speech_recognition()
    
    def _configure_tts(self):
        """
        Configure text-to-speech settings
        """
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Set voice (default to first available)
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            
            # Set speech rate (words per minute)
            self.tts_engine.setProperty('rate', self.config.get('speech_rate', 150))
            
            # Set volume (0.0 to 1.0)
            self.tts_engine.setProperty('volume', self.config.get('volume', 0.9))
            
            self.logger.info("TTS engine configured successfully")
            
        except Exception as e:
            self.logger.error(f"TTS configuration failed: {e}")
    
    def _configure_speech_recognition(self):
        """
        Configure speech recognition settings
        """
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
        """
        Start continuous speech recognition
        """
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
        """
        Stop speech recognition
        """
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
        self.logger.info("Stopped listening")
    
    def _listen_loop(self):
        """
        Main listening loop
        """
        while self.is_listening:
            try:
                with self.microphone as source:
                    self.logger.debug("Listening for speech...")
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
                
                # Recognize speech
                try:
                    text = self.recognizer.recognize_google(audio)
                    if text.strip():
                        self.logger.info(f"Recognized: {text}")
                        
                        # Add to queue
                        self.audio_queue.put({
                            'type': 'speech',
                            'text': text,
                            'timestamp': time.time(),
                            'confidence': 1.0  # Google doesn't provide confidence
                        })
                        
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
        """
        Convert text to speech
        """
        self.logger.info(f"Attempting to speak: '{text}'")
        
        if priority:
            # Clear queue and speak immediately
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
        
        self.speech_queue.put({
            'text': text,
            'timestamp': time.time(),
            'priority': priority
        })
        
        # Start speaking thread if not already running
        if not self.is_speaking or not self.speak_thread or not self.speak_thread.is_alive():
            self.speak_thread = threading.Thread(target=self._speak_loop, daemon=True)
            self.speak_thread.start()
    
    def _speak_loop(self):
        """
        Main speaking loop
        """
        self.is_speaking = True
        self.logger.info("Speaking loop started")
        
        while self.is_speaking or not self.speech_queue.empty():
            try:
                # Get next speech item
                speech_item = self.speech_queue.get(timeout=1)
                text = speech_item['text']
                
                self.logger.info(f"Speaking: {text}")
                
                # Speak the text with error handling
                try:
                    # Stop any current speech first
                    self.tts_engine.stop()
                    
                    # Create a new TTS engine for each speech to avoid conflicts
                    temp_engine = pyttsx3.init()
                    temp_engine.setProperty('rate', self.config.get('speech_rate', 150))
                    temp_engine.setProperty('volume', self.config.get('volume', 0.9))
                    
                    # Speak the text
                    temp_engine.say(text)
                    temp_engine.runAndWait()
                    
                    # Clean up temp engine
                    temp_engine.stop()
                    
                    self.logger.info(f"Successfully spoke: {text}")
                except Exception as tts_error:
                    self.logger.error(f"TTS engine error: {tts_error}")
                    # Try to reinitialize main TTS engine
                    try:
                        self.tts_engine = pyttsx3.init()
                        self._configure_tts()
                        self.logger.info("TTS engine reinitialized")
                    except Exception as reinit_error:
                        self.logger.error(f"Failed to reinitialize TTS: {reinit_error}")
                
                # Trigger callbacks
                for callback in self.audio_callbacks:
                    try:
                        callback({'type': 'speech_output', 'text': text})
                    except Exception as e:
                        self.logger.error(f"Audio callback error: {e}")
                
            except queue.Empty:
                # If queue is empty, check if we should continue
                if not self.is_speaking:
                    break
                continue
            except Exception as e:
                self.logger.error(f"Speaking error: {e}")
        
        self.is_speaking = False
        self.logger.info("Speaking loop ended")
    
    def stop_speaking(self):
        """
        Stop current speech and clear queue
        """
        self.tts_engine.stop()
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
            except queue.Empty:
                break
        self.logger.info("Stopped speaking")
    
    def get_audio_data(self) -> List[Dict]:
        """
        Get recent audio data
        """
        audio_data = []
        while not self.audio_queue.empty():
            try:
                audio_data.append(self.audio_queue.get_nowait())
            except queue.Empty:
                break
        return audio_data
    
    def add_speech_callback(self, callback: Callable):
        """
        Add callback for speech recognition events
        """
        self.speech_callbacks.append(callback)
    
    def add_audio_callback(self, callback: Callable):
        """
        Add callback for audio output events
        """
        self.audio_callbacks.append(callback)
    
    def change_voice(self, voice_id: str):
        """
        Change TTS voice
        """
        try:
            voices = self.tts_engine.getProperty('voices')
            for voice in voices:
                if voice_id in voice.id:
                    self.tts_engine.setProperty('voice', voice.id)
                    self.logger.info(f"Changed voice to: {voice.name}")
                    return True
            self.logger.warning(f"Voice {voice_id} not found")
            return False
        except Exception as e:
            self.logger.error(f"Failed to change voice: {e}")
            return False
    
    def set_speech_rate(self, rate: int):
        """
        Set speech rate (words per minute)
        """
        try:
            self.tts_engine.setProperty('rate', rate)
            self.logger.info(f"Speech rate set to: {rate} WPM")
        except Exception as e:
            self.logger.error(f"Failed to set speech rate: {e}")
    
    def set_volume(self, volume: float):
        """
        Set volume (0.0 to 1.0)
        """
        try:
            volume = max(0.0, min(1.0, volume))
            self.tts_engine.setProperty('volume', volume)
            self.logger.info(f"Volume set to: {volume}")
        except Exception as e:
            self.logger.error(f"Failed to set volume: {e}")
    
    def get_available_voices(self) -> List[Dict]:
        """
        Get list of available TTS voices
        """
        try:
            voices = self.tts_engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': voice.gender
                }
                for voice in voices
            ]
        except Exception as e:
            self.logger.error(f"Failed to get voices: {e}")
            return []
    
    def save_audio_session(self, filename: str):
        """
        Save current audio session data
        """
        session_data = {
            'timestamp': time.time(),
            'config': self.config,
            'voices': self.get_available_voices()
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(session_data, f, indent=2)
            self.logger.info(f"Audio session saved to {filename}")
        except Exception as e:
            self.logger.error(f"Failed to save audio session: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize audio system
    audio_config = {
        'speech_rate': 150,
        'volume': 0.9,
        'energy_threshold': 4000,
        'pause_threshold': 0.8
    }
    
    audio = AudioSystem(audio_config)
    
    def on_speech(text):
        print(f"🎤 Heard: {text}")
        
        # Simple echo response
        if "hello" in text.lower():
            audio.speak("Hello! How can I help you?")
        elif "time" in text.lower():
            audio.speak(f"The current time is {time.strftime('%H:%M')}")
        elif "stop" in text.lower():
            audio.speak("Goodbye!")
            audio.stop_listening()
    
    # Add speech callback
    audio.add_speech_callback(on_speech)
    
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
        audio.stop_speaking() 