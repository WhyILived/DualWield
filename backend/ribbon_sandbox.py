import requests

url = "https://app.ribbon.ai/be-api/v1/interviews/46f3b46e-5416-4531-97e4-932e1aebf4d1"

headers = {
    "accept": "application/json",
    "authorization": "Bearer efbc484a-e854-4465-9426-b98e97bd35db"
}

response = requests.get(url, headers=headers).json() # "interview_data" : {transcript: "WANTED STRING"}

transcript = response["interview_data"]["transcript"]
print(transcript)