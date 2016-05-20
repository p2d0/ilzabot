import requests
import time
import responses
import random
random.seed(53231)
def find_msg(num):
	return get_update['result'][len(get_update['result'])-num]['message']['text'].lower().replace('?','').replace('!','')

def send_msg(msg):
	text = last_message['text']
	chat_id = get_update['result'][len(get_update['result'])-1]['message']['chat']['id']
	send_msg = requests.post(get_info('sendMessage'),{'chat_id': chat_id, 'text': msg, 'reply_to_message_id': last_message['message_id']})

def get_info(method_name):
	return 'https://api.telegram.org/bot233787808:AAH71m_JtqkQP5ZADD2yxYI2ye8TKTeMnxE/' + method_name

def post_msg():
	chat_id = get_update['result'][len(get_update['result'])-1]['message']['chat']['id']
	text = last_message['text']
	print(chat_id)
	
	if 'нет' in text[len(text)-3:].lower():
		print (text[len(text)-3:])
		rand = [1,1,1]
		temp = responses.responses_list[random.randint(0,len(responses.responses_list))]
		if temp in rand:
			temp = responses.responses_list[random.randint(0,len(responses.responses_list))]
		send_msg(temp)
		rand[i] = temp
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
	elif 'можно' == find_msg(1):
		send_msg('можно машку за ляжку и козу на возу')
	elif 'интересно ' in find_msg(1):
		send_msg('интересно когда в бане тесно') 
	elif find_msg(1) in responses.zhui_list and responses.zhui_list.index(find_msg(1)) != responses.zhui_list[-1]:
		send_msg(responses.zhui_list[responses.zhui_list.index(find_msg(1))+1])
	elif 'кто пидор' in find_msg(1):
		send_msg('Серега')
i = 0
id = 0
get_update = requests.get(get_info('getUpdates')).json()
last_message = get_update['result'][len(get_update['result'])-1]['message']
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
	