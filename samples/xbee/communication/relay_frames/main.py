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

import time
from xbee import relay

INTERFACES = {
    0x00: "Serial Port",
    0x01: "Bluetooth",
    0x02: "MicroPython"
}


print(" +--------------------------------------+")
print(" | XBee MicroPython Relay Frames Sample |")
print(" +--------------------------------------+\n")

while True:
    # Start reading relay frames.
    relay_frame = relay.receive()
    while relay_frame is None:
        relay_frame = relay.receive()
        time.sleep(0.25)

    # Get the relay frame parameters.
    sender = relay_frame["sender"]
    message = relay_frame["message"].decode("utf-8")

    # Send back the answer and start reading relay frames again.
    relay.send(sender, "New message from %s: %s" % (INTERFACES[sender],
                                                    message))
