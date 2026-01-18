# bot/handlers/channel.py
from telegram import Update
from telegram.ext import ContextTypes
from bot.database import Database
from bot.config import Config

db = Database()

async def connect_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Connect a new channel"""
    if update.effective_user.id not in Config.ADMIN_IDS:
        await update.message.reply_text("🚫 Admin only command")
        return
    
    if not context.args:
        await update.message.reply_text(
            "Usage: /connect @channel_username or channel_id"
        )
        return
    
    channel_input = context.args[0]
    
    try:
        # Get channel info
        chat = await context.bot.get_chat(channel_input)
        
        success = db.add_channel(
            str(chat.id),
            chat.title,
            chat.username,
            update.effective_user.id
        )
        
        if success:
            await update.message.reply_text(
                f"✅ Channel connected successfully!\n\n"
                f"📢 Name: {chat.title}\n"
                f"🆔 ID: `{chat.id}`\n"
                f"👤 Username: @{chat.username or 'N/A'}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("⚠️ Channel already connected!")
    
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def list_channels(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all connected channels"""
    if update.effective_user.id not in Config.ADMIN_IDS:
        return
    
    channels = db.get_channels()
    
    if not channels:
        await update.message.reply_text("No channels connected yet.")
        return
    
    msg = "📢 **Connected Channels:**\n\n"
    for idx, ch in enumerate(channels, 1):
        msg += f"{idx}. {ch['channel_name']}\n"
        msg += f"   🆔 `{ch['channel_id']}`\n"
        msg += f"   👤 @{ch['channel_username'] or 'N/A'}\n\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def disconnect_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Disconnect a channel"""
    if update.effective_user.id not in Config.ADMIN_IDS:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /disconnect channel_id")
        return
    
    # Implementation here
    await update.message.reply_text("✅ Channel disconnected")

