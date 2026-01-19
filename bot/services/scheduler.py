import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PostScheduler:
    def __init__(self, database):
        self.db = database
        self.running = False

    async def start(self, bot_instance):
        """Background loop to check for scheduled posts"""
        self.running = True
        logger.info("Post scheduler service is active.")
        
        while self.running:
            try:
                # Fetch posts ready to be sent
                posts = self.db.get_pending_posts()
                for post in posts:
                    try:
                        await bot_instance.send_message(
                            chat_id=post['channel_id'], 
                            text=post['message_text']
                        )
                        self.db.update_post_status(post['id'], 'sent')
                    except Exception as send_error:
                        logger.error(f"Failed to send post {post['id']}: {send_error}")
                        self.db.update_post_status(post['id'], 'failed')
                
            except Exception as e:
                logger.error(f"Scheduler Loop Error: {e}")
            
            # Check every 60 seconds
            await asyncio.sleep(60)
