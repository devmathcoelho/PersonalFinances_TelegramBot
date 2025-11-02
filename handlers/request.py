import requests
import httpx

apiUrl: str = "https://localhost:7108"

async def getUser(user: str):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(f"{apiUrl}/users/{user}")

    return response.json()

async def createUser(user: str):
    payload = {"name": user, "createdAt": None}

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(f"{apiUrl}/users", json=payload)

    if response.status_code == 400:
        # assuming API returns 400 for "already exists"
        raise Exception("User already exists")

    return {"name": user}