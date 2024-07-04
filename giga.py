import os
from gigachat import GigaChat
from gigachat.models.chat_completion_chunk import ChoicesChunk
from gigachat.models.chat import Chat

class Bot():
    # chatbot: ChatBot
    # """Chatbot"""

    def __init__(self)-> None:
        token = os.getenv("GIGACHAT_TOKEN");
        giga = GigaChat(base_url="https://gigachat.devices.sberbank.ru/api/v1",scope="GIGACHAT_API_PERS",auth_url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth",credentials=token,verify_ssl_certs=False)
        self.messages = [];
        self.chatbot = giga
    def ask(self,text) -> str:
        self.messages.append({
            "role": "user",
            "content": text
        })
        answer = self.chatbot.chat({
            "messages": self.messages
        }).choices[0].message
        self.messages.append(answer)
        return str(answer.content)
    def ask_stream(self,text):
        self.messages.append({
            "role": "user",
            "content": text
        })
        stream = self.chatbot.stream({"messages": self.messages})
        return self._handle_stream(stream)
    def _handle_stream(self,stream):
        message = {"role": "assistant","content": ""};
        for response in stream:
            chunk: ChoicesChunk = response.choices[0]
            message["content"] += chunk.delta.content
            yield {"token":chunk.delta.content}
        self.messages.append(message)
    def reset(self):
        self.messages = [];

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
