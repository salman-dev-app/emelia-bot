import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Telegram Bot Configuration
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    API_ID = os.getenv('API_ID')
    API_HASH = os.getenv('API_HASH')
    
    # Admin Configuration (Your Telegram User ID)
    ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/emelia.db')
    
    # Web Dashboard
    SECRET_KEY = os.getenv('SECRET_KEY', 'emelia-secret-key-change-this')
    WEB_PORT = int(os.getenv('PORT', 5000))
    WEB_HOST = os.getenv('WEB_HOST', '0.0.0.0')
    DASHBOARD_USERNAME = os.getenv('DASHBOARD_USERNAME', 'admin')
    DASHBOARD_PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'emelia2024')
    
    # Bot Settings
    WEBHOOK_URL = os.getenv('WEBHOOK_URL', '')
    USE_WEBHOOK = os.getenv('USE_WEBHOOK', 'false').lower() == 'true'
    
    # Music Settings
    MUSIC_CACHE_DIR = 'data/music_cache'
    MAX_CACHE_SIZE_MB = 500
    
    # Moderation
    MAX_WARNINGS = 3
    AUTO_DELETE_LINKS = True
    SPAM_THRESHOLD = 5  # messages per minute
    
    # Analytics
    ANALYTICS_RETENTION_DAYS = 90
    
    # Scheduling
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ['BOT_TOKEN', 'ADMIN_IDS']
        missing = [key for key in required if not getattr(cls, key)]
        
        if missing:
            raise ValueError(f"Missing required config: {', '.join(missing)}")
        
        # Create necessary directories
        os.makedirs('data', exist_ok=True)
        os.makedirs('data/logs', exist_ok=True)
        os.makedirs(cls.MUSIC_CACHE_DIR, exist_ok=True)
        
        return True

# Bot Commands Documentation
COMMANDS = {
    # Channel Management
    '/connect': 'Connect a channel to Emelia',
    '/channels': 'List all connected channels',
    '/disconnect': 'Disconnect a channel',
    '/setwelcome': 'Set welcome message',
    '/deletewelcome': 'Remove welcome message',
    
    # Post Management
    '/schedule': 'Schedule a post',
    '/scheduled': 'View scheduled posts',
    '/cancel': 'Cancel scheduled post',
    '/draft': 'Save post as draft',
    '/drafts': 'View saved drafts',
    '/publish': 'Publish a draft',
    '/pin': 'Pin a message',
    '/unpin': 'Unpin message',
    
    # Moderation
    '/mute': 'Mute a user',
    '/unmute': 'Unmute a user',
    '/ban': 'Ban a user',
    '/unban': 'Unban a user',
    '/warn': 'Warn a user',
    '/warnings': 'Check user warnings',
    '/kick': 'Kick a user',
    '/purge': 'Delete multiple messages',
    
    # Auto Reply
    '/addreply': 'Add keyword auto-reply',
    '/replies': 'List auto-replies',
    '/delreply': 'Delete auto-reply',
    
    # Music
    '/play': 'Play song from YouTube',
    '/stop': 'Stop music',
    '/pause': 'Pause music',
    '/resume': 'Resume music',
    '/playlist': 'Manage playlists',
    '/trending': 'Show trending songs',
    '/nowplaying': 'Current track info',
    
    # Utility
    '/translate': 'Translate text',
    '/poll': 'Create a poll',
    '/quiz': 'Create a quiz',
    '/remind': 'Set a reminder',
    '/todo': 'Manage to-do list',
    '/caption': 'Generate caption',
    '/broadcast': 'Send to all channels',
    
    # Analytics
    '/stats': 'Channel statistics',
    '/report': 'Daily activity report',
    '/topusers': 'Most active users',
    '/growth': 'Growth analytics',
    '/engagement': 'Engagement metrics',
    '/besttime': 'Best posting times',
    
    # Settings
    '/settings': 'Bot settings',
    '/language': 'Change language',
    '/timezone': 'Set timezone',
    '/filters': 'Manage content filters',
    
    # System
    '/help': 'Show all commands',
    '/start': 'Start the bot',
    '/status': 'Bot status',
    '/backup': 'Backup database',
    '/logs': 'View recent logs',
    '/restart': 'Restart bot (admin only)',
}

# Feature Descriptions
FEATURES = [
    "Multi-channel management",
    "Admin authentication system",
    "Custom welcome messages",
    "Auto pin/unpin messages",
    "Advanced post scheduling",
    "Draft save & publish",
    "Keyword-based auto replies",
    "Smart spam detection",
    "Link auto-delete",
    "User mute/ban system",
    "Member activity logging",
    "YouTube audio playback",
    "Music pause/resume",
    "Playlist management",
    "Track play statistics",
    "Trending music tracker",
    "AI-like auto responses",
    "Multi-language translation",
    "Smart caption generator",
    "Poll & quiz creator",
    "Reminder system",
    "To-do list manager",
    "Daily activity reports",
    "Active users ranking",
    "Best posting time analysis",
    "User warnings system",
    "Message purge tool",
    "Broadcast messaging",
    "Channel growth tracking",
    "Engagement analytics",
    "Content filters",
    "Timezone support",
    "Database backup",
    "Activity logs viewer",
    "Bot status monitoring",
    "Web dashboard",
    "Scheduled post viewer",
    "Analytics visualization",
    "Multi-admin support",
    "Custom command prefix",
    "Rate limiting",
    "Message templates",
    "Quick replies",
    "User tagging",
    "Mention notifications",
    "File management",
    "Media compression",
    "Watermark adding",
    "Link shortening",
    "QR code generator",
  ]
