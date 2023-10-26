import os
from gigachat import GigaChat
from gigachat.models.chat_completion_chunk import ChoicesChunk

class Bot():
    # chatbot: ChatBot
    # """Chatbot"""

    def __init__(self)-> None:
        token = os.getenv("GIGACHAT_TOKEN");
        giga = GigaChat(base_url="https://gigachat.devices.sberbank.ru/api/v1",scope="GIGACHAT_API_PERS",auth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",credentials=token,verify_ssl_certs=False)
        self.chatbot = giga
    def ask(self,text) -> str:
        return str(self.chatbot.chat(text).choices[0].message.content)
    def ask_stream(self,text):
        stream = self.chatbot.stream(text)
        return self._handle_stream(stream)
    def _handle_stream(self,stream):
        for response in stream:
            chunk: ChoicesChunk = response.choices[0]
            if chunk.finish_reason != "stop":
                yield {"token":chunk.delta.content}
            else:
                yield None
    def reset(self):
        self.chatbot.close()

if __name__ == '__main__':
    # token = os.getenv("GIGACHAT_TOKEN");
    # giga = GigaChat(base_url="https://gigachat.devices.sberbank.ru/api/v1",scope="GIGACHAT_API_PERS",auth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",credentials=token,verify_ssl_certs=False)
    # stream = giga.stream("напиши 500 слов");
    # for response in stream:
    #     chunk: ChoicesChunk = response.choices[0]
    #     chunk.delta.content
    #     print(str(chunk))
    bot = Bot()
    stream = bot.ask_stream("напиши 10 слов")
    for response in stream:
        print(response)
