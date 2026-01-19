from telegram import Update
from telegram.ext import ContextTypes
from bot.database import Database
from datetime import datetime

db = Database()

async def schedule_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 3:
        return await update.message.reply_text("❌ Usage: `/schedule <channel_id> <YYYY-MM-DD HH:MM> <text>`", parse_mode='Markdown')
    
    channel_id = context.args[0]
    time_str = f"{context.args[1]} {context.args[2]}"
    text = " ".join(context.args[3:])
    
    try:
        scheduled_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        db.add_scheduled_post(channel_id, text, scheduled_time)
        await update.message.reply_text(f"✅ Post scheduled for `{scheduled_time}`", parse_mode='Markdown')
    except Exception as e:
        await update.message.reply_text(f"❌ Date error: {e}")
