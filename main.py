from Bots.teleClient import TelegramBotClient
from Bots.discordClient import DiscordBotClient
from imageGenerationsApi import ImageGenerationAPI
from config import config

API_ID = config.API_ID
API_HASH = config.API_HASH
BOT_USERNAME = config.BOT_USERNAME
SESSION_NAME = config.SESSION_NAME

DiscordClientBotToken = config.DiscordClientBotToken
DiscordChannelID = config.DiscordChannelID
DiscordDalleBotId = config.DiscordDalleBotID

telegram_bot_client = TelegramBotClient(API_ID, API_HASH, BOT_USERNAME, SESSION_NAME)
discord_bot_client = DiscordBotClient(DiscordClientBotToken, DiscordChannelID,DiscordDalleBotId)

# 创建一个字典，其中包含了不同平台的机器人客户端实例
bot_clients = {
    "telegram": telegram_bot_client,
    "discord": discord_bot_client,
}

# Instantiate the FastAPI application
api = ImageGenerationAPI(bot_clients)

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app="main:api.app", host="0.0.0.0", port=8000)
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")