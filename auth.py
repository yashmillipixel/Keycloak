import requests
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

KEYCLOAK_URL = "http://localhost:8080"
REALM = "Temp"
CLIENT_ID = "api_client"
CLIENT_SECRET = "qLuWGc8eVwqJ6mVeeCAcfuNz64xY5nBA"
ALGORITHM = "RS256"

# FastAPI token scheme (for /secure-data endpoints)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Fetch Keycloak public keys
DISCOVERY_URL = f"{KEYCLOAK_URL}/realms/{REALM}/.well-known/openid-configuration"
oidc_config = requests.get(DISCOVERY_URL).json()
JWKS_URL = oidc_config["jwks_uri"]
jwks = requests.get(JWKS_URL).json()

# ✅ 1. Function to get tokens from username+password
def get_keycloak_token(username: str, password: str):
    token_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
    payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": username,
        "password": password
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token request failed: {response.text}"
        )

# ✅ 2. Function to verify token
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        unverified_header = jwt.get_unverified_header(token)
        key = next(k for k in jwks["keys"] if k["kid"] == unverified_header["kid"])
        public_key = jwt.construct_rsa_key(key)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=[ALGORITHM],
            audience=CLIENT_ID,  # Make sure your client_id matches
            options={"verify_exp": True}
        )
        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# ✅ 3. Dependency to get the current user from the token
def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
