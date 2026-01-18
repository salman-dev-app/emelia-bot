# bot/services/music_service.py
import yt_dlp
import os
from bot.config import Config

class MusicService:
    """Handle YouTube audio downloads"""
    
    def __init__(self):
        self.cache_dir = Config.MUSIC_CACHE_DIR
        os.makedirs(self.cache_dir, exist_ok=True)
    
    def search_youtube(self, query):
        """Search YouTube for a song"""
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'extract_flat': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch:{query}", download=False)
                if 'entries' in result:
                    return result['entries'][0]
                return None
        except Exception as e:
            print(f"Search error: {e}")
            return None
    
    def download_audio(self, url):
        """Download audio from YouTube"""
        output_path = os.path.join(self.cache_dir, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
                return filename, info
        except Exception as e:
            print(f"Download error: {e}")
            return None, None
    
    def clean_cache(self):
        """Remove old cached files"""
        # Implementation for cache cleanup
        pass


# bot/services/translator.py
from deep_translator import GoogleTranslator

class TranslationService:
    """Handle text translation"""
    
    @staticmethod
    def translate(text, target_lang='en', source_lang='auto'):
        """Translate text to target language"""
        try:
            translator = GoogleTranslator(source=source_lang, target=target_lang)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    @staticmethod
    def detect_language(text):
        """Detect text language"""
        try:
            from langdetect import detect
            return detect(text)
        except:
            return 'unknown'


# bot/services/caption_gen.py
import random

class CaptionGenerator:
    """Generate captions for posts"""
    
    TEMPLATES = {
        'motivational': [
            "✨ {topic} - Your journey starts today!",
            "🌟 Embrace {topic} and shine bright!",
            "💪 {topic}: The power is within you!",
        ],
        'professional': [
            "📊 {topic} - Industry insights you need",
            "💼 Exploring {topic} in depth",
            "🎯 {topic}: Key takeaways for success",
        ],
        'casual': [
            "Hey! Check out {topic} 😊",
            "Just discovered {topic}! Thoughts?",
            "Loving {topic} lately! 🔥",
        ],
        'educational': [
            "📚 Learn about {topic} today",
            "🧠 Deep dive into {topic}",
            "📖 Understanding {topic}: A guide",
        ]
    }
    
    @staticmethod
    def generate(topic, style='casual'):
        """Generate a caption"""
        if style not in CaptionGenerator.TEMPLATES:
            style = 'casual'
        
        template = random.choice(CaptionGenerator.TEMPLATES[style])
        return template.format(topic=topic)
    
    @staticmethod
    def add_hashtags(text, tags):
        """Add hashtags to caption"""
        hashtags = ' '.join([f'#{tag.replace(" ", "")}' for tag in tags])
        return f"{text}\n\n{hashtags}"


# bot/services/analytics_service.py
from datetime import datetime, timedelta
from collections import defaultdict

class AnalyticsService:
    """Process and analyze channel data"""
    
    def __init__(self, database):
        self.db = database
    
    def calculate_engagement_rate(self, channel_id, days=7):
        """Calculate engagement rate"""
        stats = self.db.get_channel_stats(channel_id, days)
        
        if not stats:
            return 0
        
        total_messages = sum(s['messages_count'] for s in stats)
        total_active = sum(s['active_users'] for s in stats)
        
        if total_active == 0:
            return 0
        
        return (total_messages / total_active) * 100
    
    def get_best_posting_times(self, channel_id):
        """Analyze best times to post"""
        # Implementation for analyzing message timestamps
        # Returns list of optimal hours
        return [9, 12, 18, 21]  # Default times
    
    def get_growth_trend(self, channel_id, days=30):
        """Calculate growth trend"""
        stats = self.db.get_channel_stats(channel_id, days)
        
        if len(stats) < 2:
            return 'insufficient_data'
        
        recent = stats[:7]
        older = stats[7:14]
        
        recent_avg = sum(s['new_members'] for s in recent) / len(recent)
        older_avg = sum(s['new_members'] for s in older) / len(older)
        
        if recent_avg > older_avg * 1.1:
            return 'growing'
        elif recent_avg < older_avg * 0.9:
            return 'declining'
        else:
            return 'stable'
    
    def get_top_active_users(self, channel_id, limit=10):
        """Get most active users"""
        # Query user_actions table and aggregate
        # Returns list of top users
        return []


# bot/middleware/auth.py
from functools import wraps
from bot.config import Config

def admin_only(func):
    """Decorator to restrict commands to admins"""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        
        if user_id not in Config.ADMIN_IDS:
            await update.message.reply_text(
                "🚫 This command is only available to bot administrators."
            )
            return
        
        return await func(update, context, *args, **kwargs)
    
    return wrapper

def channel_admin_only(func):
    """Decorator to check if user is channel admin"""
    @wraps(func)
    async def wrapper(update, context, *args, **kwargs):
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        try:
            member = await context.bot.get_chat_member(chat_id, user_id)
            if member.status not in ['creator', 'administrator']:
                await update.message.reply_text(
                    "🚫 This command requires channel admin privileges."
                )
                return
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
            return
        
        return await func(update, context, *args, **kwargs)
    
    return wrapper


# bot/handlers/__init__.py
"""
Emelia Bot Handlers Package
"""

from . import admin
from . import channel
from . import music
from . import moderation
from . import analytics
from . import utility
from . import auto_reply

__all__ = [
    'admin',
    'channel',
    'music',
    'moderation',
    'analytics',
    'utility',
    'auto_reply',
]


# bot/services/__init__.py
"""
Emelia Bot Services Package
"""

from .scheduler import PostScheduler
from .music_service import MusicService
from .translator import TranslationService
from .caption_gen import CaptionGenerator
from .analytics_service import AnalyticsService

__all__ = [
    'PostScheduler',
    'MusicService',
    'TranslationService',
    'CaptionGenerator',
    'AnalyticsService',
]


# Additional utility functions
# bot/utils.py
import re
from datetime import datetime

def is_valid_channel_id(channel_id):
    """Validate channel ID format"""
    return bool(re.match(r'^-100\d{10,}$', str(channel_id)))

def format_duration(seconds):
    """Format duration in seconds to readable string"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"

def parse_time_string(time_str):
    """Parse time string to datetime"""
    formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %H:%M:%S",
        "%d/%m/%Y %H:%M",
        "%H:%M",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(time_str, fmt)
        except:
            continue
    
    raise ValueError(f"Invalid time format: {time_str}")

def truncate_text(text, max_length=100):
    """Truncate text to max length"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."

def is_url(text):
    """Check if text is a URL"""
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    return bool(url_pattern.match(text))
