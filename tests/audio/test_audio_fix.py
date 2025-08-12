#!/usr/bin/env python3
"""
Test Audio Fix - Verify TTS is working properly
"""
import time
import logging
from audio_system import AudioSystem

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_audio_system():
    """Test the audio system with simple messages"""
    print("Testing Audio System...")
    
    audio = AudioSystem({
        'speech_rate': 150,
        'volume': 0.8,
        'voice_id': 0
    })
    
    test_messages = [
        "Hello, this is a test message.",
        "Can you hear me speaking?",
        "The audio system should be working now.",
        "This is the final test message."
    ]
    
    for i, message in enumerate(test_messages, 1):
        print(f"Test {i}: Speaking '{message}'")
        audio.speak(message)
        time.sleep(2)  # Wait between messages
    
    print("Audio test completed!")
    audio.stop_speaking()

if __name__ == "__main__":
    test_audio_system() 