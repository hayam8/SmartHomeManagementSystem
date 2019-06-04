import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime
from pymongo import MongoClient

"""
NEEDS TO BE IMPLEMENTED:
    http.client for HTTPS communication
    Authentication of gateway in management system
    
"""

#Gateway Name
__name = "Pi_Gateway"
__gateway_port = 1883
# MQTT settings for MQTT communication that takes place locally on gateway
__gateway_broker = ""

# MQTT Settings for CloudMQTT broker working in cloud
__cloud_broker = "postman.cloudmqtt.com"
__cloud_port = 18467
__username = ***REMOVED***
__password = ***REMOVED***


# MongoDB Name
# db = MongoClient(***REMOVED***)
uri = "***REMOVED***"
db = MongoClient(uri)
database = db['gateway']
collection = database['DHT22']
mqtt_topics = __name + "/#" # all topics/devices under Pi_Gateway
mqtt_post_topics = __name + "/"
__Keep_Alive_Interval = 45
#_MQTT_Topic = "Pi_Gateway/DHT22/Humidity"
#_MQTT_Topic_Humidity = "Pi_Gateway/DHT22/Humidity"
#_MQTT_Topic_Temperature = "Pi_Gateway/DHT22/Temperature"

def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(__cloud_broker))
        client.subscribe(mqtt_topics)

def on_publish(client, userdata, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc != 0:
        pass

"""
    This method is responsible for adding sensor data to the gateway local storage which is implemented with 
    MongoDB
"""
def on_message(client, userdata, msg):
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

    collection.insert_one(post)


# connecting to MQTT Cloud broker and setting commands
__cloud_client = mqtt.Client(__name)
__cloud_client.on_connect = on_connect
__cloud_client.on_disconnect = on_disconnect
__cloud_client.on_publish = on_publish
__cloud_client.on_message = on_message
__cloud_client.connect(__cloud_broker, int(__cloud_port), int(__Keep_Alive_Interval))
__cloud_client.username_pw_set(__username, __password)  # must log in with username/pass for broker


# connecting to MQTT Cloud broker and setting commands
__client = mqtt.Client(__name)
__client.on_connect = on_connect
__client.on_disconnect = on_disconnect
__client.on_publish = on_publish
__client.on_message = on_message
__client.connect(__name, int(__gateway_port), int(__Keep_Alive_Interval))

__client.loop_forever()

__cloud_client.loop_forever()
# ====================================================
