# 🧠 Video Summarization via TwelveLabs

## 🎯 Purpose
This module processes a local video file by:
- Uploading it to TwelveLabs
- Indexing with audio + visual models
- Returning:
    - 🔹 A summary
    - 🔸 Chapters (start/end times, titles, summaries)

## 🧰 TwelveLabs API Usage
Services used:
- `client.task.create()` → Upload video
- `task.wait_for_done()` → Wait until ready
- `client.summarize(type="summary")` → Short-form summary
- `client.summarize(type="chapter")` → Scene-based segmentation

## 🔧 How it Works
Excerpt from `summarize.py`:
```python
def summarize_video(file_path: str) -> str:
        if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

        index = get_or_create_index(INDEX_NAME)
        video_id = get_existing_video_id(index.id, file_path)

        if not video_id:
                task = client.task.create(index_id=index.id, file=file_path)
                task.wait_for_done()
                video_id = task.video_id

        summary = client.summarize(video_id=video_id, type="summary").summary
        chapters = client.summarize(video_id=video_id, type="chapter").chapters

        chapter_text = "\n".join([
                f"🔸 Chapter {ch.chapter_number}\nStart: {ch.start}, End: {ch.end}\nTitle: {ch.chapter_title}\nSummary: {ch.chapter_summary}"
                for ch in chapters
        ])

        return f"🔹 Summary:\n{summary}\n\n{chapter_text}"
```

## 📂 How Indexing Works
- Each video is uploaded and linked to an Index
- Filename stored in `system_metadata["filename"]` for lookup
- Already-uploaded videos are reused (avoids double uploads)

## 📄 Output Format
Returned as a single text blob:
```
🔹 Summary:
<high-level summary>

🔸 Chapter 1
Start: 0, End: 45
Title: Introduction
Summary: The video begins by...
...
```
Can be returned as:
- Raw string
- JSON
- Saved to `.txt`, `.md`, or `.json` file

## 📌 Requirements
- Valid TwelveLabs API Key
- Supported language (e.g., `LANGUAGE = "en"`)
- Content must contain voice or visual content to summarize