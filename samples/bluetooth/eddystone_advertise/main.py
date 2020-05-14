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
import os
import time
import xbee

from EddystoneBeacon import EddystoneTLMFrame, EddystoneUIDFrame, EddystoneURLFrame


def form_mac_address(addr: bytes) -> str:
    return ":".join('{:02x}'.format(b) for b in addr)

# Advertise a payload for a set amount of time sending an advertisement every interval.
# Returns the number of advertisements sent
def advertise_payload_for(payload, time_sec, interval_usec):
    # Start advertising the payload
    ble.gap_advertise(interval_usec, payload)
    time.sleep(time_sec)
    # stop advertising
    ble.gap_advertise(None)
    # Calculate the number of advertisements sent
    return time_sec * 1000000 // interval_usec

# Advertising constants
TIME_BETWEEN_BEACON_TYPES_SEC = 10
ADVERTISE_INTERVAL_USEC = 50000

# Turn on BLE
ble.active(True)
# Print out the BLE Mac
print("Started Bluetooth with address of: {}".format(form_mac_address(ble.config("mac"))))

# The Ranging Data is the Tx power in dBm emitted by the beacon at 0 meters.
calibrated_ranging_data = -10 # This will need to be configured to your beacons actual value.

# The Eddystone TLM frame keeps track of the beacon's time alive and advertisement count.
count = 0
start_time = time.ticks_ms()

# A URL to advertise
url = "http://www.digi.com/"

# This is a unique ID given to each beacon, for this example it will be random.
uid = os.urandom(16)

# The TLM frame advertises the beacon's battery voltage if available. It is set to 0 if unavailable.
battery_voltage = 0

while True:
    time_alive = time.ticks_diff(time.ticks_ms(), start_time) / 1000
    beacon_temperature = xbee.atcmd('TP')
    # convert unsigned 16-bit value to signed beacon_temperature
    if beacon_temperature > 0x7FFF:
        beacon_temperature = beacon_temperature - 0x10000
    # If the %V command is supported (XBee 3 LTE-M) the following line can be uncommented.
    # battery_voltage = xbee.atcmd('%V') / 1000

    frame = EddystoneTLMFrame(
        battery_voltage=battery_voltage, beacon_temperature=beacon_temperature,
        advertisement_count=count, time_sec=time_alive
    )
    print("Advertising TLM with timestamp: {}seconds\tbattery voltage: {}V\t" \
          "beacon temperature: {}*C\tadvertisement count: {}\n"
          .format(time_alive, battery_voltage, beacon_temperature, count))
    count += advertise_payload_for(frame.get_bytes(), TIME_BETWEEN_BEACON_TYPES_SEC, ADVERTISE_INTERVAL_USEC)

    frame = EddystoneUIDFrame(ranging_data=calibrated_ranging_data, uid=uid)
    print("Advertising UID with UID: {}\tranging data {}dBm\n"
          .format(binascii.hexlify(uid), calibrated_ranging_data))
    count += advertise_payload_for(frame.get_bytes(), TIME_BETWEEN_BEACON_TYPES_SEC, ADVERTISE_INTERVAL_USEC)

    frame = EddystoneURLFrame(ranging_data=calibrated_ranging_data, url=url)
    print("Advertising URL with URL: {}\tranging data: {}dBm\n"
          .format(url, calibrated_ranging_data))
    count += advertise_payload_for(frame.get_bytes(), TIME_BETWEEN_BEACON_TYPES_SEC, ADVERTISE_INTERVAL_USEC)
