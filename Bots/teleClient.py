from Bots.bots import BotClient
from telethon import TelegramClient, events
import asyncio,os
from telethon.sessions import StringSession
from config import config
import aiofiles
from loguru import logger

class TelegramBotClient(BotClient):
    def __init__(self, api_id: int, api_hash: str, bot_username: str):
        self.client = TelegramClient(StringSession(config.SESSION_STRING), api_id, api_hash)
        self.bot_username = bot_username
        self.pending_responses = {}  # 用于存储消息 ID 和(事件,回复消息)

    async def start(self):
        await self.client.start()
        logger.info("Telegram client started!")
        await self.update_session()
        self.client.add_event_handler(self.handle_response, events.NewMessage(from_users=self.bot_username))

    async def stop(self):
        await self.client.disconnect()
    
    async def update_session(self):
        if self.client.session.save() != config.SESSION_STRING:
            async with aiofiles.open(os.path.join('data',config.SESSION_NAME),'w') as f:
                await f.write(self.client.session.save())

    async def send_message(self, text: str):
        try:
            sent_msg = await self.client.send_message(self.bot_username, text)
            msg_id = sent_msg.id
             # 为这个消息创建一个新的 Event 对象
            response_event = asyncio.Event()
            self.pending_responses[msg_id] = (response_event, None)
            try:
                await asyncio.wait_for(response_event.wait(), timeout=config.Timeout)
            except asyncio.TimeoutError:
                logger.error("Telegram message sent, but response timeout!")
            # 等待事件被触发，然后获取响应
            response_event, response_message = self.pending_responses.pop(msg_id)
            response_event.clear()
            return response_message
        except Exception as e:
            logger.error(f"Telegram client send message error: {e} \n check your input texts or your data/.env file.")

    async def handle_response(self, event):
        reply_to_msg_id = event.message.reply_to_msg_id
        if event.is_private and reply_to_msg_id in self.pending_responses:
            response_event, _ = self.pending_responses[reply_to_msg_id]
            self.pending_responses[reply_to_msg_id] = (response_event, event.message.message)
            response_event.set()