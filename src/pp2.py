import urllib.request
from bs4 import BeautifulSoup
from lxml.html import parse
import re
import os
import requests
import id_list
def pp_calc():
	info = ''
	def get_info(method_name):
		return 'https://api.telegram.org/bot233787808:AAH71m_JtqkQP5ZADD2yxYI2ye8TKTeMnxE/' + method_name
	get_update = requests.get(get_info('getUpdates')).json()
	last_message = get_update['result'][len(get_update['result'])-1]['message']
	
	def send_msg(msg):
		text = last_message['text']
		chat_id = get_update['result'][len(get_update['result'])-1]['message']['chat']['id']
		send_msg = requests.post(get_info('sendMessage'),{'chat_id': chat_id, 'text': msg, 'reply_to_message_id': last_message['message_id'],'parse_mode':'markdown'})
	top = ''
	same_file = open('C:\\Users\\thepa\Documents\GitHub\ilzabot\pp_values.txt',"r")
	top_previous = same_file.read().split(';')
	del top_previous[-1]
	print (top_previous)
	same_file.close()
	text_file = open('C:\\Users\\thepa\Documents\GitHub\ilzabot\pp_values.txt',"w")
	
	for kek in id_list.id_list:
		print (kek)
		kekData = {'k':'b40b7a7a8207b1ebd870eaf1f74bd2995f1a2cb6','u': kek}
		nickRes = requests.get('https://osu.ppy.sh/api/get_user',kekData).json()
		top +=nickRes[0]['username']+':'+nickRes[0]['pp_raw']+';'
	top_list = top.split(';')
	del top_list[-1]
	
	text_file.write(top)
	print(top_list)
	for i,num in enumerate(top_list):
		if top_list[i].split(':')[1] not in top_previous[i].split(':')[1]:
			sum = int(top_list[i].split(':')[1]) - int(top_previous[i].split(':')[1])
			info +=top_list[i].split[0] + 'поднял' + str(sum) + '\n'
	send_msg('```' + info +'```')
	
	text_file.close()	