import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from bot.config import Config, COMMANDS
from bot.database import Database
from bot.handlers import admin, channel, music, moderation, analytics, utility, auto_reply
from bot.services.scheduler import PostScheduler

logger = logging.getLogger(__name__)

class EmeliaBot:
    def __init__(self):
        Config.validate()
        self.db = Database()
        self.scheduler = PostScheduler(self.db)
        self.app = Application.builder().token(Config.BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        # Basic
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Features
        self.app.add_handler(CommandHandler("connect", channel.connect_channel))
        self.app.add_handler(CommandHandler("play", music.play_song))
        self.app.add_handler(CommandHandler("schedule", admin.schedule_post))
        self.app.add_handler(CommandHandler("ban", moderation.ban_user))
        self.app.add_handler(CommandHandler("mute", moderation.mute_user))
        self.app.add_handler(CommandHandler("warn", moderation.warn_user))
        self.app.add_handler(CommandHandler("purge", moderation.purge_messages))
        self.app.add_handler(CommandHandler("broadcast", utility.broadcast_message))
        self.app.add_handler(CommandHandler("translate", utility.translate_text))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id not in Config.ADMIN_IDS: return
        await update.message.reply_text("🤖 **Emelia Bot is Online**\nType /help to see all 50+ features.", parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = "📚 **Commands**\n\n"
        for cmd, desc in list(COMMANDS.items())[:20]:
            help_text += f"`{cmd}` - {desc}\n"
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def post_init(self, application: Application):
        asyncio.create_task(self.scheduler.start(application.bot))

    def run(self):
        self.app.post_init = self.post_init
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

def main():
    bot_instance = EmeliaBot()
    bot_instance.run()
