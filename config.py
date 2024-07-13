from dotenv import load_dotenv
import os
from loguru import logger
from aiohttp import BasicAuth

class Config:
    # Load .env file
    if not load_dotenv(dotenv_path = os.path.join('data','.env')):
        logger.error("No data/.env file found. Please make sure you are in the root directory of the project OR you have set envs manually.")

    if os.getenv('FASTAPI_SERVER_URL') is not None:
        logger.warning(f"the env 'FASTAPI_SERVER_URL' is deprecated, please remove it and set 'PORT' in your data/.env instead.(Default: PORT=8000)")
    PORT = int(os.getenv('PORT') or 8000)
    Timeout = float((os.getenv('TIMEOUT')) or 60)
    Key = os.getenv('KEY')
    Key = list(map(str.strip, Key.split(','))) if Key else None
    Web_share = os.getenv('WEB_SHARE') or 'False'
    Proxy = os.getenv('PROXY')
    Proxy_Auth = os.getenv('PROXY_AUTH')
    if Proxy:
        logger.info(f"Proxy: {Proxy} enabled.")

    # 固定补充Prompt
    addition_prompt = os.getenv('ADDITION_PROMPT') or ''

    # telegram
    TELEGRAM = os.getenv('TELEGRAM')
    API_ID = int(os.getenv('API_ID') or -1)
    API_HASH = os.getenv('API_HASH')
    BOT_USERNAME = os.getenv('BOT_USERNAME')
    BOT_USERNAME = BOT_USERNAME if BOT_USERNAME.startswith('@') else '@'+BOT_USERNAME
    SESSION_NAME = os.getenv('SESSION_NAME')+'.session'
    SESSION_STRING = os.getenv('SESSION_STRING')
    # read session file if exists
    if os.path.exists(os.path.join('data',SESSION_NAME)) and not SESSION_STRING:
        with open(os.path.join('data',SESSION_NAME),'r') as f:
            SESSION_STRING = f.read().strip()
    TelegramGroupID = int(os.getenv('TELEGRAM_GROUP_ID') or -1)

    # discord
    Discord = os.getenv('DISCORD')
    #DiscordClientBotToken = os.getenv('DISCORD_ClIENT_BOT_TOKEN')
    DiscordClientBotToken = os.getenv('DISCORD_AUTH')
    DiscordChannelID = int(os.getenv('DISCORD_CHANNEL_ID') or -1)
    DiscordDalleBotID = int(os.getenv('DISCORD_DALLE_BOT_ID') or -1)

    # mkdir data/images if not exists
    os.makedirs(os.path.join('data', 'images'), exist_ok=True)

config = Config()