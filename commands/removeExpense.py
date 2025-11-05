from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime

from handlers.request import removeExpense as removeExpenseReq, removeOnCategory,getUser

# /addExpense command logic 
async def removeExpense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("UserAuth") is None:
        await update.message.reply_text(
            "You are not logged in. Use /login to login." \
            "Or /start to create an account.")
        return
    
    args = context.args

    try:
        id = args[0]
        found = False
            
        for expense in context.user_data.get("UserAuth").expenses:
            if str(expense["id"]) == str(id):
                date_obj = expense["date"] if isinstance(expense["date"], datetime) else datetime.strptime(expense["date"], "%Y-%m-%d")
                month = date_obj.month - 1
                value = expense["value"]
                found = True
                break

        if not found:
            await update.message.reply_text("Expense not found")
            return

        await removeExpenseReq(context, context.user_data.get("UserAuth"), id)
        await removeOnCategory(context, context.user_data.get("UserAuth").name, month, value)

    except Exception as e:
        print("Error in removeExpense:", e)
        await update.message.reply_text("/removeExpense <id>")
        return
    
    context.user_data["UserAuth"] = await getUser(context.user_data.get("UserAuth").name)
    await update.message.reply_text(f"Expense removed from your list.")