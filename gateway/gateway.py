import hashlib;
import hmac;
import datetime;
import paho.mqtt.client as mqtt
import json
import calendar
import requests

broker = "postman.cloudmqtt.com"
username = ***REMOVED***
password = ***REMOVED***
port = 18467

def on_connect(mqttc, obj, flags, rc):
   print("Connected with result code "+str(rc))
   client.subscribe("gateway_identifier/device_identifier")
# The callback for when a PUBLISH message is received from the server.

def on_message(client, userdata, msg):
   v=str(msg.payload.decode('utf8'))   #string comes in as bytes so need to convert it
   sample=json.loads(v)
   t=str(sample['time'])
   t=t[1:]
   t=t[:-1]
   t=t.split(",")
   time_t=datetime.datetime(int(t[0]), int(t[1]), int(t[2]), int(t[4]), int(t[5]), int(t[6]), int(t[7]))
   timestamp_utc = calendar.timegm(time_t.timetuple())
   print('Processing sample : ' + str(sample['value']))
   body='{ "device":"' + str(sample['device']) + '", "sample_date" : "' + time_t.strftime("%Y-%m-%d") + '", "value":"' + str(sample['value']) + '", "time":"' + repr(timestamp_utc) + '" }'
   #secret = #b'Enter your MongoDB Stitch Webhook password here'
   #hash = hmac.new(secret, body.encode("utf-8"), hashlib.sha256)
   #url = #enter your Stitch Web API URL here
   header={"Content-Type":"application/json","X-Hook-Signature":"sha256=" + hash.hexdigest() }
   myResponse = requests.post(url,headers=header, data=body )
   print (myResponse.status_code)
# uncomment to debug
def on_log(mqttc, obj, level, string):
   print('Connecting to MQQT broker')
client = mqtt.Client()
client.on_message = on_message
client.on_connect = on_connect
client.on_log = on_log
client.connect(broker, port, 60)
client.username_pw_set(username, password)

client.loop_forever()