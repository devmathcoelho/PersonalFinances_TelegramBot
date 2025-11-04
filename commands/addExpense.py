from telegram import Update
from telegram.ext import ContextTypes

from handlers.request import createExpense, getUser
from models.expense import Expense

# /addExpense command logic 
async def addExpense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("UserAuth") is None:
        await update.message.reply_text(
            "You are not logged in. Use /login to login." \
            "Or /start to create an account.")
        return
    
    args = context.args
    if len(args) < 3:
        await update.message.reply_text("/addExpense <name> <value> <category> <date>")
        return
    
    try:
        name = args[0]
        value = float(args[1])
        category = args[2]
        if len(args) > 3:
            date = args[3]
        else:
            date = None
            
    except:
        await update.message.reply_text("/addExpense <name> <value> <category> <date>")
        return
    
    expense = Expense(name, value, category, context.user_data.get("UserAuth").id, date)

    await createExpense(context, expense)
    context.user_data["UserAuth"] = await getUser(context.user_data.get("UserAuth").name)
    
    await update.message.reply_text(f"Expense {name} added to your list.")