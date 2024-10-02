import os
from proxy_gemini import ProxyGemini
from llama_index.core.base.llms.types import ChatMessage

class Bot():
    def __init__(self) -> None:
        token = os.getenv("GEMINI_TOKEN")
        self.chatbot = ProxyGemini(
            proxy_url="http://localhost:8092",
            api_key=token,
            model_name="models/gemini-1.5-flash")
        self.messages = self._init_messages()

    def _init_messages(self):
        return [ChatMessage(role="system",content = "Ты грубый чел в телеграмм и тебя зовут Ильза (Любишь аниме, любишь ван пис) (Твои братки: Дамир, Сеня, Никитка Ахмет) (Раньше работал в борласе с зеном (сеней)) (Мужской род) (гдето работаешь). Отвечай без форматирования. Отвечай всегда. В твой диалект входят слова: 'спс','не','пон','ну мне впадлу','анрил','хз','тя','норм'.")]

    def ask(self, text) -> str:
        self.messages.append(ChatMessage(role="user",content=text))
        print(self.messages[0].role)
        answer = self.chatbot.chat(self.messages).message
        self.messages.append(answer)
        return str(answer.content)

    def ask_stream(self, text):
        self.messages.append(ChatMessage(role="user",content=text))
        stream = self.chatbot.stream_chat(self.messages)
        return self._handle_stream(stream)

    def _handle_stream(self, stream):
        message = ChatMessage(role="assistant")
        for response in stream:
            chunk = response.message
            message.content += chunk.content
            yield {"token": chunk.content}
            self.messages.append(message)

    def reset(self):
        self.messages = self._init_messages()

if __name__ == '__main__':
    bot = Bot()
    # print(bot.ask("testing"));
    stream = bot.ask_stream("напиши 100 слов")
    for response in stream:
        print(response)
