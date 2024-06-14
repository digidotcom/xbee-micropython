# Copyright (c) 2024,2025, Digi International, Inc.
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

import binascii
import struct
import sys
import time
import xbee
from digi import ble
from hdc1080 import HDC1080
from machine import I2C

# Constants
ADVERT_NAME = "XBIBC"

DIGI_MFG_ID = bytearray((0xDB, 0x02))  # Digi BLE Mfg ID in little endian
SENSOR_BEACON_ID = 0x00                # Digi XBIB-C sensor beacon ID

HDC1080_ADDR = 0x40

REG_TMP = 0x00
REG_HUM = 0x01

AT_CMD_SH = "SH"   # Serial Number High
AT_CMD_SL = "SL"   # Serial Number Low

SENSOR_REFRESH_RATE = 5000  # 5 seconds


def get_ble_mac():
    """
    Returns the Bluetooth MAC address of the device.

    Returns:
        The Bluetooth MAC address of the device in string format.
    """
    return ":".join('{:02x}'.format(b) for b in ble.config("mac"))


def get_xbee_mac():
    """
    Returns the XBee MAC address of the device.

    Returns:
        The XBee MAC address of the device in bytearray format.
    """
    # Read the serial number high and low from the XBee device.
    sh = xbee.atcmd(AT_CMD_SH)
    sl = xbee.atcmd(AT_CMD_SL)
    if sh is None or sl is None:
        return None

    # Transform the values to hexadecimal strings.
    sh_string = binascii.hexlify(sh).decode().upper()
    sl_string = binascii.hexlify(sl).decode().upper()

    # Add 0s at the beginning of each value if necessary.
    sh_string = (8 - len(sh_string)) * "0" + sh_string
    sl_string = (8 - len(sl_string)) * "0" + sl_string

    return bytearray.fromhex(sh_string + sl_string)


def generate_beacon(mac, temperature, humidity):
    """
    Generates a new XBIB-C sensor beacon frame containing the
    following information:
      - Advertise name
      - Company ID
      - Beacon type ID
      - XBee address
      - Temperature value
      - Humidity value

    Args:
        mac (bytearray): address of the XBee device.
        temperature (bytearray) : temperature value.
        humidity (bytearray) : humidity value.

    Returns:
        An XBIB-C sensor beacon frame in bytearray format.
    """
    frame = bytearray()
    frame.append(0x02)                  # Length of flags
    frame.append(0x01)                  # Tag for flags
    frame.append(0x06)                  # Flags data: General Discoverable, BrEdrNotSupported
    frame.append(len(ADVERT_NAME) + 1)  # Length of the advertisement data (tag + name)
    frame.append(0x08)                  # Tag for short advertisement name
    frame.extend(ADVERT_NAME.encode())  # Short advertisement name
    frame.append(0x14)                  # Length (bytes) of the manufacturer specific data: 20
    #                                       1 for manufacturer specific data tag
    #                                       2 for company ID
    #                                       1 for beacon type ID
    #                                       8 for MAC address
    #                                       4 for temperature value
    #                                       4 for humidity value
    frame.append(0xFF)                  # Tag for manufacturer specific data
    frame.extend(DIGI_MFG_ID)           # Digi's BLE Manufacturer ID
    frame.append(SENSOR_BEACON_ID)      # XBee Sensor beacon type ID
    frame.extend(mac)                   # XBee address
    frame.extend(temperature)           # Temperature value
    frame.extend(humidity)              # Humidity value
    return frame


def main():
    """
    Main execution of the application.
    """
    print(" +-----------------------------------------------+")
    print(" | XBee MicroPython XBee Beacon Advertise Sample |")
    print(" +-----------------------------------------------+\n")

    # Instantiate the HDC1080 peripheral.
    sensor = HDC1080(I2C(1))
    if sensor is None:
        print("Could not find the sensor!")
        sys.exit(1)

    # Turn on Bluetooth
    ble.active(True)
    print("- Started Bluetooth with address '{}'".format(get_ble_mac()))

    # Read the XBee MAC address of the device.
    xbee_mac = get_xbee_mac()

    # Main loop.
    while True:
        # Generate a new beacon frame to refresh temperature and humidity.
        temperature = sensor.read_temperature(True)
        humidity = sensor.read_humidity()
        frame = generate_beacon(
            xbee_mac,
            bytearray(struct.pack("f", temperature)),
            bytearray(struct.pack("f", humidity)))

        # Log info about the beacon being advertised.
        print("")
        print("- Advertising new XBIB-C beacon frame:")
        print("  {}".format(frame.hex()))
        print("  - Name: {}".format(ADVERT_NAME))
        print("  - Address: {}".format(xbee_mac.hex()))
        print("  - Temperature: {:.2f} C".format(temperature, 2))
        print("  - Humidity: {:.2f} % HR".format(humidity))

        # Advertise the beacon every 200ms
        interval_us = 200_000
        ble.gap_advertise(interval_us, frame)

        # Sleep
        time.sleep_ms(SENSOR_REFRESH_RATE)


if __name__ == '__main__':
    main()
