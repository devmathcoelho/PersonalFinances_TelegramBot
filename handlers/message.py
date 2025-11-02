from telegram import Update
from telegram.ext import ContextTypes

from handlers.request import getUser, createUser

# handle message logic
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    if context.user_data.get("awaiting_name"):
        name = user_text
        context.user_data["awaiting_name"] = False
        
        try:
            await createUser(name)
            # store the user info properly
            context.user_data["UserAuth"] = await getUser(name)
            await update.message.reply_text(f"Hello {name}, your account has been created.")
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")


    else:
        reply = response(user_text, context)
        await update.message.reply_text(reply)

def response(text: str, context: ContextTypes.DEFAULT_TYPE) -> str: 
    processed = text.lower()

    match processed:
        case 'hello': return 'Hi! How are you?'
        case 'get user': return context.user_data.get("UserAuth")
        case _: return 'I don\'t understand'