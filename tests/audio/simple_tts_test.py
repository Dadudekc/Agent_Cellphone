#!/usr/bin/env python3
"""
Simple TTS Test - Direct test without threading
"""
import time
import pyttsx3

def test_direct_tts():
    """Test TTS directly without any threading"""
    print("🔊 Testing Direct TTS (No Threading)")
    
    try:
        # Create a fresh TTS engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        print("1. Speaking: 'Hello Victor, this is test one'")
        engine.say("Hello Victor, this is test one")
        engine.runAndWait()
        print("   ✅ Test one completed")
        
        # Wait a moment
        time.sleep(1)
        
        print("2. Speaking: 'This is test two'")
        engine.say("This is test two")
        engine.runAndWait()
        print("   ✅ Test two completed")
        
        # Wait a moment
        time.sleep(1)
        
        print("3. Speaking: 'This is test three'")
        engine.say("This is test three")
        engine.runAndWait()
        print("   ✅ Test three completed")
        
        # Wait a moment
        time.sleep(1)
        
        print("4. Speaking: 'This is test four'")
        engine.say("This is test four")
        engine.runAndWait()
        print("   ✅ Test four completed")
        
        print("🎧 Did you hear all 4 messages?")
        
    except Exception as e:
        print(f"❌ Direct TTS failed: {e}")

def test_multiple_engines():
    """Test with multiple TTS engines"""
    print("\n🔊 Testing Multiple TTS Engines")
    
    try:
        print("1. Creating engine 1...")
        engine1 = pyttsx3.init()
        engine1.setProperty('rate', 150)
        engine1.setProperty('volume', 0.9)
        
        print("   Speaking: 'Engine one speaking'")
        engine1.say("Engine one speaking")
        engine1.runAndWait()
        print("   ✅ Engine 1 completed")
        
        # Clean up engine 1
        engine1.stop()
        
        time.sleep(1)
        
        print("2. Creating engine 2...")
        engine2 = pyttsx3.init()
        engine2.setProperty('rate', 150)
        engine2.setProperty('volume', 0.9)
        
        print("   Speaking: 'Engine two speaking'")
        engine2.say("Engine two speaking")
        engine2.runAndWait()
        print("   ✅ Engine 2 completed")
        
        # Clean up engine 2
        engine2.stop()
        
        time.sleep(1)
        
        print("3. Creating engine 3...")
        engine3 = pyttsx3.init()
        engine3.setProperty('rate', 150)
        engine3.setProperty('volume', 0.9)
        
        print("   Speaking: 'Engine three speaking'")
        engine3.say("Engine three speaking")
        engine3.runAndWait()
        print("   ✅ Engine 3 completed")
        
        # Clean up engine 3
        engine3.stop()
        
        print("🎧 Did you hear all 3 engines?")
        
    except Exception as e:
        print(f"❌ Multiple engines failed: {e}")

if __name__ == "__main__":
    test_direct_tts()
    test_multiple_engines() 