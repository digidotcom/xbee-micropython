"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Hardware required:
 - XBee module
 - Dev board with HDC1080 I2C Temp & Humidity Sensor
 - AWS account

Instructions:
 - Ensure that the umqtt/simple.py and hdc1080 modules are in
   the /flash/lib directory on the XBee Filesystem
 - The policy attached to the SSL certificates must allow for
   publishing, subscribing, connecting, and receiving
 - The host and region need to be filled in to create
   a valid AWS endpoint to connect to
 - "ssl_params" shows which ssl parameters are required, and gives
   examples for referencing the files
    - Be sure to replace the file paths to match the certificates you're using
 - Send this code to your XBee module using paste mode (CTRL-E)

Use:
 - To update the threshold temperature and timer configuration:
    - Use the AWS IoT built-in MQTT Client to send updates to
      the "tempsensor/update" topic
        - A "threshold_temp" parameter in the message JSON updates
          the threshold temperature
        - A "wait_timer" parameter in the message JSON updates the wait timer
 - When the system will send a temperature update is determined by
   the "wait_timer" variable
    - Temperature updates are sent every "wait_timer" seconds to
      the "tempsensor/temp" topic
 - If the temperature exceeds the "threshold_temp" value:
    - One message will be sent to the "tempsensor/alarm" topic
      regarding the status of the system
    - Message is only sent when the threshold is crossed (going above or below)

"""

from umqtt.simple import MQTTClient
from sensor.hdc1080 import HDC1080
from machine import I2C
import time, ujson

# AWS endpoint parameters
host = b'FILL_ME_IN'  # ex: b'a1p3gcs127hy79'
region = b'FILL_ME_IN'  # ex: b'us-east-2'

aws_endpoint = b'%s.iot.%s.amazonaws.com' % (host, region)
ssl_params = {'keyfile': "cert/aws.key",
              'certfile': "cert/aws.crt",
              'ca_certs': "cert/aws.ca"}  # ssl certs

threshold_temp = 80.0
wait_timer = 10
def cb_func(topic, msg):
    global threshold_temp
    global wait_timer
    d = ujson.loads(msg.decode("utf-8"))
    if "threshold_temp" in d.keys():
        try:
            threshold_temp = float(d['threshold_temp'])
            print("updated threshold to %s" % (threshold_temp))
        except ValueError:
            print("threshold_temp: Expected <class 'float'>, received %s" % type(d['threshold_temp']))
    if "wait_timer" in d.keys():
        try:
            wait_timer = int(d['wait_timer'])
            print("updated wait timer to %s" % (wait_timer))
        except ValueError:
            print("wait_timer: Expected <class 'int'>, received %s" % type(d['wait_timer']))

# "clientId" should be unique for each device connected
c = MQTTClient("clientId", aws_endpoint, ssl=True, ssl_params=ssl_params)
tempsensor = HDC1080(I2C(1))
c.set_callback(cb_func)
print("connecting...")
c.connect()
print("connected")
c.subscribe("tempsensor/update")
print("subscribed")

print("ready")
above = False
timer = 0
while 1:
    c.check_msg()
    cur_temp = tempsensor.read_temperature()
    if timer >= wait_timer:
        c.publish("tempsensor/temp", '{"temp": "%s"}' % (cur_temp))
        timer = 0
    if cur_temp >= threshold_temp:
        if not above:
            c.publish("tempsensor/alarm", '{"message": "Exceeded set threshold of %s"}' % (threshold_temp))
            above = True
    else:
        if above:
            c.publish("tempsensor/alarm", '{"message": "Below set threshold of %s"}' % (threshold_temp))
            above = False
    timer += 1
    time.sleep(1)

c.disconnect()
print("DONE")
