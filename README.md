# TeleBot 🤖

AI-powered Telegram bot with Mistral AI and Groq fallback.

## Features

- AI-powered responses using Mistral AI
- Automatic fallback to Groq if Mistral fails
- Chat logging to JSON file
- Customizable bot behavior via instructions.txt
- Production-grade logging and error handling

## Prerequisites

- Python 3.10+
- Telegram Bot Token
- Mistral API Key
- Groq API Key (backup)

## Setup

### 1. Clone Repository

```bash
git clone https://github.com/nayaksomkar/TeleBot.git
cd TeleBot
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure API Keys

Copy the example environment file and add your API keys:

```bash
copy .env.example .env
```

Edit `.env` with your actual keys:

```
TOKEN=your_telegram_bot_token
BOT_USERNAME=@your_bot_username
MISTRAL_API_KEY=your_mistral_key
GROQ_API_KEY=your_groq_key
```

Alternatively, edit `config.py` directly with your API keys.

### 6. Run the Bot

```bash
python server.py
```

## Project Structure

```
TeleBot/
├── config.py         # API keys and settings
├── .env.example     # Environment variables template
├── .env             # Your API keys (not committed)
├── ai_service.py    # AI API calls (Mistral + Groq)
├── handlers.py     # Telegram message handlers
├── chat_logger.py  # Chat logging to JSON
├── server.py       # Main entry point
├── instructions.txt # Bot personality/prompt
├── chatlogs.json   # Auto-created chat log
├── requirements.txt
└── README.md
```

## Configuration

### Bot Behavior

Edit `instructions.txt` to customize how the bot responds. This file contains the system prompt that controls the bot's personality.

### API Keys

Get your keys from:
- **Telegram**: @BotFather
- **Mistral**: mistral.ai
- **Groq**: groq.com

## Usage

- Send `/start` - Welcome message
- Send `/help` - Help info
- Private chat - AI responds to all messages
- Group chat - Respond when mentioned (`@bot_username`)

## Chat Logging

All messages are saved to `chatlogs.json` with:
- Timestamp
- User ID, username, first/last name
- Message content
- Chat type (private/group)
- Chat title (for groups)

The file is created automatically on first message.