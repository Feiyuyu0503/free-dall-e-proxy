from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
import gradio as gr
from gradio_ui import iface
import asyncio


class ImageGenerationAPI:
    def __init__(self, bot_clients: dict):
        self.app = FastAPI()
        self.bot_clients = bot_clients  # 一个包含不同机器人客户端实例的字典
        self.setup_events()
        self.mount_gradio_interface()
        self.setup_routes()

    def setup_events(self):
        self.app.on_event("startup")(self.startup_event)
        self.app.on_event("shutdown")(self.shutdown_event)

    def setup_routes(self):
        self.app.get("/")(self.root)
        self.app.post("/v1/images/generations")(self.create_image)

    def mount_gradio_interface(self):
        self.app = gr.mount_gradio_app(self.app, iface, "/gradio")

    async def root(self):
        return RedirectResponse(url="/gradio")

    async def create_image(self, payload: dict):
        text = payload["prompt"]
        platform = payload.get("platform",list(self.bot_clients.keys())[0])  # 从payload中获取平台信息，默认为第一个启用的平台
        bot_client = self.bot_clients.get(platform)
        image_markdown = await bot_client.send_message(text)
        if platform == "telegram":
            url = image_markdown.split("](", 1)[1][:-1]
            revised_prompt = image_markdown.split("](", 1)[0][2:]
        elif platform == "discord":
            url = image_markdown
            revised_prompt = text
        return JSONResponse(content={"data": [{"url": url, "revised_prompt": revised_prompt}]})

    async def startup_event(self):
        if not self.bot_clients:
            raise ValueError("No bot clients found, please check your .env file.")
        await asyncio.gather(
            *(bot_client.start() for bot_client in self.bot_clients.values())
        )

    async def shutdown_event(self):
        await asyncio.gather(
            *(bot_client.stop() for bot_client in self.bot_clients.values())
        )
