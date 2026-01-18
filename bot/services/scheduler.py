import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PostScheduler:
    """Handle scheduled post delivery"""
    
    def __init__(self, database):
        self.db = database
        self.running = False
    
    async def start(self, bot):
        """Start the scheduler loop"""
        self.running = True
        logger.info("Post scheduler started")
        
        while self.running:
            try:
                await self.process_pending_posts(bot)
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                await asyncio.sleep(60)
    
    async def process_pending_posts(self, bot):
        """Process and send pending posts"""
        posts = self.db.get_pending_posts()
        
        for post in posts:
            try:
                # Send the post
                await bot.send_message(
                    chat_id=post['channel_id'],
                    text=post['message_text']
                )
                
                # Update status
                self.db.update_post_status(post['id'], 'sent')
                logger.info(f"Sent scheduled post {post['id']}")
                
            except Exception as e:
                logger.error(f"Failed to send post {post['id']}: {e}")
                self.db.update_post_status(post['id'], 'failed')
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Post scheduler stopped")
