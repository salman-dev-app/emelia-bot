import sqlite3
from datetime import datetime
import json
import os

class Database:
    def __init__(self, db_path='data/emelia.db'):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        """Initialize all database tables"""
        conn = self.get_connection()
        c = conn.cursor()
        
        # Channels table
        c.execute('''CREATE TABLE IF NOT EXISTS channels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT UNIQUE NOT NULL,
            channel_name TEXT,
            channel_username TEXT,
            added_by INTEGER,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            welcome_message TEXT,
            is_active BOOLEAN DEFAULT 1
        )''')
        
        # Admins table
        c.execute('''CREATE TABLE IF NOT EXISTS admins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE NOT NULL,
            username TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            permissions TEXT DEFAULT 'all'
        )''')
        
        # Scheduled posts
        c.execute('''CREATE TABLE IF NOT EXISTS scheduled_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            message_text TEXT,
            media_type TEXT,
            media_url TEXT,
            scheduled_time TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            post_type TEXT DEFAULT 'regular'
        )''')
        
        # Drafts
        c.execute('''CREATE TABLE IF NOT EXISTS drafts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            message_text TEXT,
            media_type TEXT,
            media_url TEXT,
            created_by INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            title TEXT
        )''')
        
        # Auto replies
        c.execute('''CREATE TABLE IF NOT EXISTS auto_replies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            keyword TEXT NOT NULL,
            response TEXT NOT NULL,
            match_type TEXT DEFAULT 'contains',
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Music tracks
        c.execute('''CREATE TABLE IF NOT EXISTS music_tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT,
            youtube_url TEXT,
            file_path TEXT,
            duration INTEGER,
            play_count INTEGER DEFAULT 0,
            last_played TIMESTAMP,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Playlists
        c.execute('''CREATE TABLE IF NOT EXISTS playlists (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            created_by INTEGER,
            tracks TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # User actions log
        c.execute('''CREATE TABLE IF NOT EXISTS user_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT,
            user_id INTEGER,
            username TEXT,
            action_type TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            details TEXT
        )''')
        
        # Analytics daily
        c.execute('''CREATE TABLE IF NOT EXISTS analytics_daily (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            date DATE NOT NULL,
            new_members INTEGER DEFAULT 0,
            left_members INTEGER DEFAULT 0,
            messages_count INTEGER DEFAULT 0,
            active_users INTEGER DEFAULT 0,
            UNIQUE(channel_id, date)
        )''')
        
        # Banned users
        c.execute('''CREATE TABLE IF NOT EXISTS banned_users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            reason TEXT,
            banned_by INTEGER,
            banned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            UNIQUE(channel_id, user_id)
        )''')
        
        # User warnings
        c.execute('''CREATE TABLE IF NOT EXISTS user_warnings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            channel_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            username TEXT,
            warning_count INTEGER DEFAULT 0,
            last_warning TIMESTAMP,
            warnings_log TEXT
        )''')
        
        # Settings
        c.execute('''CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )''')
        
        # Reminders
        c.execute('''CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            chat_id TEXT NOT NULL,
            message TEXT NOT NULL,
            remind_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending'
        )''')
        
        # Todos
        c.execute('''CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )''')
        
        conn.commit()
        conn.close()
    
    # Channel Operations
    def add_channel(self, channel_id, channel_name, channel_username, added_by):
        conn = self.get_connection()
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO channels 
                        (channel_id, channel_name, channel_username, added_by) 
                        VALUES (?, ?, ?, ?)''',
                     (channel_id, channel_name, channel_username, added_by))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_channels(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM channels WHERE is_active = 1')
        channels = [dict(row) for row in c.fetchall()]
        conn.close()
        return channels
    
    def get_channel(self, channel_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('SELECT * FROM channels WHERE channel_id = ?', (channel_id,))
        channel = c.fetchone()
        conn.close()
        return dict(channel) if channel else None
    
    # Scheduled Posts
    def add_scheduled_post(self, channel_id, message_text, scheduled_time, 
                          media_type=None, media_url=None):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO scheduled_posts 
                    (channel_id, message_text, media_type, media_url, scheduled_time)
                    VALUES (?, ?, ?, ?, ?)''',
                 (channel_id, message_text, media_type, media_url, scheduled_time))
        conn.commit()
        post_id = c.lastrowid
        conn.close()
        return post_id
    
    def get_pending_posts(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM scheduled_posts 
                    WHERE status = 'pending' AND scheduled_time <= datetime('now')
                    ORDER BY scheduled_time''')
        posts = [dict(row) for row in c.fetchall()]
        conn.close()
        return posts
    
    def update_post_status(self, post_id, status):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('UPDATE scheduled_posts SET status = ? WHERE id = ?', 
                 (status, post_id))
        conn.commit()
        conn.close()
    
    # Auto Replies
    def add_auto_reply(self, channel_id, keyword, response, match_type='contains'):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO auto_replies 
                    (channel_id, keyword, response, match_type)
                    VALUES (?, ?, ?, ?)''',
                 (channel_id, keyword, response, match_type))
        conn.commit()
        conn.close()
    
    def get_auto_replies(self, channel_id=None):
        conn = self.get_connection()
        c = conn.cursor()
        if channel_id:
            c.execute('SELECT * FROM auto_replies WHERE channel_id = ? AND is_active = 1',
                     (channel_id,))
        else:
            c.execute('SELECT * FROM auto_replies WHERE is_active = 1')
        replies = [dict(row) for row in c.fetchall()]
        conn.close()
        return replies
    
    # Music Operations
    def add_music_track(self, title, artist, youtube_url, file_path, duration):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO music_tracks 
                    (title, artist, youtube_url, file_path, duration)
                    VALUES (?, ?, ?, ?, ?)''',
                 (title, artist, youtube_url, file_path, duration))
        conn.commit()
        track_id = c.lastrowid
        conn.close()
        return track_id
    
    def increment_play_count(self, track_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''UPDATE music_tracks 
                    SET play_count = play_count + 1, 
                        last_played = datetime('now')
                    WHERE id = ?''', (track_id,))
        conn.commit()
        conn.close()
    
    def get_trending_tracks(self, limit=10):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM music_tracks 
                    ORDER BY play_count DESC LIMIT ?''', (limit,))
        tracks = [dict(row) for row in c.fetchall()]
        conn.close()
        return tracks
    
    # Analytics
    def log_user_action(self, channel_id, user_id, username, action_type, details=None):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO user_actions 
                    (channel_id, user_id, username, action_type, details)
                    VALUES (?, ?, ?, ?, ?)''',
                 (channel_id, user_id, username, action_type, 
                  json.dumps(details) if details else None))
        conn.commit()
        conn.close()
    
    def update_daily_analytics(self, channel_id, date, **kwargs):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Try to insert, update if exists
        c.execute('''INSERT INTO analytics_daily 
                    (channel_id, date) VALUES (?, ?)
                    ON CONFLICT(channel_id, date) DO NOTHING''',
                 (channel_id, date))
        
        # Update values
        for key, value in kwargs.items():
            c.execute(f'''UPDATE analytics_daily 
                         SET {key} = {key} + ? 
                         WHERE channel_id = ? AND date = ?''',
                     (value, channel_id, date))
        
        conn.commit()
        conn.close()
    
    def get_channel_stats(self, channel_id, days=7):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM analytics_daily 
                    WHERE channel_id = ? 
                    ORDER BY date DESC LIMIT ?''',
                 (channel_id, days))
        stats = [dict(row) for row in c.fetchall()]
        conn.close()
        return stats
    
    # User Management
    def ban_user(self, channel_id, user_id, username, reason, banned_by, expires_at=None):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''INSERT OR REPLACE INTO banned_users 
                    (channel_id, user_id, username, reason, banned_by, expires_at)
                    VALUES (?, ?, ?, ?, ?, ?)''',
                 (channel_id, user_id, username, reason, banned_by, expires_at))
        conn.commit()
        conn.close()
    
    def is_user_banned(self, channel_id, user_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('''SELECT * FROM banned_users 
                    WHERE channel_id = ? AND user_id = ?
                    AND (expires_at IS NULL OR expires_at > datetime('now'))''',
                 (channel_id, user_id))
        result = c.fetchone()
        conn.close()
        return result is not None
    
    def add_warning(self, channel_id, user_id, username, reason):
        conn = self.get_connection()
        c = conn.cursor()
        
        # Get current warnings
        c.execute('''SELECT warning_count, warnings_log FROM user_warnings 
                    WHERE channel_id = ? AND user_id = ?''',
                 (channel_id, user_id))
        result = c.fetchone()
        
        if result:
            count = result['warning_count'] + 1
            warnings = json.loads(result['warnings_log']) if result['warnings_log'] else []
            warnings.append({'reason': reason, 'time': str(datetime.now())})
            
            c.execute('''UPDATE user_warnings 
                        SET warning_count = ?, warnings_log = ?, last_warning = datetime('now')
                        WHERE channel_id = ? AND user_id = ?''',
                     (count, json.dumps(warnings), channel_id, user_id))
        else:
            warnings = [{'reason': reason, 'time': str(datetime.now())}]
            c.execute('''INSERT INTO user_warnings 
                        (channel_id, user_id, username, warning_count, warnings_log)
                        VALUES (?, ?, ?, 1, ?)''',
                     (channel_id, user_id, username, json.dumps(warnings)))
            count = 1
        
        conn.commit()
        conn.close()
        return count
