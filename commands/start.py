from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from handlers.button import button

# /start command logic
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="start_yes")],
        [InlineKeyboardButton("No", callback_data="start_no")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Hey {user_first_name}! 👋 Welcome to your Personal Finances ready to register?",
        reply_markup=reply_markup
    )