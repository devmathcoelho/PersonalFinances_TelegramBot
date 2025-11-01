from telegram import Update
from telegram.ext import ContextTypes

# /start command logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    await update.message.reply_text(
        f"Hey {user_first_name}! 👋 Welcome to the bot — ready to roll?"
    )
