# server.py
import base64
import io
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify
from datetime import datetime
import json
import threading
import time
import cv2
import numpy as np
import pytesseract
import mss
from downloader import download_video
from summarize import summarize_video
from main_vellum import run_vellum_workflow
from tts_client import speak, stop, is_speaking
from ribbon_interview_module import conduct_interview

# === DOWNTIME DETECTION SETTINGS ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OCR_REGION = {"top": 450, "left": 2050, "width": 500, "height": 500}
TARGET_PHRASE = "combat report"
OCR_CONFIG = "--psm 6"

CONTENT_LOG = ""
CONTENT_BUFFER = ""
TEACHING_BOT = None
TEACHING_ACTIVE = False
CONTENT_PROCESSING_ACTIVE = True
DOWNTIME_DETECTION_ACTIVE = False

app = Flask(__name__)

def _get_payload():
    # Central helper so multiple functions don’t each parse JSON separately.
    # If parsing fails, returns None.
    return request.get_json(force=True, silent=True)

def get_log() -> str:
    """
    Returns the current contents of the global content log string.
    """
    return CONTENT_LOG

def get_buffer() -> str:
    """
    Returns the current contents of the buffer.
    """
    return CONTENT_BUFFER

def is_buffer_empty() -> bool:
    """
    Returns True if the buffer is empty, False otherwise.
    """
    return len(CONTENT_BUFFER.strip()) == 0

def is_log_empty() -> bool:
    """
    Returns True if the log is empty, False otherwise.
    """
    return len(CONTENT_LOG.strip()) == 0

