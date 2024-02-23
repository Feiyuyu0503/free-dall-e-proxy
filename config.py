from dotenv import load_dotenv
import os
from loguru import logger
import json
import threading
import time

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
    # add keys
    if os.path.exists(os.path.join('data','keys.json')):
        with open(os.path.join('data','keys.json'),'r') as f:
            keys = json.load(f)
            if 'total_keys' in keys:
                total_keys = keys['total_keys']
                Key.extend(list(total_keys.keys()))
    else:
        keys = {"total_keys":{}}
        with open(os.path.join('data','keys.json'),'w') as f:
            json.dump(keys,f)
    Web_share = os.getenv('WEB_SHARE') or 'False'
    Proxy = os.getenv('PROXY')
    Proxy_Auth = os.getenv('PROXY_AUTH')
    if Proxy:
        logger.info(f"Proxy: {Proxy} enabled.")

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
    DiscordClientBotToken = os.getenv('DISCORD_ClIENT_BOT_TOKEN')
    DiscordChannelID = int(os.getenv('DISCORD_CHANNEL_ID') or -1)
    DiscordDalleBotID = int(os.getenv('DISCORD_DALLE_BOT_ID') or -1)

    # mkdir data/images if not exists
    os.makedirs(os.path.join('data', 'images'), exist_ok=True)

    # set reset trigger
    # 每RESET_INTERVAL个小时写入一次keys.json
    left_times_each2h = int(os.getenv('CALL_TIMES') or 24)
    reset_interval = int(os.getenv('RESET_INTERVAL') or 2)
    def reset_keys():
        time.sleep(10)
        while True:
            # 重置left times
            for key in config.keys["total_keys"]:
                for user_id in config.keys["total_keys"][key]:
                    config.keys["total_keys"][key][user_id][0] = config.left_times_each2h
            with open(os.path.join('data','keys.json'),'w') as f:
                json.dump(config.keys,f)
            logger.info("keys.json updated.")
            time.sleep(60*60*config.reset_interval)
    
    threading.Thread(target=reset_keys,daemon=True).start()
    system_start_time = time.time()


config = Config()