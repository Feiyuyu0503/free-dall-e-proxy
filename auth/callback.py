from fastapi import HTTPException, Response
from fastapi.responses import RedirectResponse
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from fastapi import Depends
import aiohttp
import os
import urllib.parse

client_id = os.getenv("CLIENT_ID")
scope = ""

# GitHub OAuth2 URL
AUTHORIZATION_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"

# 设置OAuth2
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{AUTHORIZATION_URL}?client_id={client_id}",
    tokenUrl=TOKEN_URL,
)

async def auth_github():
    oauth_url = f"{AUTHORIZATION_URL}?client_id={client_id}&scope={scope}"
    return RedirectResponse(url=oauth_url)

async def auth_callback(code: str):
    # use code to acquire access token
    async with aiohttp.ClientSession() as session:
        async with session.post(TOKEN_URL, data={
            "client_id": client_id,
            "client_secret": os.getenv("CLIENT_SECRET"),
            "code": code
        }) as resp:
            text = await resp.text()
            params = urllib.parse.parse_qs(text)
            access_token = params.get('access_token', [None])[0]
            if not access_token:
                raise HTTPException(status_code=400, detail="GitHub OAuth failed")
    
    # 使用cookie传递access_token
    response = RedirectResponse(url="/dashboard")
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response
