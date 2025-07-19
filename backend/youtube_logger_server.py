# server.py
from flask import Flask, request
from datetime import datetime
import json

app = Flask(__name__)

def get_youtube_link():
    """
    No-arg helper.
    Reads JSON payload from the current request and returns a YouTube watch URL:
      1. If payload has 'url', return it as-is.
      2. Else if payload has 'videoId', synthesize a standard watch URL.
      3. Else if raw payload is a string containing 'youtube' or 'youtu.be', return it.
      4. Else None.
    """
    payload = request.get_json(force=True, silent=True)

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


@app.post("/log")
def log():
    link = get_youtube_link()
    print("YT_LINK", link) 
    return {"url": link}

if __name__ == "__main__":
    app.run(port=5001, debug=True)
