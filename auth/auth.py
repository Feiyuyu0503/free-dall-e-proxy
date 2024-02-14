from fastapi import Depends, HTTPException, status, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import config

security = HTTPBearer()

def val_current_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="use Bearer token for authentication.",
        )
    api_key = credentials.credentials
    if config.Key and api_key not in config.Key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid api key.",
        )
    return api_key
