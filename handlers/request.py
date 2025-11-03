import os
import httpx
from telegram.ext import ContextTypes
from models.user import User
from dotenv import load_dotenv

apiUrl: str = "https://localhost:7108"

load_dotenv()
OpenRouterToken: str = os.getenv("OPENROUTER_API_KEY")

async def getUser(user: str):
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
    return str(user)

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
        content = [{"type": "text", "text": message}]
        if imageUrl:
            content.append({
                "type": "image_url",
                "image_url": {"url": imageUrl}
            })

        if context.user_data.get("UserAuth") is None:
            context.user_data["UserAuth"] = "No context registred"

        userContext = [{"type": "text", "text": f"Context only: {context.user_data.get('UserAuth')}"}]

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
                        "content": "You are Personal Finance, an AI finance assistant. You help users manage personal finances, track expenses, give budgeting insights, and explain finance terms clearly. Keep responses short and practical — max 3 sentences. Your main language is Portuguese from Brasil. Don't utilize * on responses. You have commands like /start that create the account for the user. /login to users that have an account. /help that tells the user what commands they have. You don't have any other commands at the moment"
                    },
                    {
                        "role": "user",
                        "content": userContext
                    },
                    {
                        "role": "user",
                        "content": content
                    }
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

    return content