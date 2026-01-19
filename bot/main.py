import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from bot.config import Config, COMMANDS
from bot.database import Database
from bot.services.scheduler import PostScheduler
from bot.handlers import admin, channel, music, moderation, analytics, utility, auto_reply

# Logging
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
        
        # Build application - The v20 way
        self.application = Application.builder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        app = self.application
        
        # System
        app.add_handler(CommandHandler("start", self.start_command))
        app.add_handler(CommandHandler("help", self.help_command))
        
        # Channel Management
        app.add_handler(CommandHandler("connect", channel.connect_channel))
        app.add_handler(CommandHandler("channels", channel.list_channels))
        
        # Features
        app.add_handler(CommandHandler("play", music.play_song))
        app.add_handler(CommandHandler("schedule", admin.schedule_post))
        app.add_handler(CommandHandler("ban", moderation.ban_user))
        app.add_handler(CommandHandler("mute", moderation.mute_user))
        app.add_handler(CommandHandler("warn", moderation.warn_user))
        app.add_handler(CommandHandler("purge", moderation.purge_messages))
        
        # Utilities
        app.add_handler(CommandHandler("broadcast", utility.broadcast_message))
        app.add_handler(CommandHandler("translate", utility.translate_text))
        
        # Auto Replies
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_messages))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in Config.ADMIN_IDS:
            return
        await update.message.reply_text("🤖 **Emelia Advanced Bot Online**\nUse /help for commands.", parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = "📚 **All Feature Commands**\n\n"
        for cmd, desc in list(COMMANDS.items())[:25]:
            help_text += f"`{cmd}` - {desc}\n"
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def handle_messages(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Auto-reply logic is handled here
        pass

    async def post_init(self, application: Application) -> None:
        """Start background services after bot is ready"""
        asyncio.create_task(self.scheduler.start(application.bot))
        logger.info("Background services initialized.")

    def run(self):
        """Run the bot"""
        self.application.post_init = self.post_init
        logger.info("Bot is starting polling...")
        # run_polling is the standard v20 method
        self.application.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

def main():
    try:
        bot = EmeliaBot()
        bot.run()
    except Exception as e:
        logger.error(f"Critical Bot Failure: {e}")

if __name__ == '__main__':
    main()
