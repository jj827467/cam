import cv2
from flask import Flask, Response
import requests
import socket

# ====== Telegram 設定 ======
BOT_TOKEN = "8375822827:AAHn8hSmurdScTzTUXp-wK7cxxgpI1TACaE"
CHAT_ID = "7901453860"

def get_local_ip():
    """獲取本機內網 IP"""
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def send_ip_to_tg():
    """發送本機 IP 到 Telegram"""
    local_ip = get_local_ip()
    message = f"📷 Camera Server 已啟動\n\n內網IP: http://{local_ip}/video"
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        r = requests.post(url, data=data)
        print("Telegram 回應:", r.json())
    except Exception as e:
        print("無法發送 Telegram 訊息:", e)

# ====== Flask + OpenCV 部分 ======
app = Flask(__name__)
camera = cv2.VideoCapture(0)  # 0 = 默認攝像頭

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "打開 /video 即可觀看攝像頭"

if __name__ == "__main__":
    # 啟動時發送 本機 IP 到 TG
    send_ip_to_tg()
    # 在 80 端口提供服務 (http://內網IP/video)
    app.run(host="0.0.0.0", port=80, debug=False)
