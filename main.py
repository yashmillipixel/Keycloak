from fastapi import FastAPI, HTTPException
from api import upload_pdf, ask
import download  
from websocket_app.handler import router
import requests
from websocket_app.auth import get_keycloak_token

app = FastAPI()

# Include routers for different modules
app.include_router(upload_pdf.router)
app.include_router(ask.router)
app.include_router(download.router)
app.include_router(router)

# Endpoint to get JWT token
@app.post("/token")
async def token(username: str, password: str):
    try:
        token_data = get_keycloak_token(username, password)
        return token_data  # Return access token and refresh token
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=401, detail=f"Invalid credentials or server error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
