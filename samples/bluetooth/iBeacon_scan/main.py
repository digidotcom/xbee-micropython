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
import binascii
from digi import ble


def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)


def scan_for_iBeacon_frames(duration_ms: int):
    """
    Scan for iBeacon frames
    :param duration_ms: Time in milliseconds to scan for.
    """

    # Configure scan for the entire window
    with ble.gap_scan(duration_ms=duration_ms, interval_us=2500, window_us=2500) as scan:

        iBeacon_count = 0
        beacon_count = 0

        while not scan.stopped():

            for frame in scan.get():

                beacon_count += 1
                payload = frame['payload']

                if iBeacon.is_proximity_beacon(payload):
                    (uuid, power, major, minor) = iBeacon.parse_proximity_beacon(payload)

                    # Calculate approximate distance
                    calib_rssi = power - 256
                    rssi = frame['rssi']
                    db_ratio = float(calib_rssi - rssi)
                    linear_ratio = 10.0 ** (db_ratio / 10.0)
                    distance = linear_ratio ** 0.5

                    addr = binascii.hexlify(frame['address']).decode()
                    uuid = binascii.hexlify(uuid).decode()
                    print("")
                    print("Got iBeacon from {}".format(addr))
                    print("distance={:0.2f} meters (approximate)".format(distance))
                    print("UUID={} major={} minor={}".format(uuid, major, minor))
                    print("RSSI={} calibrated_RSSI={} calibrated_power={}".format(rssi, calib_rssi, power))
                    iBeacon_count += 1

    print("Found {} iBeacon frames out of a total {} beacon frames".format(iBeacon_count, beacon_count))


# Make sure BLE radio is on
active = ble.active(True)

# Print out the BLE Mac
print("Started Bluetooth with address of: {}".format(form_mac_address(ble.config("mac"))))

# Scan 30 seconds for iBeacon frames
scan_for_iBeacon_frames(30_000)
