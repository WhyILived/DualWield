#!/usr/bin/env python3
"""
Test script for the interview functionality
Press "=" key (global shortcut) to trigger interview
"""

import requests
import json

def test_interview_endpoint():
    """Test the conduct_interview endpoint"""
    
    print("🧪 Testing interview endpoint...")
    
    try:
        # Test the interview endpoint
        response = requests.post('http://localhost:5001/conduct_interview', 
                               headers={'Content-Type': 'application/json'})
        
        result = response.json()
        
        print(f"📊 Response Status: {response.status_code}")
        print(f"📝 Response: {json.dumps(result, indent=2)}")
        
        if result.get('success'):
            print("✅ Interview endpoint working!")
            if result.get('interview_link'):
                print(f"🔗 Interview Link: {result['interview_link']}")
            if result.get('questions_count'):
                print(f"📝 Questions: {result['questions_count']}")
        else:
            print(f"❌ Interview failed: {result.get('message', 'Unknown error')}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure server.py is running on port 5001")
    except Exception as e:
        print(f"❌ Error testing interview: {e}")

if __name__ == "__main__":
    test_interview_endpoint() 