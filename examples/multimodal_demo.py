#!/usr/bin/env python3
"""
Multimodal Agent Demo
Demonstrates complete AI assistant with vision, hearing, and voice capabilities
"""

import time
import logging
from multimodal_agent import MultimodalAgent

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

def demo_voice_controlled_development():
    """
    Demo voice-controlled development automation
    """
    print("🎤🎧👁️ Voice-Controlled Development Demo")
    print("=" * 50)
    
    # Create multimodal agent
    config = {
        'audio_config': {
            'speech_rate': 150,
            'volume': 0.9,
            'energy_threshold': 4000
        }
    }
    
    agent = MultimodalAgent("dev_assistant", config)
    
    print("🤖 Multimodal AI Assistant activated!")
    print("The agent can now see your screen and hear your voice commands")
    
    # Start multimodal session
    agent.start_multimodal_session()
    
    try:
        print("\n🎯 Available voice commands:")
        print("Development:")
        print("• 'Run tests' - Execute project tests")
        print("• 'Build project' - Build the current project")
        print("• 'Install dependencies' - Install project packages")
        print("• 'Check for errors' - Look for errors on screen")
        print("• 'Fix bugs' - Attempt to fix detected issues")
        print("• 'Commit changes' - Commit to git")
        print("• 'Push to git' - Push changes to remote")
        
        print("\nVision:")
        print("• 'What do you see' - Describe screen content")
        print("• 'Analyze screen' - Detailed screen analysis")
        print("• 'Find text [text]' - Search for specific text")
        print("• 'Click on [text]' - Click on specific text")
        print("• 'Look for [text]' - Search and describe findings")
        
        print("\nSystem:")
        print("• 'Help' - Show available commands")
        print("• 'Change voice' - Switch TTS voice")
        print("• 'Set speech rate [slow/normal/fast]' - Adjust speaking speed")
        print("• 'Set volume to [low/normal/high]' - Adjust volume")
        print("• 'Stop listening' - Exit the demo")
        
        print("\n💡 Try saying:")
        print("• 'What do you see'")
        print("• 'Run tests'")
        print("• 'Check for errors'")
        print("• 'Help'")
        
        print("\n🎧 Listening for voice commands...")
        print("(The agent will respond to your voice commands)")
        
        # Keep running until user says "stop listening"
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    finally:
        agent.stop_multimodal_session()
        print("✅ Multimodal session ended")

def demo_audio_capabilities():
    """
    Demo audio system capabilities
    """
    print("\n🎤 Audio System Demo")
    print("=" * 30)
    
    from audio_system import AudioSystem
    
    # Create audio system
    audio = AudioSystem({
        'speech_rate': 150,
        'volume': 0.9
    })
    
    print("🎧 Testing audio capabilities...")
    
    # Test TTS
    print("🔊 Testing text-to-speech...")
    audio.speak("Hello! This is a test of the text-to-speech system.")
    
    # Show available voices
    voices = audio.get_available_voices()
    print(f"🎭 Available voices: {len(voices)}")
    for voice in voices:
        print(f"  • {voice['name']} ({voice['gender']})")
    
    # Test speech recognition
    print("\n🎤 Testing speech recognition...")
    print("Say something when prompted...")
    
    def on_speech(text):
        print(f"🎧 Heard: {text}")
        audio.speak(f"You said: {text}")
    
    audio.add_speech_callback(on_speech)
    audio.start_listening()
    
    try:
        time.sleep(10)  # Listen for 10 seconds
    finally:
        audio.stop_listening()
        audio.stop_speaking()

def demo_vision_audio_integration():
    """
    Demo integration between vision and audio systems
    """
    print("\n👁️🎧 Vision-Audio Integration Demo")
    print("=" * 40)
    
    from agent_vision_integration import VisionEnabledAgent
    from audio_system import AudioSystem
    
    # Create vision-enabled agent
    vision_agent = VisionEnabledAgent("integration_test")
    
    # Create audio system
    audio = AudioSystem()
    
    def vision_callback(vision_data):
        """Handle vision updates with audio feedback"""
        text_content = vision_data.get('text_content', '')
        
        if text_content:
            # Look for important events
            if 'error' in text_content.lower():
                audio.speak("I detected an error on your screen.")
            elif 'test' in text_content.lower():
                audio.speak("I can see test-related content.")
            elif 'build' in text_content.lower():
                audio.speak("I can see build information.")
    
    def speech_callback(text):
        """Handle speech commands for vision tasks"""
        if 'what do you see' in text.lower():
            vision_data = vision_agent.get_vision_data()
            text_content = vision_data.get('text_content', '')
            
            if text_content:
                summary = text_content[:100] + "..." if len(text_content) > 100 else text_content
                audio.speak(f"I can see: {summary}")
            else:
                audio.speak("I can see your screen but no text content is detected.")
        
        elif 'analyze screen' in text.lower():
            vision_data = vision_agent.get_vision_data()
            ui_elements = vision_data.get('ui_elements', [])
            text_regions = vision_data.get('text_regions', [])
            
            audio.speak(f"I can see {len(text_regions)} text elements and {len(ui_elements)} UI elements.")
    
    # Set up callbacks
    vision_agent.vision_integration.add_vision_callback(vision_callback)
    audio.add_speech_callback(speech_callback)
    
    # Start both systems
    vision_agent.start_vision()
    audio.start_listening()
    
    print("🔗 Vision and audio systems are now integrated!")
    print("The agent can see your screen and respond to voice commands.")
    print("Try saying 'What do you see' or 'Analyze screen'")
    
    try:
        time.sleep(30)  # Run for 30 seconds
    finally:
        vision_agent.stop_vision()
        audio.stop_listening()
        audio.stop_speaking()

def main():
    """
    Run all multimodal demos
    """
    print("🚀 Complete Multimodal AI Assistant Demo")
    print("=" * 60)
    
    try:
        # Run demos
        demo_audio_capabilities()
        demo_vision_audio_integration()
        demo_voice_controlled_development()
        
        print("\n🎉 All demos completed!")
        print("\n💡 You now have a complete AI assistant with:")
        print("👁️ Vision - Can see your screen and understand content")
        print("🎧 Hearing - Can listen to your voice commands")
        print("🎤 Voice - Can speak responses and feedback")
        print("🖱️ Hands - Can interact with your computer")
        print("🧠 Intelligence - Can understand and execute complex tasks")
        
    except KeyboardInterrupt:
        print("\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")

if __name__ == "__main__":
    main() 