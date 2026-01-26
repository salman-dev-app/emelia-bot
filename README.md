# 🤖 Emelia - Advanced Telegram Bot

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

**Emelia** is a powerful, production-ready Telegram bot for managing channels with 50+ features, built for free deployment on Render + GitHub.

## ✨ Features (50+)

### 📢 Channel Management
1. ✅ Connect multiple channels
2. ✅ Admin-only command system
3. ✅ Custom welcome messages
4. ✅ Auto pin/unpin messages
5. ✅ Channel disconnect

### 📅 Post Management
6. ✅ Advanced post scheduling
7. ✅ View scheduled posts
8. ✅ Cancel scheduled posts
9. ✅ Save drafts
10. ✅ Publish drafts
11. ✅ Draft management

### 🎵 Music System
12. ✅ Play YouTube audio
13. ✅ Stop music
14. ✅ Pause music
15. ✅ Resume music
16. ✅ Playlist creation
17. ✅ Playlist management
18. ✅ Track statistics
19. ✅ Trending songs
20. ✅ Play count tracking

### 🛡️ Moderation
21. ✅ Mute users (timed)
22. ✅ Unmute users
23. ✅ Ban users
24. ✅ Unban users
25. ✅ Warning system
26. ✅ Kick users
27. ✅ Message purge
28. ✅ Spam detection
29. ✅ Auto link deletion
30. ✅ Member join/leave logs

### 🤖 Auto-Reply & AI
31. ✅ Keyword-based auto-replies
32. ✅ Multiple match types (exact, contains, starts)
33. ✅ Channel-specific replies
34. ✅ Reply management
35. ✅ Smart responses

### 🌐 Utilities
36. ✅ Text translation
37. ✅ Poll creation
38. ✅ Quiz creation
39. ✅ Reminder system
40. ✅ To-do list manager
41. ✅ Caption generator
42. ✅ Broadcast messaging

### 📊 Analytics
43. ✅ Channel statistics
44. ✅ Daily activity reports
45. ✅ Top active users
46. ✅ Growth analytics
47. ✅ Engagement metrics
48. ✅ Best posting time analysis
49. ✅ Member tracking
50. ✅ Message counting

### 🖥️ Web Dashboard
- Clean, responsive interface
- Login-protected access
- View connected channels
- Monitor scheduled posts
- Analytics visualization
- Bot status monitoring

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Telegram account
- GitHub account (free)
- Render account (free)

