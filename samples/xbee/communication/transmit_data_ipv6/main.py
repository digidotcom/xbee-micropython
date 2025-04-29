# Copyright (c) 2025, Digi International, Inc.
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

import socket
import time
import xbee


# TODO: replace with the IPv6 address of the other Wi-SUN module.
TARGET_IPV6_ADDR = "0000:0000:0000:0000:0000:0000:0000:0000"
PORT = 0x1234
MESSAGE = b"Hello, Wi-SUN module!"


print(" +--------------------------------------------+")
print(" | XBee MicroPython Transmit Data IPv6 Sample |")
print(" +--------------------------------------------+\n")

print("Waiting for the module to be connected to the network...")

ai = xbee.atcmd("AI")
while ai != 0:
    time.sleep(1)
    ai = xbee.atcmd("AI")

# Create the socket.
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

print("Sending data to %s >> %s" % (TARGET_IPV6_ADDR, str(MESSAGE, "utf8")))

try:
    # Send the message to the module.
    s.sendto(MESSAGE, (TARGET_IPV6_ADDR, PORT))
    print("Data sent successfully")
except Exception as e:
    print("Transmit failure: %s" % str(e))
finally:
    s.close()
