"""
Handlers Module
Handles incoming Telegram messages and commands.
Manages message routing, AI responses, and error handling.
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes
import ai_service
import config
import chat_logger


logger = logging.getLogger(__name__)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /start command.
    Send welcome message and log the command.
    """
    if not update.message:
        return
    
    # Log the command
    chat_logger.log_message(update)
    
    await update.message.reply_text(
        "Hey there! I'm your AI buddy. Just text me anything and I'll reply! 😄"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle /help command.
    Send help information and log the command.
    """
    if not update.message:
        return
    
    # Log the command
    chat_logger.log_message(update)
    
    await update.message.reply_text(
        "Just send me a message and I'll chat with you! "
        "In groups, tag me first to get a response."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming text messages.
    Routes to AI service and sends response back to user.
    Logs all messages before processing.
    """
    # Validate message exists
    if not update.message or not update.message.text:
        return
    
    # Log the message to chatlogs.json
    chat_logger.log_message(update)
    
    message_type = update.message.chat.type
    text = update.message.text
    
    logger.info(f"Message from user {update.message.chat.id} in {message_type}: {text}")
    
    # Determine response based on chat type
    if message_type == "group":
        # Only respond if bot username is mentioned
        if config.BOT_USERNAME in text:
            # Remove bot username from message
            new_text = text.replace(config.BOT_USERNAME, "").strip()
            response = await ai_service.get_ai_response(new_text)
        else:
            # Ignore messages that don't mention the bot
            return
    else:
        # Private chat - respond to all messages
        response = await ai_service.get_ai_response(text)
    
    logger.info(f"Bot response: {response}")
    
    # Send response back to user
    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle errors that occur during message processing.
    Logs error details for debugging.
    """
    logger.error(f"Update {update} caused error: {context.error}")