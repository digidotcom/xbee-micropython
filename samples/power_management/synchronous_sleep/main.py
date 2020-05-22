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
import xbee
from machine import I2C
from hdc1080 import HDC1080

MODEM_STATUS_NETWORK_WOKE = 0x0B

# Initialize the HDC1080 sensor.
sensor = HDC1080(I2C(1))


def handle_modem_status(status):
    if status == MODEM_STATUS_NETWORK_WOKE:
        temp_celsius = sensor.read_temperature(True)
        aggregator_addr = xbee.atcmd("DH") + xbee.atcmd("DL")
        xbee.transmit(aggregator_addr, "{}".format(temp_celsius))


# Register the above function as the modem status callback so that it
# will be called whenever a modem status is generated.
xbee.modem_status.callback(handle_modem_status)

# Enable sync sleep modem status messages
xbee.atcmd("SO", 4)

# Enable sync sleep
xbee.atcmd("SM", 8)

while True:
    # The callback will fire even if the app is in another blocking call,
    # such as a long time.sleep call.
    time.sleep(120)

# Note that even after this code completes the modem status callback
# will still be registered and will continue to execute until
# MicroPython is rebooted or xbee.modem_status.callback(None) is called.
