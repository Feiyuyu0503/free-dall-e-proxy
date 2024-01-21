# Free DALL·E Proxy

## Project Introduction
`free-dall-e-proxy` is a project that leverages the power of bots supported by the [coze](https://www.coze.com) (currently Telegram and Discord) to provide free access to OpenAI's DALL·E 3 image generation capabilities. This proxy service offers an OpenAI-standard API endpoint, allowing developers to easily integrate DALL·E 3 into their applications.

## Prerequisites
Before you can start using `free-dall-e-proxy`, you need to configure agents on the [Coze platform](https://www.coze.com/docs/publish/telegram.html). These agents act as intermediaries, facilitating the communication between your application and the DALL·E 3 API through the supported bots.

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
3. Build the Docker image:
   ```bash
   docker build -t free-dall-e-proxy .
   ```
4. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 -v $PWD/data:/app/data free-dall-e-proxy
   ```

The proxy service will now be running on port 8000 of your host machine.

### Python Execution
If you prefer to run the proxy service directly with Python, you can follow these steps:

1. Ensure you have Python 3.9+ installed on your machine.
2. Install the necessary Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your Coze platform bot credentials in the `.env` file.
4. Run the proxy server:
   ```bash
   python main.py
   ```

The proxy service will now be accessible on the configured port.

## Usage
To generate images with DALL·E 3, send a POST request to the proxy's API endpoint with your image generation parameters. The proxy will handle the request, communicate with the Coze platform supported bots(like Telegram,Discord...), and return the generated image.

## Support
For any questions or issues regarding the deployment or usage of `free-dall-e-proxy`, please feel free to open an issue in the GitHub repository.
