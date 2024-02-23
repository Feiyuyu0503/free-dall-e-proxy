# Free DALL·E Proxy
<p>
   <img src="https://img.shields.io/github/actions/workflow/status/Feiyuyu0503/free-dall-e-proxy/docker-publish.yml?label=Build">
   <img src="https://img.shields.io/docker/pulls/feiyuyu/free-dall-e-proxy">
   <img src="https://img.shields.io/github/license/Feiyuyu0503/free-dall-e-proxy">
   <img src="https://img.shields.io/website?url=https%3A%2F%2Fdalle.feiyuyu.net%2Fgradio">
   <br></br>
   <img src=".github\images\demo.webp" width="50%" height="50%"><img src=".github\images\demo2.webp" width="50%" height="50%">
</p>

### English · [简体中文](./README.zh-CN.md) · [Changelog](./docs/CHANGELOG.md)
## Introduction
`free-dall-e-proxy` is a project that leverages the power of bots supported by the [coze](https://www.coze.com) (currently Telegram and Discord) to provide free access to OpenAI's DALL·E 3 image generation capabilities. This proxy service offers an OpenAI-standard API endpoint, allowing developers to easily integrate DALL·E 3 into their applications.

## Prerequisites
Before you can start using `free-dall-e-proxy`, you need to configure agents on the [Coze platform](https://www.coze.com/docs/publish/telegram.html). These agents act as intermediaries, facilitating the communication between your application and the DALL·E 3 API through the supported bots. More details refer to [how_to_create_coze_agent](./docs/how_to_create_coze_agent.md).

## Deployment

### Docker Deployment
For ease of deployment, `free-dall-e-proxy` is containerized using Docker. To deploy the proxy using Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Feiyuyu0503/free-dall-e-proxy.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd free-dall-e-proxy
   ```
3. Configure your related credentials in the `data/.env` file according to the prompt, now the [docs](docs/how_to_configure.md) is here:
   ```bash
   cp data/.env.example data/.env
   vim data/.env
   ```
4. Pull the published image:
   ```bash
   # Pull my published image. Alternatively, you can build the Docker image yourself.
   docker pull feiyuyu/free-dall-e-proxy
   ```
5. Run the Docker container:
   ```bash
   # if you set `Telegram` to True in the data/.env, it might require to login with your phone after running following commands.
   # after logining, you can press 'ctrl+p+q' to detach the container without stoping the container.
   # run:
   docker run -it -p 8000:8000 -v $PWD/data:/app/data --name free-dall-e-proxy feiyuyu/free-dall-e-proxy

   # if you only set `DISCORD` to True in the data/.env, you can run the following command instead:
   docker run -it -d -p 8000:8000 -v $PWD/data:/app/data --name free-dall-e-proxy feiyuyu/free-dall-e-proxy
   ```

The proxy service will now be running on port 8000 of your host machine.

### Python Execution
If you prefer to run the proxy service directly with Python, you can follow these steps: (Ensure you have Python 3.8+ installed on your machine.)

1. Clone the repository:
   ```bash
   git clone https://github.com/Feiyuyu0503/free-dall-e-proxy.git
   ```
2. Navigate to the cloned directory:
   ```bash
   cd free-dall-e-proxy
   ```
3. Install the necessary Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your related credentials in the `data/.env` file according to the prompt, now the [docs](docs/how_to_configure.md) is here:
   ```bash
   cp data/.env.example data/.env
   vim data/.env
   ```
5. Run the proxy server (python or uvicorn):
   ```bash
   # use python
   python main.py
   # or use uvicorn
   uvicorn main:api.app
   ```
The proxy service will now be accessible on the configured port(default:8000).

## Usage
To generate images with DALL·E 3, send a POST request to the proxy's API endpoint with your image generation parameters. The proxy will handle the request, communicate with the Coze platform supported bots(like Telegram,Discord...), and return the generated image.
1. Curl
   ```bash
   # You should replace the endpoint with your ip/domain:port
   # Use this command to send a request to the DALL·E image generation API.
   curl https://dalle.feiyuyu.net/v1/images/generations \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $KEY" \
     -d '{
       "model": "dall-e-3",
       "prompt": "A cute cat",
       "n": 1,
       "size": "1024x1024"
     }'

   # The following is the response:
   {
      "data":[
          {
            "url":"https://p16-flow-sign-va.ciciai.com/ocean-cloud-tos-us/1eff818cf88645bfa838109a0bc08910.png~tplv-6bxrjdptv7-image.png?rk3s=18ea6f23&x-expires=1737554903&x-signature=axs1WxYA0QK2%2BI3zISnequao3UY%3D",
            "revised_prompt":"A cute cat"
          }
      ]
   }
   ```

## Support
For any questions or issues regarding the deployment or usage of `free-dall-e-proxy`, please feel free to open an issue in the GitHub repository.

## Disclaimer

This project is open-source and intended solely for educational purposes. It must not be used for any illegal activities.

---
