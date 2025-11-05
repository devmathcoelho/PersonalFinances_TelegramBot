import os
from dotenv import load_dotenv
from telegram.ext import (
    ApplicationBuilder, 
    CommandHandler, 
    MessageHandler, 
    ContextTypes, 
    filters, 
    CallbackQueryHandler)

from commands.start import start
from commands.help import help
from commands.login import login
from commands.addExpense import addExpense
from commands.removeExpense import removeExpense
from handlers.message import message
from handlers.button import button

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("login", login))
    app.add_handler(CommandHandler("addExpense", addExpense))
    app.add_handler(CommandHandler("removeExpense", removeExpense))

    # message handler
    app.add_handler(MessageHandler(filters.TEXT, message))
    
    # button callback
    app.add_handler(CallbackQueryHandler(button))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()