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

from digi import ble
import binascii

from EddystoneBeacon import TYPE_URL, TYPE_UID, TYPE_TLM, parse


def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)

def handle_eddystone(adv: dict):
    try:
        eddystone_type, frame = parse(adv["payload"])
    except TypeError:
        # The payload did not have an eddystone payload
        return

    print("Received a beacon of length {} from address {} and RSSI {}"
          .format(len(adv["payload"]), form_mac_address(adv["address"]), adv["rssi"]))

    if eddystone_type == TYPE_URL:
        print("Received URL with URL: {}\tranging data: {}dBm\n".format(frame.url, frame.ranging_data))
    elif eddystone_type == TYPE_UID:
        print("Received UID: {}\tranging data {}dBm\n".format(binascii.hexlify(frame.uid), frame.ranging_data))
    elif eddystone_type == TYPE_TLM:
        print("Received TLM with timestamp: {}seconds\tbattery voltage: {}V\t" \
              "beacon temperature: {}*C\tadvertisement count: {}\n"
              .format(frame.time_sec, frame.battery_voltage, frame.beacon_temperature, frame.advertisement_count))
    else:
        raise TypeError("Bad Eddystone advertisement")


# Turn on Bluetooth
ble.active(True)
print("Started Bluetooth with address of: {}".format(form_mac_address(ble.config("mac"))))

scanner = None
try:
    # Start a scan to run for 30 seconds
    scanner = ble.gap_scan(30000, interval_us=50000, window_us=50000)
    # Loop through all advertisements until the scan has stopped.
    for adv in scanner:
        handle_eddystone(adv)
finally:
    if scanner is not None:
        scanner.stop()

# Scan with a context manager this time.
with ble.gap_scan(30000, interval_us=50000, window_us=50000) as scanner:
    # Loop through the available advertisements, blocking if there are none. Exits when the scan stops.
    for adv in scanner:
        handle_eddystone(adv)

    # Leaving the context would automatically end the scan by an implicit scanner.stop()
