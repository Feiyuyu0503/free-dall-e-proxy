from Bots.bots import BotClient
from telethon import TelegramClient, events
import asyncio

class TelegramBotClient(BotClient):
    def __init__(self, api_id: int, api_hash: str, bot_username: str,session_name: str):
        self.client = TelegramClient(session_name, api_id, api_hash)
        self.bot_username = bot_username
        self.pending_responses = {}  # 用于存储消息 ID 和(事件,回复消息)

    async def start(self):
        await self.client.start()
        print("Telegram client started!")
        self.client.add_event_handler(self.handle_response, events.NewMessage(from_users=self.bot_username))

    async def stop(self):
        await self.client.disconnect()

    async def send_message(self, text: str):
        sent_msg = await self.client.send_message(self.bot_username, text)
        msg_id = sent_msg.id
         # 为这个消息创建一个新的 Event 对象
        response_event = asyncio.Event()
        self.pending_responses[msg_id] = (response_event, None)
        await response_event.wait()
        # 等待事件被触发，然后获取响应
        response_event, response_message = self.pending_responses.pop(msg_id)
        response_event.clear()
        return response_message

    async def handle_response(self, event):
        reply_to_msg_id = event.message.reply_to_msg_id
        if event.is_private and reply_to_msg_id in self.pending_responses:
            response_event, _ = self.pending_responses[reply_to_msg_id]
            self.pending_responses[reply_to_msg_id] = (response_event, event.message.message)
            response_event.set()