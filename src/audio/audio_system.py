import pyttsx3
import logging
from typing import Dict, Callable, List


class AudioSystem:
    """Audio system that provides text-to-speech capabilities."""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.tts_engine = pyttsx3.init()
        self.speech_callbacks: List[Callable[[str], None]] = []
        self._configure_tts()

    def _configure_tts(self):
        """Configure text-to-speech settings."""
        try:
            voices = self.tts_engine.getProperty("voices")
            if voices:
                self.tts_engine.setProperty("voice", voices[0].id)
            self.tts_engine.setProperty("rate", self.config.get("speech_rate", 150))
            self.tts_engine.setProperty("volume", self.config.get("volume", 0.9))
            self.logger.info("TTS engine configured successfully")
        except Exception as e:
            self.logger.error(f"TTS configuration failed: {e}")

    # --- Speech recognition stubs ---
    def add_speech_callback(self, callback: Callable[[str], None]):
        """Register a speech callback (no-op)."""
        self.speech_callbacks.append(callback)

    def start_listening(self, callback: Callable[[str], None] = None):
        """Start speech recognition (not implemented)."""
        if callback:
            self.add_speech_callback(callback)
        self.logger.warning("Speech recognition is not available in this build.")

    def stop_listening(self):
        """Stop speech recognition (not implemented)."""
        self.logger.warning("Speech recognition is not available in this build.")

    # --- Text-to-speech ---
    def speak(self, text: str, priority: bool = False):
        """Convert text to speech."""
        self.logger.info(f"Speaking: {text}")
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            self.logger.error(f"TTS error: {e}")

    def stop_speaking(self):
        """Stop any ongoing speech."""
        try:
            self.tts_engine.stop()
        except Exception as e:
            self.logger.error(f"TTS stop error: {e}")

