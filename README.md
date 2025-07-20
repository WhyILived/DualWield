# HackThe6ith

A collaborative project for HackThe6ix hackathon.

## 🚀 About

This repository contains the project developed for HackThe6ix hackathon.

Are you a gamer who needs to *truly* lock in? Here’s your chance to dual‑wield studying and gaming, turning those brief mid‑match downtimes into productive study bursts.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- API keys for:
  - Gemini AI
  - Vellum AI
  - 12 Labs
  - 11 Labs
  - Ribbon AI
- FFmpeg 
  - Windows: Follow https://phoenixnap.com/kb/ffmpeg-windows
  - Also direct download link here: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
  - Mac: Follow https://phoenixnap.com/kb/ffmpeg-mac

    - After downloading the zip, extract it
    -get into the bin and copy the directory, ex - C:\Users\shadh\Downloads\ffmpeg-7.1.1-essentials_build\ffmpeg-7.1.1-essentials_build\bin
    - search and open "edit the system environmental varibales" in windows search
    -click on environmental variables in the bottom
    -edit path in system variables
    -add the path 

### Installation

1. Clone the repository
```bash
git clone https://github.com/AndrewidRizk/hackthe6ith.git
cd hackthe6ith
```

2. Set up the Backend
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API keys
# Copy the example and add your keys:
# VELLUM_API_KEY=your_vellum_key_here
# GEMINI_API_KEY=your_gemini_key_here
# TWELVE_LABS_API_KEY=your_twelve_labs_key_here
# ELEVEN_LABS_API_KEY=your_eleven_labs_key_here
# RIBBON_API_KEY=your_ribbon_key_here
```

3. Run the project
```bash
# Backend (from backend directory with venv activated)
python main.py
```

4. Setup chrome extension

Load the extension in chrome
- Open Chrome.
- Go to: chrome://extensions/
- Toggle Developer mode ON (top right).
- Click “Load unpacked”.
- Select the /youtube_watch_logger/extension folder.
- Extension appears in list (you can pin it; it has no popup, that’s fine).

Run the backend: backend/youtube_logger_server.py

## 📁 Project Structure

```
hackthe6ith/
├── README.md
├── src/
├── docs/
└── [other directories]
```

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## 👥 Team

- Mushfiqur Shadhin
- Ammar Mohamed
- Andro Rizk
- Sammy Hawari

## 📞 Contact

- Project Link: [https://github.com/AndrewidRizk/hackthe6ith](https://github.com/AndrewidRizk/hackthe6ith)

---


## 📚 Documentation

- [Game Management](https://github.com/WhyILived/HT6ix/blob/main/documentation/Game_Management.md)
- [Twelve Labs Integration](https://github.com/WhyILived/HT6ix/blob/main/documentation/Twelve_labs.md)
- [YouTube Download](https://github.com/WhyILived/HT6ix/blob/main/documentation/Youtube_download.md)
- [TwelveLab Game Report Research](https://github.com/WhyILived/HT6ix/tree/main/TwelveLabGameReport)
