import os
from bardapi import Bard

class Bot():
    # chatbot: ChatBot
    # """Chatbot"""

    def __init__(self)-> None:
        self.chatbot = Bard(token="dQjsuWqEl1eqez8uYkwDduda1Az6_V65bmDi21o6F11qqH6COAHhTczm_GeOqSJdOc-1gQ.")
    def ask(self,text) -> str:
        return str(self.chatbot.get_answer(text)['content'])
    def ask_stream(self,text) -> str:
        return [{"token": self.ask(text)['content']}]
    def reset(self):
        pass




if __name__ == '__main__':
    # cookies = json.loads(open("./hug.json", encoding="utf-8").read())
    # chatbot = hugchat.ChatBot(cookies)
    # query_result = chatbot.query("Hi!")
    # print(query_result) # or query_result.text or query_result["text"]
    bot = Bot()
    print(bot.ask("Hi"))
