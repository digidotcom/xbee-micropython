"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

Send this code to your XBee module using paste mode (CTRL-E), and then
run it by calling the test_sub() function:

test_sub('test.mosquitto.org', 'xbpy_reply')

Once running, you can publish messages from your PC.  First, make sure you
have the paho-mqtt client installed:
  pip install paho-mqtt

Then use the following commands to connect to a server and publish to a topic.

import paho.mqtt.client as mqtt
client.connect('test.mosquitto.org')
client.publish('xbpy_reply', 'testing').wait_for_publish()

You publish different values, and call `client.disconnect()` when done.
"""

import time
from umqtt.simple import MQTTClient

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print((topic, msg))

def test_sub(server="localhost", topic=b"foo_topic", blocking=True):
    c = MQTTClient("umqtt_client", server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(topic)
    while True:
        if blocking:
            # Blocking wait for message
            c.wait_msg()
        else:
            # Non-blocking wait for message
            c.check_msg()
            # Then need to sleep to avoid 100% CPU usage (in a real
            # app other useful actions would be performed instead)
            time.sleep(1)

    c.disconnect()
