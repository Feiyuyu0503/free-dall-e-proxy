# Free DALL·E Proxy
<p>
   <img src="https://img.shields.io/github/actions/workflow/status/Feiyuyu0503/free-dall-e-proxy/docker-publish.yml?label=Build">
   <img src="https://img.shields.io/docker/pulls/feiyuyu/free-dall-e-proxy">
   <img src="https://img.shields.io/github/license/Feiyuyu0503/free-dall-e-proxy">
   <img src="https://img.shields.io/website?url=https%3A%2F%2Fdalle.feiyuyu.net%2Fgradio">
   <br></br>
   <img src=".github\images\demo.webp" width="50%" height="50%"><img src=".github\images\demo2.webp" width="50%" height="50%">
</p>

### [English](./README.md) · 简体中文 · [更新记录](./docs/CHANGELOG.md)
## 介绍
`free-dall-e-proxy`是利用由[coze](https://www.coze.com)支持的机器人（目前是Telegram和Discord），提供免费访问OpenAI的DALL·E 3图像生成的代理服务。项目提供了一个符合OpenAI标准的API端点，允许开发者轻松地将此DALL·E 3代理服务集成到他们的应用程序中。

## 预备条件
在你开始使用`free-dall-e-proxy`之前，你需要在[Coze平台](https://www.coze.com/docs/publish/telegram.html)上配置智能体Agent。更多细节参考[如何创建coze智能体](./docs/how_to_create_coze_agent.md)。

## 部署
### Docker部署
为了便于部署，`free-dall-e-proxy`提供了Docker部署方式。要使用Docker部署代理，请按照以下步骤操作：

1. 克隆仓库：
   ```bash
   git clone https://github.com/Feiyuyu0503/free-dall-e-proxy.git
   ```
2. 进入到克隆下来的目录：
   ```bash
   cd free-dall-e-proxy
   ```
3. 根据提示在项目`data/.env`文件中配置你的相关参数，详细[配置文档](docs/how_to_configure.md)在这里：
   ```bash
   cp data/.env.example data/.env
   vim data/.env
   ```
4. 拉取我发布的镜像或自己构建Docker镜像：
   ```bash
   # 拉取我发布的镜像,或者你也可以自己构建Docker镜像
   docker pull feiyuyu/free-dall-e-proxy
   ```
5. 运行Docker容器：
   ```bash
   # 如果你在data/.env中设置`Telegram`为True，可能需要在运行以下命令后根据提示用你的账号登录。
   # 登录后，你可以按'ctrl+p+q'来脱离容器而不停止容器。
   # 运行：
   docker run -it -p 8000:8000 -v $PWD/data:/app/data --name free-dall-e-proxy feiyuyu/free-dall-e-proxy

   # 如果你在data/.env中只设置了`DISCORD`为True，你可以运行以下命令代替：
   docker run -it -d -p 8000:8000 -v $PWD/data:/app/data --name free-dall-e-proxy feiyuyu/free-dall-e-proxy
   ```

代理服务现在将在你的主机机器的8000端口上运行。

### Python执行
如果你想直接用Python运行代理服务，你可以按照这些步骤操作：（确保你的机器上安装了Python 3.8+。）

1. 克隆仓库：
   ```bash
   git clone https://github.com/Feiyuyu0503/free-dall-e-proxy.git
   ```
2. 进入到克隆下来的目录：
   ```bash
   cd free-dall-e-proxy
   ```
3. 安装必要的Python依赖项：
   ```bash
   pip install -r requirements.txt
   ```
4. 根据提示在项目`data/.env`文件中配置你的相关参数，详细[配置文档](docs/how_to_configure.md)在这里：
   ```bash
   cp data/.env.example data/.env
   vim data/.env
   ```
5. 运行代理服务器（python或uvicorn）：
   ```bash
   # 使用python
   python main.py
   # 或使用uvicorn
   uvicorn main:api.app
   ```
代理服务现在将可以在配置的端口（默认：8000）上访问。

## 使用
要使用DALL·E 3生成图像，请向代理的API端点发送POST请求，附上你的图像生成参数。代理将处理请求，与Coze平台支持的机器人（如Telegram, Discord...）通信，并返回生成的图像。
1. Curl
   ```bash
   # 你应该使用你的ip/domain:port替换该端点
   # 使用此命令发送请求到 DALL·E图像生成API。
   curl https://dalle.feiyuyu.net/v1/images/generations \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $KEY" \
     -d '{
       "model": "dall-e-3",
       "prompt": "一只可爱的猫",
       "n": 1,
       "size": "1024x1024"
     }'

   # 以下是响应：
   {
      "data":[
          {
            "url":"https://p16-flow-sign-va.ciciai.com/ocean-cloud-tos-us/1eff818cf88645bfa838109a0bc08910.png~tplv-6bxrjdptv7-image.png?rk3s=18ea6f23&x-expires=1737554903&x-signature=axs1WxYA0QK2%2BI3zISnequao3UY%3D",
            "revised_prompt":"一只可爱的猫"
          }
      ]
   }
   ```

## 支持
对于部署或使用`free-dall-e-proxy`的任何问题，请随时在GitHub仓库中开启一个issue。

## 免责声明

该项目是开源的，仅用于学习目的。不得用于任何非法活动。

---