# 📥 YouTube Video Downloader (yt-dlp + FFmpeg)

## 🎯 Purpose

This module enables:
- Downloading videos from YouTube
- Ensuring high-quality audio and video
- Merging streams using FFmpeg
- Preparing `.mp4` files for AI processing (e.g., summarization)

## 🧰 Technologies Used

- **yt-dlp**  
    Modern video downloader (fork of youtube-dl)  
    Handles streaming formats, metadata extraction, and format selection

- **FFmpeg**  
    Merges separate audio/video streams  
    Ensures `.mp4` compatibility  
    Adds metadata when possible

## 🔍 Why Merging is Needed

YouTube delivers DASH streams:
- `bestvideo` → high-res video (no audio)
- `bestaudio` → clean audio (no video)

Both must be downloaded and merged for a usable `.mp4`.

## 🔧 How it Works

**Excerpt from `downloader.py`:**
```python
def download_video(url: str, output_path: str = ".") -> str:
        ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                'outtmpl': f'{output_path}/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'postprocessors': [{'key': 'FFmpegMetadata'}],
                'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return ydl.prepare_filename(info)
```

**Step-by-Step:**
1. Accepts a YouTube URL
2. yt-dlp:
     - Selects best video and audio
     - Downloads both streams
3. FFmpeg:
     - Merges into a single `.mp4`
     - Adds metadata

**Output:**  
A complete, high-quality `.mp4` stored in `downloads/`  
Filename = YouTube video title

## ✅ Benefits

- Maintains original audio/video quality
- Ensures `.mp4` is playable anywhere
- Clean integration with AI or analytics backends

## ⚠️ Requirements

- **FFmpeg** must be installed and added to system PATH  
    - Windows: `C:\ffmpeg\bin\ffmpeg.exe` → PATH  
    - Mac/Linux: `brew install ffmpeg` or `apt install ffmpeg`