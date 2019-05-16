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

import network
import time
import usocket
import ussl

# AWS endpoint parameters.
# TODO: replace with your account values.
HOST = b'FILL_ME_IN'        # ex: b'abcdefg1234567'
REGION = b'FILL_ME_IN'      # ex: b'us-east-1'
THING_NAME = b'FILL_ME_IN'  # ex: b'IMEI_12345'

AWS_ENDPOINT = b'%s.iot.%s.amazonaws.com' % (HOST, REGION)

# SSL certificates.
SSL_PARAMS = {'keyfile': "/flash/cert/aws.key",
              'certfile': "/flash/cert/aws.crt",
              'ca_certs': "/flash/cert/aws.ca"}


def https_test(hostname=AWS_ENDPOINT, sslp=SSL_PARAMS):
    """
    Tests the HTTPS connectivity with AWS. Sends an HTTP request to obtain the
    shadow of a thing and prints it.

    :param hostname: AWS hostname to connect to.
    :param sslp: SSL certificate parameters.
    """

    # Connect to AWS.
    s = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM,
                       usocket.IPPROTO_SEC)
    s.setblocking(False)
    w = ussl.wrap_socket(s, **sslp)
    print("- Connecting to AWS... ", end="")
    w.connect((hostname, 8443))
    print("[OK]")
    # Send HTTP request.
    print("- Sending shadow request for thing '%s'... " % THING_NAME, end="")
    w.write(b'GET /things/%s/shadow HTTP/1.0\r\n'
            b'Host: %s\r\n'
            b'\r\n' % (THING_NAME, hostname))
    print("[OK]")
    # Read answer.
    print("- Waiting for data... ", end="")
    while True:
        data = w.read(1024)
        if data:
            print("[OK]")
            print("- Received shadow for thing '%s':" % THING_NAME)
            print(64 * "-")
            print(str(data, 'utf-8'))
            print(64 * "-")
            break
    # Disconnect.
    w.close()
    print("- Done")


print(" +-----------------------------------+")
print(" | XBee MicroPython AWS HTTPS Sample |")
print(" +-----------------------------------+\n")

conn = network.Cellular()

print("- Waiting for the module to be connected to the cellular network... ",
      end="")
while not conn.isconnected():
    time.sleep(5)
print("[OK]")

https_test()
