import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self, database):
        self.db = database
        self.running = False

    async def start(self, bot):
        self.running = True
        while self.running:
            try:
                posts = self.db.get_pending_posts()
                for post in posts:
                    await bot.send_message(chat_id=post['channel_id'], text=post['message_text'])
                    self.db.update_post_status(post['id'], 'sent')
                    logger.info(f"Sent scheduled post {post['id']}")
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(60)
