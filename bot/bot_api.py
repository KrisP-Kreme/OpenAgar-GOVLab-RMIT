from flask import Flask, request, jsonify
import os, threading, subprocess

app = Flask(__name__)

BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN", "topsecret")
BOT_CONTROLLER_CMD = ["python", "./bot_controller.py", "-s", "./bot_fsm.py", "6"]

@app.route("/start-bots", methods=["POST"])
def start_bots():
    print(">>>> /start-bots called")
    token = request.headers.get("Authorization", "")
    if token != f"Bearer {BOT_API_TOKEN}":
        return jsonify({"error":"unauthorized"}), 401

    body = request.get_json(silent=True) or {}
    count = body.get("count", 6)
    script = body.get("script", "./bot_fsm.py")

    try:
        cmd = ["python", "./bot_controller.py", "-s", script, str(count)]
        thread = threading.Thread(target=subprocess.run, args=(cmd,), kwargs={"check":False})
        thread.daemon = True
        thread.start()
        return jsonify({"status":"started", "count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
