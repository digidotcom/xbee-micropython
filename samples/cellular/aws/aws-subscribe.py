"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

 - Ensure that the umqtt/simple.py module is in the /flash/lib directory
   on the XBee Filesystem
 - The policy attached to the SSL certificates must allow for
   publishing, subscribing, connecting, and receiving
 - The host and region need to be filled in to create a valid
   AWS endpoint to connect to
 - "ssl_params" shows which ssl parameters are required, and gives
   examples for referencing the files
    - Be sure to replace the file paths to match the certificates you're using
 - Send this code to your XBee module using paste mode (CTRL-E)
 - If you want to change any of the params in the method, call the method again
   and pass in the params you want

"""

from umqtt.simple import MQTTClient
from time import sleep

# AWS endpoint parameters
# AWS endpoint parameters
host = b'FILL_ME_IN'  # ex: b'a1p3gcs127hy79'
region = b'FILL_ME_IN'  # ex: b'us-east-2'

aws_endpoint = b'%s.iot.%s.amazonaws.com' % (host, region)
ssl_params = {'keyfile': "cert/aws.key",
              'certfile': "cert/aws.crt",
              'ca_certs': "cert/aws.ca"}  # ssl certs

# Received messages from subscriptions will be delivered to this callback
def sub_cb(topic, msg):
    print(topic, msg)

def subscribe_test(clientId="clientId", hostname=aws_endpoint, sslp=ssl_params):
    # "clientId" should be unique for each device connected
    c = MQTTClient(clientId, hostname, ssl=True, ssl_params=sslp)
    c.set_callback(sub_cb)
    print("connecting...")
    c.connect()
    print("connected")
    c.subscribe("sample/xbee")
    print("subscribed")
    print('waiting...')
    for i in range(20):
        c.check_msg()
        sleep(1)
    c.disconnect()
    print("DONE")

subscribe_test()
