#!/usr/bin/env python3
"""
Test script for Vellum workflow
"""

from main_vellum import run_vellum_workflow

def test_vellum_workflow():
    """Test the Vellum workflow with example text"""
    
    # Example text - you can replace this with your own content
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
    
    print("🚀 Testing Vellum workflow...")
    print(f"📝 Input text length: {len(example_text)} characters")
    print(f"📝 First 100 chars: {example_text[:100]}...")
    
    # Run the workflow
    learning_content = run_vellum_workflow(example_text)
    
    if learning_content:
        print("✅ Workflow completed successfully!")
        print("\n📊 Structured Learning Content:")
        print(f"📚 Overall Topic: {learning_content.get('overall_topic', 'N/A')}")
        print(f"📝 Number of Subtopics: {len(learning_content.get('subtopic', []))}")
        
        # Display each subtopic
        for i, subtopic in enumerate(learning_content.get('subtopic', [])):
            print(f"\n🔹 Subtopic {i+1}: {subtopic.get('section_title', 'N/A')}")
            
            # Show summaries (now an array)
            summaries = subtopic.get('Summaries', [])
            print(f"   📖 Summaries: {len(summaries)} bullet points")
            for k, summary in enumerate(summaries):
                bullet_point = summary.get('Bullet_Point', 'N/A')
                read_status = summary.get('Read_Status', False)
                print(f"     {k+1}. {bullet_point[:60]}{'...' if len(bullet_point) > 60 else ''}")
                print(f"        Status: {'✅ Read' if read_status else '❌ Not read'}")
            
            # Show quiz questions
            quiz_questions = subtopic.get('quiz_questions', [])
            print(f"   ❓ Quiz Questions: {len(quiz_questions)}")
            for j, question in enumerate(quiz_questions):
                print(f"     {j+1}. {question.get('question_text', 'N/A')[:60]}{'...' if len(question.get('question_text', '')) > 60 else ''}")
                print(f"        Correct: {question.get('correct_answer', 'N/A')[:40]}{'...' if len(question.get('correct_answer', '')) > 40 else ''}")
    else:
        print("❌ Workflow failed or returned None")

if __name__ == "__main__":
    test_vellum_workflow() 