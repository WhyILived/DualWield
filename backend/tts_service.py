import os
import tempfile
import subprocess
import platform
import threading
import time
import requests
import io
from pathlib import Path
from dotenv import load_dotenv

# Try to import pygame for direct audio playback
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Pygame not available, falling back to system player")

# Load environment variables from root directory
import os
from pathlib import Path

# Get the project root directory (two levels up from backend)
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
print(f"🔍 Loading .env from: {env_path}")
print(f"📁 File exists: {env_path.exists()}")

# Load the .env file
load_dotenv(env_path)

# Debug: Check what environment variables are loaded
print(f"🔑 Environment variables after loading:")
for key, value in os.environ.items():
    if 'API_KEY' in key:
        print(f"  {key}: {value[:10]}..." if value else f"  {key}: None")

class TTSService:
    def __init__(self):
        self.api_key = os.getenv('ELEVEN_LABS_API_KEY')
        self.is_speaking = False
        self.current_audio_file = None
        
        # Voice settings for AI Teaching Bot
        self.voice_id = 'ErXwobaYiN019PkySvjV'  # Antoni - good for teaching
        self.base_url = 'https://api.elevenlabs.io/v1'
        
        # Initialize pygame if available
        if PYGAME_AVAILABLE:
            pygame.mixer.init()
        
        if not self.api_key:
            print(f"Warning: ELEVEN_LABS_API_KEY not found in environment variables")
            print(f"Looking for .env file at: {env_path}")
            print(f"File exists: {env_path.exists()}")
            if env_path.exists():
                print(f"File contents: {env_path.read_text()[:100]}...")
        else:
            print(f"✅ Found ELEVEN_LABS_API_KEY: {self.api_key[:10]}...")
    
    def initialize(self):
        """Initialize the TTS service"""
        try:
            print("🎤 TTS Service initialized successfully")
            if PYGAME_AVAILABLE:
                print("🔊 Using pygame for direct audio playback")
            else:
                print("🔊 Using system media player")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize TTS service: {e}")
            return False
    
    def speak(self, text: str) -> bool:
        """
        Speak text using TTS
        
        Args:
            text (str): Text to speak
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not text or not text.strip():
            print("❌ No text provided for TTS")
            return False
        
        if not self.api_key:
            print("❌ Eleven Labs API key not configured")
            return False
        
        try:
            # Stop any current speech
            if self.is_speaking:
                self.stop()
            
            self.is_speaking = True
            
            print(f"🎤 Generating speech for: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            # Prepare the request
            url = f"{self.base_url}/text-to-speech/{self.voice_id}"
            headers = {
                'xi-api-key': self.api_key,
                'Content-Type': 'application/json'
            }
            data = {
                'text': text,
                'model_id': 'eleven_monolingual_v1',
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.75,
                    'style': 0.0,
                    'use_speaker_boost': True
                }
            }
            
            # Make the API request
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            
            # Play audio directly
            if PYGAME_AVAILABLE:
                self._play_audio_pygame(response.content)
            else:
                self._play_audio_system(response.content)
            
            return True
            
        except Exception as e:
            print(f"❌ Error in TTS speak: {e}")
            self.is_speaking = False
            return False
    
    def _play_audio_pygame(self, audio_data: bytes):
        """Play audio directly using pygame"""
        try:
            # Create a file-like object from the audio data
            audio_stream = io.BytesIO(audio_data)
            
            # Load and play the audio
            pygame.mixer.music.load(audio_stream)
            pygame.mixer.music.play()
            
            print("🔊 Playing audio with pygame...")
            
            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            self.is_speaking = False
            print("✅ Audio playback completed")
            
        except Exception as e:
            print(f"❌ Error playing audio with pygame: {e}")
            self.is_speaking = False
    
    def _play_audio_system(self, audio_data: bytes):
        """Play audio using system player (fallback)"""
        try:
            # Save to temporary file
            temp_dir = Path(tempfile.gettempdir()) / "ht6ix-tts"
            temp_dir.mkdir(exist_ok=True)
            
            audio_file = temp_dir / "speech.mp3"
            
            # Save the audio
            with open(audio_file, 'wb') as f:
                f.write(audio_data)
            
            self.current_audio_file = audio_file
            
            # Play the audio
            system = platform.system().lower()
            
            if system == "windows":
                subprocess.Popen(['start', '', str(audio_file)], shell=True)
            elif system == "darwin":  # macOS
                subprocess.Popen(['afplay', str(audio_file)])
            elif system == "linux":
                subprocess.Popen(['xdg-open', str(audio_file)])
            else:
                print(f"❌ Unsupported operating system: {system}")
                return
            
            print(f"🔊 Playing audio: {audio_file}")
            
            # Clean up file after a delay
            def cleanup():
                time.sleep(10)  # Wait 10 seconds
                try:
                    if audio_file.exists():
                        audio_file.unlink()
                        print(f"🧹 Cleaned up: {audio_file}")
                except Exception as e:
                    print(f"❌ Could not clean up audio file: {e}")
            
            cleanup_thread = threading.Thread(target=cleanup)
            cleanup_thread.daemon = True
            cleanup_thread.start()
            
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
    
    def stop(self) -> bool:
        """Stop current TTS"""
        try:
            self.is_speaking = False
            
            # Stop pygame if playing
            if PYGAME_AVAILABLE:
                pygame.mixer.music.stop()
            
            # Clean up current audio file
            if self.current_audio_file and self.current_audio_file.exists():
                try:
                    self.current_audio_file.unlink()
                    print(f"⏹️ Stopped and cleaned up: {self.current_audio_file}")
                except Exception as e:
                    print(f"❌ Could not clean up audio file: {e}")
            
            self.current_audio_file = None
            return True
            
        except Exception as e:
            print(f"❌ Error stopping TTS: {e}")
            return False
    
    def get_speaking_status(self) -> bool:
        """Check if currently speaking"""
        return self.is_speaking

# Create global instance
tts = TTSService() 