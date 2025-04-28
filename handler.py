from fastapi import APIRouter, Depends
from websocket_app.auth import get_current_user  # Assuming the correct import

router = APIRouter()

@router.get("/secure-data")
def secure_data(user: dict = Depends(get_current_user)):
    """
    This endpoint is secured and requires a valid JWT token to access.
    The user will be authenticated through Keycloak, and user details will be returned.
    """
    return {
        "message": "You are authenticated 🎉",
        "user": user  # User details from Keycloak (like email, sub, etc.)
    }

@router.get("/public")
def public_data():
    """
    This endpoint is public and doesn't require authentication.
    """
    return {"message": "This is a public endpoint!"}
