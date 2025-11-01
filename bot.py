import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from handlers.start import start
from handlers.help import help
from handlers.message import message

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))

    app.add_handler(MessageHandler(filters.TEXT, message))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()

if __name__ == "__main__":
    main()
