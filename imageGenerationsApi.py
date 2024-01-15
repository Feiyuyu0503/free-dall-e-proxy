from teleClient import TelegramBotClient
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
import gradio as gr
from gradio_ui import iface
class ImageGenerationAPI:
    def __init__(self, telegram_bot_client: TelegramBotClient):
        self.app = FastAPI()
        self.telegram_bot_client = telegram_bot_client
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
        self.app = gr.mount_gradio_app(self.app, iface, '/gradio')

    async def root(self):
        return RedirectResponse(url="/gradio")

    async def create_image(self, text: str = Form(...)):
        image_markdown = await self.telegram_bot_client.send_message(text)
        return JSONResponse(content={"markdown": image_markdown})
    
    async def startup_event(self):
        await self.telegram_bot_client.start()

    async def shutdown_event(self):
        await self.telegram_bot_client.stop()