class TeachingBot:
    def __init__(self):
        self.learning_content = None
        self.current_subtopic_index = 0
        self.current_bullet_index = 0
        self.is_downtime = False
        self.teaching_active = False
        self.downtime_thread = None
        self.teaching_thread = None
        self.unread_bullet_points = []
        self.current_bullet_index = 0
        
    def load_content(self, text_content: str) -> bool:
        """
        Load learning content from Vellum workflow
        
        Args:
            text_content (str): The text to process
            
        Returns:
            bool: True if successful, False otherwise
        """
        print("🚀 Loading learning content from Vellum...")
        
        self.learning_content = run_vellum_workflow(text_content)
        
        if self.learning_content:
            print(f"✅ Content loaded successfully!")
            print(f"📚 Overall Topic: {self.learning_content.get('overall_topic', 'N/A')}")
            print(f"📝 Number of Subtopics: {len(self.learning_content.get('subtopic', []))}")
            
            # Prepare unread bullet points
            self.prepare_unread_bullet_points()
            return True
        else:
            print("❌ Failed to load learning content")
            return False
    
    def prepare_unread_bullet_points(self):
        """Prepare list of all unread bullet points"""
        self.unread_bullet_points = []
        
        for subtopic_idx, subtopic in enumerate(self.learning_content.get('subtopic', [])):
            summaries = subtopic.get('Summaries', [])
            
            for bullet_idx, summary in enumerate(summaries):
                if not summary.get('Read_Status', False):
                    self.unread_bullet_points.append({
                        'subtopic_idx': subtopic_idx,
                        'bullet_idx': bullet_idx,
                        'section_title': subtopic.get('section_title', 'Unknown'),
                        'bullet_point': summary.get('Bullet_Point', ''),
                        'summary': summary
                    })
        
        print(f"📚 Prepared {len(self.unread_bullet_points)} unread bullet points")
    
    def mark_bullet_as_read(self, subtopic_idx: int, bullet_idx: int):
        """Mark a specific bullet point as read"""
        try:
            subtopic = self.learning_content['subtopic'][subtopic_idx]
            summary = subtopic['Summaries'][bullet_idx]
            summary['Read_Status'] = True
            print(f"✅ Marked bullet point as read: {summary['Bullet_Point'][:50]}...")
        except Exception as e:
            print(f"❌ Error marking bullet as read: {e}")
    
    def read_bullet_point(self, bullet_data: dict, is_new_section: bool = False):
        """Read a single bullet point using TTS"""
        subtopic_idx = bullet_data['subtopic_idx']
        bullet_idx = bullet_data['bullet_idx']
        section_title = bullet_data['section_title']
        bullet_point = bullet_data['bullet_point']
        
        print(f"\n📖 Reading: {section_title}")
        print(f"   Bullet: {bullet_point[:100]}{'...' if len(bullet_point) > 100 else ''}")
        
        # Create reading format - only include section title for new sections
        if is_new_section:
            reading_text = f"Section: {section_title}. {bullet_point}"
        else:
            reading_text = bullet_point
        
        # Send TTS message to frontend
        self.send_tts_message(reading_text)
        
        # Speak the content
        success = speak(reading_text)
        
        if success:
            # Wait for speech to finish
            while is_speaking():
                time.sleep(0.1)
            
            # Mark as read
            self.mark_bullet_as_read(subtopic_idx, bullet_idx)
            return True
        else:
            print(f"❌ Failed to speak bullet point")
            return False
    
    def send_tts_message(self, text):
        """Send TTS message to frontend (placeholder for now)"""
        # This would ideally send a WebSocket message or use Server-Sent Events
        # For now, we'll just print it and the frontend can poll for updates
        print(f"🎤 TTS: {text}")
    
    def start_teaching_session(self):
        """Start teaching session"""
        if not self.learning_content or self.teaching_active:
            return
        
        self.teaching_active = True
        print("📚 Starting teaching session...")
        
        # Start teaching thread
        self.teaching_thread = threading.Thread(target=self.teach_content, daemon=True)
        self.teaching_thread.start()
    
    def stop_teaching_session(self):
        """Stop teaching session"""
        self.teaching_active = False
        print("⏹️ Stopping teaching session...")
        
        # Stop any current TTS
        stop()
    
    def start_downtime_detection(self):
        """Start monitoring for downtime (combat report)"""
        print("🎮 Starting downtime detection...")
        self.downtime_thread = threading.Thread(target=self.monitor_downtime, daemon=True)
        self.downtime_thread.start()
    
    def monitor_downtime(self):
        """Monitor screen for combat report (downtime detection)"""
        was_visible = False
        last_seen_time = None
        
        with mss.mss() as sct:
            try:
                while self.teaching_active:
                    # Capture and preprocess screen
                    img = np.array(sct.grab(OCR_REGION))
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

                    # OCR
                    text = pytesseract.image_to_string(thresh, config=OCR_CONFIG).lower()

                    if TARGET_PHRASE in text:
                        if not was_visible:
                            was_visible = True
                            last_seen_time = time.time()
                            print(f"[✅] '{TARGET_PHRASE}' appeared at {time.strftime('%H:%M:%S')}")
                            self.on_downtime_start()
                    else:
                        if was_visible:
                            was_visible = False
                            duration = time.time() - last_seen_time
                            print(f"[❎] '{TARGET_PHRASE}' disappeared at {time.strftime('%H:%M:%S')} (Visible for {duration:.2f}s)")
                            self.on_downtime_end()

                    time.sleep(0.1)

            except Exception as e:
                print(f"❌ Error in downtime detection: {e}")
    
    def on_downtime_start(self):
        """Called when downtime (combat report) appears"""
        self.is_downtime = True
        print("🎓 Downtime detected - TTS can now speak")
    
    def on_downtime_end(self):
        """Called when downtime (combat report) disappears"""
        self.is_downtime = False
        print("🎮 Downtime ended - stopping TTS")
        stop()
    
    def teach_content(self):
        """Teach content during downtime periods"""
        current_section = None
        
        # Start downtime detection
        self.start_downtime_detection()
        
        while self.teaching_active:
            # Check if we have unread bullet points
            if self.current_bullet_index >= len(self.unread_bullet_points):
                print("✅ All bullet points have been read!")
                break
            
            # Get current bullet point
            bullet_data = self.unread_bullet_points[self.current_bullet_index]
            
            # Check if this is a new section
            section_title = bullet_data['section_title']
            is_new_section = (section_title != current_section)
            
            if is_new_section:
                current_section = section_title
                print(f"📚 New section: {section_title}")
            
            # Only read if in downtime
            if self.is_downtime:
                # Read the bullet point
                success = self.read_bullet_point(bullet_data, is_new_section)
                
                if success:
                    self.current_bullet_index += 1
                    print(f"📖 Progress: {self.current_bullet_index}/{len(self.unread_bullet_points)}")
                else:
                    print(f"❌ Failed to read bullet point {self.current_bullet_index + 1}")
                    break
            else:
                print("⏸️ Waiting for downtime to continue teaching...")
            
            # Small pause between bullet points
            time.sleep(0.5)
            
            # Check if still active
            if not self.teaching_active:
                print("⏸️ Teaching stopped...")
                break
        
        self.teaching_active = False
        print("🏁 Teaching session ended")
    
    def get_progress(self):
        """Get current reading progress"""
        if not self.learning_content:
            return 0, 0
        
        total_bullets = 0
        read_bullets = 0
        
        for subtopic in self.learning_content.get('subtopic', []):
            summaries = subtopic.get('Summaries', [])
            total_bullets += len(summaries)
            
            for summary in summaries:
                if summary.get('Read_Status', False):
                    read_bullets += 1
        
        return read_bullets, total_bullets

