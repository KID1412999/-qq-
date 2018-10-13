#获取uins方法
#给定qq号，找和他相关的qq号，返回列表
import networkx as nx
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import random
import sys	
import requests
import re
import json
import time
import jsonpath
import nltk

my_friend=[]
friend=[]
uinkey=[]
url='https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi'
url2='https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6'
url3='https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com/cgi-bin/new/get_msgb'
url4='https://user.qzone.qq.com/proxy/domain/users.qzone.qq.com/cgi-bin/likes/get_like_list_app'
url5= 'http://www.xicidaili.com/nn/'#代理IP获取网址

header={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
data={
'uin': '****',
'g_tk':'1594482951',
'do': '1',
	}
data2={
"uin":"****",
"pos":"0",#移动
"num":"20",#显示的页数
"g_tk":"1594482951"
}
data3={
'hostUin': '****',
'start': '0',#移动
's': '0.5485568764022071',
'num': '10',
'g_tk': '1594482951',
}
data4={
'uin':'****',#自己qq
'unikey': '****',
'begin_uin': '0',
'query_count': '60',
'if_first_page': '1',
'g_tk': '1166180126'
}
def get_ip_list(url, headers):
	web_data = requests.get(url, headers=headers)
	soup = BeautifulSoup(web_data.text, 'lxml')
	ips = soup.find_all('tr')
	ip_list = []
	for i in range(1, len(ips)):
		ip_info = ips[i]
		tds = ip_info.find_all('td')
		ip_list.append(tds[1].text + ':' + tds[2].text)
	return ip_list

def get_random_ip(ip_list):
	proxy_list = []
	for ip in ip_list:
		proxy_list.append('http://' + ip)
	proxy_ip = random.choice(proxy_list)
	proxies = {'http': proxy_ip}
	return proxies

def update_cookie_gtk(uin,myuin,password):#更新cookie和gtk
	def LeftShiftInt(number, step):	 # 由于左移可能自动转为long型，通过这个转回来	
		return int(number << step)
	def LongToInt(value):# 由于int+int超出范围后自动转为long型，通过这个转回来	
		if isinstance(value, int):
			return int(value)
		else:
			return int(value & sys.maxint) 
	def getGTK(cookie):
		a = 5381
		for i in range(0, len(skey)):  
			a = a + LeftShiftInt(a, 5) + ord(skey[i])  
			a = LongToInt(a)  
		return a & 0x7fffffff
	def getNewGTK(p_skey, skey):  
		b = p_skey or skey	
		a = 5381
		for i in range(0, len(b)):	
			a = a + LeftShiftInt(a, 5) + ord(b[i])	
			a = LongToInt(a)  
		return a & 0x7fffffff
	driver = webdriver.Chrome()
	driver.get('https://user.qzone.qq.com/'+uin)
	driver.switch_to.frame('login_frame')
	driver.find_element_by_id('switcher_plogin').click()
	driver.find_element_by_id('u').clear()
	driver.find_element_by_id('u').send_keys(myuin)	 #这里填写你的QQ号
	driver.find_element_by_id('p').clear()
	driver.find_element_by_id('p').send_keys(password)	#这里填写你的password
	driver.find_element_by_id('login_button').click()
	time.sleep(2)
	#---------------获得 gtk
	cookie = {}#初始化cookie字典
	for elem in driver.get_cookies():#取cookies
		cookie[elem['name']] = elem['value']
	# print(cookie)
	gtk=getNewGTK(cookie['p_skey'],cookie['skey'])
	cookieText =''
	for item in driver.get_cookies():#解析cookies
		cookieText = cookieText + item['name'] + '=' + item['value'] + ';'
	cookieText = cookieText[0:-1]
	data.update({'g_tk':gtk})
	data2.update({'g_tk':gtk})
	data3.update({'g_tk':gtk})
	data4.update({'g_tk':gtk})
	data2.update({'uin':uin})
	data3.update({'hostUin':uin})
	header.update({'cookie': cookieText})
def loads_jsonp(_jsonp):#将jsonp转为python对象
		try:
			return json.loads(re.match(".*?({.*}).*",_jsonp,re.S).group(1))
		except:
			raise ValueError('Invalid Input')

def get_like(uin,ip):#获取点赞列表
	for i in range(2):
		data4.update({'if_first_page':str(i)})
		for key in uinkey:
			data4.update({'unikey':'http://user.qzone.qq.com/'+uin+'/mood/'+key})
			#html=requests.get(url4,headers=header,params=data4,proxies=get_random_ip(ip))
			html=requests.get(url4,headers=header,params=data4)
			if html.text:
				t=loads_jsonp(html.text)
				l=jsonpath.jsonpath(t,'$..fuin')
				if l:
					for i in l:
						friend.append(str(i))
					# print(friend,len(friend))
def deal(html_text,r):#将数据存入friend列表或uinkey列表
	t=loads_jsonp(html_text)
	l=jsonpath.jsonpath(t,r)
	for i in l:
		if r=='$..uin':
			friend.append(str(i))
		else:
			if isinstance(i,str):
				uinkey.append(i)
	# if r=='$..tid':
		# print(uinkey,len(uinkey))
	# else:
		# print(friend,len(friend))
def serch(k_,k,ip):
	# #说说#
	for m in range(0,k_*20,20):
		data.update(pos=m)
		#html=requests.get(url2,headers=header,params=data2,proxies=get_random_ip(ip))
		html=requests.get(url2,headers=header,params=data2)
		deal(html.text,'$..uin')
	#点赞
	# for m in range(0,k_*20,20):
		# data.update(pos=m)
		# html=requests.get(url2,headers=header,params=data2,proxies=get_random_ip(ip))
		# deal(html.text,'$..tid')
	# #留言# 
	# for n in range(0,k*10,10):
		# time.sleep(1)
		# data.update(start=n)
		# html=requests.get(url3,headers=header,params=data3)
		# deal(html.text,'$..uin')


def uin2uins(uin,myuin,password):
	global friend,people
	friend=[]
	uinkey=[]
	ip_list = get_ip_list(url5, headers=header)#获取IP
	uin=uin#目标qq
	myuin=myuin#myqq
	password=password#
	update_cookie_gtk(uin,myuin,password)#更新cookie等信息0 
	serch(1,1,ip_list)#查看2页说说1页留言
	#get_like(uin,ip_list)#获取点赞好友
	n =10#获取信息条数
	a = nltk.FreqDist(friend)
	L = sorted(a.items(),key=lambda item:item[1],reverse=True)
	dictdata =[]
	for l in L[:n]:
		dictdata.append(l[0])
	print(list(set(dictdata)))
	return list(set(dictdata))
if __name__=='__main__':
	uin2uins('hostuin','yourqq','password')
