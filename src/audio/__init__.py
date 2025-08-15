"""
Audio System Module
==================
Contains all audio-related functionality including:
- Audio system management
- Voice selection
- TTS (Text-to-Speech) functionality
"""

from .audio_system import AudioSystem
from .voice_selector import VoiceSelector

__all__ = [
    'AudioSystem',
    'VoiceSelector'
]