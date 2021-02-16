# Copyright (c) 2020, 2021 Digi International, Inc.
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

from hdc1080 import HDC1080
from machine import I2C
from binascii import hexlify
import sys
import time
import xbee

# Constants
SLEEP_TIME_MS = 8000  # 8 seconds.
AWAKE_TIME_MS = 2000  # 2 seconds.

MSG_ON = "ON"
MSG_OFF = "OFF"
MSG_SEPARATOR = "@@@"
MSG_AWAKE = "AWAKE"

PROTOCOL_ZB = "Zigbee"
PROTOCOL_DM = "DigiMesh"
PROTOCOL_802 = "802.15.4"

DEST_NODE_ID = "GATEWAY"


def get_destination(xb_prot):
    if xb_prot == PROTOCOL_ZB:
        return xbee.ADDR_COORDINATOR

    return find_gateway()


def get_protocol():
    version = xb.atcmd("VR")

    if version >= 0x3000:
        return PROTOCOL_DM

    if version >= 0x2000:
        return PROTOCOL_802

    return PROTOCOL_ZB


def find_gateway(retries=3):
    for i in range(1, retries + 1):
        print("Searching destination %s %d/%d" % (DEST_NODE_ID, i, retries))

        try:
            devices = xbee.discover()
        except OSError:
            devices = []

        for dev in devices:
            if dev.get('node_id', None) == DEST_NODE_ID:
                gateway = dev.get('sender_eui64', None)
                return gateway if gateway else dev.get('sender_nwk', None)
        time.sleep_ms(1500)

    return None


def transmit_data(dest, msg, retries=3):
    for i in range(1, retries + 1):
        try:
            xbee.transmit(dest, msg)
            break
        except OSError as e:
            print("Could not transmit data (%d/%d): %s" % (i, retries, str(e)))


def rx_callback(data):
    if not data or data['broadcast']:
        return

    if protocol == PROTOCOL_ZB and data['sender_nwk'] != 0:
        return

    if protocol == PROTOCOL_DM and data['sender_eui64'] != destination:
        return

    if protocol == PROTOCOL_802 and data['sender_eui64'] != destination:
        return

    try:
        payload = int(data.get('payload', bytearray()).decode())
    except ValueError:
        return

    if payload < 0:
        return

    # Update the sleep time.
    global sleep_time
    sleep_time = payload * 1000
    print("Temperature/humidity service stopped.\n" if not sleep_time
          else "Changed sleep time to %d s.\n" % payload)


print(" +------------------------------------+")
print(" | XBee MicroPython End to End Sample |")
print(" +------------------------------------+\n")

sleep_time = SLEEP_TIME_MS

# Instantiate the HDC1080 peripheral.
sensor = HDC1080(I2C(1))

# Instantiate the XBee device.
xb = xbee.XBee()

protocol = get_protocol()
print("Current protocol: %s\n" % protocol)

destination = get_destination(protocol)
if not destination:
    print("Unable to find destination node: %s" % DEST_NODE_ID)
    sys.exit(1)
print("Destination %s\n" % hexlify(bytearray(destination)).decode().upper())

# Register the reception data callback.
xbee.receive_callback(rx_callback)

# Configure sleep mode to be managed by MicroPython.
xb.atcmd("SM", 0x06)

# Start reading temperature and humidity measures.
while True:
    # Notify the gateway that the XBee is awake.
    transmit_data(destination, MSG_AWAKE)

    # Wait during the configured time for incoming messages.
    time.sleep(AWAKE_TIME_MS / 1000)

    # Check if temperature/humidity service is disabled.
    if not sleep_time:
        continue

    # Read the temperature and humidity.
    temp_celsius = sensor.read_temperature(True)
    humidity_hr = sensor.read_humidity()

    # Print values in the console.
    print("- Temperature: %sC" % round(temp_celsius, 1))
    print("- Humidity: %s%%\n" % round(humidity_hr, 1))

    # Create the message to send with the temperature and humidity.
    temp_hum_msg = "{0}{1}{2}".format(
        round(temp_celsius, 1),
        MSG_SEPARATOR,
        round(humidity_hr, 1)
    )

    # Send values to the gateway (coordinator).
    transmit_data(destination, temp_hum_msg)

    # Sleep for the configured timeout.
    xb.sleep_now(sleep_time)

