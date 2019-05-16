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

from machine import I2C
from hdc1080 import HDC1080
from umqtt.simple import MQTTClient
import network
import time
import ujson

# AWS endpoint parameters.
HOST = b'FILL_ME_IN'    # ex: b'abcdefg1234567'
REGION = b'FILL_ME_IN'  # ex: b'us-east-1'

CLIENT_ID = "clientID"  # Should be unique for each device connected.
AWS_ENDPOINT = b'%s.iot.%s.amazonaws.com' % (HOST, REGION)

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC_UPDATE = "sample/update"
TOPIC_TEMP = "sample/temp"
TOPIC_ALARM = "sample/alarm"

VAR_THRESHOLD_TEMP = "threshold_temp"
VAR_WAIT_TIMER = "wait_timer"


def cb_func(topic, msg):
    """
     Callback executed when messages from subscriptions are received. Updates
     the temperature threshold or wait timer accordingly.

    :param topic: Topic of the message.
    :param msg: Received message.
    """

    global threshold_temp
    global wait_timer

    print("- Message received!")
    d = ujson.loads(msg.decode("utf-8"))
    if VAR_THRESHOLD_TEMP in d.keys():
        try:
            threshold_temp = float(d[VAR_THRESHOLD_TEMP])
            print("   * Updated threshold to '%s'" % threshold_temp)
        except ValueError:
            print("   * [%s] Expected <class 'float'>, received %s"
                  % (VAR_THRESHOLD_TEMP, type(d[VAR_THRESHOLD_TEMP])))
    if VAR_WAIT_TIMER in d.keys():
        try:
            wait_timer = int(d[VAR_WAIT_TIMER])
            print("   * Updated wait timer to '%s'" % wait_timer)
        except ValueError:
            print("   * [%s] Expected <class 'int'>, received %s"
                  % (VAR_WAIT_TIMER, type(d[VAR_WAIT_TIMER])))


print(" +------------------------------------------------+")
print(" | XBee MicroPython AWS Temperature Sensor Sample |")
print(" +------------------------------------------------+\n")

threshold_temp = 80.0
wait_timer = 10
conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

# Connect to AWS.
client = MQTTClient("clientId", AWS_ENDPOINT, ssl=True, ssl_params=SSL_PARAMS)
temp_sensor = HDC1080(I2C(1))
client.set_callback(cb_func)
print("- Connecting to AWS... ", end="")
client.connect()
print("[OK]")
# Subscribe to topic.
print("- Subscribing to topic '%s'... " % TOPIC_UPDATE, end="")
client.subscribe(TOPIC_UPDATE)
print("[OK]")

# Start taking temperature samples.
above = False
timer = 0
while True:
    client.check_msg()
    cur_temp = temp_sensor.read_temperature()
    if timer >= wait_timer:
        # If the wait timer expires, update the value of the temperature.
        print("- Publishing temperature... ", end="")
        client.publish(TOPIC_TEMP, '{"temp": "%s"}' % cur_temp)
        print("[OK]")
        timer = 0
    if cur_temp >= threshold_temp:
        # If the temperature exceeds the threshold and an alarm was not set,
        # send an alarm.
        if not above:
            print("- Publishing alarm (high temperature)... ", end="")
            client.publish(TOPIC_ALARM,
                           '{"message": "Exceeded set threshold of %s"}'
                           % threshold_temp)
            print("[OK]")
            above = True
    else:
        # If the temperature is below the threshold and an alarm was not set,
        # send an alarm.
        if above:
            print("- Publishing alarm (low temperature)... ", end="")
            client.publish(TOPIC_ALARM,
                           '{"message": "Below set threshold of %s"}'
                           % threshold_temp)
            print("[OK]")
            above = False
    timer += 1
    time.sleep(1)
