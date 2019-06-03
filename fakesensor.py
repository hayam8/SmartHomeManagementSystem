import paho.mqtt.client as mqtt
import random
import threading
import json
from datetime import datetime

__deviceName = "DHT22"
__humidity = "Humidity"
__temperature = "Temperature"
toggle = 0

# MQTT settings for sensor to send data to gateway through MQTT
# Needs to be updated to send once device is authenticated and has gateway ID info
__broker = ""
__port = 1871


class DHT22:

    """
        Values passed in when creating a sensor object is the host name of the gateway used for sending
        MQTT data and port it will be sent on.
        When device is created it is authenticated with the gateway and will connect to it using MQTT
        It will then automatically begin publishing sensor data to gateway in encrypted format
    """
    def __init__(self, gateway_name, port):
        self.__broker = gateway_name
        self.__port = port
        self.__keep_alive_interval = 45
        # MQTT broker connection
        self.__client = mqtt.Client(self.__deviceName)
        self.__client.on_connect = self.on_connect
        self.__client.on_disconnect = self.on_disconnect
        self.__client.on_publish = self.on_publish
        self.__client.on_message = self.on_message
        self.__client.connect(self.__broker, int(self.__port), int(self.__keep_alive_interval))
        self.publish_fake_sensor_values_to_mqtt()
        self.__client.loop_forever()

    def on_connect(self, client, userdata, rc):
        if rc != 0:
            pass
            print("Unable to connect to MQTT Broker...")
        else:
            print("Connected with MQTT Broker: " + self.__broker)

    def on_publish(self, client, userdata, mid):
        pass

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            pass

    """
        This method generates random temperature and humidity data from a DHT22 sensor and returns them
        to the gateway
    """
    def publish_fake_sensor_values_to_mqtt(self):
        threading.Timer(3.0, self.publish_fake_sensor_values_to_mqtt).start()  # loop to continuously send sensor data
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
            topic = self.__broker + "/" + self.__deviceName + "/" + self.__humidity
            self.publish_to_topic(topic, humidity_data)
        else:
            temperature_fake_value = float("{0:.2f}".format(random.uniform(1, 30)))

            temperature_data = {}
            temperature_data['Sensor_ID'] = self.__deviceName
            temperature_data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
            temperature_data['Temperature'] = temperature_fake_value
            temperature_json_data = json.dumps(temperature_data)

            print("Publishing fake Temperature Value: " + str(temperature_fake_value) + "...")
            toggle = 0
            topic = self.__broker + "/" + self.__deviceName + "/" + self.__temperature
            self.publish_to_topic(topic, temperature_data)

    def publish_to_topic(self, topic, message):
        self.client.publish(topic, message)
        print("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
        print("\n")

    def get_device(self):
        return self.__deviceName

    def get_sensor_type(self):
        global toggle
        if toggle == 0:
            return self.__humidity
        else:
            return self.__temperature
