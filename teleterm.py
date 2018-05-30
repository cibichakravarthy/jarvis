import json
import requests
import time
import urllib
import subprocess
import shlex
#from urlparse import urlparse
CHID = [];
tm = {};
k = -1;
l = {};
TOKEN="528755840:AAFplUr6mhusmKwPgF0f9r04DTncetzPi78";
URL = "https://api.telegram.org/bot{}/".format(TOKEN);

def get_json(url):
	res = requests.get(url);
	con = res.content.decode("utf8");
	js = json.loads(con)
	return js

def get_up(offset=None):
	url = URL + "getUpdates";
	if(offset):
		url += "?offset={}".format(offset);
	return get_json(url); 

def send_mess(text,chid,rply_m=None):
	url = URL + "sendmessage?chat_id={}&parse_mode=Markdown".format(chid);
	if rply_m:
		url+="&reply_markup={}".format(rply_m)
	if text:
		#text = urllib.parse.quote_plus(text);
		url+="&text={}".format(text)
	get_json(url);


def get_mess(messages):
	messages = messages["result"]
	offset = 0;
	for message in messages:
		offset = message["update_id"];
		message = message["message"];
		sender = message["from"];
		if  "first_name" in sender.keys() and sender["first_name"]=="C_b_":
			text = message["text"]
			args = shlex.split(text)
			output = "ERROR ";
			print(text)
			try:
				output,error = subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE).communicate();
				print(output.decode("ascii"));
				print(sender["id"])
				output = output.decode('ascii');
				output = output.split("\n");
				for out in output:
					send_mess(out,sender["id"]);
				send_mess(error,sender["id"]);
			except:
				print("error");
		else:
			send_mess("I wont serve you",sender["id"]);
			
	return offset + 1	 

if __name__ == '__main__':
	offset=None
	while True:
		offset = get_mess(get_up(offset));
		time.sleep(1);


