import yt_dlp
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

async def play_song(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("COMMAND USAGE: /play [SONG NAME]")
    
    query = " ".join(context.args)
    status_msg = await update.message.reply_text("PROCESS: INITIALIZING SEARCH...")
    
    # Premium YouTube Download Options to bypass detection
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'data/music_cache/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        },
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            await status_msg.edit_text("PROCESS: EXTRACTING DATA...")
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            file_path = f"data/music_cache/{info['title']}.mp3"
            
            # Premium Player Buttons
            keyboard = [[InlineKeyboardButton("TERMINATE", callback_data="stop_music")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_audio(
                audio=open(file_path, 'rb'),
                caption=f"TRACK: {info['title'].upper()}\nSOURCE: YOUTUBE",
                reply_markup=reply_markup
            )
            await status_msg.delete()
            if os.path.exists(file_path): os.remove(file_path)
            
    except Exception as e:
        error_msg = str(e)
        if "Sign in" in error_msg:
            await status_msg.edit_text("ERROR: YOUTUBE SECURITY BLOCK. TRYING ALTERNATIVE SOURCE...")
            # Here you could implement a SoundCloud or other fallback
        else:
            await status_msg.edit_text(f"ERROR: {error_msg}")
