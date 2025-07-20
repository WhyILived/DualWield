import cv2
import numpy as np
import pytesseract
import mss
import time

# === SETTINGS ===
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
OCR_REGION = {"top": 450, "left": 2050, "width": 500, "height": 500}
TARGET_PHRASE = "combat report"
OCR_CONFIG = "--psm 6"

# === LOGIC STATE ===
was_visible = False
last_seen_time = None

print("[INFO] Watching for 'combat report'...")

with mss.mss() as sct:
    try:
        while True:
            # Capture and preprocess screen
            img = np.array(sct.grab(OCR_REGION))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)

            # OCR
            text = pytesseract.image_to_string(thresh, config=OCR_CONFIG).lower()

            if TARGET_PHRASE in text:
                if not was_visible:
                    was_visible = True
                    last_seen_time = time.time()
                    print(f"[✅] '{TARGET_PHRASE}' appeared at {time.strftime('%H:%M:%S')}")
            else:
                if was_visible:
                    was_visible = False
                    duration = time.time() - last_seen_time
                    print(f"[❎] '{TARGET_PHRASE}' disappeared at {time.strftime('%H:%M:%S')} (Visible for {duration:.2f}s)")

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n[EXIT] Stopped.")
