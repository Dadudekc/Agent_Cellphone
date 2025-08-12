#!/usr/bin/env python3
"""
Test TTS Fix - Debug the speaking issue
"""
import time
import logging
from audio_system import AudioSystem

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_tts():
    """Test TTS functionality"""
    print("Testing TTS System...")
    
    # Initialize audio system
    audio = AudioSystem({
        'speech_rate': 150,
        'volume': 0.9,
        'energy_threshold': 4000
    })
    
    try:
        print("1. Testing first speech...")
        audio.speak("Hello, this is test number one.")
        time.sleep(2)
        
        print("2. Testing second speech...")
        audio.speak("This is test number two.")
        time.sleep(2)
        
        print("3. Testing third speech...")
        audio.speak("And this is test number three.")
        time.sleep(2)
        
        print("4. Testing conversation response...")
        audio.speak("I can speak multiple times without getting stuck.")
        time.sleep(2)
        
        print("5. Testing final message...")
        audio.speak("TTS test completed successfully!")
        time.sleep(2)
        
        print("✅ TTS Test completed!")
        
    except Exception as e:
        print(f"❌ TTS Test failed: {e}")
    
    finally:
        # Clean up
        audio.stop_speaking()
        audio.stop_listening()

if __name__ == "__main__":
    test_tts() 