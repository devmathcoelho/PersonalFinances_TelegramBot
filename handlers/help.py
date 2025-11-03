from telegram import Update
from telegram.ext import ContextTypes

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Available commands:" \
        "\n/start - configures the bot" \
        "\n/help - show all the commands" \
        "\n/login - login to your account"
    )