async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set welcome message for a channel"""
    if update.effective_user.id not in Config.ADMIN_IDS:
        return
    
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /setwelcome channel_id Welcome message here"
        )
        return
    
    # Implementation here
    await update.message.reply_text("✅ Welcome message set!")


# bot/handlers/admin.py
from telegram import Update
from telegram.ext import ContextTypes
from bot.database import Database
from datetime import datetime, timedelta
import pytz

db = Database()

async def schedule_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Schedule a post"""
    if not context.args or len(context.args) < 3:
        await update.message.reply_text(
            "Usage: /schedule channel_id time(YYYY-MM-DD HH:MM) message"
        )
        return
    
    channel_id = context.args[0]
    time_str = f"{context.args[1]} {context.args[2]}"
    message = ' '.join(context.args[3:])
    
    try:
        scheduled_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        post_id = db.add_scheduled_post(channel_id, message, scheduled_time)
        
        await update.message.reply_text(
            f"✅ Post scheduled!\n\n"
            f"📅 Time: {scheduled_time}\n"
            f"📝 ID: {post_id}"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def list_scheduled(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List scheduled posts"""
    posts = db.get_pending_posts()
    
    if not posts:
        await update.message.reply_text("No scheduled posts")
        return
    
    msg = "📅 **Scheduled Posts:**\n\n"
    for post in posts[:10]:
        msg += f"📝 ID: {post['id']}\n"
        msg += f"⏰ Time: {post['scheduled_time']}\n"
        msg += f"📢 Channel: {post['channel_id']}\n\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def save_draft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Save message as draft"""
    await update.message.reply_text("✅ Draft saved!")

async def list_drafts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all drafts"""
    await update.message.reply_text("📝 Your drafts list")

async def publish_draft(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Publish a draft"""
    await update.message.reply_text("✅ Draft published!")

async def pin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pin a message"""
    if update.message.reply_to_message:
        try:
            await update.message.reply_to_message.pin()
            await update.message.reply_text("📌 Message pinned!")
        except Exception as e:
            await update.message.reply_text(f"❌ Error: {str(e)}")
    else:
        await update.message.reply_text("Reply to a message to pin it")

async def unpin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unpin message"""
    try:
        await context.bot.unpin_chat_message(update.effective_chat.id)
        await update.message.reply_text("📍 Message unpinned!")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


# bot/handlers/moderation.py
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mute a user"""
    if not update.message.reply_to_message:
        await update.message.reply_text("Reply to a user's message to mute them")
        return
    
    user = update.message.reply_to_message.from_user
    duration = int(context.args[0]) if context.args else 60  # minutes
    
    try:
        until_date = datetime.now() + timedelta(minutes=duration)
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            permissions={'can_send_messages': False},
            until_date=until_date
        )
        await update.message.reply_text(
            f"🔇 {user.first_name} muted for {duration} minutes"
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ban a user"""
    if not update.message.reply_to_message:
        return
    
    user = update.message.reply_to_message.from_user
    reason = ' '.join(context.args) if context.args else "No reason"
    
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        db.ban_user(
            str(update.effective_chat.id),
            user.id,
            user.username,
            reason,
            update.effective_user.id
        )
        await update.message.reply_text(f"🚫 {user.first_name} has been banned")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Warn a user"""
    if not update.message.reply_to_message:
        return
    
    user = update.message.reply_to_message.from_user
    reason = ' '.join(context.args) if context.args else "Violation"
    
    count = db.add_warning(
        str(update.effective_chat.id),
        user.id,
        user.username,
        reason
    )
    
    await update.message.reply_text(
        f"⚠️ {user.first_name} warned!\n"
        f"Warnings: {count}/{Config.MAX_WARNINGS}\n"
        f"Reason: {reason}"
    )
    
    if count >= Config.MAX_WARNINGS:
        await ban_user(update, context)

async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Kick a user"""
    if not update.message.reply_to_message:
        return
    
    user = update.message.reply_to_message.from_user
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"👢 {user.first_name} kicked")
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unmute a user"""
    await update.message.reply_text("🔊 User unmuted")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Unban a user"""
    await update.message.reply_text("✅ User unbanned")

async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete multiple messages"""
    await update.message.reply_text("🗑️ Messages purged")


# bot/handlers/music.py
async def play_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Play song from YouTube"""
    if not context.args:
        await update.message.reply_text("Usage: /play song name")
        return
    
    query = ' '.join(context.args)
    await update.message.reply_text(f"🎵 Searching for: {query}...")

async def stop_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stop music"""
    await update.message.reply_text("⏹️ Music stopped")

async def pause_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Pause music"""
    await update.message.reply_text("⏸️ Music paused")

async def resume_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Resume music"""
    await update.message.reply_text("▶️ Music resumed")

async def manage_playlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage playlists"""
    await update.message.reply_text("🎵 Playlist manager")

async def trending_songs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show trending songs"""
    tracks = db.get_trending_tracks(10)
    
    msg = "🔥 **Trending Songs:**\n\n"
    for idx, track in enumerate(tracks, 1):
        msg += f"{idx}. {track['title']}\n"
        msg += f"   ▶️ Plays: {track['play_count']}\n\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')


# bot/handlers/analytics.py
async def channel_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show channel statistics"""
    channel_id = context.args[0] if context.args else str(update.effective_chat.id)
    stats = db.get_channel_stats(channel_id, days=7)
    
    msg = "📊 **Channel Statistics (7 days)**\n\n"
    total_members = sum(s['new_members'] - s['left_members'] for s in stats)
    total_messages = sum(s['messages_count'] for s in stats)
    
    msg += f"👥 Net members: {total_members:+d}\n"
    msg += f"💬 Total messages: {total_messages}\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def daily_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate daily report"""
    await update.message.reply_text("📈 Daily report generated")

async def top_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show top active users"""
    await update.message.reply_text("👥 Top users list")

async def growth_analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show growth analytics"""
    await update.message.reply_text("📈 Growth analytics")


# bot/handlers/utility.py
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Translate text"""
    await update.message.reply_text("🌐 Translation feature")

async def create_poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a poll"""
    await update.message.reply_text("📊 Poll creator")

async def create_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create a quiz"""
    await update.message.reply_text("❓ Quiz creator")

async def set_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set a reminder"""
    await update.message.reply_text("⏰ Reminder set")

async def manage_todo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manage to-do list"""
    await update.message.reply_text("✅ To-do manager")

async def generate_caption(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate caption"""
    await update.message.reply_text("📝 Caption generator")

async def broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Broadcast to all channels"""
    await update.message.reply_text("📢 Broadcast sent")


# bot/handlers/auto_reply.py
async def add_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Add auto-reply"""
    if len(context.args) < 2:
        await update.message.reply_text(
            "Usage: /addreply keyword response text"
        )
        return
    
    keyword = context.args[0]
    response = ' '.join(context.args[1:])
    
    db.add_auto_reply(
        str(update.effective_chat.id),
        keyword,
        response
    )
    
    await update.message.reply_text(
        f"✅ Auto-reply added!\n\n"
        f"Keyword: {keyword}\n"
        f"Response: {response}"
    )

async def list_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List auto-replies"""
    replies = db.get_auto_replies(str(update.effective_chat.id))
    
    if not replies:
        await update.message.reply_text("No auto-replies configured")
        return
    
    msg = "🤖 **Auto-Replies:**\n\n"
    for r in replies:
        msg += f"• {r['keyword']} → {r['response'][:50]}...\n"
    
    await update.message.reply_text(msg, parse_mode='Markdown')

async def delete_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete auto-reply"""
    await update.message.reply_text("✅ Auto-reply deleted")
