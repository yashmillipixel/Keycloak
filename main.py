from fastapi import FastAPI, HTTPException
from api import upload_pdf, ask
import download  
from websocket_app.handler import router
import requests


app = FastAPI()

# Include routers for different modules
app.include_router(upload_pdf.router)
app.include_router(ask.router)
app.include_router(download.router)
app.include_router(router)
    
    

