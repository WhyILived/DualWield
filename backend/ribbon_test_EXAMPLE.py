# example_usage.py
from ribbon_interview_module import conduct_interview

# Just provide questions and additional info
questions = [
    "What is recursion?",
    "What are the SOLID principles?"
]

additional_info = "This is NOT an interview persay, rather a test after a lesson to see what the participant has learned - stick closely to the questions"

link, transcript = conduct_interview(questions, additional_info)

if transcript:
    print(f"Interview completed! Transcript should be done - no errors and got here")