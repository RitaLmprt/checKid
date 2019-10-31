#!/usr/bin/env python
import time
import click
from datetime import datetime
import requests


@click.command()
@click.argument('period', default=60*5)
def run(period):
	while True:
		print("cron %s" % datetime.now())
		query(datetime.now())
		time.sleep(period)


def query(now):
	# type: (datetime) -> None
	r = requests.get('http://localhost:3000/classes')
	data = r.json()
	msg = ' Send sms'
	#sms = requests.post("https://www.sms4free.co.il/ApiSMS/SendSMS" , data = {'key' : '94Ccwa8G5','user' : '0544840133', 'pass' : 94627586, 'sender' : 'checkid', 'recipient' : '0544846033', 'msg' : msg})
	#print(sms.status_code, sms.reason)

	for item in data:
		class_id = str(item["id"])
		name = item["name"]
		alert_str = item["alert"]
		alert = datetime.strptime(alert_str, '%H:%M').time()
		needs_alert = alert < now.time()
		print("class: %s, alert: %s" % (name, alert_str))
		print("Needs alert: %s" % needs_alert)
		if needs_alert == True:
			sendAlert(class_id)
			url = 'http://localhost:3000/classes/%s' % class_id
			timestamp = datetime.now().timestamp()
			item.update({"last_alert": timestamp})
			r1 = requests.put(url, verify=False, json=item)
			print(r1.status_code)

def sendAlert(class_id):
	url1 = 'http://localhost:3000/students?_expand=class&classId=%s' % class_id
	r2 = requests.get(url1)
	data1 = r2.json()
	for item1 in data1:
		kid_id = item1["kidId"]
		url2 = 'http://localhost:3000/guardians'
		r3 = requests.get(url2)
		data2 = r3.json()
		for item2 in data2:
			guarded_kid = item2["kidId"]
			if kid_id == guarded_kid:
				adult_id = item2["adultId"]
				print("Need to send alert about child %s to guardian %s" %(kid_id, adult_id))










if __name__ == "__main__":
	 run()
	

	