import cv2
import numpy as np
import mss
import time
import os

# === SETTINGS ===
monitor = {"top": 350, "left": 1450, "width": 500, "height": 500}  # initial region
step = 5  # pixels moved/resized per key press

def draw_info(frame, region):
    text = f"Region: top={region['top']} left={region['left']} width={region['width']} height={region['height']}"
    cv2.putText(frame, text, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

def save_current_frame(frame):
    os.makedirs("frames", exist_ok=True)
    timestamp = int(time.time())
    filename = f"frames/region_{timestamp}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[💾] Saved region to {filename}")

print("[INFO] Starting region tuner. Use arrow keys and WASD to move/resize. Press S to save. Q to quit.")

with mss.mss() as sct:
    try:
        while True:
            frame = np.array(sct.grab(monitor))
            draw_info(frame, monitor)
            cv2.imshow("Region Tuner", frame)

            key = cv2.waitKey(50) & 0xFF

            if key == ord("q"):
                break
            elif key == ord("s"):
                save_current_frame(frame)

            # === Move region ===
            elif key == 81:  # ←
                monitor["left"] -= step
            elif key == 83:  # →
                monitor["left"] += step
            elif key == 82:  # ↑
                monitor["top"] -= step
            elif key == 84:  # ↓
                monitor["top"] += step

            # === Resize region ===
            elif key == ord("w"):
                monitor["height"] -= step
            elif key == ord("s"):
                monitor["height"] += step
            elif key == ord("a"):
                monitor["width"] -= step
            elif key == ord("d"):
                monitor["width"] += step

    except KeyboardInterrupt:
        print("\n[EXIT] Stopped by user.")

cv2.destroyAllWindows()
