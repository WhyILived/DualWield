# 🎤 AI-Powered Interview Conductor via Ribbon.ai

## 🎯 Purpose
This module creates and manages AI-powered interviews by:
- Creating interview flows with custom questions
- Generating phone-call based interviews - more interactive
- Retrieving transcripts after completion
TDLR: Create an immersive oral tests where users can express their ideas while targeting confidence and fluency!

## 🧰 Ribbon.ai API Usage
Services used:
- `POST /interview-flows` → Create interview template
- `POST /interviews` → Generate interview from flow
- `GET /interviews/{id}` → Check status and retrieve transcript
*Other API Enpoints were also used in testing / debugging scripts! (mainly GET /interviews)

### For dynamically-appearing data that appears on the Ribbon dashboard, we used Selenium to scrape the numbers and save them (to be fed along with the transcript into gemini for advanced feedback) 

## 🔧 How it Works
Excerpt from `ribbon_interview_module.py`:
```python
def conduct_interview(questions, additional_info):
    interviewer = RibbonInterviewer()
    
    # Create the interview
    interview_id, interview_link = interviewer.create_interview(questions, additional_info)
    if not interview_id:
        return None, None
    
    # Automatically open the link in the default browser
    webbrowser.open(interview_link)
    print("✅ Interview link opened in browser")
    
    return interview_link, None
```

## 📋 Interview Flow Creation
The system creates interviews in two steps:
1. **Interview Flow** → Template with questions and AI instructions
2. **Interview Instance** → Actual interview link generated from flow

Configuration options:
- 🔹 **Voice-enabled**: Phone calls supported (`is_phone_call_enabled: True`)
- 🔸 **Voice model**: Uses "11labs-Kate" voice
- 🔹 **Language**: English (en-US)
- 🔸 **No video**: Video disabled for phone-only interviews

## 🎯 Interview Parameters
```python
payload = {
    "org_name": "Dualwield",
    "title": "Assessment - Study Session Recap",
    "questions": questions,                    # List of questions
    "additional_info": additional_info,        # AI context/instructions
    "interview_type": "general",
    "is_video_enabled": False,                # Phone-only
    "is_phone_call_enabled": True,
    "voice_id": "11labs-Kate",
    "language": "en-US"
}
```

## 📞 Transcript Retrieval
Two modes available:
- **Immediate**: Quick check without waiting
- **Polling**: Wait up to 5 minutes for completion

```python
def get_transcript(self, interview_id=None, wait_for_completion=True):
    if wait_for_completion:
        # Poll every 10 seconds for up to 5 minutes
        while time.time() - start_time < max_wait:
            # Check status and transcript availability
```

## 💾 Data Persistence
- Interview IDs saved to `latest_interview_id.txt`
- Full interview data saved to `interview_data_{id}.json`
- Transcripts saved as `transcript_{id}_{timestamp}.txt`

## 📄 Output Format
The system provides:
```
✅ Interview created!
   ID: abc123-def456-ghi789
   Link: https://app.ribbon.ai/interview/...

🌐 Opening interview link automatically
✅ Interview link opened in browser

📝 Transcript saved to: transcript_abc123_20250720_143052.txt
```

## 🚀 Usage Examples
**Quick Interview Creation:**
```python
questions = [
    "What is the difference between a stack and a queue?",
    "Explain Big O notation in simple terms."
]

additional_info = "This is a computer science knowledge test."

link, transcript = conduct_interview(questions, additional_info)
```

**Check Latest Transcript:**
```python
# Command line usage
python ribbon_interview_simple.py check

# Or programmatically
transcript = get_latest_transcript()
```

## 📌 Requirements
- Valid Ribbon.ai API Key
- Internet connection for API calls
- Default web browser for automatic link opening
- Phone access for interviewees (voice-only interviews)