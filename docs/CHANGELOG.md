# Changelog
### 2024-7-13 version="0.6.5"
1. 修复webui中的请求地址(如果是localhost则自动替换为请求127.0.0.1)
2. 当discord的coze bot不遵循prompt时，等待10s，再尝试获取图片url

### 2024-7-13 version="0.6.4"
1. 修复功能，持久化保存在webui中输入的api key

### 2024-7-13 version="0.6.3"
1. 新增环境变量ADDITION_PROMPT，追加此提示文本至每条请求文本的最后
2. 修复Discord获取图片url的方式

### 2024-2-24 version="0.6.1"
1. 持久化保存在webui中输入的api key

### 2024-2-23 version="0.6.0"
1. 修复Discord无法得到coze bot响应的问题(注意！使用Discord用户账号登录程序，存在一定风险！后果自负！TG同理！)

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