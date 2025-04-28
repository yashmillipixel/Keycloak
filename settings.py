import requests

KEYCLOAK_REALM_URL = "http://localhost:8080/realms/first-test"
KEYCLOAK_CLIENT_ID ="fastapi-client"
OIDC_CONFIG_URL = f"{KEYCLOAK_REALM_URL}/.well-known/openid-configuration"
OIDC_CONFIG = requests.get(OIDC_CONFIG_URL).json()
JWKS_URL = OIDC_CONFIG["jwks_uri"]