#!/usr/bin/env python3
"""
Comprehensive TTS Test - Verify actual speech output
"""
import time
import logging
from audio_system import AudioSystem

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_comprehensive_tts():
    """Test TTS functionality with actual speech"""
    print("🎤 Comprehensive TTS Test Starting...")
    
    # Initialize audio system
    audio = AudioSystem({
        'speech_rate': 150,
        'volume': 0.9,
        'energy_threshold': 4000
    })
    
    try:
        print("1. Testing basic speech...")
        audio.speak("Hello Victor, this is Jarvis speaking.")
        time.sleep(3)
        
        print("2. Testing conversation response...")
        audio.speak("I can now speak multiple times without getting stuck.")
        time.sleep(3)
        
        print("3. Testing DreamVault integration...")
        audio.speak("I have access to your DreamVault with 398 conversations.")
        time.sleep(3)
        
        print("4. Testing command response...")
        audio.speak("You can ask me to search your conversations or show your product ideas.")
        time.sleep(3)
        
        print("5. Testing final confirmation...")
        audio.speak("TTS system is now working properly. You can speak to me!")
        time.sleep(3)
        
        print("✅ Comprehensive TTS Test completed!")
        print("🎧 Did you hear all 5 messages? If yes, TTS is working!")
        
    except Exception as e:
        print(f"❌ TTS Test failed: {e}")
    
    finally:
        # Clean up
        audio.stop_speaking()
        audio.stop_listening()

if __name__ == "__main__":
    test_comprehensive_tts() 