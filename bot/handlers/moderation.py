from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from bot.database import Database
from bot.config import Config
from datetime import timedelta, datetime

db = Database()

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("❌ Reply to a user to ban them.")
    
    user = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.effective_chat.id, user.id)
    await update.message.reply_text(f"🚫 **{user.first_name}** has been banned.", parse_mode='Markdown')

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        update.effective_chat.id, user.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=datetime.now() + timedelta(hours=24)
    )
    await update.message.reply_text(f"🔇 **{user.first_name}** muted for 24 hours.")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return
    user = update.message.reply_to_message.from_user
    count = db.add_warning(str(update.effective_chat.id), user.id, user.username, "Reason provided by Admin")
    
    await update.message.reply_text(f"⚠️ **{user.first_name}** warned! ({count}/{Config.MAX_WARNINGS})", parse_mode='Markdown')
    if count >= Config.MAX_WARNINGS:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text("🚫 Max warnings reached. User banned.")

async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    count = int(context.args[0])
    await context.bot.purge_chat_messages(update.effective_chat.id, count + 1)
