from fastapi import FastAPI, Depends, HTTPException, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
import aiohttp,os,aiofiles
import uuid
import json
from config import config

url = "https://api.github.com"

# 获取star数
async def get_stargazers(owner: str, repo: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url}/repos/{owner}/{repo}") as resp:
            repo = await resp.json()
            return repo['stargazers_count']

# 检查所有star这个repo的用户
async def check_stargazers(owner: str, repo: str):
    # 首先检查star数
    total_stars = await get_stargazers(owner, repo)
    pages = total_stars // 100 + 1
    # 获得所有star这个repo的用户,一页100个,加入query参数per_page,pages
    stargazers_id = []
    for page in range(1, pages + 1):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{url}/repos/{owner}/{repo}/stargazers?per_page=100&page={page}") as resp:
                users = await resp.json()
                for user in users:
                    stargazers_id.append(user['id'])
    return stargazers_id

# 使用access_token获取用户信息
async def get_user(access_token: str):
    async with aiohttp.ClientSession() as session:
        headers = { "Authorization": f"token {access_token}" }
        async with session.get(f"{url}/user", headers=headers) as resp:
            user = await resp.json()
            return user['login'], user['id']

# 检查用户是否生成了key
async def check_key(user_id: int):
    keys = config.keys["total_keys"]
    for key in keys:
        if str(user_id) in keys[key]:
            return key,keys[key]
    uuids = str(uuid.uuid4()).split('-')
    keys[uuids[0]+'-'+uuids[1]] = {str(user_id):[config.left_times_each2h,0]} #{key:{user_id:[left_times,used_times]}}
    config.Key.append(uuids[0]+'-'+uuids[1])
    config.keys = {"total_keys":keys}
    async with aiofiles.open(f"data/keys.json", 'w') as f:
        await f.write(json.dumps(config.keys))
    return uuids[0]+'-'+uuids[1],keys[uuids[0]+'-'+uuids[1]]
        
# Dashboard页面
async def dashboard(access_token: str = Cookie(None)):
    if not access_token:
        return RedirectResponse(url="/auth/github")
    
    great_users = await check_stargazers("feiyuyu0503", "free-dall-e-proxy")
    user_name,id = await get_user(access_token)
    if id in great_users:
        key,times = await check_key(id)
        left_times,total_usage = times[str(id)]
        html_content = f'''
        <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <h1>{user_name}, Welcome to the Dashboard</h1>
            <p>Due to the high volume of requests we receive daily, we are compelled to impose certain restrictions. You can deploy it yourself to remove all the restrictions.</p>
            <p>As this is a free service, there is no SLA guarantee.</p>
            <p>Your api key is: {key}</p>
            <p>You have {left_times} times left to use in every 24h.</p>
            <p>You have requested {total_usage} times in total.</p>
            <p>Try it out:</p>
            <pre>
            <code>
            curl https://dalle.feiyuyu.net/v1/images/generations \\
            -H "Content-Type: application/json" \\
            -H "Authorization: Bearer {key}" \\
            -d '{{
              "model": "dall-e-3",
              "prompt": "A cute cat",
              "n": 1,
              "size": "1024x1024"
            }}'
            </code>
            </pre>
        </body>
        </html>
        '''
    else:
        html_content = f'''
        <html>
        <head>
            <title>Dashboard</title>
        </head>
        <body>
            <h1>{user_name},Welcome to the Dashboard</h1>
            <p>Sorry, you have not starred the repository; therefore, you cannot use this service. Alternatively, you can deploy it yourself.</p>
            <p><a href="https://github.com/feiyuyu0503/free-dall-e-proxy" target="_blank">Star⭐ the Repo</a>, then refresh the site, and you will receive a key to use this service.</p>
        </body>
        </html>
        '''
    return HTMLResponse(content=html_content)
    
    