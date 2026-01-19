import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from bot.config import Config, COMMANDS
from bot.database import Database
from bot.services.scheduler import PostScheduler
from bot.handlers import admin, channel, music, moderation, analytics, utility, auto_reply

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class EmeliaBot:
    def __init__(self):
        Config.validate()
        self.db = Database()
        self.scheduler = PostScheduler(self.db)
        
        # Initialize Application (The modern way in v20)
        self.application = ApplicationBuilder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        app = self.application
        
        # System Commands
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # Feature Commands
        app.add_handler(CommandHandler("connect", channel.connect_channel))
        app.add_handler(CommandHandler("channels", channel.list_channels))
        app.add_handler(CommandHandler("play", music.play_song))
        app.add_handler(CommandHandler("schedule", admin.schedule_post))
        app.add_handler(CommandHandler("ban", moderation.ban_user))
        app.add_handler(CommandHandler("mute", moderation.mute_user))
        app.add_handler(CommandHandler("warn", moderation.warn_user))
        app.add_handler(CommandHandler("purge", moderation.purge_messages))
        app.add_handler(CommandHandler("broadcast", utility.broadcast_message))
        
        # Message Handler for Auto-Reply
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_auto_reply))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in Config.ADMIN_IDS: return
        await update.message.reply_text("🤖 **Emelia Bot Online**\nType /help to see all features.", parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = "📚 **Available Commands**\n\n"
        # Only show first 20 to avoid message length limits
        for cmd, desc in list(COMMANDS.items())[:20]:
            help_text += f"`{cmd}` - {desc}\n"
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_auto_reply(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Implementation for Keyword Replies
        pass

    async def post_init(self, application):
        """Task to run after the bot starts"""
        asyncio.create_task(self.scheduler.start(application.bot))
        logger.info("Background Scheduler Started.")

    def run(self):
        """Run the bot in polling mode"""
        self.application.post_init = self.post_init
        logger.info("Starting polling...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    try:
        bot_instance = EmeliaBot()
        bot_instance.run()
    except Exception as e:
        logger.error(f"Failed to launch bot: {e}")
