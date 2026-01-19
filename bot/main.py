import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

from bot.config import Config, COMMANDS
from bot.database import Database
from bot.services.scheduler import PostScheduler
from bot.handlers import admin, channel, music, moderation, utility

logger = logging.getLogger(__name__)

class EmeliaBot:
    def __init__(self):
        Config.validate()
        self.db = Database()
        self.scheduler = PostScheduler(self.db)
        self.application = ApplicationBuilder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        app = self.application
        app.add_handler(CommandHandler("start", self.start))
        app.add_handler(CommandHandler("connect", channel.connect_channel))
        app.add_handler(CommandHandler("play", music.play_song))
        app.add_handler(CommandHandler("ban", moderation.ban_user))
        app.add_handler(CommandHandler("mute", moderation.mute_user))
        app.add_handler(CommandHandler("purge", moderation.purge_messages))
        app.add_handler(CommandHandler("schedule", admin.schedule_post))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 **Emelia Bot Online (Python 3.12 Stable)**", parse_mode='Markdown')

    async def post_init(self, application):
        asyncio.create_task(self.scheduler.start(application.bot))

    def run(self):
        self.application.post_init = self.post_init
        logger.info("Bot starting in polling mode...")
        self.application.run_polling(drop_pending_updates=True)

def main():
    bot = EmeliaBot()
    bot.run()
