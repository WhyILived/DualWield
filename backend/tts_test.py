#!/usr/bin/env python3
"""
Simple test script for TTS functionality
"""

from tts_client import speak, stop, is_speaking
import time

def test_tts():
    """Test the TTS functionality"""
    print("🎤 Testing TTS functionality...")
    
    # Test 1: Basic speech
    print("\n📝 Test 1: Basic speech")
    success = speak("Hello! I am your AI teaching assistant. I'm here to help you learn while you game.")
    print(f"✅ Speech test result: {success}")
    
    # Wait for speech to finish
    while is_speaking():
        time.sleep(0.1)
    
    # Test 2: Stop functionality
    print("\n📝 Test 2: Stop functionality")
    speak("This speech will be interrupted.")
    time.sleep(1)  # Let it start speaking
    stop_result = stop()
    print(f"✅ Stop test result: {stop_result}")
    
    # Test 3: Short message
    print("\n📝 Test 3: Short message")
    success = speak("TTS is working correctly!")
    print(f"✅ Short message test result: {success}")
    
    print("\n🎉 TTS testing completed!")

if __name__ == "__main__":
    test_tts() 