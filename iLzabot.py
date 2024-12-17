#!/usr/bin/python3.9

import asyncio
import aiohttp
from EdgeGPT.EdgeGPT import Chatbot, ConversationStyle
import re
import time
from datetime import datetime
import responses
import random
from dateutil.relativedelta import relativedelta
from telegram import Update, ReplyParameters, InlineQueryResultArticle, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ChatAction, ParseMode
from telegram.error import NetworkError
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, MessageReactionHandler, filters
from gigachad import gigachad_vid
from telegram.ext import InlineQueryHandler, CallbackQueryHandler
from imagegen import ImageGenAsyncWithProxy
import logging
import json
import sys
from typing import List
from footnote_links import parse_text_with_footnote_links, replace_footnotes_with_html_url, remove_footnotes
from summarize import get_transcript
# from hug import Bot
from dotenv import load_dotenv
# from giga import Bot
# from gemini import Bot
from openrouter import Bot
# from hug import Bot
import yt_dlp
from yt_dlp.YoutubeDL import DownloadError
import os
# import cv2
# from yt_dlp.postprocessor.ffmpeg import FFmpegExtractAudioPP
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
from db import setup_database, store_message, get_user_id_by_message_id
from yt import download_random_short
import atexit
# from faces import facetrack_video
import io
import base64

load_dotenv()

logging.basicConfig(level=logging.INFO,format='%(asctime)s %(message)s')
cookies = json.loads(open("./new_cookie.json", encoding="utf-8").read())

conn = setup_database()
bot = Bot()


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
        if "не" in prompt.lower():
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


async def handle_add_to_chatbot_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    bot.add_context(f"Сообщение от пользователя {update.message.from_user.first_name} {update.message.from_user.username}: '{update.message.text}'")

async def handle_chatbot_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file = await update.message.photo[-1].get_file()
    iobufferedbase = io.BytesIO()
    await file.download_to_memory(iobufferedbase)
    iobufferedbase.seek(0)
    base64_encoded = base64.b64encode(iobufferedbase.read()).decode('utf-8')
    caption = update.message.caption if update.message.caption else None
    response_text = bot.ask_image(base64_encoded, caption)
    await update.message.reply_text(response_text, parse_mode=ParseMode.HTML)

async def handle_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.set_reaction("👌")
    reply_text = ""
    if update.message.reply_to_message and update.message.reply_to_message.from_user.username != "iLza_bot":
        reply_text = f"Сообщение от пользователя {update.message.reply_to_message.from_user.first_name} @{update.message.reply_to_message.from_user.username}: '{update.message.reply_to_message.text}'\n"
    try:
        stream = bot.ask_stream(reply_text + f"Сообщение от пользователя {update.message.from_user.first_name} {update.message.from_user.username}: '{update.message.text}'")
    except Exception as e:
        logging.exception(e)
        await update.message.set_reaction("😢")
        return;

    message = None
    every_30_messages = 0
    response_text = ""
    for response in stream:
        if response:
            response_text += response['token']
            every_30_messages += 1
        if not message:
            message = await update.message.reply_text(response_text, parse_mode=ParseMode.HTML)
        elif every_30_messages % 30 == 0:
            await message.edit_text(response_text, parse_mode=ParseMode.HTML)
    if message:
        await message.edit_text(response_text, parse_mode=ParseMode.HTML)


    # if "нет" in response_text.lower():
    #     await gigachad_vid(f"@{update.message.from_user.username}\: {update.message.text}",f"@iLza_bot\: {response_text}")
    #     await update.message.reply_video("./output_final.mp4")


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
    bot.reset()
    await update.message.reply_text("Чат стерт")

app = ApplicationBuilder().media_write_timeout(240).token(os.getenv("TELEGRAM_TOKEN")).build()


random.seed(time.time())
i=0
ahmetoff_message_count = 1  # Variable to keep track of the message count for user 'ahmetoff'
androncerx_message_count = 1  # Variable to keep track of the message count for user 'ahmetoff'
rate_limit = 5  # 1 message per second

# Dictionary to keep track of the last message time for each user
last_message_time = {}

