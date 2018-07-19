"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

Run this program on your computer to subscribe to a topic that you
will publish to from the XBee Cellular.

Make sure you have the paho-mqtt client installed:
  pip install paho-mqtt

...and then run this sample:
  python pc_client.py

Next, run this code on your XBee:

from umqtt.simple import MQTTClient
c = MQTTClient('umqtt_client', 'test.mosquitto.org')
c.connect()
c.publish(b'xbpy_test', b'test from xbee')

Repeat the last line to publish different information, and it should appear
on the PC running pc_client.py.

When done on the XBee, call `c.disconnect()`.
"""

import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("xbpy_test")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
