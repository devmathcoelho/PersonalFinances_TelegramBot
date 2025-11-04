from telegram import Update
from telegram.ext import ContextTypes
from collections import deque

from handlers.request import getUser, createUser, openRouterAI

# handle message logic
async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    context.user_data.setdefault("UserAuth", None)

    # check if the user are logged or not
    if context.user_data.get("UserAuth") is None and not context.user_data.get("awaiting_name"):
        await update.message.reply_text(
            "You are not logged in. Use /login to login." \
            "Or /start to create an account.")
        return

    if context.user_data.get("awaiting_name"):
        name = user_text
        context.user_data["awaiting_name"] = False

        # check if the user is making a login
        if context.user_data.get("making_login"):
            # store the user info on context
            context.user_data["UserAuth"] = await getUser(name)
            context.user_data["making_login"] = False

            if context.user_data.get("UserAuth") is None:
                await update.message.reply_text(f"User {name} does not exist. Use /start to create an account.")
                return
            
            await update.message.reply_text(f"Hello {name}, you are logged in.")

        # check if the user is creating an account and are not logged in
        else:
            try:
                await createUser(name)
                # store the user info on context
                context.user_data["UserAuth"] = await getUser(name)
                await update.message.reply_text(f"Hello {name}, your account has been created.")
            except Exception as e:
                await update.message.reply_text(f"Error: {str(e)}")

    else:
        reply = await response(user_text, context)
        await update.message.reply_text(reply)

async def response(text: str, context: ContextTypes.DEFAULT_TYPE) -> str:
    # call the OpenRouterAI API to make AI responses
    return await openRouterAI(text, context)