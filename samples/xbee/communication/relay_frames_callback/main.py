# Copyright (c) 2020, Digi International, Inc.
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

def relay_frame_callback(relay_frame):
    sender = relay_frame["sender"]
    message = relay_frame["message"].decode("utf-8")

    # Send back a response.
    relay.send(sender, "New message from %s: %s" % (INTERFACES[sender],
                                                    message))

print(" +-----------------------------------------------+")
print(" | XBee MicroPython Relay Frames Callback Sample |")
print(" +-----------------------------------------------+\n")

# Register a callback to handle incoming relay frames.
relay.callback(relay_frame_callback)

while True:
    # The callback will fire even if the app is in another blocking call,
    # such as a long time.sleep call.
    time.sleep(120)