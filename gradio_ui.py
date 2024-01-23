import gradio as gr
import requests
from config import config

# FastAPI 服务器的 URL
FASTAPI_SERVER_URL = config.FASTAPI_SERVER_URL

def get_image_url(text):
    # 向 FastAPI 后端发送 POST 请求，并获取图片 URL
    payload = {
        "prompt": text,
        "model": 'dall-e-3',
        "n": 1,
        "quality": 'standard',
        "response_format": 'url',
        "size": '1024x1024',
        "style": 'vivid',
        "user": 'free-dall-e-user'
    }
    response = requests.post(f"{FASTAPI_SERVER_URL}/v1/images/generations", json=payload)
    #print(response.json())
    image_url = response.json()["data"][0]["url"]
    prompt = response.json()["data"][0]["revised_prompt"]
    return f"## {prompt}\n![Generated Image]({image_url})"

# 创建 Gradio 界面
iface = gr.Interface(
    fn=get_image_url,
    inputs=gr.Textbox(lines=2, placeholder="Enter text here..."),
    outputs="markdown",  # 使用 markdown 组件显示图片
    title="Text to Image",
    description='''Enter some text and submit to generate an image.
                   <div id="custom-footer">
                       <a href="/docs" target="_blank">Api Documentation</a>
                   </div>''',
    allow_flagging="never",
    css='''
        footer {visibility: hidden}
        #custom-footer {
            position: fixed;
            bottom: 10px;
            width: 80%;
            text-align: center;
        }
        #custom-footer a {
            color: blue;
            text-decoration: none;
        }
    '''
)

if __name__ == '__main__':
    # 启动 Gradio 界面
    app,local_url,share_url = iface.launch(share=False)

