#!/usr/bin/python3.9

import asyncio
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import requests
import re
import time
from datetime import datetime
import responses
import random
from dateutil.relativedelta import relativedelta
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from gigachad import gigachad_vid
from telegram.ext import InlineQueryHandler, CallbackQueryHandler
from imagegen import ImageGenAsyncWithProxy
import logging
import json
import sys
from typing import List
from footnote_links import parse_text_with_footnote_links, replace_footnotes_with_html_url, remove_footnotes
from summarize import get_transcript
import yt_dlp
# from yt_dlp.postprocessor.ffmpeg import FFmpegExtractAudioPP

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
cookies = json.loads(open("./new_cookie.json", encoding="utf-8").read())


async def handle_imagegen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action(ChatAction.UPLOAD_PHOTO, update.message.message_thread_id)
    async with ImageGenAsyncWithProxy("./new_cookie.json","socks5://localhost:8093",True) as image_generator:
        try:
            photos = await image_generator.get_images(update.message.text)
            media = [InputMediaPhoto(photo) for photo in photos]
            await update.message.reply_media_group(media)
        except Exception as e:
            log.error(e)
            await update.message.reply_text(str(e))


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

def suggestedResponsesKeyboard(responses):
    keyboard = []
    for response in responses:
        if response["text"]:
            text = response["text"][:32] + "..." if len(response["text"]) > 35 else response["text"]
            keyboard.append([InlineKeyboardButton(text, callback_data=text)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    logging.info(reply_markup)

    return reply_markup

async def edgegpt(prompt,update: Update) -> None:
    message = None
    every_30_messages = 0
    try:
        async for final, response in bot.ask_stream(prompt=prompt,conversation_style="creative"):
            if not final:
                logging.info(response)
                links = parse_text_with_footnote_links(response)
                response = remove_footnotes(response)
                response = replace_footnotes_with_html_url(links,response)
                if not message:
                    if response:
                        message = await update.message.reply_text(text=response, parse_mode = ParseMode.HTML)
                else:
                    if "Searching" in response:
                        continue;
                    if every_30_messages % 30 == 0:
                        if message is not None:  # added check for None
                            await message.edit_text(text=response,parse_mode = ParseMode.HTML)
                    every_30_messages+=1
        logging.info(response)
        # logging.info(json.dumps(response))
        last_message = response["item"]["messages"][-1]
        if "adaptiveCards" not in last_message:
            raise KeyError("adaptiveCards key not found in the last message.")
        suggested_responses = last_message.get("suggestedResponses", [])
        throttling = response["item"]["throttling"]
        msg = last_message["adaptiveCards"][0]["body"][0]["text"]
        msg += f"\nОсталось {throttling['numUserMessagesInConversation']} из {throttling['maxNumUserMessagesInConversation']} сообщений."
        reply_markup = suggestedResponsesKeyboard(suggested_responses) if suggested_responses else None
        links = parse_text_with_footnote_links(msg)
        msg = remove_footnotes(msg)
        msg = replace_footnotes_with_html_url(links,msg)
        if message:
            await message.edit_text(text=msg, reply_markup=reply_markup,parse_mode = ParseMode.HTML)
        else:
            await update.message.reply_text(text=msg, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
        if "нет" in prompt.lower():
            giga  = gigachad_vid(prompt,msg)
            await update.message.reply_video(giga)
    except Exception as e:
        error_msg = f"Ошибка {str(e)}"
        await update.message.reply_text(text=error_msg)
        raise e

async def handle_edgegpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query:
        prompt = query.data
        update = query;
    else:
        prompt = update.message.text
    prompt = "#no_search " + prompt
    await edgegpt(prompt,update);


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Get the callback query and data
    query = update.callback_query
    data = query.data
    # Get the user who pressed the button
    user = query.from_user
    # Add the user's name or username to the message
    name = user.first_name
    username = user.username
    if username:
        message = f'{name} (@{username}) нажал "{data}"'
    else:
        message = f'{name} нажал "{data}"'
    await query.message.reply_text(message)
    await handle_edgegpt(update,context)


async def newchat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await bot.reset()
    await update.message.reply_text("Чат стерт")

app = ApplicationBuilder().read_timeout(5000).write_timeout(10000).token("233787808:AAH71m_JtqkQP5ZADD2yxYI2ye8TKTeMnxE").build()


random.seed(time.time())
i=0
ahmetoff_message_count = 0  # Variable to keep track of the message count for user 'ahmetoff'

async def post_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    global ahmetoff_message_count  # Access the message count variable
    # Check if the message is from 'ahmetoff'
    if update.message.from_user.username == 'ahmetoff' and text.startswith("/"):
        # Increment the message count for 'ahmetoff'
        ahmetoff_message_count += 1

        # Check if this is the 5th message from 'ahmetoff' and delete it
        if ahmetoff_message_count % 5 == 0:
            giga  = gigachad_vid(text,"нет")
            await update.message.reply_video(giga)
            await update.message.delete()
            return

    if '/ilzadembel' in text:
        date = relativedelta(datetime.now(), datetime(2016, 5, 22))
        await update.message.reply_text(f"Со времен возвращения илюззии прошло {date.years} лет {date.months} месяцев {date.days} дней 👮")
    elif 'ильза' in text:
        await handle_edgegpt(update, context)
    elif '/eugenedembel' in text:
        date = datetime.now() - datetime(2022, 12, 16)
        await update.message.reply_text(f"🔥🔥🔥 Со времени возвращения Жеки прошло {date.days} дней 🎊🔥🔥🔥")
    elif '/pauk' in text:
        date = datetime(2021, 12, 18, 10, 20) - datetime.now()
        await update.message.reply_text(f"До паука осталось: {int(date.seconds/3600)} часов {int((date.seconds/60)%60)} минут")
    elif '/help' in text:
        await update.message.reply_text('''
            list of commands:
            /pp - посмотреть сколько нафармили боги из топ 50
            на этом всё''')
    elif text.endswith('нет'):
        rand = [1, 1, 1]
        temp = random.choice(responses.responses_list)
        while temp in rand:
            temp = random.choice(responses.responses_list)
        await update.message.reply_text(temp)
        rand[i] = temp
    elif text.endswith('да'):
        da_used_list = [1, 1, 1]
        temp = random.choice(responses.da_responses_list)
        while temp in da_used_list:
            temp = random.choice(responses.da_responses_list)
        await update.message.reply_text(temp)
        da_used_list[i] = temp
    elif "иди в жопу" in text:
        giga  = gigachad_vid(text,"нет")
        await update.message.reply_video(giga)
    elif 'ржд' in text:
        await update.message.reply_text('Я')
    elif 'https://osu.ppy.sh/ss/' in text:
        await update.message.reply_text('Ебнутый')
    elif text in responses.kakay_list[0][0]:
        await update.message.reply_text(' '.join(responses.kakay_list[0]))
    elif text in responses.ruka_list:
        await update.message.reply_text(' '.join(responses.ruka_list))
    elif text in responses.money_list:
        await update.message.reply_text(' '.join(responses.money_list))
    elif 'иди нахуй' in text:
        await update.message.reply_text(responses.hui)
    elif 'можно' in text:
        await update.message.reply_text(random.choice(responses.mozhno_responses_list))
    elif 'интересно ' in text:
        await update.message.reply_text('интересно когда в бане тесно')
    elif '@ilza_bot' in text:
        await update.message.reply_text('Спасибо')
    elif any(link in text for link in ['youtube.com/clip/','youtube.com/shorts/','instagram.com/reel/', 'twitter.com/', 'reddit.com/','tiktok.com']):
        text = update.message.text
        link_regex = r'(https?://(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
        match = re.search(link_regex, text)

        # Download the video using yt-dlp
        with yt_dlp.YoutubeDL({'outtmpl': 'video.mp4',"overwrites": True, 'format': '[ext=mp4]', 'cookiefile': './instacookie'}) as ydl:
            ydl.download([match.group(0)])
        # Send the video to the chat
        with open('video.mp4', 'rb') as video_file:
            await update.message.reply_video(video=video_file,caption = f"<b>{update.message.from_user.username or update.message.from_user.first_name}</b>:\n{update.message.text}",parse_mode=ParseMode.HTML)
            await update.message.delete()
    elif any(link in text for link in ['youtube.com/','youtu.be']):
        text = update.message.text
        link_regex = r'(https?://(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
        match = re.search(link_regex, text)
        link = match.group(0);
        transcript = get_transcript(link);
        await bot.reset()
        await edgegpt(f'Summarize yourself the following youtube transcript (output in russian) "{transcript}"',update)


app.add_handler(CommandHandler("hello", hello))
# app.add_handler(CommandHandler("ilzapolite", openai_ilzapolite_response))
# app.add_handler(CommandHandler("gpt", openai_gpt3_response))
# app.add_handler(CommandHandler("imagegen", handle_imagegen))
app.add_handler(CommandHandler("newchat", newchat))
# app.add_handler(CommandHandler("trueilza", openai_trueilza_response))
app.add_handler(MessageHandler(filters.TEXT & filters.Entity('mention') & filters.Regex('@iLza_bot'),handle_edgegpt))
app.add_handler(MessageHandler(filters.TEXT,post_msg))
# app.add_handler(InlineQueryHandler(inline_query))
app.add_handler(CallbackQueryHandler(button_click))
async def main():
    global bot;
    print(cookies)
    # bot = await Chatbot.create(cookies=cookies,proxy="socks5://localhost:8091")
    # await bot.ask(prompt="pepegas",conversation_style="creative")

try:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    app.run_polling()
except Exception as e:
    logging.exception(e)
