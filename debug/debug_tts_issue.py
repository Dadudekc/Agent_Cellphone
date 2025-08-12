#!/usr/bin/env python3
"""
Debug TTS Issue - Find out why only first message is spoken
"""
import time
import logging
import threading
from audio_system import AudioSystem

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def debug_tts_issue():
    """Debug the TTS issue step by step"""
    print("🔍 Debugging TTS Issue...")
    
    # Initialize audio system
    audio = AudioSystem({
        'speech_rate': 150,
        'volume': 0.9,
        'energy_threshold': 4000
    })
    
    try:
        print("1. Testing direct TTS call...")
        print("   Speaking: 'Hello, this is test one'")
        audio.speak("Hello, this is test one")
        
        # Wait and check if thread is alive
        time.sleep(2)
        if audio.speak_thread and audio.speak_thread.is_alive():
            print("   ✅ Speaking thread is alive")
        else:
            print("   ❌ Speaking thread is dead")
        
        print("2. Testing second message...")
        print("   Speaking: 'This is test two'")
        audio.speak("This is test two")
        
        time.sleep(2)
        if audio.speak_thread and audio.speak_thread.is_alive():
            print("   ✅ Speaking thread is still alive")
        else:
            print("   ❌ Speaking thread died")
        
        print("3. Testing third message...")
        print("   Speaking: 'This is test three'")
        audio.speak("This is test three")
        
        time.sleep(2)
        if audio.speak_thread and audio.speak_thread.is_alive():
            print("   ✅ Speaking thread is still alive")
        else:
            print("   ❌ Speaking thread died")
        
        print("4. Checking queue status...")
        print(f"   Queue size: {audio.speech_queue.qsize()}")
        print(f"   Is speaking: {audio.is_speaking}")
        
        # Wait a bit more to see if anything processes
        time.sleep(5)
        print(f"   Final queue size: {audio.speech_queue.qsize()}")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
    
    finally:
        # Clean up
        audio.stop_speaking()
        audio.stop_listening()

def test_simple_tts():
    """Test TTS without threading to see if it works"""
    print("\n🧪 Testing Simple TTS...")
    
    import pyttsx3
    
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("1. Simple TTS test one...")
        engine.say("Simple test one")
        engine.runAndWait()
        print("   ✅ Simple test one completed")
        
        print("2. Simple TTS test two...")
        engine.say("Simple test two")
        engine.runAndWait()
        print("   ✅ Simple test two completed")
        
        print("3. Simple TTS test three...")
        engine.say("Simple test three")
        engine.runAndWait()
        print("   ✅ Simple test three completed")
        
    except Exception as e:
        print(f"❌ Simple TTS failed: {e}")

if __name__ == "__main__":
    debug_tts_issue()
    test_simple_tts() 