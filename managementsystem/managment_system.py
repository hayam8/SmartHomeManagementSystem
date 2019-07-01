"""
TODO: 
    Make managment_system file
    connect it to broker with code
    have it send broker on_message() data to mongoDB in cloud
    TEST with data from Haya

"""


import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime
from pymongo import MongoClient
import http.client
import json
***REMOVED***
***REMOVED***
from six.moves.urllib.request import urlopen

#Gateway Name
__name = "Pi_Gateway"
__gateway_port = 1883
# MQTT settings for MQTT communication that takes place locally on gateway
__gateway_broker = ""

# MQTT Settings for CloudMQTT broker working in cloud
__cloud_broker = "postman.cloudmqtt.com"
__cloud_port = 18467
__username = ""
__password = ""


# MongoDB Name
# Populate with unique uri
uri = ""
db = MongoClient(uri)
database = db['gateway']
collection = database['DHT22']
mqtt_topics = __name + "/#" # all topics/devices under Pi_Gateway
mqtt_post_topics = __name + "/"
__Keep_Alive_Interval = 45

def on_connect(client, userdata,flags, rc):
    
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(__cloud_broker))
        client.subscribe(mqtt_topics)
        print("On_connect")
        publish_fake_message("gateway_identifier/DHT22/Humidity",__cloud_client)

def on_publish(client, userdata,flags, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass

"""
    This method is responsible for adding sensor data to the gateway local storage which is implemented with 
    MongoDB
"""
def on_message(client, userdata,flags, msg):
    print("Message recived")
    receive_time = datetime.datetime.now()
    message = msg.payload.decode("utf-8")
    is_float_value = False
    try:
        val = float(message)
        is_float_value = True
    except:
        is_float_value = False

    if is_float_value:
        print(str(receive_time) + ": " + msg.topic + " " + str(val))
        post = {"time": receive_time, "topic": msg.topic, "value": val}
    else:
        print(str(receive_time) + ": " + msg.topic + " " + message)
        post = {"time": receive_time, "topic": msg.topic, "value": message}
    collection.insert_one(data)
    

# connecting to MQTT Cloud broker and setting commands
__cloud_client = mqtt.Client(__name)
__cloud_client.on_connect = on_connect
__cloud_client.on_disconnect = on_disconnect
__cloud_client.on_publish = on_publish
__cloud_client.on_message = on_message
__cloud_client.connect(__cloud_broker, int(__cloud_port), int(__Keep_Alive_Interval))
__cloud_client.username_pw_set(__username, __password)  # must log in with username/pass for broker

def publish_fake_message(topic, clients):
    __cloud_client = clients
    humidity_data = {}
    humidity_data['Sensor_ID'] = "Dummy-1"
    humidity_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
    humidity_data['Humidity'] = 322
    humidity_json_data = json.dumps(humidity_data)
    message = humidity_json_data
    __cloud_client.publish(topic, message)


__cloud_client.loop_forever()
