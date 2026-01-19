import sys
import os
import logging

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Main entry point"""
    try:
        logger.info("=" * 60)
        logger.info("🤖 Starting Emelia Bot...")
        logger.info("=" * 60)
        
        # Import and run the bot
        from bot.main import main as run_bot
        run_bot()
        
    except ImportError as e:
        logger.error(f"❌ Import Error: {e}")
        logger.error("Make sure all files are present:")
        logger.error("  - bot/main.py")
        logger.error("  - bot/config.py")
        logger.error("  - bot/database.py")
        raise
        
    except Exception as e:
        logger.error(f"❌ Fatal Error: {e}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
