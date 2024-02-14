from Bots import TelegramBotClient,DiscordBotClient
from imageGenerationsApi import ImageGenerationAPI
from config import config
import uvicorn


def setup_bots():
    # 创建一个字典，其中包含了不同平台的机器人客户端实例
    bot_clients = {}

    if config.TELEGRAM.lower() == "true":
        telegram_bot_client = TelegramBotClient(config.API_ID, config.API_HASH, config.BOT_USERNAME)
        bot_clients["telegram"] = telegram_bot_client

    if config.Discord.lower() == "true":
        discord_bot_client = DiscordBotClient(config.DiscordClientBotToken, config.DiscordChannelID,config.DiscordDalleBotID)
        bot_clients["discord"] = discord_bot_client
    
    return bot_clients

# Instantiate the FastAPI application
api = ImageGenerationAPI(setup_bots())

if __name__ == "__main__":
    try:
        uvicorn.run(app="main:api.app", host="0.0.0.0", port=config.PORT)
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")