def get_youtube_link():
    """
    No-arg helper.
    Reads JSON payload from the current request and returns a YouTube watch URL:
      1. If payload has 'url', return it as-is.
      2. Else if payload has 'videoId', synthesize a standard watch URL.
      3. Else if raw payload is a string containing 'youtube' or 'youtu.be', return it.
      4. Else None.
    """
    payload = _get_payload()

    if isinstance(payload, dict):
        if 'url' in payload:
            return payload['url']
        vid = payload.get('videoId')
        if vid:
            return f"https://www.youtube.com/watch?v={vid}"
        return None

    if isinstance(payload, str):
        if 'youtube' in payload or 'youtu.be' in payload:
            return payload

    return None

def get_pdf():
    """
    Expects JSON with key 'pdf_base64' (optionally a data URI).
    Decodes and returns *all* extracted text as a string, or None if:
      - key missing
      - decode fails
      - extraction yields no text
    """
    payload = _get_payload() or {}
    if not isinstance(payload, dict):
        return None
    b64 = payload.get("pdf_base64")
    if not b64:
        return None
    # Strip an optional data URI prefix.
    if "," in b64:
        b64 = b64.split(",", 1)[1]
    try:
        raw = base64.b64decode(b64, validate=True)
    except Exception:
        return None
    try:
        reader = PdfReader(io.BytesIO(raw))
        parts = []
        for page in reader.pages:
            try:
                txt = page.extract_text() or ""
            except Exception:
                txt = ""
            parts.append(txt)
        full = "\n".join(parts).strip()
        return full or None
    except Exception:
        return None

def summarize_youtube_video(youtube_url: str) -> str:
    """
    Complete pipeline:
    1. Download video from YouTube
    2. Upload & summarize via TwelveLabs
    3. Return the full text
    """
    print("🎥 Downloading:", youtube_url)
    downloaded_path = download_video(youtube_url, output_path="downloads")
    print("🧠 Summarizing:", downloaded_path)
    return summarize_video(downloaded_path)

def extract_quiz_questions():
    """
    Extract all quiz questions from the current learning content.
    
    Returns:
        list: List of quiz question strings
    """
    if not TEACHING_BOT or not TEACHING_BOT.learning_content:
        return []
    
    questions = []
    for subtopic in TEACHING_BOT.learning_content.get('subtopic', []):
        quiz_questions = subtopic.get('quiz_questions', [])
        print(f"🔍 Quiz questions from subtopic '{subtopic.get('section_title', 'Unknown')}': {quiz_questions}")
        questions.extend(quiz_questions)
    
    # Convert all questions to strings and clean them up
    cleaned_questions = []
    for i, question in enumerate(questions):
        if isinstance(question, dict):
            # If question is a dict, try to extract the question text
            if 'question_text' in question:
                cleaned_questions.append(str(question['question_text']))
            elif 'question' in question:
                cleaned_questions.append(str(question['question']))
            elif 'text' in question:
                cleaned_questions.append(str(question['text']))
            else:
                # If it's a dict but we don't know the structure, convert to string
                cleaned_questions.append(str(question))
        elif isinstance(question, str):
            cleaned_questions.append(question)
        else:
            # Convert any other type to string
            cleaned_questions.append(str(question))
    
    print(f"🧹 Cleaned {len(cleaned_questions)} questions: {cleaned_questions[:3]}...")  # Show first 3
    return cleaned_questions

