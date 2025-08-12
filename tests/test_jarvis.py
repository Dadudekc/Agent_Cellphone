#!/usr/bin/env python3
"""
Test Jarvis - Quick test to verify audio system and start multimodal agent
"""

import time
import logging
from audio_system import AudioSystem

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def test_audio_system():
    """
    Test the audio system components
    """
    print("🎤 Testing Audio System...")
    
    try:
        # Create audio system
        audio = AudioSystem({
            'speech_rate': 150,
            'volume': 0.9
        })
        
        print("✅ Audio system created successfully!")
        
        # Test TTS
        print("🔊 Testing text-to-speech...")
        audio.speak("Hello! I am Jarvis, your AI assistant. The audio system is working perfectly!")
        
        # Show available voices
        voices = audio.get_available_voices()
        print(f"🎭 Available voices: {len(voices)}")
        for voice in voices:
            print(f"  • {voice['name']} ({voice.get('gender', 'Unknown')})")
        
        time.sleep(2)
        
        # Test speech recognition
        print("\n🎧 Testing speech recognition...")
        print("Say something when prompted (you have 5 seconds)...")
        
        def on_speech(text):
            print(f"🎧 Heard: {text}")
            audio.speak(f"You said: {text}")
        
        audio.add_speech_callback(on_speech)
        audio.start_listening()
        
        time.sleep(5)  # Listen for 5 seconds
        
        audio.stop_listening()
        audio.stop_speaking()
        
        print("✅ Audio system test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Audio system test failed: {e}")
        return False

def start_jarvis():
    """
    Start the complete Jarvis multimodal agent
    """
    print("\n🤖 Starting Jarvis...")
    
    try:
        from multimodal_agent import MultimodalAgent
        
        # Create Jarvis
        config = {
            'audio_config': {
                'speech_rate': 150,
                'volume': 0.9,
                'energy_threshold': 4000
            }
        }
        
        jarvis = MultimodalAgent("jarvis", config)
        
        print("🎤🎧👁️ Jarvis is ready!")
        print("Starting multimodal session...")
        
        # Start Jarvis
        jarvis.start_multimodal_session()
        
        print("\n🎯 Jarvis is now active!")
        print("You can now talk to Jarvis. Try saying:")
        print("• 'What do you see'")
        print("• 'Help'")
        print("• 'Run tests'")
        print("• 'Stop listening' to exit")
        
        # Keep Jarvis running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ Stopping Jarvis...")
        finally:
            jarvis.stop_multimodal_session()
            print("✅ Jarvis stopped.")
            
    except Exception as e:
        print(f"❌ Failed to start Jarvis: {e}")

def main():
    """
    Main function to test and start Jarvis
    """
    print("🚀 Jarvis Initialization")
    print("=" * 40)
    
    # Test audio system first
    if test_audio_system():
        print("\n🎉 Audio system is working! Starting Jarvis...")
        start_jarvis()
    else:
        print("\n❌ Audio system test failed. Please check your microphone and speakers.")

if __name__ == "__main__":
    main() 