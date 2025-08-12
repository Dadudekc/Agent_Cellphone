"""
Audio System Module
==================
Contains all audio-related functionality including:
- Audio system management
- Voice recognition
- Voice selection
- TTS (Text-to-Speech) functionality
"""

from .audio_system import AudioSystem
from .simple_audio_system import SimpleAudioSystem
from .voice_recognition import VoiceRecognition
from .voice_selector import VoiceSelector

__all__ = [
    'AudioSystem',
    'SimpleAudioSystem', 
    'VoiceRecognition',
    'VoiceSelector'
] 