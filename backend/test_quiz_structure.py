#!/usr/bin/env python3
"""
Test script to verify quiz question structure and extraction
"""

from main_vellum import run_vellum_workflow
from ribbon_interview_module import conduct_interview

def test_quiz_structure():
    """Test the quiz question structure and extraction"""
    
    # Example text to generate quiz questions
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
    
    print("🧪 Testing quiz question structure...")
    
    # Run Vellum workflow to get structured content
    learning_content = run_vellum_workflow(example_text)
    
    if not learning_content:
        print("❌ Failed to get learning content")
        return
    
    print("✅ Got learning content from Vellum")
    
    # Extract quiz questions
    questions = []
    for subtopic in learning_content.get('subtopic', []):
        quiz_questions = subtopic.get('quiz_questions', [])
        print(f"\n📝 Subtopic: {subtopic.get('section_title', 'Unknown')}")
        print(f"   Quiz questions found: {len(quiz_questions)}")
        
        for i, question in enumerate(quiz_questions):
            print(f"   Question {i+1}: {type(question).__name__}")
            if isinstance(question, dict):
                print(f"     Keys: {list(question.keys())}")
                if 'question_text' in question:
                    print(f"     Text: {question['question_text'][:50]}...")
                if 'correct_answer' in question:
                    print(f"     Answer: {question['correct_answer'][:30]}...")
            else:
                print(f"     Value: {str(question)[:50]}...")
        
        questions.extend(quiz_questions)
    
    print(f"\n📊 Total questions: {len(questions)}")
    
    # Test our extraction function
    print("\n🧹 Testing question extraction...")
    cleaned_questions = []
    for i, question in enumerate(questions):
        if isinstance(question, dict):
            if 'question_text' in question:
                cleaned_questions.append(str(question['question_text']))
            elif 'question' in question:
                cleaned_questions.append(str(question['question']))
            elif 'text' in question:
                cleaned_questions.append(str(question['text']))
            else:
                cleaned_questions.append(str(question))
        elif isinstance(question, str):
            cleaned_questions.append(question)
        else:
            cleaned_questions.append(str(question))
    
    print(f"✅ Cleaned questions: {len(cleaned_questions)}")
    for i, q in enumerate(cleaned_questions[:3]):  # Show first 3
        print(f"   {i+1}. {q[:60]}...")
    
    # Test with Ribbon API (optional - uncomment to test)
    if cleaned_questions:
        print(f"\n🎤 Testing with Ribbon API...")
        print(f"   Questions to send: {len(cleaned_questions)}")
        print(f"   First question: {cleaned_questions[0][:50]}...")
        
        # Uncomment the lines below to actually test the interview creation
        # additional_info = "This is a machine learning knowledge test. Ask follow-up questions to assess understanding of ML concepts."
        # link, transcript = conduct_interview(cleaned_questions, additional_info)
        # if link:
        #     print(f"✅ Interview created: {link}")
        # else:
        #     print("❌ Interview creation failed")
    else:
        print("❌ No questions to test with")

if __name__ == "__main__":
    test_quiz_structure() 