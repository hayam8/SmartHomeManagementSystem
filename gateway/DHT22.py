import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime

deviceName = "DHT22"
humidity = "Humidity"
temperature = "Temperature"
toggle = 0

# MQTT settings for sensor to send data to gateway through MQTT
# Needs to be updated to send once device is authenticated and has gateway ID info
__broker = ""


"""
    This method generates random temperature and humidity data from a DHT22 sensor and returns them 
    to the gateway
"""
def fake_sensor_values():
    threading.Timer(3.0, fake_sensor_values).start() # loop to continuously send sensor data
    global toggle
    if toggle == 0:
        humidity_fake_value = float("{0:.2f}".format(random.uniform(50, 100)))

        humidity_data = {}
        humidity_data['Sensor_ID'] = "Dummy-1"
        humidity_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        humidity_data['Humidity'] = humidity_fake_value
        humidity_json_data = json.dumps(humidity_data)

        print("Publishing fake Humidity Value: " + str(humidity_fake_value) + "...")
        toggle = 1
        return humidity_json_data
    else:
        temperature_fake_value = float("{0:.2f}".format(random.uniform(1, 30)))

        temperature_data = {}
        temperature_data['Sensor_ID'] = "Dummy-2"
        temperature_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
        temperature_data['Temperature'] = temperature_fake_value
        temperature_json_data = json.dumps(temperature_data)

        print("Publishing fake Temperature Value: " + str(temperature_fake_value) + "...")
        toggle = 0
        return temperature_json_data


def get_device():
    return deviceName


def get_sensor_type():
    global toggle
    if toggle == 0:
        return humidity
    else:
        return temperature
