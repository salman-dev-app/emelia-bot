import yt_dlp
import os
from telegram import Update
from telegram.ext import ContextTypes

async def play_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Usage: `/play song_name`", parse_mode='Markdown')
    
    query = " ".join(context.args)
    m = await update.message.reply_text(f"🔍 Searching for `{query}`...", parse_mode='Markdown')
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'data/music_cache/%(title)s.%(ext)s',
        'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
        'quiet': True, 'noplaylist': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            file_path = f"data/music_cache/{info['title']}.mp3"
            
            await update.message.reply_audio(
                audio=open(file_path, 'rb'),
                caption=f"🎵 **{info['title']}**",
                parse_mode='Markdown'
            )
            await m.delete()
            if os.path.exists(file_path): os.remove(file_path)
    except Exception as e:
        await m.edit_text(f"❌ Error: {str(e)}")

async def stop_music(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⏹️ Music playback stopped.")
