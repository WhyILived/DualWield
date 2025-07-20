## Valorant Combat Report Detector (OCR-based Death Detection)
This script uses OCR (Optical Character Recognition) to detect when the "Combat Report" appears on screen in Valorant, signaling that the player has died. It logs both:

✅ When the combat report appears (you died)
❎ When it disappears (you respawn or round ends)

# 📦 Features
🔍 Real-time OCR using Tesseract
🎯 Scans only a small screen region for performance
🕒 Logs precise timestamps of death and respawn
🔁 Loop runs until user exits
💻 No interference with game process — safe and ban-free
## 🧰 Prerequisites

### 1. Python (3.8+ Recommended)
Download from: [python.org/downloads](https://www.python.org/downloads/)

### 2. Required Python Libraries
Install with pip:
```bash
pip install opencv-python numpy mss pytesseract
```

### 3. Tesseract OCR (required by pytesseract)
**Install Tesseract for Windows:**  
Download and install from:  
👉 [UB Mannheim Tesseract Wiki](https://github.com/UB-Mannheim/tesseract/wiki)

Recommended installer: `tesseract-ocr-w64-setup-5.x.x.exe`

During install:
- Enable English language
- Default install path: `C:\Program Files\Tesseract-OCR\`

**Add Tesseract to PATH:**  
Open "Edit the system environment variables" and add:
```
C:\Program Files\Tesseract-OCR\
```
Or set it manually in your script:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

---

## 🚀 How to Use

**Script:** `downtime.py`  
Run with:
```bash
python downtime.py
```
The script will continuously scan a 500×500 pixel region of your screen:

Region: `{"top": 350, "left": 1450, "width": 500, "height": 500}`

- If "combat report" appears in that region, it logs the time.
- When the phrase disappears, it logs the duration it was visible.

---

## 🧪 Sample Output
```bash
[🟢] 'combat report' appeared at 20:18:32
[🔴] 'combat report' disappeared at 20:18:45 (Visible for 13.21s)
```

---

## 🧠 Why "Combat Report"?

In Valorant, the "Combat Report" appears as soon as you're eliminated. It's a consistent on-screen element, making it reliable for OCR-based death detection.

---

## ✅ Safe for Use

- Does **not** read game memory
- Does **not** inject code
- Just looks at pixels on screen
- Safe with anti-cheat (uses same screen capture as OBS)

---

## 📌 Future Ideas

- Add automatic log saving to CSV or JSON
- Integrate with sound alert or Discord bot
- Use OpenCV template matching instead of or alongside OCR

Let me know if you want this turned into a README.md file directly, or want to add multiple script modes (OCR-only, template-only, hybrid).
