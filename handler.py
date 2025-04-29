from fastapi import FastAPI, Depends, HTTPException, status, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import httpx
from typing import Optional
from websocket_app.auth import verify_token, get_public_key


router = APIRouter()

KEYCLOAK_URL = "http://localhost:8080/realms/Temp"
CLIENT_ID = "api_client"
CLIENT_SECRET = "7nMtpV7kTBTk3zana7MZqsIJfaplp9uN"

@router.post("/token")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    client_id: str = Form(default=CLIENT_ID),
    client_secret: str = Form(default=CLIENT_SECRET),
):
    async with httpx.AsyncClient() as client:
        data = {
            "grant_type": "password",  # <<< this MUST be present
            "username": username,
            "password": password,
            "client_id": client_id,
        }
        if client_secret:
            data["client_secret"] = client_secret

        print('data:', data)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        response = await client.post(
            f"{KEYCLOAK_URL}/protocol/openid-connect/token",
            data=data,
            headers=headers
        )
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)
    return response.json()


@router.get("/protected")
async def protected_route(user: dict = Depends(verify_token)):
    return {"message": "You're authenticated", "user": user}
