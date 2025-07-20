# test_ribbon_api_cs.py
import requests
import json
import os
from datetime import datetime

# Your API key
API_KEY = "efbc484a-e854-4465-9426-b98e97bd35db"
BASE_URL = "https://app.ribbon.ai/be-api/v1"

# Headers with your API key
headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

# File to store interview IDs
INTERVIEW_ID_FILE = "latest_interview_id.txt"

print("🔑 Testing Ribbon AI API with your API key...\n")

# Test 1: Ping the API
print("1️⃣ Testing /ping endpoint...")
try:
    response = requests.get(f"{BASE_URL}/ping", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}\n")
    
    if response.status_code == 200:
        print("✅ API key is valid! Connection successful.\n")
    else:
        print("❌ API key might be invalid or there's an issue.\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 2: Create an interview flow with CS questions
print("2️⃣ Creating an interview flow...")
interview_flow_data = {
    "org_name": "Tech Company",
    "title": "Computer Science Interview",
    "questions": [
        "What is the difference between a stack and a queue data structure, and can you provide a real-world example of each?",
        "Explain the concept of time complexity and why Big O notation is important in algorithm analysis."
    ]
}

try:
    response = requests.post(
        f"{BASE_URL}/interview-flows",
        headers=headers,
        json=interview_flow_data
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}\n")
    
    if response.status_code == 201 or response.status_code == 200:
        result = response.json()
        interview_flow_id = result.get('interview_flow_id')
        print(f"✅ Interview flow created successfully!")
        print(f"Interview Flow ID: {interview_flow_id}\n")
        
        # Test 3: Create an interview
        print("3️⃣ Creating an interview...")
        interview_data = {
            "interview_flow_id": interview_flow_id
        }
        
        response = requests.post(
            f"{BASE_URL}/interviews",
            headers=headers,
            json=interview_data
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}\n")
        
        if response.status_code == 201 or response.status_code == 200:
            result = response.json()
            interview_id = result.get('interview_id')
            interview_link = result.get('interview_link')
            print(f"✅ Interview created successfully!")
            print(f"Interview ID: {interview_id}")
            print(f"Interview Link: {interview_link}\n")
            
            # Save the interview ID to file
            with open(INTERVIEW_ID_FILE, 'w') as f:
                f.write(interview_id)
            print(f"💾 Interview ID saved to {INTERVIEW_ID_FILE}")
            
    else:
        print("❌ Failed to create interview flow\n")
        
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 4: Get all interviews
print("4️⃣ Getting all interviews...")
try:
    response = requests.get(f"{BASE_URL}/interviews", headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}...\n")  # First 500 chars
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Successfully retrieved {len(result.get('interviews', []))} interviews\n")
except Exception as e:
    print(f"❌ Error: {e}\n")