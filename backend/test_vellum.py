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
    outputs = run_vellum_workflow(example_text)
    
    if outputs:
        print("✅ Workflow completed successfully!")
        print("📊 Outputs:")
        print(outputs)
    else:
        print("❌ Workflow failed or returned None")

if __name__ == "__main__":
    test_vellum_workflow() 