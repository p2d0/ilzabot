#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p "python3.withPackages(ps: [ ps.requests ps.dateutil ps.beautifulsoup4 ])"

import requests
import time
from datetime import datetime
import responses
import random
from dateutil.relativedelta import relativedelta
from pp2 import pp_calc


random.seed(time.time())
def find_msg(num):
	print(get_update['result'][len(get_update['result'])-num])
	last_message = get_last_message();
	print(last_message)
	return last_message['text'].lower().replace('?','').replace('!','')

def send_msg(msg):
	text = last_message['text']
	chat_id = get_last_message()['chat']['id']
	send_msg = requests.post(get_info('sendMessage'),{'chat_id': chat_id, 'text': msg, 'reply_to_message_id': last_message['message_id'],'parse_mode':'markdown'})

def get_info(method_name):
	return 'https://api.telegram.org/bot233787808:AAH71m_JtqkQP5ZADD2yxYI2ye8TKTeMnxE/' + method_name

def post_msg():
	last_message = get_last_message();
	chat_id = last_message['chat']['id']
	if("text" not in last_message):
		return
	text = last_message['text']
	if '/pp' in text.lower():
		pp_calc()
	elif '/ilzadembel' in text.lower():
		date = relativedelta(datetime.now(),datetime(2016,5,22));
		send_msg("Со времен возвращения илюззии прошло {} лет {} месяцев {} дней 👮".format(date.years,date.months,date.days))
	elif '/eugenedembel' in text.lower():
		date = datetime(2022,12,6) - datetime.now();
		send_msg("До возвращения Жеки осталось: " + str(date.days) + " дней  👮 (+-пару дней)")
	elif '/pauk' in text.lower():
		date = datetime(2021,12,18,10,20) - datetime.now();
		send_msg("До паука осталось: " + str(int(date.seconds/3600)) + " часов " + str(int((date.seconds/60)%60 )) + " минут")
	elif '/help' in text.lower():
		send_msg('''```
			list of commands:
			/pp - посмотреть сколько нафармили боги из топ 50
			на этом всё```''')
	elif 'нет' in text[len(text)-3:].lower():
		print (text[len(text)-3:])
		rand = [1,1,1]
		temp = responses.responses_list[random.randint(0,len(responses.responses_list))]
		if temp in rand:
			temp = responses.responses_list[random.randint(0,len(responses.responses_list))]
		send_msg(temp)
		rand[i] = temp
	elif 'да' in text[len(text)-2:].lower():
		print (text[len(text)-2:])
		da_used_list = [1,1,1];
		temp = responses.da_responses_list[random.randint(0,len(responses.da_responses_list))]
		if temp in da_used_list:
			temp = responses.da_responses_list[random.randint(0,len(responses.da_responses_list))]
		send_msg(temp)
		da_used_list[i] = temp
	elif 'ржд' in text:
		send_msg('Я')
	elif 'https://osu.ppy.sh/ss/' in text:
		send_msg('Ебнутый')
	elif find_msg(1) in responses.pizda_list and (find_msg(2) in responses.pizda_list or find_msg(3) in responses.pizda_list):
		send_msg(' '.join(responses.pizda_list[2:]))
	elif find_msg(1) in responses.kakay_list[0][0]:
		send_msg(' '.join(responses.kakay_list[0]))
	elif find_msg(1) in responses.ruka_list:
		send_msg(' '.join(responses.ruka_list))
	elif find_msg(1) in responses.money_list:
		send_msg(' '.join(responses.money_list))
	elif 'иди нахуй' in find_msg(1):
		send_msg(responses.hui)
	elif 'можно' in find_msg(1):
		send_msg(responses.mozhno_responses_list[random.randint(0,len(responses.mozhno_responses_list))])
	elif 'интересно ' in find_msg(1):
		send_msg('интересно когда в бане тесно')
	elif '@iLza_bot' in text:
		send_msg("Спасибо")
	elif find_msg(1) in responses.zhui_list and responses.zhui_list.index(find_msg(1)) != responses.zhui_list[-1]:
		send_msg(responses.zhui_list[responses.zhui_list.index(find_msg(1))+1])
i = 0
id = 0
get_update = requests.get(get_info('getUpdates')).json()

def get_last_message():
	get_update = requests.get(get_info('getUpdates')).json()
	update = get_update['result'][len(get_update['result'])-1]
	if('message' in update):
		return update['message']
	else:
		return update['edited_message']

last_message = get_last_message();

while True:
	if last_message['message_id'] == id:
		get_update = requests.get(get_info('getUpdates'),{'offset':get_update['result'][len(get_update['result'])-1]['update_id']-2}).json()
		last_message = get_update['result'][len(get_update['result'])-1]['message']
		time.sleep(0.5)
		continue
	id = last_message['message_id']
	try:
		print(last_message['text'])
	except KeyError:
		pass
	print(get_update['result'][len(get_update['result'])-1]['update_id'])
	post_msg()
	i+=1
	if i > 2:
		i = 0
