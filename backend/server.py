# server.py
import base64
import io
from PyPDF2 import PdfReader
from flask import Flask, request, jsonify
from datetime import datetime
import json
from downloader import download_video
from summarize import summarize_video

CONTENT_LOG = ""

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

@app.post("/log")
def log():
    link = get_youtube_link()
    print("YT_LINK", link) 
    try:
        summary_text = summarize_youtube_video(link)
        print(summary_text)
        global CONTENT_LOG
        CONTENT_LOG += f"{summary_text}\n"
        return jsonify({
            "url": link,
            "summary": summary_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/pdf")
def pdf():
    text = get_pdf()
    print("PDF_TEXT_LEN", len(text) if text else 0)
    global CONTENT_LOG
    CONTENT_LOG += f"{text}\n"
    return {"text": text}

@app.get("/dump")
def dump():
    return {"log": get_log()}

if __name__ == "__main__":
    app.run(port=5001, debug=True)
