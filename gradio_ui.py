import gradio as gr
import requests
from config import Config

# FastAPI 服务器的 URL
FASTAPI_SERVER_URL = Config.FASTAPI_SERVER_URL

def get_image_url(text):
    # 向 FastAPI 后端发送 POST 请求，并获取图片 URL
    response = requests.post(f"{FASTAPI_SERVER_URL}/v1/images/generations", data={"text": text})
    #print(response.json())
    image_markdowm = response.json()["markdown"]
    return f"{image_markdowm}"

# 创建 Gradio 界面
iface = gr.Interface(
    fn=get_image_url,
    inputs=gr.Textbox(lines=2, placeholder="Enter text here..."),
    outputs="markdown",  # 使用 markdown 组件显示图片
    title="Text to Image",
    description="Enter some text and submit to generate an image."
)

if __name__ == '__main__':
    # 启动 Gradio 界面
    app,local_url,share_url = iface.launch(share=True)

