from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

# /login command logic
async def login(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name

    context.user_data["awaiting_name"] = True
    context.user_data["making_login"] = True
    await update.message.reply_text(
        f"Hi {user_first_name}! 👋 Please tell me your login Name",
        )