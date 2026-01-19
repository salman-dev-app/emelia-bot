import threading
import logging
import sys
import os
import asyncio
from bot.main import start_emelia
from web.app import run_web_server

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_flask():
    """Run Flask in a separate thread"""
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Flask error: {e}")

if __name__ == '__main__':
    logger.info("🚀 Starting Emelia Bot on Python 3.13...")
    
    # 1. Start Flask in background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # 2. Run the Bot in the main thread using the new async entry point
    try:
        asyncio.run(start_emelia())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logger.error(f"Main Loop Error: {e}", exc_info=True)
