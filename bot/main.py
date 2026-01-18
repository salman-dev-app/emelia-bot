import logging
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)
import asyncio
from config import Config
from database import Database
from handlers import (
    admin, channel, music, moderation, 
    analytics, utility, auto_reply
)
from services.scheduler import PostScheduler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('data/logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EmeliaBot:
    def __init__(self):
        Config.validate()
        self.db = Database()
        self.application = None
        self.scheduler = PostScheduler(self.db)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        if user_id not in Config.ADMIN_IDS:
            await update.message.reply_text(
                "🚫 Access Denied. This bot is for authorized admins only."
            )
            return
        
        welcome_msg = f"""
🤖 **Welcome to Emelia Bot!**

I'm your advanced Telegram channel management assistant.

**Quick Start:**
/help - View all commands
/connect - Connect a channel
/channels - View connected channels

**Top Features:**
✅ Multi-channel management
✅ Smart scheduling & drafts
✅ Music playback from YouTube
✅ Auto-moderation & spam filter
✅ Analytics & reports
✅ Auto-replies & AI responses
✅ Translation & utilities

Type /help to see all 50+ commands!
        """
        
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show all commands"""
        from config import COMMANDS
        
        help_text = "📚 **Emelia Bot Commands**\n\n"
        
        categories = {
            'Channel Management': ['/connect', '/channels', '/disconnect', '/setwelcome'],
            'Posts & Scheduling': ['/schedule', '/scheduled', '/draft', '/publish', '/pin'],
            'Moderation': ['/mute', '/ban', '/warn', '/kick', '/purge'],
            'Music': ['/play', '/stop', '/pause', '/playlist', '/trending'],
            'Utilities': ['/translate', '/poll', '/remind', '/todo', '/caption'],
            'Analytics': ['/stats', '/report', '/topusers', '/growth'],
            'Settings': ['/settings', '/language', '/timezone'],
        }
        
        for category, cmds in categories.items():
            help_text += f"\n**{category}:**\n"
            for cmd in cmds:
                if cmd in COMMANDS:
                    help_text += f"`{cmd}` - {COMMANDS[cmd]}\n"
        
        help_text += f"\n💡 Total: {len(COMMANDS)} commands available"
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot status"""
        channels = self.db.get_channels()
        
        status_msg = f"""
📊 **Emelia Bot Status**

✅ Bot is running
🔗 Connected channels: {len(channels)}
👥 Admins: {len(Config.ADMIN_IDS)}
📅 Uptime: Active

**Recent Activity:**
• Scheduled posts: {len(self.db.get_pending_posts())}
• Auto-replies active
• Music cache ready
        """
        
        await update.message.reply_text(status_msg, parse_mode='Markdown')
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages for auto-reply"""
        if not update.message or not update.message.text:
            return
        
        chat_id = str(update.effective_chat.id)
        message_text = update.message.text.lower()
        
        # Check auto-replies
        replies = self.db.get_auto_replies(chat_id)
        
        for reply in replies:
            keyword = reply['keyword'].lower()
            match_type = reply['match_type']
            
            matched = False
            if match_type == 'exact' and message_text == keyword:
                matched = True
            elif match_type == 'contains' and keyword in message_text:
                matched = True
            elif match_type == 'starts' and message_text.startswith(keyword):
                matched = True
            
            if matched:
                await update.message.reply_text(reply['response'])
                break
    
    def setup_handlers(self):
        """Register all command handlers"""
        app = self.application
        
        # Basic commands
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        app.add_handler(CommandHandler("status", self.status_command))
        
        # Channel management
        app.add_handler(CommandHandler("connect", channel.connect_channel))
        app.add_handler(CommandHandler("channels", channel.list_channels))
        app.add_handler(CommandHandler("disconnect", channel.disconnect_channel))
        app.add_handler(CommandHandler("setwelcome", channel.set_welcome))
        
        # Post management
        app.add_handler(CommandHandler("schedule", admin.schedule_post))
        app.add_handler(CommandHandler("scheduled", admin.list_scheduled))
        app.add_handler(CommandHandler("draft", admin.save_draft))
        app.add_handler(CommandHandler("drafts", admin.list_drafts))
        app.add_handler(CommandHandler("publish", admin.publish_draft))
        app.add_handler(CommandHandler("pin", admin.pin_message))
        app.add_handler(CommandHandler("unpin", admin.unpin_message))
        
        # Moderation
        app.add_handler(CommandHandler("mute", moderation.mute_user))
        app.add_handler(CommandHandler("unmute", moderation.unmute_user))
        app.add_handler(CommandHandler("ban", moderation.ban_user))
        app.add_handler(CommandHandler("unban", moderation.unban_user))
        app.add_handler(CommandHandler("warn", moderation.warn_user))
        app.add_handler(CommandHandler("kick", moderation.kick_user))
        app.add_handler(CommandHandler("purge", moderation.purge_messages))
        
        # Auto-reply
        app.add_handler(CommandHandler("addreply", auto_reply.add_reply))
        app.add_handler(CommandHandler("replies", auto_reply.list_replies))
        app.add_handler(CommandHandler("delreply", auto_reply.delete_reply))
        
        # Music
        app.add_handler(CommandHandler("play", music.play_song))
        app.add_handler(CommandHandler("stop", music.stop_music))
        app.add_handler(CommandHandler("pause", music.pause_music))
        app.add_handler(CommandHandler("resume", music.resume_music))
        app.add_handler(CommandHandler("playlist", music.manage_playlist))
        app.add_handler(CommandHandler("trending", music.trending_songs))
        
        # Utilities
        app.add_handler(CommandHandler("translate", utility.translate_text))
        app.add_handler(CommandHandler("poll", utility.create_poll))
        app.add_handler(CommandHandler("quiz", utility.create_quiz))
        app.add_handler(CommandHandler("remind", utility.set_reminder))
        app.add_handler(CommandHandler("todo", utility.manage_todo))
        app.add_handler(CommandHandler("caption", utility.generate_caption))
        app.add_handler(CommandHandler("broadcast", utility.broadcast_message))
        
        # Analytics
        app.add_handler(CommandHandler("stats", analytics.channel_stats))
        app.add_handler(CommandHandler("report", analytics.daily_report))
        app.add_handler(CommandHandler("topusers", analytics.top_users))
        app.add_handler(CommandHandler("growth", analytics.growth_analytics))
        
        # Message handler for auto-reply
        app.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            self.message_handler
        ))
        
        logger.info("All handlers registered successfully")
    
    async def post_init(self, application: Application):
        """Post initialization tasks"""
        # Start scheduler
        asyncio.create_task(self.scheduler.start(application.bot))
        logger.info("Post scheduler started")
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Emelia Bot...")
        
        # Create application
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        
        # Setup handlers
        self.setup_handlers()
        
        # Post init
        self.application.post_init = self.post_init
        
        # Run bot
        if Config.USE_WEBHOOK and Config.WEBHOOK_URL:
            logger.info(f"Starting webhook mode: {Config.WEBHOOK_URL}")
            self.application.run_webhook(
                listen="0.0.0.0",
                port=Config.WEB_PORT,
                url_path=Config.BOT_TOKEN,
                webhook_url=f"{Config.WEBHOOK_URL}/{Config.BOT_TOKEN}"
            )
        else:
            logger.info("Starting polling mode...")
            self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    """Main entry point"""
    try:
        bot = EmeliaBot()
        bot.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
