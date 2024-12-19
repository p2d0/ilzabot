#!/usr/bin/env python3.9

import asyncio
import sys
from EdgeGPT import Chatbot, ConversationStyle
bot = Chatbot(cookiePath='./cookie.json')

async def main():
    """
    Main function
    """
    print("Initializing...")
    prompt = "Hello"
    print("Bot:")
    wrote = 0
    async for final, response in bot.ask_stream(prompt=prompt):
        if not final:
            print(response[wrote:], end="")
            wrote = len(response)
            sys.stdout.flush()
    print()
    sys.stdout.flush()
    await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
