# get_latest_interview_analytics.py
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

# File to read interview ID from
INTERVIEW_ID_FILE = "latest_interview_id.txt"

def get_latest_interview_id():
    """Read the latest interview ID from file"""
    if os.path.exists(INTERVIEW_ID_FILE):
        with open(INTERVIEW_ID_FILE, 'r') as f:
            return f.read().strip()
    return None

def get_interview_analytics_logic(interview_id):
    """Get analytics for a specific interview"""
    print(f"📊 Getting analytics for interview: {interview_id}\n")
    
    try:
        response = requests.get(
            f"{BASE_URL}/interviews/{interview_id}",
            headers=headers
        )
        
        if response.status_code == 200:
            analytics = response.json()
            print("✅ Interview analytics retrieved!\n")
            
            # Display analytics
            print("📋 Interview Details:")
            print(f"   ID: {analytics.get('interview_id', 'N/A')}")
            print(f"   Status: {analytics.get('status', 'N/A')}")
            print(f"   Flow ID: {analytics.get('interview_flow_id', 'N/A')}")
            
            # Display transcript if available
            if analytics.get('transcript'):
                print(f"\n📝 Transcript:")
                print("-" * 50)
                print(analytics['transcript'])
                print("-" * 50)
            else:
                print("\n⏳ Transcript not yet available (interview may still be in progress)")
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"interview_{interview_id}_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(analytics, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Full analytics saved to: {filename}")
            
            # Also save transcript to a text file if available
            if analytics.get('transcript'):
                transcript_filename = f"transcript_{interview_id}_{timestamp}.txt"
                with open(transcript_filename, 'w', encoding='utf-8') as f:
                    f.write(f"Interview ID: {interview_id}\n")
                    f.write(f"Status: {analytics.get('status', 'N/A')}\n")
                    f.write(f"{'='*50}\n\n")
                    f.write(analytics['transcript'])
                print(f"📝 Transcript saved to: {transcript_filename}")
            
            return analytics
        else:
            print(f"❌ Failed to get interview analytics: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    
def get_latest_analytics():
    print("🔍 Looking for latest interview ID...\n")
    
    # Get the latest interview ID from file
    interview_id = get_latest_interview_id()
    
    if interview_id:
        print(f"✅ Found interview ID: {interview_id}\n")
        get_interview_analytics_logic(interview_id)
    else:
        print(f"❌ No interview ID found in {INTERVIEW_ID_FILE}")
        print("Make sure to run test_ribbon_api_cs.py first to create an interview.")
        
if __name__ == "__main__":
    get_latest_analytics()