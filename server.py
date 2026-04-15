"""
Server Module
Main entry point for the Telegram bot application.
Configures handlers, sets up logging, and starts the bot.
"""
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import config
import handlers
import chat_logger


# Configure logging for production
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main function to start the Telegram bot.
    Initializes application, registers handlers, and starts polling.
    """
    # Ensure chatlogs.json exists
    chat_logger.ensure_file_exists()
    logger.info("Chat log file initialized")
    
    # Build and configure the bot application
    logger.info("Building Telegram bot application...")
    app = Application.builder().token(config.TOKEN).build()
    
    # Register command handlers
    app.add_handler(CommandHandler("start", handlers.start_command))
    app.add_handler(CommandHandler("help", handlers.help_command))
    
    # Register message handler for text messages
    app.add_handler(MessageHandler(filters.TEXT, handlers.handle_message))
    
    # Register error handler
    app.add_error_handler(handlers.error)
    
    # Start polling for incoming updates
    logger.info("Bot is now polling for messages...")
    app.run_polling(poll_interval=1)


if __name__ == "__main__":
    main()