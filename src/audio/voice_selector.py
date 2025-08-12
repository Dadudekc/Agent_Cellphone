#!/usr/bin/env python3
"""
Voice Selector - List and select available TTS voices
"""
import pyttsx3
import logging

def list_available_voices():
    """List all available TTS voices"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print("🎤 Available Voices:")
        print("=" * 50)
        
        for i, voice in enumerate(voices):
            print(f"{i+1}. {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   Languages: {voice.languages}")
            print(f"   Gender: {voice.gender}")
            print(f"   Age: {voice.age}")
            print("-" * 30)
        
        return voices
        
    except Exception as e:
        print(f"❌ Error listing voices: {e}")
        return []

def test_voice(voice_index=None):
    """Test a specific voice"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if voice_index is not None and 0 <= voice_index < len(voices):
            engine.setProperty('voice', voices[voice_index].id)
            print(f"🎤 Testing voice: {voices[voice_index].name}")
        else:
            print("🎤 Testing default voice")
        
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        engine.say("Hello Victor, this is a voice test. How do I sound?")
        engine.runAndWait()
        
        print("✅ Voice test completed!")
        
    except Exception as e:
        print(f"❌ Voice test failed: {e}")

def set_voice_preference(voice_index):
    """Set voice preference for Jarvis"""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if 0 <= voice_index < len(voices):
            selected_voice = voices[voice_index]
            print(f"✅ Voice set to: {selected_voice.name}")
            
            # Save to config
            config = {
                'voice_id': selected_voice.id,
                'voice_name': selected_voice.name,
                'voice_index': voice_index
            }
            
            import json
            with open('voice_config.json', 'w') as f:
                json.dump(config, f)
            
            print(f"💾 Voice preference saved to voice_config.json")
            return config
        else:
            print(f"❌ Invalid voice index: {voice_index}")
            return None
            
    except Exception as e:
        print(f"❌ Error setting voice: {e}")
        return None

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🎤 Voice Selector for Jarvis")
    print("=" * 40)
    
    # List available voices
    voices = list_available_voices()
    
    if voices:
        print(f"\n📊 Found {len(voices)} voices")
        
        # Test current voice
        print("\n🎧 Testing current voice...")
        test_voice()
        
        # Ask user to select
        try:
            choice = input(f"\nSelect voice (1-{len(voices)}) or press Enter for default: ")
            if choice.strip():
                voice_index = int(choice) - 1
                if 0 <= voice_index < len(voices):
                    print(f"\n🎧 Testing selected voice...")
                    test_voice(voice_index)
                    
                    confirm = input("Use this voice? (y/n): ")
                    if confirm.lower() == 'y':
                        set_voice_preference(voice_index)
                        print("✅ Voice preference updated! Restart Jarvis to apply changes.")
                    else:
                        print("❌ Voice selection cancelled.")
                else:
                    print("❌ Invalid selection.")
            else:
                print("✅ Using default voice.")
        except ValueError:
            print("❌ Invalid input.")
        except KeyboardInterrupt:
            print("\n👋 Voice selection cancelled.")
    else:
        print("❌ No voices found.") 