#!/usr/bin/env python3
"""
Test script for the buffer system
"""

import requests
import json
import time

def test_buffer_system():
    """Test the buffer system functionality"""
    
    base_url = "http://localhost:5001"
    
    print("🧪 Testing Buffer System")
    print("=" * 40)
    
    # Test 1: Check initial buffer status
    print("\n1. Checking initial buffer status...")
    try:
        response = requests.get(f"{base_url}/buffer_status")
        result = response.json()
        print(f"   Buffer empty: {result['buffer_empty']}")
        print(f"   Buffer content length: {len(result['buffer_content'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Simulate adding content to buffer (YouTube)
    print("\n2. Simulating YouTube content to buffer...")
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
    
    # Test 4: Simulate adding PDF content to buffer
    print("\n4. Simulating PDF content to buffer...")
    try:
        test_pdf_data = {
            "pdf_base64": "JVBERi0xLjQKJcOkw7zDtsO8DQoxIDAgb2JqDQo8PA0KL1R5cGUgL0NhdGFsb2cNCi9QYWdlcyAyIDAgUg0KPj4NCmVuZG9iag0KMiAwIG9iag0KPDwNCi9UeXBlIC9QYWdlcw0KL0NvdW50IDENCi9LaWRzIFsgMyAwIFIgXQ0KPj4NCmVuZG9iag0KMyAwIG9iag0KPDwNCi9UeXBlIC9QYWdlDQovUGFyZW50IDIgMCBSDQovUmVzb3VyY2VzIDw8DQovRm9udCA8PA0KL0YxIDQgMCBSDQo+Pg0KPj4NCi9Db250ZW50cyA1IDAgUg0KL01lZGlhQm94IFsgMCAwIDYxMiA3OTIgXQ0KPj4NCmVuZG9iag0KNCAwIG9iag0KPDwNCi9UeXBlIC9Gb250DQovU3VidHlwZSAvVHlwZTENCi9CYXNlRm9udCAvSGVsdmV0aWNhDQovRW5jb2RpbmcgL1dpbkFuc2lFbmNvZGluZw0KPj4NCmVuZG9iag0KNSAwIG9iag0KPDwNCi9MZW5ndGggMzQNCj4+DQpzdHJlYW0NCkJUCjcwIDUwIFRECi9GMSAxMiBUZgooSGVsbG8gV29ybGQpIFRqCkVUCmVuZG9iag0KeHJlZg0KMCA2DQowMDAwMDAwMDAwIDY1NTM1IGYNCjAwMDAwMDAwMTAgMDAwMDAgbg0KMDAwMDAwMDA3OSAwMDAwMCBuDQowMDAwMDAwMTczIDAwMDAwIG4NCjAwMDAwMDAzMDEgMDAwMDAgbg0KMDAwMDAwMDM4MCAwMDAwMCBuDQp0cmFpbGVyDQo8PA0KL1NpemUgNg0KL1Jvb3QgMSAwIFINCj4+DQpzdGFydHhyZWYNCjQ5Mg0KJSVFT0Y="
        }
        response = requests.post(f"{base_url}/pdf", json=test_pdf_data)
        result = response.json()
        print(f"   Response: {result}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Check buffer status after PDF
    print("\n5. Checking buffer status after PDF...")
    try:
        response = requests.get(f"{base_url}/buffer_status")
        result = response.json()
        print(f"   Buffer empty: {result['buffer_empty']}")
        print(f"   Buffer content length: {len(result['buffer_content'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Commit buffer to log
    print("\n6. Committing buffer to log...")
    try:
        response = requests.post(f"{base_url}/commit_buffer")
        result = response.json()
        print(f"   Success: {result['success']}")
        print(f"   Message: {result['message']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Check buffer status after commit
    print("\n7. Checking buffer status after commit...")
    try:
        response = requests.get(f"{base_url}/buffer_status")
        result = response.json()
        print(f"   Buffer empty: {result['buffer_empty']}")
        print(f"   Buffer content length: {len(result['buffer_content'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 8: Check log content
    print("\n8. Checking log content...")
    try:
        response = requests.get(f"{base_url}/dump")
        result = response.json()
        print(f"   Log content length: {len(result['log'])}")
        print(f"   Log preview: {result['log'][:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n✅ Buffer system test completed!")

if __name__ == "__main__":
    test_buffer_system() 