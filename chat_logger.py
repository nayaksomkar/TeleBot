"""
Chat Logger Module
Handles saving all incoming messages to chatlogs.json file.
"""
import json
import os
from datetime import datetime
from typing import Optional
from telegram import Update


# File to store all chat logs
CHAT_LOG_FILE = "chatlogs.json"


def ensure_file_exists() -> None:
    """
    Ensure chatlogs.json exists on startup.
    Creates an empty list if file doesn't exist.
    """
    if not os.path.exists(CHAT_LOG_FILE):
        with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_chats() -> list:
    """
    Load existing chats from chatlogs.json.
    Returns empty list if file doesn't exist or is corrupted.
    """
    if os.path.exists(CHAT_LOG_FILE):
        try:
            with open(CHAT_LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def save_chat(user_id: int, username: Optional[str], 
              first_name: Optional[str], last_name: Optional[str], 
              message: str, is_group: bool, 
              chat_title: Optional[str] = None) -> None:
    """
    Save a single chat entry to the log file.
    Loads existing chats, appends new entry, and saves back.
    """
    chats = load_chats()
    
    chat_entry = {
        "timestamp": datetime.now().isoformat(),
        "user_id": user_id,
        "username": username or "N/A",
        "first_name": first_name or "N/A",
        "last_name": last_name or "N/A",
        "message": message,
        "chat_type": "group" if is_group else "private",
        "chat_title": chat_title or "N/A"
    }
    
    chats.append(chat_entry)
    
    with open(CHAT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(chats, f, indent=2, ensure_ascii=False)


def log_message(update: Update) -> None:
    """
    Log an incoming message from Telegram update.
    Extracts user info and message details.
    """
    if not update.message or not update.message.text:
        return
    
    user = update.message.from_user
    chat = update.message.chat
    
    save_chat(
        user_id=user.id if user else 0,
        username=user.username if user else None,
        first_name=user.first_name if user else None,
        last_name=user.last_name if user else None,
        message=update.message.text,
        is_group=chat.type == "group",
        chat_title=chat.title if hasattr(chat, "title") else None
    )