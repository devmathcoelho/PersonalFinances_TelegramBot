from telegram import Update
from telegram.ext import ContextTypes

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    reply = response(user_text)
    await update.message.reply_text(reply)


def response(text: str) -> str: 
    processed = text.lower()

    if 'hello' in processed:
        return 'Hi! How are you?'
    return 'I don\'t understand'