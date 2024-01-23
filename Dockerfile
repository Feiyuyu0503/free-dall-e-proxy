# 使用官方Python镜像作为基础镜像
FROM python:3.9-alpine
LABEL author="feiyuyu"
LABEL email="admin@feiyuyu.net"
LABEL version="0.2.0"

# 设置工作目录为/app
WORKDIR /app

COPY requirements.txt ./
# 安装依赖项
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件（除了.dockerignore中排除的）复制到容器中的/app目录
COPY . .


EXPOSE 8000

# 运行应用程序
CMD ["uvicorn", "main:api.app", "--host", "0.0.0.0", "--port", "8000"]
