import json
import sqlite3
from pymongo import MongoClient
import datetime
import paho.mqtt.client as mqtt

# SQLite DB Name
db = MongoClient(***REMOVED***)
database = db['gateway']
collection = database['DHT22']
MQTT_Topic = "gateway_identifier/DHT22/#"

# MQTT Settings
MQTT_Broker = "postman.cloudmqtt.com"
MQTT_Port = 18467
username = ***REMOVED***
password = ***REMOVED***

Keep_Alive_Interval = 45


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_Topic)


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


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
client.username_pw_set(username, password) # must log in with username/pass for broker
client.loop_forever()

"""
# Database Manager Class


class DatabaseManager():
    def __init__(self):
        self.connection = MongoClient(***REMOVED***)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def add_del_update_db_record(self, sql_query, args=()):
        self.cur.execute(sql_query, args)
        self.conn.commit()
        return

    def __del__(self):
        self.cur.close()
        self.conn.close()


# Functions to push Sensor Data into Database


# Function to save Temperature to DB Table
def dht22_temp_data_handler(json_data):
    # Parse Data
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = json_dict['Date']
    temperature = json_dict['Temperature']

    # Push into DB Table
    db_obj = DatabaseManager()
    db_obj.add_del_update_db_record(
        "insert into DHT22_Temperature_Data (SensorID, Date_n_Time, Temperature) values (?,?,?)",
        [sensor_id, data_and_time, temperature])
    del db_obj

    print("Inserted Temperature Data into Database.")
    print("")


# Function to save Humidity to DB Table
def dht22_humidity_data_handler(json_data):
    # Parse Data
    json_dict = json.loads(json_data)
    sensor_id = json_dict['Sensor_ID']
    data_and_time = json_dict['Date']
    humidity = json_dict['Humidity']

    # Push into DB Table
    db_obj = DatabaseManager()
    db_obj.add_del_update_db_record("insert into DHT22_Humidity_Data (SensorID, Date_n_Time, Humidity) values (?,?,?)",
                                    [sensor_id, data_and_time, humidity])
    del db_obj
    print("Inserted Humidity Data into Database.")
    print("")


# Master Function to Select DB Function based on MQTT Topic

def sensor_data_handler(topic, json_data):
    if topic == "Home/BedRoom/DHT22/Temperature":
        dht22_temp_data_handler(json_data)
    elif topic == "Home/BedRoom/DHT22/Humidity":
        dht22_humidity_data_handler(json_data)
"""
