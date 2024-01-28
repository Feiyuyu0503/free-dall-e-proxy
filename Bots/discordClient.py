import discord
from Bots.bots import BotClient
import asyncio
from config import config
from loguru import logger

class DiscordBotClient(BotClient):
    def __init__(self, token: str, channel_id: int,dalle_bot_id: int):
        intents = discord.Intents.default()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.token = token
        self.channel_id = channel_id
        self.pending_responses = {}  # 用于存储消息 ID 和(事件,回复消息)
        self.dalle_bot = dalle_bot_id

        @self.client.event
        async def on_ready():
            logger.info("Discord client started! We have logged in as {self.client.user}!")

    async def start(self):
        self.client.event(self.on_message)
        asyncio.create_task(self.client.start(self.token))

    async def stop(self):
        await self.client.close()

    async def send_message(self, text: str):
        try:
            channel = self.client.get_channel(self.channel_id)
            if channel is None:
                raise ValueError(f"Discord Channel ID {self.channel_id} not found")

            sent_msg = await channel.send(f"<@{self.dalle_bot}> "+text)
            msg_id = sent_msg.id
            # 为这个消息创建一个新的 Event 对象
            response_event = asyncio.Event()
            self.pending_responses[msg_id] = (response_event, None)
            try:
                await asyncio.wait_for(response_event.wait(), timeout=config.Timeout)
            except asyncio.TimeoutError:
                logger.error("Discord message sent, but response timeout!")
            # 等待事件被触发，然后获取响应
            response_event, response_message = self.pending_responses.pop(msg_id)
            response_event.clear()
            return response_message
        except Exception as e:
            logger.error(f"Discord client send message error: {e} \n check your input texts or your data/.env file.")

    async def on_message(self, message):
        # 请确保不响应机器人自己发送的消息
        if message.author == self.client.user:
            return
        reply_to_msg_id = message.reference.message_id if message.reference else None
        if reply_to_msg_id is not None and reply_to_msg_id in self.pending_responses:
            try:
                response_event, _ = self.pending_responses[reply_to_msg_id]
                self.pending_responses[reply_to_msg_id] = (response_event, message.embeds[0].image.url)
                response_event.set()
            except Exception as e:
                logger.error(f"Discord client handle response error: {e}")

    