### Step 1: Get Your Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow instructions to create your bot
4. Copy the **bot token** (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get API Credentials

1. Visit https://my.telegram.org
2. Login with your phone number
3. Click "API development tools"
4. Create a new application
5. Copy **API ID** and **API Hash**

### Step 3: Get Your User ID

1. Open Telegram and search for [@userinfobot](https://t.me/userinfobot)
2. Send `/start`
3. Copy your **User ID** (numbers only)

### Step 4: Deploy to GitHub

```bash
# Clone or fork this repository
git clone https://github.com/yourusername/Emelia-bot.git
cd Emelia-bot

# Create .env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Edit `.env`:
```env
BOT_TOKEN=your_bot_token_here
API_ID=your_api_id
API_HASH=your_api_hash
ADMIN_IDS=your_user_id
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=your_secure_password
```

```bash
# Push to GitHub
git add .
git commit -m "Initial setup"
git push origin main
```

### Step 5: Deploy to Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select **Emelia-bot** repository
5. Configure:
   - **Name**: `emelia-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python run.py`
   - **Instance Type**: `Free`

6. Add Environment Variables:
   - `BOT_TOKEN`: Your bot token
   - `API_ID`: Your API ID
   - `API_HASH`: Your API hash
   - `ADMIN_IDS`: Your user ID(s)
   - `DASHBOARD_USERNAME`: admin
   - `DASHBOARD_PASSWORD`: Your password
   - `PORT`: 5000

7. Click **"Create Web Service"**

8. Wait 5-10 minutes for deployment

### Step 6: Access Your Bot

**Telegram Bot:**
- Open Telegram
- Search for your bot (@yourbotname)
- Send `/start`

**Web Dashboard:**
- Visit: `https://emelia-bot.onrender.com`
- Login with your credentials

---

## 📋 Complete Command List

### Basic Commands
```
/start - Start the bot
/help - View all commands
/status - Check bot status
```

### Channel Management
```
/connect @channel - Connect a channel
/channels - List connected channels
/disconnect <id> - Disconnect channel
/setwelcome <id> <message> - Set welcome message
```

### Post Management
```
/schedule <id> <time> <message> - Schedule post
/scheduled - View scheduled posts
/cancel <post_id> - Cancel scheduled post
/draft <message> - Save as draft
/drafts - View drafts
/publish <draft_id> - Publish draft
/pin - Pin message (reply to message)
/unpin - Unpin message
```

### Moderation
```
/mute <minutes> - Mute user (reply to message)
/unmute - Unmute user (reply)
/ban <reason> - Ban user (reply)
/unban - Unban user
/warn <reason> - Warn user (reply)
/kick - Kick user (reply)
/purge <count> - Delete messages
```

### Auto-Reply
```
/addreply <keyword> <response> - Add auto-reply
/replies - List auto-replies
/delreply <id> - Delete auto-reply
```

### Music
```
/play <song name> - Play from YouTube
/stop - Stop music
/pause - Pause music
/resume - Resume music
/playlist - Manage playlists
/trending - Show trending songs
```

### Utilities
```
/translate <text> - Translate text
/poll <question> - Create poll
/quiz <question> - Create quiz
/remind <time> <message> - Set reminder
/todo <task> - Manage to-do
/caption - Generate caption
/broadcast <message> - Send to all channels
```

### Analytics
```
/stats <channel_id> - Channel statistics
/report - Daily activity report
/topusers - Most active users
/growth - Growth analytics
```

---

## 🗂️ Project Structure

```
Emelia-bot/
├── bot/
│   ├── main.py              # Bot core
│   ├── config.py            # Configuration
│   ├── database.py          # Database operations
│   ├── handlers/            # Command handlers
│   │   ├── admin.py
│   │   ├── channel.py
│   │   ├── music.py
│   │   ├── moderation.py
│   │   ├── analytics.py
│   │   ├── utility.py
│   │   └── auto_reply.py
│   └── services/            # Background services
│       ├── scheduler.py
│       └── music_service.py
├── web/
│   ├── app.py               # Flask app
│   ├── templates/           # HTML templates
│   └── static/              # CSS/JS
├── data/
│   ├── emelia.db            # SQLite database
│   └── logs/                # Log files
├── requirements.txt
├── render.yaml
├── run.py                   # Main entry
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | ✅ Yes | Telegram bot token |
| `API_ID` | ❌ No | Telegram API ID (recommended) |
| `API_HASH` | ❌ No | Telegram API hash (recommended) |
| `ADMIN_IDS` | ✅ Yes | Comma-separated admin user IDs |
| `SECRET_KEY` | ❌ No | Flask secret key (auto-generated) |
| `DASHBOARD_USERNAME` | ❌ No | Dashboard login (default: admin) |
| `DASHBOARD_PASSWORD` | ✅ Yes | Dashboard password |
| `PORT` | ❌ No | Web port (default: 5000) |
| `TIMEZONE` | ❌ No | Timezone (default: UTC) |

---

## 🛠️ Local Development

```bash
# Clone repository
git clone https://github.com/yourusername/Emelia-bot.git
cd Emelia-bot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your credentials

# Run bot
python run.py
```

Access dashboard at: http://localhost:5000

---

## 📊 Database Schema

Emelia uses SQLite with the following tables:

- **channels** - Connected channels
- **admins** - Bot administrators
- **scheduled_posts** - Queued messages
- **drafts** - Saved drafts
- **auto_replies** - Keyword responses
- **music_tracks** - Song history
- **playlists** - User playlists
- **user_actions** - Activity logs
- **analytics_daily** - Daily metrics
- **banned_users** - Moderation records
- **user_warnings** - Warning system
- **reminders** - Reminder system
- **todos** - To-do lists
- **settings** - Bot configuration

---

## 🔒 Security

- ✅ Admin-only command authentication
- ✅ Login-protected dashboard
- ✅ Session management
- ✅ Secure password storage
- ✅ Rate limiting
- ✅ Input validation

---

## 🐛 Troubleshooting

### Bot not responding
1. Check bot token in environment variables
2. Verify admin user ID is correct
3. Check Render logs for errors

### Web dashboard not loading
1. Verify PORT environment variable
2. Check Render service status
3. Clear browser cache

### Commands not working
1. Ensure you're an authorized admin
2. Check bot has admin rights in channel
3. Verify command syntax

### Database errors
1. Check write permissions
2. Verify data/ directory exists
3. Restart the service

---

## 📈 Performance Tips

- Keep music cache under 500MB
- Archive old analytics (90+ days)
- Limit auto-replies to essential keywords
- Use scheduling for off-peak hours

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

---

## 📝 License

MIT License - feel free to use and modify!

---

## 🆘 Support

- 📧 Email: support@emelia.bot
- 💬 Telegram: @EmeliaSupport
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/Emelia-bot/issues)

---

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- [Flask](https://flask.palletsprojects.com/)
- [Render](https://render.com)

---

## 📌 Roadmap

### Version 2.0 (Planned)
- [ ] Multi-language support
- [ ] Advanced analytics dashboard
- [ ] AI-powered content suggestions
- [ ] Video download & processing
- [ ] Custom plugin system
- [ ] API for external integrations

---

**Made with ❤️ by Emelia Team**

⭐ Star this repo if you find it useful!
