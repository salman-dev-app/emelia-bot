from telegram import Update, ChatPermissions
from telegram.ext import ContextTypes
from datetime import timedelta

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"🚫 {user.first_name} banned.")

async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user.id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(hours=24)
        )
        await update.message.reply_text(f"🔇 {user.first_name} muted.")

async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        count = int(context.args[0])
        await context.bot.purge_chat_messages(update.effective_chat.id, count + 1)
