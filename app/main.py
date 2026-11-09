import json
from pathlib import Path
from flask import Flask, render_template

app = Flask(__name__)

# Load the questionnaire once at startup. Read-only after this.
DATA = json.loads((Path(__file__).parent / "data" / "questionnaire.json").read_text(encoding="utf-8"))

@app.after_request
def security_headers(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "no-referrer"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return resp

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/posture")
def posture():
    return render_template("posture.html")

@app.get("/questionnaire")
def questionnaire():
    return render_template("questionnaire.html", items=DATA)