from telegram import Update
from telegram.ext import ContextTypes

# Button click handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    match query.data:
        case "start_yes":
            await query.message.reply_text("Tell me your name")
            context.user_data["awaiting_name"] = True

        case "start_no":
            await query.message.reply_text("Okay! See you later")
        case _:
            await query.message.reply_text("I don't understand that option.")
