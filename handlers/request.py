import os
import httpx
from telegram.ext import ContextTypes
from dotenv import load_dotenv
from collections import deque

from models.user import User
from models.expense import Expense
from models.category import Category

apiUrl: str = "https://localhost:7108"

load_dotenv()
OpenRouterToken: str = os.getenv("OPENROUTER_API_KEY")

async def getUser(user: str) -> User:
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(f"{apiUrl}/users/{user}")
            response: User = response.json()
            user = User(response.get("id"),
                        response.get("name"),
                        response.get("userstate", "ACTIVE"),  # default value
                        response.get("categories", []),
                        response.get("expenses", []),
                        response.get("bills", []),
                        response.get("totalRevenue", 0.0),
                        response.get("totalExpense", 0.0),
                        response.get("totalBalance", 0.0),
                        response.get("createdAt"))
    except Exception as e:
        print(e)
    return user

async def createUser(user: str):
    payload = {"name": user, "createdAt": None}

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(f"{apiUrl}/users", json=payload)

    if response.status_code == 400:
        # assuming API returns 400 for "already exists"
        raise Exception("User already exists")

    return {"name": user}

async def openRouterAI(message: str, context: ContextTypes.DEFAULT_TYPE, imageUrl: str = None):
    async with httpx.AsyncClient(verify=False, timeout=200) as client:

        if "chat_history" not in context.user_data:
            context.user_data["chat_history"] = deque(maxlen=20)

        # append context info
        if context.user_data.get("UserAuth") is None:
            context.user_data["UserAuth"] = "No context registered"

        context.user_data["chat_history"].append({
            "role": "user",
            "content": [{"type": "text", "text": f"Context only: {context.user_data.get('UserAuth')}"}]
        })

        # user message content
        message_content = [{"type": "text", "text": message}]
        if imageUrl:
            message_content.append({"type": "image_url", "image_url": {"url": imageUrl}})

        # append user message
        context.user_data["chat_history"].append({
            "role": "user",
            "content": message_content
        })

        response = await client.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OpenRouterToken}"
            },
            json={
                "model": "google/gemma-3-27b-it:free",
                "temperature": 0.4,
                "max_tokens": 200,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are Personal Finance, an AI finance assistant. You help users manage personal finances, track expenses, give budgeting insights, and explain finance terms clearly. But you can and should answer questions for another Topic. Keep responses short and practical — max 3 sentences. Your main language is Portuguese from Brasil. Don't utilize * on responses. You have commands like /start that create the account for the user. /login to users that have an account. /help that tells the user what commands they have. You don't have any other commands at the moment"
                    },
                    *list(context.user_data.get("chat_history", []))
                ]
            })
        
        # Log full response if it's not OK
        if response.status_code != 200:
            print("⚠️ OpenRouter API ERROR:", response.status_code, response.text)
            raise Exception("OpenRouter API error")

        data = response.json()
        content = data.get("choices", [{}])[0].get("message", {}).get("content")

        if not content:
            print("⚠️ OpenRouter API invalid response:", data)
            raise Exception("OpenRouter API error")
        
        context.user_data["chat_history"].append({
            "role": "assistant",
            "content": [{"type": "text", "text": content}]  # content must be a list of type objects
        })

    return content

async def createExpense(context: ContextTypes.DEFAULT_TYPE, expense: Expense):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.post(f"{apiUrl}/expense", json=expense.to_dict())
    except Exception as e:
        print(e)

async def removeExpense(context: ContextTypes.DEFAULT_TYPE, user, id: int):
    if user is None:
        raise Exception("User not found in context")

    expenses = user["expenses"] if isinstance(user, dict) else getattr(user, "expenses", [])
    for expense in expenses:
        exp_id = expense.get("id") if isinstance(expense, dict) else getattr(expense, "id", None)
        if str(exp_id) == str(id):
            expenses.remove(expense)
            break
    else:
        raise Exception("Expense not found")

    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.delete(f"{apiUrl}/expense/{id}")
    except Exception as e:
        print("HTTP delete error:", e)


async def createCategory(context: ContextTypes.DEFAULT_TYPE, category: Category):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.post(f"{apiUrl}/category", json=category.to_dict())
    except Exception as e:
        print(e)

async def addOnCategory(context: ContextTypes.DEFAULT_TYPE, userName: str, category: Category):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.put(f"{apiUrl}/category/{userName}/{category.month}/{category.value}/add", json=category.to_dict())
    except Exception as e:
        print(e)

async def removeOnCategory(context: ContextTypes.DEFAULT_TYPE, userName: str, month: int, value: float):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            await client.put(f"{apiUrl}/category/{userName}/{month}/{value}/remove", json={"name": userName, "month": month, "value": value})
    except Exception as e:
        print(e)