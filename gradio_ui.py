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

# 自定义 HTML 内容作为页脚
footer_html = '''
                <div id="footer">
                    <a href="/docs">API</a>
                     • 
                    <a href="https://github.com/Feiyuyu0503/free-dall-e-proxy">Github</a>
                </div>
              '''

# 自定义 CSS
custom_css = '''
                footer {
                    display: none !important;
                }
                #footer {
                    text-align: center;
                    position: fixed;
                    left: 0;
                    bottom: 10px;
                    width: 100%;
                }
                #footer div {
                    display: inline-block;
                }
             '''

# 创建 Gradio Blocks 界面
with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# Text to Image")
    gr.Markdown("Enter some text and submit to generate an image.")
    with gr.Row():
       with gr.Column():
           input_text = gr.Textbox(lines=2, placeholder="Enter text here...")
           submit_button = gr.Button("Submit")
       with gr.Column():
           output_markdown = gr.Markdown()
    submit_button.click(fn=get_image_url, inputs=input_text, outputs=output_markdown)
    gr.HTML(footer_html)

if __name__ == '__main__':
    # 启动 Gradio 界面
    app,local_url,share_url = demo.launch(share=False)

