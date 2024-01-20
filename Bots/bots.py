import abc
# 抽象基类，定义了所有机器人客户端的通用接口
class BotClient(abc.ABC):
    @abc.abstractmethod
    async def start(self):
        pass

    @abc.abstractmethod
    async def stop(self):
        pass

    @abc.abstractmethod
    async def send_message(self, text: str):
        pass