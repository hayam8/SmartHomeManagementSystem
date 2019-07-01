import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime
from pymongo import MongoClient
from http.client import HTTPSConnection

"""

Author: Haya Majeed
"""


class Gateway:

    # Gateway Name
    __name = "Pi_Gateway"
    __gateway_port = 1883
    # MQTT settings for MQTT communication that takes place locally on gateway
    # Enter Name for local gateway
    __gateway_broker = ""

    # MQTT Settings for CloudMQTT broker working in cloud
    __cloud_broker = "postman.cloudmqtt.com"
    __cloud_port = 18467
    __username = ""
    __password = ""

    # MongoDB Name
    # Must enter unique credentials for MongoDB host
    db = MongoClient()
    database = db['gateway']
    collection = database['DHT22']
    mqtt_topics = __name + "/#" # all topics/devices under Pi_Gateway
    mqtt_post_topics = __name + "/"
    __Keep_Alive_Interval = 45

    def __init__(self, token, api_link):
        # connecting to MQTT Cloud broker and setting commands
        __cloud_client = mqtt.Client(self.__name)
        __cloud_client.on_connect = self.on_connect
        __cloud_client.on_disconnect = self.on_disconnect
        __cloud_client.on_publish = self.on_publish
        __cloud_client.on_message = self.on_message
        __cloud_client.connect(self.__cloud_broker, int(self.__cloud_port), int(self.__Keep_Alive_Interval))
        __cloud_client.username_pw_set(self.__username, self.__password)  # must log in with username/pass for broker
        __cloud_client.loop_forever()

    """
        This function is used as a callback to paho-mqtt on_connect function. It verifies if a connection is made 
        successfully or not and then subscribes to appropriate topics.
    """
    def on_connect(self, client, userdata, rc):
        if rc != 0:
            pass
            print("Unable to connect to MQTT Broker...")
        else:
            print("Connected with MQTT Broker: " + str(self.__cloud_broker))
            client.subscribe(self.mqtt_topics)

    """
        Callback function to paho-mqtt on_publish function
    """
    def on_publish(self, client, userdata, mid):
        pass

    """
        Callback function to paho-mqtt on_disconnect function
    """
    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            pass

    """
        This method is responsible for adding sensor data to the gateway local storage which is implemented with 
        MongoDB
    """
    def on_message(self, client, userdata, msg):
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
        self.collection.insert_one(post) # inserting data to database

