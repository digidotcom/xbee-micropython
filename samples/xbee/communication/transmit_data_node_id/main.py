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

import sys
import xbee


# TODO: replace with the node identifier of your target device.
TARGET_NODE_ID = "RECEIVER"
MESSAGE = "Hello XBee!"


def find_device(node_id):
    """
    Finds the XBee device with the given node identifier in the network and
    returns it.

    :param node_id: Node identifier of the XBee device to find.

    :return: The XBee device with the given node identifier or ``None`` if it
        could not be found.
    """
    for dev in xbee.discover():
        if dev['node_id'] == node_id:
            return dev
    return None


print(" +--------------------------------------------+")
print(" | XBee MicroPython Transmit Data (NI) Sample |")
print(" +--------------------------------------------+\n")

# Find the device with the configure node identifier.
device = find_device(TARGET_NODE_ID)
if not device:
    print("Could not find the device with node identifier '%s'" % TARGET_NODE_ID)
    sys.exit(-1)

addr16 = device['sender_nwk']
addr64 = device['sender_eui64']

print("Sending data to %s >> %s" % (TARGET_NODE_ID, MESSAGE))

try:
    # Some protocols do not have 16-bit address. In those cases, use the 64-bit one.
    xbee.transmit(addr16 if addr16 else addr64, MESSAGE)
    print("Data sent successfully")
except Exception as e:
    print("Transmit failure: %s" % str(e))
