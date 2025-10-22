from flask import Flask, jsonify, render_template_string
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


@app.route("/")
def index():
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Monitor App</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .alive { color: green; }
            .dead { color: red; }
        </style>
    </head>
    <body>
        <h1>Monitor App</h1>
        <table>
            <thead>
                <tr>
                    <th>URL</th>
                    <th>Status</th>
                    <th>HTTP Code</th>
                    <th>Last Check</th>
                </tr>
            </thead>
            <tbody>
                {% for url, info in status.items() %}
                <tr>
                    <td>{{ url }}</td>
                    <td class="{{ 'alive' if info.alive else 'dead' }}">
                        {{ "Alive" if info.alive else "Dead" }}
                    </td>
                    <td>{{ info.code if info.code else "N/A" }}</td>
                    <td>{{ info.last_check }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(html_template, status=status)

if __name__ == "__main__":
    t = threading.Thread(target=check_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=True)

