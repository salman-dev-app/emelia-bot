from telegram import Update
from telegram.ext import ContextTypes
from bot.database import Database
from bot.config import Config

db = Database()

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔇 User muted")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔊 User unmuted")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 User banned")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ User unbanned")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ User warned")

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👢 User kicked")

async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗑️ Messages purged")
