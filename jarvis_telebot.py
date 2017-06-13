import json
import requests
import time
import urllib
#from urlparse import urlparse
from jarv_telebot_db import DBHelper
CHID = [];
tm = {};
k = -1;
l = {};
TOKEN="397103390:AAFaqnt0Tlbn8lDwfrTN73yIaMsQG9kW6DY";
URL = "https://api.telegram.org/bot{}/".format(TOKEN);
db = DBHelper();

def build_key(items):
	key = [[item] for item in items];
	rply = {"keyboard":key,"one_time_keyboard":True};
	return json.dumps(rply); 

def get_json(url):
	res = requests.get(url);
	con = res.content.decode("utf8");
	js = json.loads(con)
	return js

def get_up(offset=None):
	url = URL + "getUpdates";
	if(offset):
		url += "?timeout=10&offset={}".format(offset);
	return get_json(url); 

def send_mess(text,chid,rply_m=None):
	url = URL + "sendmessage?chat_id={}&parse_mode=Markdown".format(chid);
	if rply_m:
		url+="&reply_markup={}".format(rply_m)
	if text:
		text = urllib.parse.quote_plus(text);
		url+="&text={}".format(text)
	get_json(url);

def getmess(up):
	n = len(up["result"])
	i = n - 1;
	ti = time.localtime(time.time());
	print(1);
	for ch in CHID:
		ke = ti.tm_year+ti.tm_yday+ti.tm_min;
		if ke> tm[ch] and l[ch]==0:
			key = build_key(["start"])
			send_mess("....",ch,rply_m=key);
			l[ch]=1
	if i< 0:
		return
	k = up["result"][i]["update_id"];
	while i>=0:
		text = up["result"][i]["message"]["text"]
	       # print(text);
		chid = up["result"][i]["message"]["chat"]["id"]
		if chid not in CHID:
			CHID.append(chid);
		l[chid]=0;
		tm[chid] = ti.tm_year+ti.tm_yday+ti.tm_min
		print(str(tm[chid])+" uptime")
		ite = db.get_items(chid);
		if text == '/done':
			key = build_key(ite);
			send_mess("select to delete",chid,key)
		else:
			if text in ite:
				db.delete_item(text,chid);
			else:
				db.add_item(text,chid);
			ite = db.get_items(chid);
			text = "";
			for ite1 in ite:
				text += ite1 + "\n"
			if(text == ""):
				text = "no items in to-do"
			send_mess(text,chid);
		i=i-1;
	get_up(k+1);
	
if __name__ == '__main__':
	db.setup();
	while True:
		getmess(get_up());
		time.sleep(1);
	











		
