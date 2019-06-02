import paho.mqtt.client as mqtt
import random
import threading
import json
import DHT22
from datetime import datetime
from pymongo import MongoClient

"""
NEEDS TO BE IMPLEMENTED:
    http.client for HTTPS communication
    Authentication of gateway in management system
    
"""
#Gateway Name
name = "Pi_Gateway"

# MQTT settings for MQTT communication that takes place locally on gateway
__broker = ""

# MQTT Settings for CloudMQTT broker working in cloud
__MQTT_Broker = "postman.cloudmqtt.com"
__MQTT_Port = 18467
__username = ***REMOVED***
__password = ***REMOVED***


# MongoDB Name
db = MongoClient(***REMOVED***)
database = db['gateway']
collection = database['DHT22']
mqtt_topics = name + "/#" # all topics/devices under Pi_Gateway
mqtt_post_topics = name + "/"
__Keep_Alive_Interval = 45
#_MQTT_Topic = "Pi_Gateway/DHT22/Humidity"
#_MQTT_Topic_Humidity = "Pi_Gateway/DHT22/Humidity"
#_MQTT_Topic_Temperature = "Pi_Gateway/DHT22/Temperature"


def on_connect(client, userdata, rc):
    if rc != 0:
        pass
        print("Unable to connect to MQTT Broker...")
    else:
        print("Connected with MQTT Broker: " + str(__MQTT_Broker))
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
        post = {"time": receive_time, "topic": msg.topic, "value" : message}

    collection.insert_one(post)


# connecting to mqtt broker and setting commands
client = mqtt.Client(name)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.on_message = on_message
client.connect(__MQTT_Broker, int(__MQTT_Port), int(__Keep_Alive_Interval))
client.username_pw_set(__username, __password) # must log in with username/pass for broker


def publish_to_topic(topic, message):
    client.publish(topic, message)
    print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
    print("\n")


# FAKE SENSOR
# Dummy code used as Fake Sensor to publish some random values to MQTT Broker


def publish_fake_sensor_values_to_mqtt():
    # threading.Timer(3.0, publish_fake_sensor_values_to_mqtt).start()
    # these values are specific to the fake sensor data being collected
    device = DHT22.get_device()
    # checks if device name is in local data storage, doesn't collect information otherwise
    if device in database.list_collection_names():
        sensor_type = DHT22.get_sensor_type()
        sensor_data = DHT22.fake_sensor_values()
        topic = name + "/" + device + "/" + sensor_type
        publish_to_topic(topic, sensor_data)


publish_fake_sensor_values_to_mqtt()

client.loop_forever()
# ====================================================
