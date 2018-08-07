"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

 - Ensure that the umqtt/simple.py module is in the /flash/lib directory
   on the XBee Filesystem
 - Ensure that the SSL certificate files are in the /flash/cert directory
   on the XBee Filesystem
    - "ssl_params" shows which ssl parameters are required, and gives
     examples for referencing the files
    - If needed, replace the file paths to match the certificates you're using
 - The policy attached to the SSL certificates must allow for
   publishing, subscribing, connecting, and receiving
 - The host and region need to be filled in to create a valid
   AWS endpoint to connect to
 - The loop that checks for incoming traffic will end after it recieves
   "msg_limit" messages
 - Send this code to your XBee module using paste mode (CTRL-E)

 - If you want to change any of the params in the method, call the method again
   and pass in the params you want

"""

from umqtt.simple import MQTTClient
import time, network

# AWS endpoint parameters
host = b'FILL_ME_IN'  # ex: b'abcdefg1234567'
region = b'FILL_ME_IN'  # ex: b'us-east-1'

aws_endpoint = b'%s.iot.%s.amazonaws.com' % (host, region)
ssl_params = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}  # ssl certs

msgs_received = 0
conn = network.Cellular()
while not conn.isconnected():
    print("waiting for network connection...")
    time.sleep(4)
print("network connected")

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    global msgs_received
    msgs_received += 1
    print(topic, msg)

def subscribe_test(clientId="clientId", hostname=aws_endpoint, sslp=ssl_params, msg_limit=2):
    # "clientId" should be unique for each device connected
    c = MQTTClient(clientId, hostname, ssl=True, ssl_params=sslp)
    c.set_callback(sub_cb)
    print("connecting...")
    c.connect()
    print("connected")
    c.subscribe("sample/xbee")
    print("subscribed")
    print('waiting...')
    global msgs_received
    msgs_received = 0
    while msgs_received < msg_limit:
        c.check_msg()
        time.sleep(1)
    c.disconnect()
    print("DONE")

subscribe_test()
