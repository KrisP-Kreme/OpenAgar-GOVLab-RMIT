from flask import Flask, request, jsonify, Response
import os, threading, subprocess
from subprocess import Popen
import signal

app = Flask(__name__)

BOT_API_TOKEN = os.environ.get("BOT_API_TOKEN", "topsecret")
BOT_CONTROLLER_CMD = ["python", "./bot_controller.py", "-s", "./bot_fsm.py", "6"]

processes = []

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

        # Create a new process group
        p = Popen(cmd, preexec_fn=os.setsid)

        processes.append(p)

        return jsonify({"status":"started", "count": count}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/stop-bots", methods=["POST"])
def stop_bots():
    global processes

    token = request.headers.get("Authorization", "")
    if token != f"Bearer {BOT_API_TOKEN}":
        return jsonify({"error":"unauthorized"}), 401

    killed = 0
    for p in processes:
        try:
            pgid = os.getpgid(p.pid)
            os.killpg(pgid, signal.SIGTERM)
            killed += 1
        except:
            pass

    processes = []

    print(f"Killed {killed} bot groups")

    return jsonify({"status": "stopped", "count": killed}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
