#
# DEVELOPER IS RESPONSIBLE FOR OBTAINING THE NECESSARY LICENSES FROM APPLE.
#
# iBeacon(TM) is a trademark of Apple Inc. and use of this code must comply with
# their licence.
#

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

import iBeacon
import time
import binascii
from digi import ble


def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)


# Make sure the BLE radio is on
active = ble.active(True)
# Print out the BLE Mac
print("Started Bluetooth with address of: {}".format(form_mac_address(ble.config("mac"))))

# iBeacon frame parameters
uuid = binascii.unhexlify('b7a8bf1d-f5bd-4b57-9b35-12c7be74eb7a'.replace('-', ''))  # Randomly generated UUID
major = 44
minor = 47
calib_power = 189  # Calibrated power 1 meter away (-67 dBm)

# Create the iBeacon frame
frame = iBeacon.make_proximity_beacon(uuid, calib_power, major, minor)

# Advertise the iBeacon frame every 200ms
interval_us = 200_000
ble.gap_advertise(interval_us, frame)

time.sleep(60)

# Stop advertising
ble.gap_advertise(None)
