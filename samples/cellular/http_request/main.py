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
import socket
import time


HOST = "http://www.micropython.org/ks/test.html"


print(" +--------------------------------------+")
print(" | XBee MicroPython HTTP Request Sample |")
print(" +--------------------------------------+\n")

cellular = network.Cellular()

print("Waiting for the module to be connected to the cellular network...")

# Before sending HTTP request, wait until the module is connected to the cellular network.
while not cellular.isconnected():
    time.sleep(1)

scheme, _, host, path = HOST.split("/", 3)

# Create the socket.
s = socket.socket()

try:
    # Connect to the host using the port 80 (HTTP).
    s.connect((host, 80))

    request = bytes("GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n" % (path, host), "utf8")
    print("Requesting /%s from host %s\n" % (path, host))

    # Send the HTTP request.
    s.send(request)

    while True:
        # Receive data from the socket.
        data = s.recv(500)
        print(str(data, "utf8"), end="")
finally:
    s.close()
