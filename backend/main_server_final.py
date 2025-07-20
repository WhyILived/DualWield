#!/usr/bin/env python3
"""
Main server for AI Teaching Bot
Runs Vellum workflow and uses TTS to read through learning content during downtime
"""

import time
import json
import threading
import cv2
import numpy as np
import pytesseract
import mss
from main_vellum import run_vellum_workflow
from tts_client import speak, stop, is_speaking

# === DOWNTIME DETECTION SETTINGS ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OCR_REGION = {"top": 450, "left": 2050, "width": 500, "height": 500}
TARGET_PHRASE = "combat report"
OCR_CONFIG = "--psm 6"

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
                while True:
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
        print("🎓 Downtime detected - starting teaching session...")
        
        # Start teaching if not already active
        if not self.teaching_active:
            self.start_teaching_session()
    
    def on_downtime_end(self):
        """Called when downtime (combat report) disappears"""
        self.is_downtime = False
        print("🎮 Downtime ended - stopping teaching session...")
        
        # Stop current teaching
        self.stop_teaching_session()
    
    def start_teaching_session(self):
        """Start teaching session during downtime"""
        if not self.learning_content or self.teaching_active:
            return
        
        self.teaching_active = True
        print("📚 Starting teaching session...")
        
        # Start teaching thread
        self.teaching_thread = threading.Thread(target=self.teach_during_downtime, daemon=True)
        self.teaching_thread.start()
    
    def stop_teaching_session(self):
        """Stop teaching session"""
        self.teaching_active = False
        print("⏹️ Stopping teaching session...")
        
        # Stop any current TTS
        stop()
    
    def teach_during_downtime(self):
        """Teach content during downtime periods"""
        current_section = None
        
        while self.teaching_active and self.is_downtime:
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
            
            # Read the bullet point
            success = self.read_bullet_point(bullet_data, is_new_section)
            
            if success:
                self.current_bullet_index += 1
                print(f"📖 Progress: {self.current_bullet_index}/{len(self.unread_bullet_points)}")
            else:
                print(f"❌ Failed to read bullet point {self.current_bullet_index + 1}")
                break
            
            # Small pause between bullet points
            time.sleep(0.5)
            
            # Check if still in downtime
            if not self.is_downtime:
                print("⏸️ Downtime ended, pausing teaching...")
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

def main():
    """Main function to run the teaching bot with downtime detection"""
    
    # Example text - you can replace this with your content
    example_text = """
    Machine learning is a subset of artificial intelligence that focuses on algorithms 
    and statistical models that enable computers to improve their performance on a 
    specific task through experience. It involves training models on data to make 
    predictions or decisions without being explicitly programmed for every scenario.
    
    There are three main types of machine learning:
    1. Supervised Learning - where the model learns from labeled training data
    2. Unsupervised Learning - where the model finds patterns in unlabeled data
    3. Reinforcement Learning - where the model learns through trial and error
    
    Common applications include image recognition, natural language processing, 
    recommendation systems, and autonomous vehicles.
    """
    
    # Initialize teaching bot
    bot = TeachingBot()
    
    print("🚀 Preloading learning content...")
    
    # Preload content immediately (regardless of downtime)
    if not bot.load_content(example_text):
        print("❌ Failed to initialize teaching bot")
        return
    
    print("✅ Learning content preloaded successfully!")
    print(f"📚 Topic: {bot.learning_content.get('overall_topic', 'N/A')}")
    print(f"📝 Subtopics: {len(bot.learning_content.get('subtopic', []))}")
    print(f"📖 Unread bullet points: {len(bot.unread_bullet_points)}")
    
    # Show initial progress
    read, total = bot.get_progress()
    print(f"📊 Initial Progress: {read}/{total} bullet points read")
    
    # Start downtime detection (only for TTS control)
    bot.start_downtime_detection()
    
    print("\n🎮 Teaching bot is now monitoring for downtime...")
    print("📖 TTS will only play when 'combat report' appears")
    print("⏹️ TTS will stop when 'combat report' disappears")
    print("🔄 Press Ctrl+C to exit")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
            # Show progress periodically
            if bot.is_downtime and bot.teaching_active:
                read, total = bot.get_progress()
                print(f"📊 Progress: {read}/{total} bullet points read")
                
    except KeyboardInterrupt:
        print("\n🛑 Shutting down teaching bot...")
        bot.stop_teaching_session()

if __name__ == "__main__":
    main() 