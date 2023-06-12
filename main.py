import os
import telebot
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN:Final = '<BOT_TOKEN>'             # Add your '<BOT_TOKEN>' here.
BOT_USERNAME:Final = '<BOT_USERNAME>'   # Add your '<BOT_USERNAME>' here.



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('hello 596489')

async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
        Name   :    
        Ph.No  :    
        Email  :    ''')

def handle_response(text : str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hello in'
    
    elif 'bye' in processed:
        return 'bye'
    
    else:
        return 'can\'t help you that.'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type} : "{text}')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME,'').strip()
            response: str = handle_response(new_text)

        else:
            return
        
    else:
        response: str = handle_response(text)

    print('Bot : ',response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused the error {context.error}')

if __name__ == '__main__':
    print('program srart')
    app = Application.builder().token(TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start',start_command))
    app.add_handler(CommandHandler('info',info_command))

    #Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    #Errors
    app.add_error_handler(error)
    
    #Polling
    print('polling')
    app.run_polling(poll_interval=1)