async def post_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if(update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot):
        return await handle_chatbot(update,context)
    text = update.message.text.lower()
    global ahmetoff_message_count  # Access the message count variable
    global androncerx_message_count  # Access the message count variable
    if text.startswith("/imagegen") and update.message.message_thread_id != 39:
        await update.message.reply_text("Не тот чат чертила, пиши в iLzaBot & AI Stuff")
        await update.message.delete()
        return
    user_id = update.message.from_user.id
    current_time = time.time()
    if not(any(name in text for name in ['ильза','ильзух'])):
        await handle_add_to_chatbot_history(update,context)
    imagegen_count = text.count("/imagegen")
    if imagegen_count > 1:
        await update.message.reply_text("Много имагегенов в одном сообщении, УДАЛЯЮ")
        await update.message.delete()
        return;

    if text.startswith("/imagegen") and user_id in last_message_time and current_time - last_message_time[user_id] < rate_limit:
        await update.message.delete();
        return

    if text.startswith("/imagegen"):
        last_message_time[user_id] = current_time

    if (ahmetoff_message_count + androncerx_message_count) % 25 == 0:
        await update.message.reply_video("./fight1.mp4")
        ahmetoff_message_count += 1  # Variable to keep track of the message count for user 'ahmetoff'
        androncerx_message_count += 1  # Variable to keep track of the message count for user 'ahmetoff'
        return
    if update.message.from_user.username == 'Arsn17' and text.startswith("/imagegen"):
            short = download_random_short();
            await update.message.set_reaction("👌")
            selected_video = facetrack_video(short)
            await update.message.reply_video(selected_video)
            return
    if update.message.from_user.username == 'serene_boy' and text.startswith("/imagegen"):
        short = download_random_short();
        await update.message.set_reaction("👌")
        selected_video = facetrack_video(short)
        await update.message.reply_video(selected_video)
        return
    if update.message.from_user.username == 'ahmetoff' and text.startswith("/imagegen"):
        ahmetoff_message_count += 1
        short = download_random_short();
        await update.message.set_reaction("👌")
        selected_video = facetrack_video(short)
        await update.message.reply_video(selected_video)
        return
    if update.message.from_user.username == 'androncerx' and text.startswith("/imagegen"):
        androncerx_message_count += 1
        short = download_random_short();
        await update.message.set_reaction("👌")
        selected_video = facetrack_video(short)
        await update.message.reply_video(selected_video)
        return
    if '/ilzadembel' in text:
        date = relativedelta(datetime.now(), datetime(2016, 5, 22))
        await update.message.reply_text(f"Со времен возвращения илюззии прошло {date.years} лет {date.months} месяцев {date.days} дней 👮")
    elif 'ильза' in text.lower():
        await handle_chatbot(update, context)
    elif 'ильзух' in text.lower():
        await handle_chatbot(update, context)
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
    elif any(link in text for link in ['douyin.com','youtube.com/clip/','youtube.com/shorts/','instagram.com/reel/', "x.com/", 'twitter.com/', 'reddit.com/','tiktok.com']):
        text = update.message.text
        link_regex = r'(https?://(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
        match = re.search(link_regex, text)
        await update.message.set_reaction("👌")
        # Download the video using yt-dlp
        try:
            proxy = 'http://localhost:8092' if 'reddit.com/' not in match.group(0) else None
            with yt_dlp.YoutubeDL({'outtmpl': 'video.%(ext)s',"overwrites": True,"format":"bv*[ext=mp4][filesize<10M]+ba[ext=m4a]/b[ext=mp4][filesize<10M] / bv*+ba/b", 'cookiefile': './instacookie',
                                'proxy': proxy,
                                'postprocessors': [{
                                    "key": "FFmpegVideoRemuxer",
                                    "preferedformat": "mp4"
                                }]
                                }) as ydl:
                ydl.download([match.group(0)])
        except DownloadError:
            await update.message.set_reaction("😢")
            return
        try:
            reply = await update.message.reply_video(video='./video.mp4',caption = f"<b>@{update.message.from_user.username or update.message.from_user.first_name}</b>:\n{update.message.text}",parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"An error occurred: {e}. Retrying...")
            await update.message.set_reaction("😡")
            try:
                reply = await update.message.reply_video(video='./video.mp4',caption = f"<b>@{update.message.from_user.username or update.message.from_user.first_name}</b>:\n{update.message.text}",parse_mode=ParseMode.HTML)
            except Exception as e:
                print(f"An error occurred again: {e}. Setting reaction to crying emoji...")
                await update.message.set_reaction("😢")
                return
            return
        await update.message.delete()
        store_message(conn, reply.message_id, update.message.from_user.id)

    elif any(link in text for link in ['youtube.com/','youtu.be']):
        text = update.message.text
        link_regex = r'(https?://(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
        match = re.search(link_regex, text)
        link = match.group(0);
        transcript = get_transcript(link);
        if transcript:
            answer = bot.ask(f'(Отвечай по русски!) Извлеки суть: "{transcript}" (Отвечай по русски!)')
            await update.message.reply_text(answer)

