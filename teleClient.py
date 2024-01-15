from telethon import TelegramClient, events
import asyncio
from config import Config

class TelegramBotClient:
    def __init__(self, api_id: int, api_hash: str, bot_username: str,session_name: str):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.bot_username = bot_username
        self.response_event = asyncio.Event()
        self.response_message = None

    async def start(self):
        await self.client.start()
        print("Telegram client started!")
        self.client.add_event_handler(self.handle_response, events.NewMessage(from_users=self.bot_username))

    async def stop(self):
        await self.client.disconnect()

    async def send_message(self, text: str):
        await self.client.send_message(self.bot_username, text)
        await self.response_event.wait()
        self.response_event.clear()
        return self.response_message

    async def handle_response(self, event):
        if event.is_private:
            self.response_message = event.message.message
            self.response_event.set()