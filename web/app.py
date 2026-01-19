from flask import Flask, render_template
import os
from bot.config import Config
from bot.database import Database

app = Flask(__name__)
db = Database()

@app.route('/')
def index():
    return "Emelia Dashboard is Running!"

@app.route('/dashboard')
def dashboard():
    channels = db.get_channels()
    return f"Connected Channels: {len(channels)}"

def run_web_server():
    # Use the port Render gives us
    port = int(os.environ.get("PORT", 10000))
    # use_reloader=False is CRITICAL when running in a thread
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