def convert_video_to_gif(video_path, gif_path, max_width=480):
    clip = VideoFileClip(video_path)
    resized_clip = clip.resize(0.3)
    resized_clip.write_gif(gif_path, fps=10, opt='OptimizePlus', fuzz=10)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video
    if video and video.duration <= 15:
        video_file = await context.bot.get_file(video)
        await video_file.download_to_drive('video.mp4')

        convert_video_to_gif('video.mp4', 'output.gif')

        with open('output.gif', 'rb') as gif:
            await update.message.reply_document(document=gif)
            await update.message.delete()

        os.remove('video.mp4')
    else:
        await update.message.reply_text('Please send a video shorter than 30 seconds.')

def add_text_to_gif(gif_path, text, start_time, end_time, text_color='white', font_size=36, font='/nix/var/nix/profiles/system/sw/share/X11/fonts/Roboto-Medium.ttf'):
    clip = VideoFileClip(gif_path)
    text_clip = TextClip(text, font=font, fontsize=font_size, color=text_color)
    text_clip = text_clip.set_position(('center',"bottom"))
    final_clip = CompositeVideoClip([clip, text_clip.set_duration(end_time - start_time).set_start(start_time)])
    final_clip.write_gif(gif_path, fps=10, opt='OptimizePlus', fuzz=10)

async def add_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) >= 3:
        start_time = float(args[0])
        end_time = float(args[1])
        text = ' '.join(args[2:])

        add_text_to_gif('output.gif', text, start_time, end_time)

        with open('output.gif', 'rb') as gif:
            await update.message.reply_document(document=gif)
            await update.message.delete()
    else:
        await update.message.reply_text('Usage: /add-text <start time> <end time> <text>')

async def handle_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reaction = update.message_reaction.new_reaction
    message_id = update.message_reaction.message_id
    chat_id = update.message_reaction.chat.id
    username = update.message_reaction.user.username
    user_id = get_user_id_by_message_id(conn, message_id)
    if user_id is not None:
        emoji = reaction[0].emoji
        await context.bot.send_message(chat_id=user_id, text=f"@{username}: {emoji}", reply_parameters=ReplyParameters(message_id,chat_id))



async def leaderboards(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Fetch the leaderboard data from the cloud storage
    async with aiohttp.ClientSession() as session:
        async with session.get('https://ahmetgame-2c5cd-default-rtdb.europe-west1.firebasedatabase.app/leaderboards.json') as response:
            if response.status == 200:
                leaderboard = await response.json()
                leaderboard_text = "Leaderboard:\n"
                for entry in leaderboard:
                    leaderboard_text += f"@{entry['name']}: {entry['score']}\n"
                
                button = InlineKeyboardButton("Play the game", url="https://t.me/iLza_bot/ahmet")
                reply_markup = InlineKeyboardMarkup([[button]])
                
                await update.message.reply_text(leaderboard_text, reply_markup=reply_markup)
            else:
                await update.message.reply_text('Failed to load leaderboard.')

app.add_handler(CommandHandler("leaderboards", leaderboards))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("newchat", newchat))
app.add_handler(CommandHandler('add_text', add_text))
app.add_handler(MessageHandler(filters.PHOTO,handle_chatbot_photo))
app.add_handler(MessageHandler(filters.TEXT & filters.Entity('mention') & filters.Regex('@iLza_bot'),handle_chatbot))
app.add_handler(MessageHandler(filters.TEXT,post_msg))
app.add_handler(CallbackQueryHandler(button_click))
app.add_handler(MessageReactionHandler(handle_reactions))

async def main():
    global bot;
    print(os.getcwd())
    print(os.environ.get('PATH'))

try:
    atexit.register(bot.cache_context)
    import os
    if os.getenv("HOSTTYPE") == "armv7l":
        app.run_webhook(
            listen="0.0.0.0",
            port=9999,
            webhook_url='https://bots.upgradegamma.ru/'
            # secret_token=''
        )
    else:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
        app.run_polling(allowed_updates=Update.ALL_TYPES, close_loop=False)
        loop.close()
except NetworkError as e:
    pass
except Exception as e:
    logging.exception(e)
