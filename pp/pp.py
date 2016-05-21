import urllib.request
from bs4 import BeautifulSoup
from lxml.html import parse
import re
import os
import requests
requests.get
pagecounter = 'https://osu.ppy.sh/p/pp/?m=0&s=3&o=1&f=&page='
top = {}
text_file = open('C:\\kek.txt',"w")

for lul in range(1,3):
	print (pagecounter+str(lul))
	page = urllib.request.urlopen(pagecounter+str(lul))
	soup = BeautifulSoup(page,'lxml')
	keksearch = soup.find_all(href=re.compile('/u/'))
	for kek in keksearch:
		
		mainKek = kek['href'].split('/u/')[-1]
		print (mainKek)
		kekData = {'k':'b40b7a7a8207b1ebd870eaf1f74bd2995f1a2cb6','u': mainKek}
		res = requests.get('https://osu.ppy.sh/api/get_user_best',kekData)
		nickRes = requests.get('https://osu.ppy.sh/api/get_user',kekData)
		ppRain = res.json()
		ppName = nickRes.json()
		top[ppRain[0]['pp']] = '#' + ppName[0]['pp_country_rank'] + ' ' + ppName[0]["username"] + ' ' + ppRain[0]['pp']
path = "C:\\kek"
if not os.path.exists(path):
	os.makedirs(path)
i = 1
for lele in sorted(top, reverse=True):
	text_file.write(str(i) + "  " + top[lele] + '\n')
	i+=1
text_file.close