from teleClient import TelegramBotClient
from imageGenerationsApi import ImageGenerationAPI
from config import Config

API_ID = Config.API_ID
API_HASH = Config.API_HASH
BOT_USERNAME = Config.BOT_USERNAME
SESSION_NAME = Config.SESSION_NAME

# Instantiate the Telegram client
telegram_bot_client = TelegramBotClient(API_ID, API_HASH, BOT_USERNAME, SESSION_NAME)
# Instantiate the FastAPI application
api = ImageGenerationAPI(telegram_bot_client)

if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app="main:api.app", host="127.0.0.1", port=8000)
    except Exception as e:
        print(f"启动服务器时发生错误: {e}")