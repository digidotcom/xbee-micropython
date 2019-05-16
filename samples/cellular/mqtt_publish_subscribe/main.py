# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from machine import Pin
from umqtt.simple import MQTTClient
import network
import time

# AWS endpoint parameters.
SERVER = "test.mosquitto.org"
TOPIC = "xbee_topic"
MESSAGE = "Test from XBee!"

# Pin D0 (AD0/DIO0)
INPUT_PIN_ID = "D0"

CLIENT_ID = "clientID"  # Should be unique for each device connected.


def sub_cb(topic, msg):
    """
    Callback executed when messages from subscriptions are received. Prints
    the topic and the message.

    :param topic: Topic of the message.
    :param msg: Received message.
    """

    print("- Message received!")
    print("   * %s: %s" % (topic.decode("utf-8"), msg.decode("utf-8")))


def subscribe_test(client_id=CLIENT_ID, hostname=SERVER, topic=TOPIC,
                   blocking=True):
    """
    Connects to the MQTT server subscribes to a topic and waits for messages
    coming from that topic.

    :param client_id: Unique identifier for the device connected.
    :param hostname: Host name to connect to.
    :param topic: Name of the topic to subscribe.
    :param blocking: `True` to block the client waiting for messages, `False`
        to poll for messages.
    """

    # Connect to the MQTT server.
    client = MQTTClient(client_id, hostname)
    client.set_callback(sub_cb)
    print("- Connecting to '%s'... " % hostname, end="")
    client.connect()
    print("[OK]")
    # Subscribe to topic.
    print("- Subscribing to topic '%s'... " % topic, end="")
    client.subscribe(topic)
    print("[OK]")
    # Wait for messages.
    print("- Press D0 to publish a message.")
    while True:
        if blocking:
            # Blocking wait for message.
            client.wait_msg()
        else:
            # Non-blocking wait for message.
            client.check_msg()
            # Check if the button is pressed to publish a message.
            if input_pin.value() == 0:
                publish_message(client, topic, MESSAGE)
                # Wait some time to avoid button bounces.
                time.sleep(1)
            # Need to sleep to avoid 100% CPU usage.
            time.sleep(0.2)


def publish_message(client, topic, message):
    """
    Publishes the given message to the specified topic.

    :param client: MQTT client that publishes the message.
    :param topic: Name of the topic to publish to.
    :param message: Message to publish.
    """

    # Publish message.
    print("- Publishing message... ", end="")
    client.publish(topic, message)
    print("[OK]")


print(" +------------------------------------------------+")
print(" | XBee MicroPython MQTT Publish Subscribe Sample |")
print(" +------------------------------------------------+\n")

# Set up the button pin object to check the input value. Configure the pin
# as input and enable the internal pull-up.
input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

subscribe_test(blocking=False)
