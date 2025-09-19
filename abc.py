import os
import cv2
from flask import Flask, Response

app = Flask(__name__)

# 嘗試打開攝像頭（Render 上通常失敗）
camera = cv2.VideoCapture(0)

def generate_frames():
    if not camera.isOpened():
        # 如果沒有攝像頭，就用一張假的圖片
        import numpy as np
        import time
        while True:
            # 建立一張黑圖
            frame = 255 * np.ones((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "No Camera in Render", (50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(0.5)
    else:
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "打開 /video 即可觀看攝像頭或示範影像"

# ⚠️ 注意：不要在這裡寫 app.run()
# Render 會用 gunicorn 啟動 (Procfile 設定)
