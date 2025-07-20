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
            print("⏳ Waiting for interview completion...")
            max_wait = 300  # 5 minutes
            check_interval = 10  # Check every 10 seconds
            start_time = time.time()
            
            while time.time() - start_time < max_wait:
                try:
                    response = requests.get(
                        f"{self.base_url}/interviews/{interview_id}",
                        headers=self.headers
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('status') == 'completed' and data.get('transcript'):
                            print("✅ Interview completed!")
                            return data['transcript']
                        else:
                            print(f"   Status: {data.get('status', 'unknown')}")
                    
                    time.sleep(check_interval)
                    
                except Exception as e:
                    print(f"❌ Error checking status: {e}")
                    time.sleep(check_interval)
            
            print("⏱️ Timeout reached")
            return None
        else:
            # Just get current transcript without waiting
            try:
                response = requests.get(
                    f"{self.base_url}/interviews/{interview_id}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    return response.json().get('transcript')
                    
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
    input()
    
    # # Get the transcript
    # transcript = interviewer.get_transcript(interview_id)
    
    # if transcript:
    #     # Save transcript
    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     filename = f"transcript_{interview_id}_{timestamp}.txt"
    #     with open(filename, 'w', encoding='utf-8') as f:
    #         f.write(transcript)
    #     print(f"\n📝 Transcript saved to: {filename}")
    
    transcript = "feed an eventually answer here to gemini*"
    
    return interview_link, transcript


# Example usage when run directly
if __name__ == "__main__":
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