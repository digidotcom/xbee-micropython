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

import xbee


print(" +-------------------------------------------+")
print(" | XBee MicroPython Network Discovery Sample |")
print(" +-------------------------------------------+\n")

print("Discovering network devices...\n")

# Discover the network devices and print their basic information.
for device in xbee.discover():
    addr64 = device['sender_eui64']
    node_id = device['node_id']
    rssi = device['rssi']

    print("New discovered device:\n"
          "  - 64-bit address: %s\n"
          "  - Node identifier: %s\n"
          "  - RSSI: %d\n"
          % (''.join('{:02x}'.format(x).upper() for x in addr64), node_id, rssi))

print("Network discovery finished")
