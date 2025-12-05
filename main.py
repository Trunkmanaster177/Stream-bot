import os
import time
from datetime import datetime, timedelta
from keep_alive import keep_alive

# ---------- CONFIG ----------
DAILY_START_TIME = "18:00"  # 24hr format, e.g., 09:00 = 9 AM
STREAM_URL = "rtmp://a.rtmp.youtube.com/live2/"
STREAM_KEY = "g8qz-gwg4-5x0b-xyf7-dd5q"  # replace with your key
VIDEO = "video.mp4"
STREAM_DURATION_HOURS = 2  # stops after 2 hours
# ----------------------------

keep_alive()

def wait_until_start():
    while True:
        now = datetime.now().strftime("%H:%M")
        if now == DAILY_START_TIME:
            print("Starting livestream!")
            break
        time.sleep(30)

def start_stream():
    end_time = datetime.now() + timedelta(hours=STREAM_DURATION_HOURS)
    while datetime.now() < end_time:
        # FFmpeg command loops the video
        command = f'''ffmpeg -re -stream_loop -1 -i "{VIDEO}" -vf "scale=1080:1920" \
-c:v libx264 -preset veryfast -maxrate 4500k -bufsize 9000k -pix_fmt yuv420p \
-c:a aac -b:a 128k -f flv "{STREAM_URL}{STREAM_KEY}"'''
        os.system(command)
        # Small delay before next loop just in case
        time.sleep(1)
    print(f"Stream ended after {STREAM_DURATION_HOURS} hours.")

while True:
    wait_until_start()
    start_stream()
    print("Waiting for next day's start time...")
    # Sleep 60 sec before checking start time again
    time.sleep(60)
