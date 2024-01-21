from dotenv import load_dotenv
import os

class Config:
    load_dotenv(dotenv_path = os.path.join('data','.env'))  # Load .env file

    API_ID = int(os.getenv('API_ID'))
    API_HASH = os.getenv('API_HASH')
    BOT_USERNAME = os.getenv('BOT_USERNAME')
    SESSION_NAME = os.getenv('SESSION_NAME')
    FASTAPI_SERVER_URL = os.getenv('FASTAPI_SERVER_URL')

    DiscordClientBotToken = os.getenv('DiscordClientBotToken')
    DiscordChannelID = int(os.getenv('DiscordChannelID'))
    DiscordDalleBotID = int(os.getenv('DiscordDalleBotId'))
