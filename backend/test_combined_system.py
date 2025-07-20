#!/usr/bin/env python3
"""
Test script for the combined server system
Tests buffer, log, and teaching functionality
"""

import requests
import json
import time

def test_combined_system():
    """Test the combined server system functionality"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Combined Server System")
    print("=" * 50)
    
    # Test 1: Check initial status
    print("\n1. Checking initial status...")
    try:
        # Buffer status
        response = requests.get(f"{base_url}/buffer_status")
        buffer_result = response.json()
        print(f"   Buffer empty: {buffer_result['buffer_empty']}")
        
        # Log status
        response = requests.get(f"{base_url}/log_status")
        log_result = response.json()
        print(f"   Log empty: {log_result['log_empty']}")
        
        # Teaching status
        response = requests.get(f"{base_url}/teaching_status")
        teaching_result = response.json()
        print(f"   Teaching active: {teaching_result['active']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Add content to buffer
    print("\n2. Adding content to buffer...")
    try:
        test_youtube_data = {
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        }
        response = requests.post(f"{base_url}/log", json=test_youtube_data)
        result = response.json()
        print(f"   Response: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check buffer status after content
    print("\n3. Checking buffer status after content...")
    try:
        response = requests.get(f"{base_url}/buffer_status")
        result = response.json()
        print(f"   Buffer empty: {result['buffer_empty']}")
        print(f"   Buffer content length: {len(result['buffer_content'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Commit buffer to log
    print("\n4. Committing buffer to log...")
    try:
        response = requests.post(f"{base_url}/commit_buffer")
        result = response.json()
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Check log status after commit
    print("\n5. Checking log status after commit...")
    try:
        response = requests.get(f"{base_url}/log_status")
        result = response.json()
        print(f"   Log empty: {result['log_empty']}")
        print(f"   Log content length: {len(result['log_content'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Start teaching session
    print("\n6. Starting teaching session...")
    try:
        response = requests.post(f"{base_url}/start_teaching")
        result = response.json()
        print(f"   Success: {result['success']}")
        if result['success']:
            print(f"   Topic: {result['topic']}")
            print(f"   Subtopics: {result['subtopics']}")
            print(f"   Bullet points: {result['bullet_points']}")
        else:
            print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Check teaching status
    print("\n7. Checking teaching status...")
    try:
        response = requests.get(f"{base_url}/teaching_status")
        result = response.json()
        print(f"   Active: {result['active']}")
        if result['active']:
            print(f"   Progress: {result['progress']['read']}/{result['progress']['total']}")
            print(f"   Percentage: {result['progress']['percentage']:.1f}%")
            print(f"   Topic: {result['topic']}")
        else:
            print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Wait a bit and check progress
    print("\n8. Waiting 5 seconds and checking progress...")
    time.sleep(5)
    try:
        response = requests.get(f"{base_url}/teaching_status")
        result = response.json()
        print(f"   Active: {result['active']}")
        if result['active']:
            print(f"   Progress: {result['progress']['read']}/{result['progress']['total']}")
            print(f"   Percentage: {result['progress']['percentage']:.1f}%")
        else:
            print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 9: Stop teaching session
    print("\n9. Stopping teaching session...")
    try:
        response = requests.post(f"{base_url}/stop_teaching")
        result = response.json()
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 10: Final status check
    print("\n10. Final status check...")
    try:
        response = requests.get(f"{base_url}/teaching_status")
        result = response.json()
        print(f"   Teaching active: {result['active']}")
        
        response = requests.get(f"{base_url}/log_status")
        result = response.json()
        print(f"   Log empty: {result['log_empty']}")
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Combined system test completed!")

if __name__ == "__main__":
    test_combined_system() 