# Additional info for the interview - you can edit this variable to customize the AI interviewer's behavior
INTERVIEW_ADDITIONAL_INFO = """
You are an AI interviewer conducting a study session recap. 
Ask the user about what they learned from their study session.
Be quick and to the point. Dont ask too much follow-up questions based on their responses.
Let them answer the questions in their own words and just let them know if they are correct or not. Be quick and to the point.
"""

@app.post("/log")
def log():
    global CONTENT_PROCESSING_ACTIVE
    
    if not CONTENT_PROCESSING_ACTIVE:
        return jsonify({
            "error": "Content processing is disabled during teaching session"
        }), 503
    
    link = get_youtube_link()
    print("YT_LINK", link) 
    try:
        summary_text = summarize_youtube_video(link)
        print(summary_text)
        global CONTENT_BUFFER
        CONTENT_BUFFER = f"{summary_text}\n"  # Replace buffer with new content
        return jsonify({
            "url": link,
            "summary": summary_text,
            "buffer_empty": is_buffer_empty()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/pdf")
def pdf():
    global CONTENT_PROCESSING_ACTIVE
    
    if not CONTENT_PROCESSING_ACTIVE:
        return jsonify({
            "error": "Content processing is disabled during teaching session"
        }), 503
    
    text = get_pdf()
    print("PDF_TEXT_LEN", len(text) if text else 0)
    global CONTENT_BUFFER
    CONTENT_BUFFER = f"{text}\n"  # Replace buffer with new content
    return {"text": text, "buffer_empty": is_buffer_empty()}

@app.get("/dump")
def dump():
    return {"log": get_log()}

@app.post("/commit_buffer")
def commit_buffer():
    """
    Appends the buffer content to the log and clears the buffer.
    """
    global CONTENT_LOG, CONTENT_BUFFER
    if CONTENT_BUFFER.strip():
        CONTENT_LOG += CONTENT_BUFFER
        CONTENT_BUFFER = ""
        return jsonify({
            "success": True,
            "message": "Buffer committed to log",
            "buffer_empty": True
        })
    else:
        return jsonify({
            "success": False,
            "message": "Buffer is empty",
            "buffer_empty": True
        })

@app.get("/buffer_status")
def buffer_status():
    """
    Returns the current buffer status.
    """
    return jsonify({
        "buffer_empty": is_buffer_empty(),
        "buffer_content": get_buffer()
    })

@app.get("/log_status")
def log_status():
    """
    Returns the current log status.
    """
    return jsonify({
        "log_empty": is_log_empty(),
        "log_content": get_log()
    })

@app.post("/start_teaching")
def start_teaching():
    """
    Start teaching session using log content.
    """
    global TEACHING_BOT, TEACHING_ACTIVE, CONTENT_PROCESSING_ACTIVE
    
    if TEACHING_ACTIVE:
        return jsonify({
            "success": False,
            "message": "Teaching session already active"
        })
    
    if is_log_empty():
        return jsonify({
            "success": False,
            "message": "No content in log to teach"
        })
    
    try:
        # Stop content processing
        CONTENT_PROCESSING_ACTIVE = False
        print("🛑 Content processing stopped - teaching session active")
        
        # Initialize teaching bot
        TEACHING_BOT = TeachingBot()
        
        # Load content from log
        log_content = get_log()
        if TEACHING_BOT.load_content(log_content):
            # Start teaching session
            TEACHING_BOT.start_teaching_session()
            TEACHING_ACTIVE = True
            
            return jsonify({
                "success": True,
                "message": "Teaching session started - content processing stopped",
                "topic": TEACHING_BOT.learning_content.get('overall_topic', 'N/A'),
                "subtopics": len(TEACHING_BOT.learning_content.get('subtopic', [])),
                "bullet_points": len(TEACHING_BOT.unread_bullet_points)
            })
        else:
            # Re-enable content processing if teaching failed
            CONTENT_PROCESSING_ACTIVE = True
            return jsonify({
                "success": False,
                "message": "Failed to load content for teaching"
            })
            
    except Exception as e:
        # Re-enable content processing if teaching failed
        CONTENT_PROCESSING_ACTIVE = True
        return jsonify({
            "success": False,
            "message": f"Error starting teaching session: {str(e)}"
        })

@app.post("/stop_teaching")
def stop_teaching():
    """
    Stop teaching session.
    """
    global TEACHING_BOT, TEACHING_ACTIVE, CONTENT_PROCESSING_ACTIVE
    
    if not TEACHING_ACTIVE or not TEACHING_BOT:
        return jsonify({
            "success": False,
            "message": "No teaching session active"
        })
    
    try:
        TEACHING_BOT.stop_teaching_session()
        TEACHING_ACTIVE = False
        
        # Re-enable content processing
        CONTENT_PROCESSING_ACTIVE = True
        print("🔄 Content processing re-enabled - teaching session stopped")
        
        return jsonify({
            "success": True,
            "message": "Teaching session stopped - content processing re-enabled"
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error stopping teaching session: {str(e)}"
        })

@app.get("/teaching_status")
def teaching_status():
    """
    Returns the current teaching status.
    """
    global TEACHING_BOT, TEACHING_ACTIVE
    
    if not TEACHING_BOT or not TEACHING_ACTIVE:
        return jsonify({
            "active": False,
            "message": "No teaching session active"
        })
    
    try:
        read, total = TEACHING_BOT.get_progress()
        return jsonify({
            "active": True,
            "progress": {
                "read": read,
                "total": total,
                "percentage": (read / total * 100) if total > 0 else 0
            },
            "topic": TEACHING_BOT.learning_content.get('overall_topic', 'N/A'),
            "current_bullet": TEACHING_BOT.current_bullet_index,
            "total_bullets": len(TEACHING_BOT.unread_bullet_points)
        })
        
    except Exception as e:
        return jsonify({
            "active": False,
            "message": f"Error getting teaching status: {str(e)}"
        })

@app.get("/tts_message")
def get_tts_message():
    """
    Returns the current TTS message being spoken.
    """
    global TEACHING_BOT, TEACHING_ACTIVE
    
    if not TEACHING_BOT or not TEACHING_ACTIVE:
        return jsonify({
            "active": False,
            "message": "No teaching session active"
        })
    
    try:
        # Get current bullet point being read
        if TEACHING_BOT.current_bullet_index < len(TEACHING_BOT.unread_bullet_points):
            bullet_data = TEACHING_BOT.unread_bullet_points[TEACHING_BOT.current_bullet_index]
            section_title = bullet_data['section_title']
            bullet_point = bullet_data['bullet_point']
            
            # Check if this is a new section
            current_section = None
            if TEACHING_BOT.current_bullet_index > 0:
                prev_bullet = TEACHING_BOT.unread_bullet_points[TEACHING_BOT.current_bullet_index - 1]
                current_section = prev_bullet['section_title']
            
            is_new_section = (section_title != current_section)
            
            if is_new_section:
                reading_text = f"Section: {section_title}. {bullet_point}"
            else:
                reading_text = bullet_point
            
            return jsonify({
                "active": True,
                "message": reading_text,
                "section": section_title,
                "is_new_section": is_new_section
            })
        else:
            return jsonify({
                "active": False,
                "message": "All content has been read"
            })
        
    except Exception as e:
        return jsonify({
            "active": False,
            "message": f"Error getting TTS message: {str(e)}"
        })

@app.post("/conduct_interview")
def conduct_interview_endpoint():
    """
    Conduct an interview using quiz questions from the learning content.
    """
    try:
        # Extract quiz questions
        questions = extract_quiz_questions()
        
        if not questions:
            return jsonify({
                "success": False,
                "message": "No quiz questions available. Please load content first."
            })
        
        print(f"🎤 Starting interview with {len(questions)} questions...")
        print(f"📝 Questions: {questions}")
        print(f"📝 Question types: {[type(q).__name__ for q in questions[:5]]}")  # Show types of first 5
        
        # Conduct the interview
        interview_link, transcript = conduct_interview(questions, INTERVIEW_ADDITIONAL_INFO)
        
        if interview_link:
            return jsonify({
                "success": True,
                "message": "Interview created successfully",
                "interview_link": interview_link,
                "transcript": transcript,
                "questions_count": len(questions)
            })
        else:
            return jsonify({
                "success": False,
                "message": "Failed to create interview"
            })
            
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Error conducting interview: {str(e)}"
        })

if __name__ == "__main__":
    app.run(port=5001, debug=True)
