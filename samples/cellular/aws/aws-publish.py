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

# AWS endpoint parameters
host = b'FILL_ME_IN'  # ex: b'a1p3gcs127hy79'
region = b'FILL_ME_IN'  # ex: b'us-east-2'

aws_endpoint = b'%s.iot.%s.amazonaws.com' % (host, region)
ssl_params = {'keyfile': "cert/aws.key",
              'certfile': "cert/aws.crt",
              'ca_certs': "cert/aws.ca"}  # ssl certs

def publish_test(clientId="clientId", hostname=aws_endpoint, sslp=ssl_params):
    # "clientId" should be unique for each device connected
    c = MQTTClient(clientId, aws_endpoint, ssl=True, ssl_params=sslp)
    print("connecting...")
    c.connect()
    print("connected")

    # topic: "sample/xbee"
    # message: {message: AWS Samples are cool!}
    print("publishing message...")
    c.publish("sample/xbee", '{"message": "AWS Sample Message"}')
    print("published")
    c.disconnect()
    print("DONE")

publish_test()
