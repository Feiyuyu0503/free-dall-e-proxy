# 使用官方Python镜像作为基础镜像
FROM python:3.9-slim
LABEL author="feiyuyu"
LABEL email="admin@feiyuyu.net"
LABEL version="0.1.0"

# 设置工作目录为/app
WORKDIR /app

# 将当前目录下的所有文件（除了.dockerignore中排除的）复制到容器中的/app目录
COPY . .

# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# 运行Python应用程序
CMD ["python", "main.py"]
