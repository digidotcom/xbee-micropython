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


PORT = 0x1234


print(" +-------------------------------------------+")
print(" | XBee MicroPython Receive Data IPv6 Sample |")
print(" +-------------------------------------------+\n")

print("Waiting for the module to be connected to the network...")

ai = xbee.atcmd("AI")
while ai != 0:
    time.sleep(1)
    ai = xbee.atcmd("AI")

local_addr = xbee.atcmd("MY")
print("Receiver IPv6 address: %s" % local_addr)

# Create the socket.
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.bind((local_addr, PORT))

print("Waiting for data...\n")

try:
    while True:
        # Receive messages.
        data, address = s.recvfrom(1024)
        print("Data received from %s >> %s" % (address, data.decode()))
finally:
    s.close()
