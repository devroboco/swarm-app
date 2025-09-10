from flask import Flask, jsonify
import socket, datetime

app = Flask(__name__)

def read_config_message():
    try:
        with open("/run/configs/app-message", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "Backend OK"

def read_secret_token():
    try:
        with open("/run/secrets/app-token", "r", encoding="utf-8") as f:
            return f.read().strip()
    except:
        return "no-secret"

@app.get("/info")
def info():
    return jsonify({
        "service": "backend",
        "hostname": socket.gethostname(),
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "message": read_config_message(),
        "secret_loaded": read_secret_token() != "no-secret"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
