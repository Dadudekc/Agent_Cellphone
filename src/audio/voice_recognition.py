#!/usr/bin/env python3
"""
Voice Recognition - Learn and recognize specific user voice
"""
import speech_recognition as sr
import numpy as np
import json
import os
import time
import logging
from typing import Dict, List, Tuple
import threading

class VoiceRecognition:
    """
    Voice recognition system that learns user's voice characteristics
    """
    
    def __init__(self, user_name: str = "Victor"):
        self.user_name = user_name
        self.logger = logging.getLogger(__name__)
        
        # Voice characteristics storage
        self.voice_profile_file = f"voice_profile_{user_name.lower()}.json"
        self.voice_profile = self._load_voice_profile()
        
        # Recognition settings
        self.confidence_threshold = 0.7
        self.min_voice_samples = 5
        self.max_voice_samples = 20
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Configure recognition
        self._configure_recognition()
    
    def _load_voice_profile(self) -> Dict:
        """Load existing voice profile"""
        if os.path.exists(self.voice_profile_file):
            try:
                with open(self.voice_profile_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                self.logger.error(f"Error loading voice profile: {e}")
        
        return {
            'user_name': self.user_name,
            'voice_samples': [],
            'voice_characteristics': {},
            'training_complete': False,
            'last_updated': None
        }
    
    def _save_voice_profile(self):
        """Save voice profile to file"""
        try:
            with open(self.voice_profile_file, 'w') as f:
                json.dump(self.voice_profile, f, indent=2)
            self.logger.info("Voice profile saved")
        except Exception as e:
            self.logger.error(f"Error saving voice profile: {e}")
    
    def _configure_recognition(self):
        """Configure speech recognition settings"""
        try:
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            
            # Set recognition parameters
            self.recognizer.energy_threshold = 3000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            self.logger.info("Voice recognition configured")
            
        except Exception as e:
            self.logger.error(f"Voice recognition configuration failed: {e}")
    
    def _extract_voice_characteristics(self, audio_data) -> Dict:
        """Extract voice characteristics from audio"""
        try:
            # Convert audio to numpy array for analysis
            audio_array = np.frombuffer(audio_data.get_raw_data(), dtype=np.int16)
            
            # Basic voice characteristics
            characteristics = {
                'duration': len(audio_array) / audio_data.sample_rate,
                'sample_rate': audio_data.sample_rate,
                'amplitude_mean': np.mean(np.abs(audio_array)),
                'amplitude_std': np.std(audio_array),
                'zero_crossings': np.sum(np.diff(np.sign(audio_array)) != 0),
                'energy': np.sum(audio_array ** 2),
                'peak_frequency': self._estimate_peak_frequency(audio_array, audio_data.sample_rate)
            }
            
            return characteristics
            
        except Exception as e:
            self.logger.error(f"Error extracting voice characteristics: {e}")
            return {}
    
    def _estimate_peak_frequency(self, audio_array, sample_rate):
        """Estimate peak frequency using FFT"""
        try:
            # Apply FFT
            fft = np.fft.fft(audio_array)
            freqs = np.fft.fftfreq(len(audio_array), 1/sample_rate)
            
            # Get positive frequencies only
            positive_freqs = freqs[:len(freqs)//2]
            positive_fft = np.abs(fft[:len(fft)//2])
            
            # Find peak frequency
            peak_idx = np.argmax(positive_fft)
            peak_freq = positive_freqs[peak_idx]
            
            return float(peak_freq)
            
        except Exception as e:
            self.logger.error(f"Error estimating peak frequency: {e}")
            return 0.0
    
    def _calculate_similarity(self, char1: Dict, char2: Dict) -> float:
        """Calculate similarity between two voice characteristics"""
        try:
            # Normalize characteristics for comparison
            features = ['amplitude_mean', 'amplitude_std', 'zero_crossings', 'energy', 'peak_frequency']
            
            similarities = []
            for feature in features:
                if feature in char1 and feature in char2:
                    val1 = char1[feature]
                    val2 = char2[feature]
                    
                    if val1 != 0 and val2 != 0:
                        # Calculate similarity (0-1 scale)
                        similarity = 1 - abs(val1 - val2) / max(abs(val1), abs(val2))
                        similarities.append(max(0, similarity))
            
            return np.mean(similarities) if similarities else 0.0
            
        except Exception as e:
            self.logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def train_voice(self, num_samples: int = 10):
        """Train the voice recognition system"""
        print(f"🎤 Voice Training for {self.user_name}")
        print("=" * 40)
        print("I'll record your voice samples to learn your voice characteristics.")
        print("Please speak clearly and naturally.")
        print()
        
        samples_collected = 0
        
        for i in range(num_samples):
            print(f"Sample {i+1}/{num_samples}")
            print("🎤 Please say something (I'll record for 3 seconds)...")
            
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Extract characteristics
                characteristics = self._extract_voice_characteristics(audio)
                
                if characteristics:
                    self.voice_profile['voice_samples'].append(characteristics)
                    samples_collected += 1
                    print(f"✅ Sample {i+1} recorded successfully")
                else:
                    print(f"❌ Sample {i+1} failed - no characteristics extracted")
                
                time.sleep(1)
                
            except sr.WaitTimeoutError:
                print(f"❌ Sample {i+1} failed - no speech detected")
            except Exception as e:
                print(f"❌ Sample {i+1} failed: {e}")
        
        # Calculate average characteristics
        if samples_collected >= self.min_voice_samples:
            self._calculate_average_characteristics()
            self.voice_profile['training_complete'] = True
            self.voice_profile['last_updated'] = time.time()
            self._save_voice_profile()
            
            print(f"\n✅ Voice training completed!")
            print(f"📊 Collected {samples_collected} voice samples")
            print(f"💾 Voice profile saved to {self.voice_profile_file}")
        else:
            print(f"\n❌ Insufficient samples collected ({samples_collected}/{self.min_voice_samples})")
            print("Please try training again.")
    
    def _calculate_average_characteristics(self):
        """Calculate average voice characteristics from samples"""
        try:
            samples = self.voice_profile['voice_samples']
            if not samples:
                return
            
            # Calculate averages for each characteristic
            avg_characteristics = {}
            features = ['amplitude_mean', 'amplitude_std', 'zero_crossings', 'energy', 'peak_frequency']
            
            for feature in features:
                values = [s.get(feature, 0) for s in samples if s.get(feature) is not None]
                if values:
                    avg_characteristics[feature] = float(np.mean(values))
                    avg_characteristics[f"{feature}_std"] = float(np.std(values))
            
            self.voice_profile['voice_characteristics'] = avg_characteristics
            
        except Exception as e:
            self.logger.error(f"Error calculating average characteristics: {e}")
    
    def recognize_voice(self, audio_data) -> Tuple[bool, float]:
        """Recognize if the voice belongs to the trained user"""
        try:
            if not self.voice_profile['training_complete']:
                return False, 0.0
            
            # Extract characteristics from current audio
            current_characteristics = self._extract_voice_characteristics(audio_data)
            
            if not current_characteristics:
                return False, 0.0
            
            # Compare with stored characteristics
            stored_characteristics = self.voice_profile['voice_characteristics']
            
            similarity = self._calculate_similarity(current_characteristics, stored_characteristics)
            
            is_match = similarity >= self.confidence_threshold
            
            self.logger.info(f"Voice recognition: {similarity:.2f} confidence, match: {is_match}")
            
            return is_match, similarity
            
        except Exception as e:
            self.logger.error(f"Error in voice recognition: {e}")
            return False, 0.0
    
    def get_voice_status(self) -> Dict:
        """Get current voice recognition status"""
        return {
            'user_name': self.user_name,
            'training_complete': self.voice_profile['training_complete'],
            'samples_collected': len(self.voice_profile['voice_samples']),
            'min_samples': self.min_voice_samples,
            'confidence_threshold': self.confidence_threshold,
            'last_updated': self.voice_profile.get('last_updated')
        }

def main():
    """Main function for voice recognition training"""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create voice recognition system
    voice_recognition = VoiceRecognition("Victor")
    
    # Show current status
    status = voice_recognition.get_voice_status()
    print("🎤 Voice Recognition Status")
    print("=" * 30)
    print(f"User: {status['user_name']}")
    print(f"Training Complete: {status['training_complete']}")
    print(f"Samples Collected: {status['samples_collected']}/{status['min_samples']}")
    print(f"Confidence Threshold: {status['confidence_threshold']}")
    
    if status['last_updated']:
        print(f"Last Updated: {time.ctime(status['last_updated'])}")
    
    print()
    
    # Ask if user wants to train
    if not status['training_complete']:
        print("❌ Voice recognition not trained yet.")
        train = input("Would you like to train voice recognition? (y/n): ")
        
        if train.lower() == 'y':
            voice_recognition.train_voice()
        else:
            print("👋 Voice training skipped.")
    else:
        print("✅ Voice recognition is trained!")
        retrain = input("Would you like to retrain? (y/n): ")
        
        if retrain.lower() == 'y':
            voice_recognition.train_voice()
        else:
            print("👋 Using existing voice profile.")

if __name__ == "__main__":
    main() 