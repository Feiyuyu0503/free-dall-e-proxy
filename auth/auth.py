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
            detail="invalid api key. Go here to get your api key: https://dalle.feiyuyu.net",
        )
    if api_key in config.keys["total_keys"].keys():
        user_id = list(config.keys["total_keys"][api_key].keys())[0]
        curr_usage = config.keys["total_keys"][api_key][user_id][0]
        if curr_usage < 0:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="out of usage! Try again after reset. Or deploy your own server without restrictions: https://github.com/Feiyuyu0503/free-dall-e-proxy",
            )
        else:
            config.keys["total_keys"][api_key][user_id][0] -= 1
            config.keys["total_keys"][api_key][user_id][1] += 1
    return api_key

def val_query_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    if credentials.scheme != "Bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="use Bearer token for authentication.",
        )
    api_key = credentials.credentials
    if config.Key and api_key not in config.Key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid api key. Go here to get your api key: https://dalle.feiyuyu.net",
        )
    return api_key