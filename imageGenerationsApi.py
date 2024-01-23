from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
import gradio as gr
from gradio_ui import iface
import asyncio
from pydantic import BaseModel, Field
from typing import Optional

class ImageGenerationRequest(BaseModel):
    prompt: str = Field(..., description="A text description of the desired image(s).", max_length=4000)
    model: Optional[str] = Field("dall-e-3", description="The model to use for image generation.")
    n: Optional[int] = Field(1, description="The number of images to generate.For dall-e-3, only n=1 is supported.", ge=1, le=10)
    quality: Optional[str] = Field("standard", description="The quality of the image that will be generated. hd creates images with finer details and greater consistency across the image. This param is only supported for dall-e-3")
    response_format: Optional[str] = Field("url", description="The format in which the generated images are returned.")
    size: Optional[str] = Field("1024x1024", description="The size of the generated images. Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3 models.")
    style: Optional[str] = Field("vivid", description="The style of the generated images.Must be one of vivid or natural")
    user: Optional[str] = Field(None, description="A unique identifier representing your end-user.")
    platform: Optional[str] = Field(None, description="The platform which coze supported to use for image generation.")

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

    async def create_image(self, payload: ImageGenerationRequest):
        text = payload.prompt
        platform = payload.platform or list(self.bot_clients.keys())[0]  # 从payload中获取平台信息，默认为第一个启用的平台
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
