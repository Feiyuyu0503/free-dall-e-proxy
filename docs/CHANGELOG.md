# Changelog
### 2024-2-14 version="0.5.5"
1. 修复Telegram在并发场景下图片无法对应的问题，需要把程序bot和画图的coze bot拉到同一个群组中
2. 优化回复响应的一些问题

### 2024-2-9 version="0.5.0"
1. 支持访问控制，在data/.env中设置KEY，多个api key用逗号','分开
2. 允许网页公开使用，在data/.env中设置WEB_SHARE=True，也允许必须输入api key才能使用，设置WEB_SHARE=False(默认)

### 2024-2-2 version="0.3.8"
1. Discord、Telegram支持设置代理登录 https://stackoverflow.com/a/71668186

### 2024-2-1 version="0.3.5"
1. 适配Telegram对发送图片行为的改动
2. 通过Telgram平台生成的图片会保存在data/images