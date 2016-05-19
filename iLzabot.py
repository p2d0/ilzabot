import requests
import time
from responses import responses_list
import random

random.seed(53231)
def send_msg(msg):
	random.seed(time.time())
	text = last_message['text']
	chat_id = get_update['result'][len(get_update['result'])-1]['message']['chat']['id']
	send_msg = requests.post(get_info('sendMessage'),{'chat_id': chat_id, 'text': msg, 'reply_to_message_id': last_message['message_id']})
def get_updates():
	return requests.get(get_info('getUpdates')).json()
def get_info(method_name):
	return 'https://api.telegram.org/bot233787808:AAH71m_JtqkQP5ZADD2yxYI2ye8TKTeMnxE/' + method_name
def post_msg():
	chat_id = get_update['result'][len(get_update['result'])-1]['message']['chat']['id']
	text = last_message['text']
	data = {}
	print(chat_id)
	if 'нет' in text[len(text)-3:]:
		print (text[len(text)-3:])
		send_msg(responses_list[random.randint(0,len(responses_list))])
	elif 'https://osu.ppy.sh/ss/' in text:
		send_msg('Ебнутый')
		
id = 0
get_update = requests.get(get_info('getUpdates')).json()
last_message = get_update['result'][len(get_update['result'])-1]['message']
while True:
	if last_message['message_id'] == id:
		get_update = requests.get(get_info('getUpdates')).json()
		last_message = get_update['result'][len(get_update['result'])-1]['message']
		time.sleep(0.5)
		continue
	id = last_message['message_id']
	print(last_message['text'])
	post_msg()
	