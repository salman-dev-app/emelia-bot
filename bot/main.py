import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from bot.config import Config, COMMANDS
from bot.database import Database
from bot.services.scheduler import PostScheduler
from bot.handlers import admin, channel, music, moderation, analytics, utility, auto_reply

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmeliaBot:
    def __init__(self):
        Config.validate()
        self.db = Database()
        self.scheduler = PostScheduler(self.db)
        # Use ApplicationBuilder for v20+
        self.application = ApplicationBuilder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        app = self.application
        # Core
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("help", self.help))
        # Features
        app.add_handler(CommandHandler("connect", channel.connect_channel))
        app.add_handler(CommandHandler("play", music.play_song))
        app.add_handler(CommandHandler("schedule", admin.schedule_post))
        app.add_handler(CommandHandler("ban", moderation.ban_user))
        app.add_handler(CommandHandler("mute", moderation.mute_user))
        app.add_handler(CommandHandler("purge", moderation.purge_messages))
        # Auto-replies
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_msg))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id in Config.ADMIN_IDS:
            await update.message.reply_text("🤖 **Bot Active**", parse_mode='Markdown')

    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("📚 Use /connect to start.")

    async def handle_msg(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass

    async def post_init(self, application):
        asyncio.create_task(self.scheduler.start(application.bot))

    def run(self):
        self.application.post_init = self.post_init
        self.application.run_polling(drop_pending_updates=True)

def main():
    try:
        bot = EmeliaBot()
        bot.run()
    except Exception as e:
        logger.error(f"Critical Failure: {e}")

if __name__ == '__main__':
    main()
