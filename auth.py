from fastapi import FastAPI, Depends, HTTPException, status, Form, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
import httpx
from typing import Optional

router=APIRouter()

KEYCLOAK_URL = "http://localhost:8080/realms/Temp"
CLIENT_ID = "api_client"
CLIENT_SECRET = "7nMtpV7kTBTk3zana7MZqsIJfaplp9uN"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def get_public_key():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{KEYCLOAK_URL}/protocol/openid-connect/token")
        return r.json()["keys"][0]

async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        public_key = await get_public_key()
        key = jwt.algorithms.RSAAlgorithm.from_jwk(public_key)
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            audience=CLIENT_ID,
            options={"verify_exp": True}
        )
        return payload
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )

 
