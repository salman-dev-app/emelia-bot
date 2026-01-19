import threading
import logging
import sys
import os
import asyncio

# Ensure project root is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.main import main as start_bot
from web.app import run_web_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_dashboard():
    """Start Flask without signal handlers to avoid conflict with Bot"""
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Dashboard Error: {e}")

if __name__ == '__main__':
    logger.info("🚀 Starting Emelia Bot...")
    
    # Run dashboard in a background thread
    web_thread = threading.Thread(target=start_dashboard, daemon=True)
    web_thread.start()
    
    # Start the Bot (This must be in the main thread)
    start_bot()
