# server.py
from flask import Flask, request, jsonify
from datetime import datetime
import json
from downloader import download_video
from summarize import summarize_video


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

@app.post("/log")
def log():
    link = get_youtube_link()
    print("YT_LINK", link) 
    try:
        summary_text = summarize_youtube_video(link)
        print(summary_text)
        return jsonify({
            "url": link,
            "summary": summary_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5001, debug=True)
