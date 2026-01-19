from telegram import Update
from telegram.ext import ContextTypes
from bot.database import Database

db = Database()

async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Auto-reply added")

async def list_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Auto-replies list")

async def delete_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Auto-reply deleted")
