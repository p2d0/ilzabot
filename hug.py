import os
import json
from hugchat import hugchat
from hugchat.hugchat import ChatBot
from hugchat.login import Login

class Bot():
    # chatbot: ChatBot
    # """Chatbot"""

    def __init__(self)-> None:
        cookies = json.loads(open("./hug.json", encoding="utf-8").read())
        self.chatbot = hugchat.ChatBot(cookies)
    async def ask(self,text) -> str:
        return str(self.chatbot.query(text,web_search=True))
    async def reset(self):
        id = self.chatbot.new_conversation()
        self.chatbot.change_conversation(id)




if __name__ == '__main__':
    cookies = json.loads(open("./hug.json", encoding="utf-8").read())
    chatbot = hugchat.ChatBot(cookies)
    query_result = chatbot.query("Hi!")
    print(query_result) # or query_result.text or query_result["text"]
