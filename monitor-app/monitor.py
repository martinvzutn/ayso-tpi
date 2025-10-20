from flask import Flask, jsonify
import threading, time, requests, os

app = Flask(__name__)

targets = os.environ.get("TARGETS", "").split(",")
interval = int(os.environ.get("INTERVAL", 10))
status = {url: {"alive": False, "last_check": None} for url in targets}

def check_loop():
    while True:
        for url in targets:
            if not url:
                continue
            try:
                r = requests.get(url, timeout=2)
                status[url] = {"alive": True, "code": r.status_code, "last_check": time.ctime()}
            except Exception:
                status[url] = {"alive": False, "code": None, "last_check": time.ctime()}
        time.sleep(interval)

@app.route("/status")
def get_status():
    return jsonify(status)

if __name__ == "__main__":
    t = threading.Thread(target=check_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=True)

