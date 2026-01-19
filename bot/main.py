import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from bot.config import Config, COMMANDS
from bot.database import Database
from bot.services.scheduler import PostScheduler
from bot.handlers import admin, channel, music, moderation, utility

logger = logging.getLogger(__name__)

async def start_emelia():
    """Manual async startup to bypass the 'Updater' bug in Python 3.13"""
    Config.validate()
    db = Database()
    scheduler = PostScheduler(db)

    # Initialize Application
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()

    # Register Handlers
    application.add_handler(CommandHandler("start", lambda u, c: u.message.reply_text("🤖 Emelia Online")))
    application.add_handler(CommandHandler("connect", channel.connect_channel))
    application.add_handler(CommandHandler("play", music.play_song))
    application.add_handler(CommandHandler("ban", moderation.ban_user))
    application.add_handler(CommandHandler("mute", moderation.mute_user))
    application.add_handler(CommandHandler("purge", moderation.purge_messages))
    application.add_handler(CommandHandler("schedule", admin.schedule_post))

    # Start Scheduler
    asyncio.create_task(scheduler.start(application.bot))

    # Initialize and Start the Application manually
    async with application:
        await application.initialize()
        await application.start()
        
        # Start Polling WITHOUT signal handlers (stops the 'Updater' crash)
        logger.info("Bot Polling started (Signal Handlers Disabled for Stability)")
        await application.updater.start_polling(drop_pending_updates=True)
        
        # Keep the bot running until the program is stopped
        while True:
            await asyncio.sleep(3600)
