# ribbon_interview_simple.py
import requests
import json
import os
import time
from datetime import datetime

class RibbonInterviewer:
    def __init__(self, api_key="efbc484a-e854-4465-9426-b98e97bd35db"):
        self.api_key = api_key
        self.base_url = "https://app.ribbon.ai/be-api/v1"
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        self.interview_id_file = "latest_interview_id.txt"
        
    def create_interview(self, questions, additional_info):
        """
        Create an interview with questions and additional info
        
        Args:
            questions (list): List of questions for the interview
            additional_info (str): Additional context/instructions for the AI
        
        Returns:
            tuple: (interview_id, interview_link) or (None, None) if failed
        """
        # Step 1: Create interview flow
        print("📋 Creating interview flow...")
        
        payload = {
            "org_name": "Dualwield",
            "title": "Assessment - Study Session Recap",
            "questions": questions,
            "additional_info": additional_info,
            "interview_type": "general",
            "is_video_enabled": False,
            "is_phone_call_enabled": True,
            "is_doc_upload_enabled": False,
            "voice_id": "11labs-Kate",
            "language": "en-US"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/interview-flows",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code not in [200, 201]:
                print(f"❌ Failed to create interview flow: {response.text}")
                return None, None
                
            flow_id = response.json().get('interview_flow_id')
            print(f"✅ Interview flow created! ID: {flow_id}")
            
            # Step 2: Create interview from flow
            print("🎤 Creating interview...")
            
            response = requests.post(
                f"{self.base_url}/interviews",
                headers=self.headers,
                json={"interview_flow_id": flow_id}
            )
            
            if response.status_code not in [200, 201]:
                print(f"❌ Failed to create interview: {response.text}")
                return None, None
                
            result = response.json()
            interview_id = result.get('interview_id')
            interview_link = result.get('interview_link')
            
            # Save interview ID
            with open(self.interview_id_file, 'w') as f:
                f.write(interview_id)
            
            print(f"✅ Interview created!")
            print(f"   ID: {interview_id}")
            print(f"   Link: {interview_link}")
            
            return interview_id, interview_link
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None, None
    
    def get_transcript(self, interview_id=None, wait_for_completion=True):
        """
        Get transcript for an interview
        
        Args:
            interview_id (str): Interview ID (uses latest if not provided)
            wait_for_completion (bool): Wait for interview to complete
        
        Returns:
            str: Transcript text or None
        """
        if not interview_id:
            # Try to read from file
            if os.path.exists(self.interview_id_file):
                with open(self.interview_id_file, 'r') as f:
                    interview_id = f.read().strip()
            else:
                print("❌ No interview ID provided")
                return None
        
        if wait_for_completion:
            print("⏳ Waiting for interview completion and transcript...")
            max_wait = 300  # 5 minutes
            check_interval = 10  # Check every 10 seconds
            start_time = time.time()
            
            # Track if we've seen completed status
            seen_completed = False
            
            while time.time() - start_time < max_wait:
                try:
                    response = requests.get(
                        f"{self.base_url}/interviews/{interview_id}",
                        headers=self.headers
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        status = data.get('status', 'unknown')
                        has_transcript = bool(data.get('transcript'))
                        
                        # Print status only if it changed
                        if status == 'completed' and not seen_completed:
                            print("✅ Interview completed! Waiting for transcript...")
                            seen_completed = True
                        elif status != 'completed':
                            print(f"   Status: {status}")
                        
                        # Check for transcript
                        if has_transcript:
                            print("✅ Transcript available!")
                            
                            # Save the full response for debugging
                            debug_file = f"interview_data_{interview_id}.json"
                            with open(debug_file, 'w') as f:
                                json.dump(data, f, indent=2)
                            
                            return data['transcript']
                        elif seen_completed:
                            # If completed but no transcript, show that we're waiting
                            print("   Waiting for transcript processing...")
                    else:
                        print(f"❌ API error: {response.status_code}")
                    
                    time.sleep(check_interval)
                    
                except Exception as e:
                    print(f"❌ Error checking status: {e}")
                    time.sleep(check_interval)
            
            # Final attempt to get transcript
            print("⏱️ Timeout reached - making final check...")
            try:
                response = requests.get(
                    f"{self.base_url}/interviews/{interview_id}",
                    headers=self.headers
                )
                if response.status_code == 200:
                    data = response.json()
                    if data.get('transcript'):
                        return data['transcript']
                    else:
                        print("❌ Interview completed but transcript not available")
                        print("   Try running the script again in a few minutes")
            except:
                pass
                
            return None
        else:
            # Just get current transcript without waiting
            try:
                response = requests.get(
                    f"{self.base_url}/interviews/{interview_id}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get('transcript')
                    
            except Exception as e:
                print(f"❌ Error: {e}")
            
            return None


# Simple function for easy use
def conduct_interview(questions, additional_info):
    """
    Conduct an interview and get the transcript
    
    Args:
        questions (list): List of questions for the interview
        additional_info (str): Additional context/instructions for the AI
    
    Returns:
        tuple: (interview_link, transcript) or (None, None) if failed
    """
    interviewer = RibbonInterviewer()
    
    # Create the interview
    interview_id, interview_link = interviewer.create_interview(questions, additional_info)
    if not interview_id:
        return None, None
    
    print(f"\n🌐 Open this link to complete the interview:")
    print(f"   {interview_link}")
    print("\nPress Enter after completing the interview to retrieve the transcript...")
    
    input() # Comment Out Eventually!
    
    # Get the transcript
    url = f"https://app.ribbon.ai/be-api/v1/interviews/{interview_id}"

    headers = {
        "accept": "application/json",
        "authorization": "Bearer efbc484a-e854-4465-9426-b98e97bd35db"
    }

    try:
        response = requests.get(url, headers=headers).json()
        
        # if response:
        #     # Save response
        #     filename = f"response_{interview_id}.json"
        #     with open(filename, 'w', encoding='utf-8') as f:
        #         json.dump(response, f, indent=2, ensure_ascii=False)
        #     print(f"\n📝 response saved to: {filename}")
        
        transcript = response["interview_data"]["transcript"]
        return interview_link, transcript
    except:
        return "Transcript Failed"


# Function to just get transcript without waiting
def get_latest_transcript():
    """Get transcript for the latest interview without waiting"""
    interviewer = RibbonInterviewer()
    
    # Get the latest interview ID
    interview_id = None
    if os.path.exists(interviewer.interview_id_file):
        with open(interviewer.interview_id_file, 'r') as f:
            interview_id = f.read().strip()
    
    if not interview_id:
        print("❌ No interview ID found")
        return None
    
    print(f"🔍 Checking interview: {interview_id}")
    
    # Get without waiting
    transcript = interviewer.get_transcript(interview_id, wait_for_completion=False)
    
    if transcript:
        print("✅ Transcript found!")
        # Save it
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"transcript_{interview_id}_{timestamp}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"📝 Transcript saved to: {filename}")
    else:
        print("❌ Transcript not available yet")
    
    return transcript


# Example usage when run directly
if __name__ == "__main__":
    import sys
    
    # Check if running in "check" mode
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        get_latest_transcript()
    else:
        questions = [
            "What is the difference between a stack and a queue?",
            "Explain Big O notation in simple terms."
        ]
        
        additional_info = "This is a computer science knowledge test. Ask follow-up questions to assess understanding of data structures and algorithms."
        
        link, transcript = conduct_interview(questions, additional_info)
        
        if transcript:
            print("\n📝 Transcript:")
            print("-" * 50)
            print(transcript)
        else:
            print("\n❌ Could not get transcript. You can try again with:")
            print("   python ribbon_interview_simple.py check")