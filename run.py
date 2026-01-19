import threading
import logging
import sys
import os

# Add directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from bot.main import main as start_bot
from web.app import run_web_server

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_dashboard():
    try:
        run_web_server()
    except Exception as e:
        logger.error(f"Dashboard Error: {e}")

if __name__ == '__main__':
    # Start dashboard thread
    d_thread = threading.Thread(target=start_dashboard, daemon=True)
    d_thread.start()
    
    # Start Bot
    logger.info("🚀 Launching Emelia Bot System...")
    start_bot()
