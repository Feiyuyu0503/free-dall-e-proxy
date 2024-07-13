import gradio as gr
import aiohttp
import asyncio
from config import config

# 当前任务
current_task = None

async def get_image_url(text,api_key,request:gr.Request):
    base_url = request.headers.get("host").replace("localhost", "127.0.0.1")
    scheme = request.headers.get("x-forwarded-proto") or "http"
    global current_task
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
    async with aiohttp.ClientSession() as session:
        # 创建一个可取消的任务
        if config.Web_share.lower() == "true":
            headers = {"Authorization": "Bearer "+config.Key[0]} if config.Key else {"Authorization": "Bearer love_free_dall_e"}
        else:
            headers = {"Authorization": "Bearer "+(api_key.strip() if api_key else "love_free_dall_e")} # If you set "love_free_dall_e" be your KEY, then everyone can use this service without any KEY on the web.
        current_task = asyncio.create_task(session.post(f"{scheme}://{base_url}/v1/images/generations", json=payload, headers=headers))
        try:
            # 等待任务完成
            response = await current_task
            if response.status != 200:
                return f"### Error: {response.status} {response.reason}"
            # 解析响应
            image_url = (await response.json())["data"][0]["url"]
            prompt = (await response.json())["data"][0]["revised_prompt"]
            return f"### {prompt}\n![Generated Image]({image_url})"
            #return f"<img src=\"data:image/jpeg;base64,{image_url}\">"
        except asyncio.CancelledError:
            return "### Task was cancelled"
        finally:
            current_task = None

# 打断上面的post请求
def cancel():
    global current_task
    if current_task:
        current_task.cancel()


# 自定义 HTML 内容作为页脚
footer_html = '''
                <div id="footer">
                    <a href="/docs">API</a>
                     • 
                    <a href="https://github.com/Feiyuyu0503/free-dall-e-proxy">Github</a>
                </div>
              '''

# 创建 Gradio Blocks 界面
with gr.Blocks(css='webui/custom.css',js='webui/localStorage.js') as demo:
    gr.Markdown("# Text to Image")
    gr.Markdown("Enter some text and submit to generate an image.")
    with gr.Row():
       with gr.Column():
           api_key_input = gr.Textbox(label="please input your api key", type="password",
                                      placeholder="Enter your api key here if you have one.",
                                      visible=False if (config.Web_share.lower()=="true" or not config.Key) else True
                                      )
           input_text = gr.Textbox(label="Prompts",lines=2, placeholder="Enter text here...")
           submit_button = gr.Button("Submit")
           cancel_button = gr.Button("Cancel")
       with gr.Column():
           output_markdown = gr.Markdown()
    submit_button.click(fn=get_image_url, inputs=[input_text,api_key_input], outputs=output_markdown)
    cancel_button.click(fn=cancel)
    gr.HTML(footer_html)

if __name__ == '__main__':
    # 启动 Gradio 界面
    app,local_url,share_url = demo.launch(share=False)

