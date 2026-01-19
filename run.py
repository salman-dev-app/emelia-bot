import threading
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.main import main as start_bot
from web.app import run_web_server

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_web():
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Web Dashboard failed to start: {e}")

if __name__ == '__main__':
    logger.info("🚀 Starting Emelia Bot System...")
    
    # Start Web Dashboard in background
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Start Bot in main thread
    try:
        start_bot()
    except Exception as e:
        logger.error(f"❌ Fatal Error: {e}", exc_info=True)
