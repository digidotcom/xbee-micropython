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

from umqtt.simple import MQTTClient
import network
import time

# AWS endpoint parameters.
HOST = b'FILL_ME_IN'    # ex: b'abcdefg1234567'
REGION = b'FILL_ME_IN'  # ex: b'us-east-1'

CLIENT_ID = "clientID"  # Should be unique for each device connected.
AWS_ENDPOINT = b'%s.iot.%s.amazonaws.com' % (HOST, REGION)

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}

TOPIC = "sample/xbee"
MESSAGE = "AWS Sample Message"


def publish_test(client_id=CLIENT_ID, hostname=AWS_ENDPOINT, sslp=SSL_PARAMS):
    """
    Connects to AWS, publishes a message and disconnects.

    :param client_id: Unique identifier for the device connected.
    :param hostname: AWS hostname to connect to.
    :param sslp: SSL certificate parameters.
    """

    # Connect to AWS.
    client = MQTTClient(client_id, hostname, ssl=True, ssl_params=sslp)
    print("- Connecting to AWS... ", end="")
    client.connect()
    print("[OK]")
    # Publish message.
    print("- Publishing message... ", end="")
    client.publish(TOPIC, '{"message": "%s"}' % MESSAGE)
    print("[OK]")
    # Disconnect.
    client.disconnect()
    print("- Done")


print(" +-------------------------------------+")
print(" | XBee MicroPython AWS Publish Sample |")
print(" +-------------------------------------+\n")

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

publish_test()
