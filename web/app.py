from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from functools import wraps
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from bot.config import Config
from bot.database import Database

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
db = Database()

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == Config.DASHBOARD_USERNAME and password == Config.DASHBOARD_PASSWORD:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    channels = db.get_channels()
    scheduled = db.get_pending_posts()
    
    # Calculate stats
    stats = {
        'total_channels': len(channels),
        'scheduled_posts': len(scheduled),
        'active_admins': len(Config.ADMIN_IDS),
    }
    
    return render_template('dashboard.html', stats=stats, channels=channels[:5])

@app.route('/channels')
@login_required
def channels():
    all_channels = db.get_channels()
    return render_template('channels.html', channels=all_channels)

@app.route('/scheduled')
@login_required
def scheduled_posts():
    posts = db.get_pending_posts()
    return render_template('scheduled.html', posts=posts)

@app.route('/analytics')
@login_required
def analytics():
    channels = db.get_channels()
    
    analytics_data = []
    for channel in channels:
        stats = db.get_channel_stats(channel['channel_id'], days=7)
        analytics_data.append({
            'channel': channel,
            'stats': stats
        })
    
    return render_template('analytics.html', data=analytics_data)

@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html')

# API Endpoints
@app.route('/api/stats')
@login_required
def api_stats():
    channels = db.get_channels()
    scheduled = db.get_pending_posts()
    
    return jsonify({
        'channels': len(channels),
        'scheduled': len(scheduled),
        'admins': len(Config.ADMIN_IDS)
    })

@app.route('/api/channels')
@login_required
def api_channels():
    channels = db.get_channels()
    return jsonify(channels)

def run_web_server():
    """Run the Flask web server"""
    app.run(
        host=Config.WEB_HOST,
        port=Config.WEB_PORT,
        debug=False
    )

if __name__ == '__main__':
    run_web_server()
