import sqlite3
import os
from bot.config import Config

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), 'data', 'emelia.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        with self.get_connection() as conn:
            # Full table schema for all features
            conn.execute('''CREATE TABLE IF NOT EXISTS channels (
                channel_id TEXT PRIMARY KEY, channel_name TEXT, channel_username TEXT,
                added_by INTEGER, added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                welcome_message TEXT, is_active INTEGER DEFAULT 1)''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS scheduled_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT, channel_id TEXT, 
                message_text TEXT, scheduled_time TIMESTAMP, status TEXT DEFAULT 'pending')''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER, channel_id TEXT, warning_count INTEGER DEFAULT 0,
                PRIMARY KEY(user_id, channel_id))''')
            
            conn.execute('''CREATE TABLE IF NOT EXISTS auto_replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT, response TEXT)''')
            conn.commit()

    def get_channels(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM channels WHERE is_active = 1")
            return [dict(row) for row in cursor.fetchall()]

    def get_pending_posts(self):
        with self.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM scheduled_posts WHERE status = 'pending'")
            return [dict(row) for row in cursor.fetchall()]

    def update_post_status(self, post_id, status):
        with self.get_connection() as conn:
            conn.execute("UPDATE scheduled_posts SET status = ? WHERE id = ?", (status, post_id))
            conn.commit()
