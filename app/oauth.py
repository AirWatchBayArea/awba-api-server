import os
from fastapi.security import (
    OAuth2AuthorizationCodeBearer,
    SecurityScopes,
)
from .models.oauth import *

OAUTH_CLIENT_ID = os.environ['OAUTH_CLIENT_ID']
OAUTH_SECRET = os.environ['OAUTH_SECRET']
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://id.heroku.com/oauth/authorize",
    tokenUrl="https://id.heroku.com/oauth/token",
    refreshUrl="https://id.heroku.com/oauth/token",
    scopes={"identity": "Read information about the user.", "read": "Read information about which apps the user has access."}
)

