from flask import Flask, jsonify
import socket, datetime, requests, os

app = Flask(__name__)
BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:5000/info")

def read_config_message():
    try:
        with open("/run/configs/app-message", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "Frontend OK"

def read_secret_token():
    try:
        with open("/run/secrets/app-token", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "no-secret"

@app.get("/")
def root():
    backend_hits = []
    for _ in range(3):
        try:
            r = requests.get(BACKEND_URL, timeout=2)
            j = r.json()
            backend_hits.append({"backend_hostname": j.get("hostname"), "time": j.get("time")})
        except Exception as e:
            backend_hits.append({"error": str(e)})
    return jsonify({
        "service": "frontend",
        "frontend_hostname": socket.gethostname(),
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "message": read_config_message(),
        "secret_loaded": read_secret_token() != "no-secret",
        "backend_calls": backend_hits
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
