import threading
import logging
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.main import main as start_bot
from web.app import run_web_server

# Global logging config
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def run_web():
    """Run Flask Dashboard"""
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Web Dashboard error: {e}")

if __name__ == '__main__':
    logger.info("🚀 Emelia Bot System Starting...")
    
    # Start Web Dashboard in a separate thread
    web_thread = threading.Thread(target=run_web, daemon=True)
    web_thread.start()
    
    # Run Bot in the main thread
    try:
        start_bot()
    except KeyboardInterrupt:
        logger.info("Stopped by user.")
    except Exception as e:
        logger.error(f"❌ CRITICAL FATAL ERROR: {e}", exc_info=True)
