#!/usr/bin/env python3
"""
Main server for AI Teaching Bot
Runs Vellum workflow and uses TTS to read through learning content
"""

import time
import json
from main_vellum import run_vellum_workflow
from tts_client import speak, stop, is_speaking

class TeachingBot:
    def __init__(self):
        self.learning_content = None
        self.current_subtopic_index = 0
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
            return True
        else:
            print("❌ Failed to load learning content")
            return False
    
    def get_unread_bullet_points(self):
        """Get all unread bullet points from all subtopics"""
        unread_points = []
        
        for subtopic_idx, subtopic in enumerate(self.learning_content.get('subtopic', [])):
            summaries = subtopic.get('Summaries', [])
            
            for bullet_idx, summary in enumerate(summaries):
                if not summary.get('Read_Status', False):
                    unread_points.append({
                        'subtopic_idx': subtopic_idx,
                        'bullet_idx': bullet_idx,
                        'section_title': subtopic.get('section_title', 'Unknown'),
                        'bullet_point': summary.get('Bullet_Point', ''),
                        'summary': summary
                    })
        
        return unread_points
    
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
    
    def teach_all_content(self):
        """Read through all unread bullet points"""
        if not self.learning_content:
            print("❌ No learning content loaded")
            return False
        
        print("\n🎓 Starting teaching session...")
        
        unread_points = self.get_unread_bullet_points()
        total_points = len(unread_points)
        
        if total_points == 0:
            print("✅ All content has been read!")
            return True
        
        print(f"📚 Found {total_points} unread bullet points")
        
        current_section = None
        
        for i, bullet_data in enumerate(unread_points):
            print(f"\n📖 Progress: {i+1}/{total_points}")
            
            # Check if this is a new section
            section_title = bullet_data['section_title']
            is_new_section = (section_title != current_section)
            
            if is_new_section:
                current_section = section_title
                print(f"📚 New section: {section_title}")
            
            # Read the bullet point (with section title only for new sections)
            success = self.read_bullet_point(bullet_data, is_new_section)
            
            if not success:
                print(f"❌ Failed to read bullet point {i+1}")
                continue
            
            # Small pause between bullet points
            time.sleep(0.5)
        
        print(f"\n🎉 Teaching session completed!")
        print(f"✅ Read {total_points} bullet points")
        return True
    
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
    """Main function to run the teaching bot"""
    
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
    
    # Load content
    if not bot.load_content(example_text):
        print("❌ Failed to initialize teaching bot")
        return
    
    # Show initial progress
    read, total = bot.get_progress()
    print(f"\n📊 Initial Progress: {read}/{total} bullet points read")
    
    # Start teaching
    bot.teach_all_content()
    
    # Show final progress
    read, total = bot.get_progress()
    print(f"\n📊 Final Progress: {read}/{total} bullet points read")

if __name__ == "__main__":
    main() 