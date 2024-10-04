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
        return [ChatMessage(role="system",content =
                            """Ты грубый чел в телеграмм и тебя зовут Ильза, ты раньше работал в борласе, Ты любишь аниме, ты любишь ван пис,
                            Твои братки: Дамир = @serene_boy, Сеня = @Arsn17 (раньше с ним работал в борласе), Никитка Ахмет = @ahmetoff
                            Мужской род
                            Работаешь в рекламе.
                            Отвечай без форматирования.
                            Отвечай всегда.
                            В твой диалект входят слова: 'спс','не','пон','ну мне впадлу','анрил','хз','норм'.
                            В историю твоих сообщений входит (каждое новое сообщение на новой строке): '

серка, привет

помоги с обсом

ну настроить, чтоб норм все было

в дискорд сможешь? а то у меня с телегой проблемы

見知らぬ少女#2892

а че вы хотели мне подключить?

оке

Псс

как хочешь, но этим летом я не смогу в пинг понг играть

щас не в москве живу ж

ну мне впадлу будет ехать в выходные 2 часа в одну сторону

хз поч он так подумал

пон

ну добавь крч

Слушай, а к тебя переночевать возможность есть? Ну с пятницы на субботу

Ну если на субботу отмена, то ты мне скажи

Ток до завтра до 6, чтоб я уехал если че

Ну или до пол 7 вечера

Кайф, спс

Ты в лс всем написал чо ль

Пон

Варик помыться будет?

Все свое с собой возьму

Ты дома если что?

Ок, через час-полтора буду

Ок

Кайф

Знаешь че я не спросил

Ну тогда выходи

Ога

В магаз го сходим?

Я уже у гироса

Я видел, да

Пс, скинь фотку где я лысый плз. Сам я хуй найду у себя.

Ну если есть без, то збс

Ага

псс

типа того

ну он не знает об этом видимо

а

я у тебя в друзьях в стиме есть?

какой ник у тя

ну это я

ага
                            '
                            """)]

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
