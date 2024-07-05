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

import iBeacon
import time
from digi import ble


# Constants
COMPANY_ID_DIGI = bytearray((0xDB, 0x02))
COMPANY_ID_APPLE = bytearray((0x4C, 0x00))

BEACON_ID_IBEACON = bytearray((0x02, 0x15))

DIGI_BEACON_MIN_LENGTH = 7       # 3 for 'Flags' AD
#                                  2 for 'Mfg Data' AD
#                                  2 for Company ID
DIGI_BEACON_MIN_LENGTH_EXT = 19  # 3 for 'Flags' AD
#                                  2 for 'Name' AD length and tag
#                                 10 for 'XBeeMobile' name
#                                  2 for 'Mfg Data' AD
#                                  2 for Company ID
DIGI_COMPANY_INDEX = 5
DIGI_COMPANY_INDEX_EXT = 17

SCAN_MESSAGE_INTERVAL = 5000  # 5 seconds


def is_digi_beacon(payload):
    """
    Checks if the payload corresponds to a custom Digi beacon packet.

    Args:
        payload: The payload to check.

    Returns:
        True if the payload is a Digi beacon packet, False otherwise.
    """
    return get_digi_company_id_index(payload) != -1


def get_digi_company_id_index(payload):
    """
    Returns the index of the Digi company ID in the provided beacon payload
    or -1 if the Digi company ID was not found. As the beacon payload can
    include the advertisement name, the method must account for both cases
    where the advertisement name is present or absent.

    Args:
        payload: The beacon  payload to check.

    Returns:
        The index of the Digi company ID, -1 if it was not found.
    """
    # Check if the payload includes the advertisement name.
    if (len(payload) > DIGI_BEACON_MIN_LENGTH_EXT
            and payload[DIGI_COMPANY_INDEX_EXT:DIGI_COMPANY_INDEX_EXT + 2] == COMPANY_ID_DIGI):
        return DIGI_COMPANY_INDEX_EXT

    # Check now if the payload does not include the advertisement name.
    if (len(payload) > DIGI_BEACON_MIN_LENGTH
            and payload[DIGI_COMPANY_INDEX:DIGI_COMPANY_INDEX + 2] == COMPANY_ID_DIGI):
        return DIGI_COMPANY_INDEX

    return -1


def parse_ibeacon(payload):
    """
    Parses the iBeacon payload to extract relevant information.

    Args:
        payload: The payload to parse.

    Returns:
        A tuple containing the UUID, major, minor and power values.
    """
    uuid = payload[9:25]
    major = (payload[25] << 8) + payload[26]
    minor = (payload[27] << 8) + payload[28]
    power = payload[29]
    return uuid, major, minor, power


def parse_digi_beacon(payload):
    """
    Parses the custom Digi beacon payload to extract the text message.

    Args:
        payload: The payload to parse.

    Returns:
        The text message contained in the payload.
    """
    company_id_index = get_digi_company_id_index(payload)
    if company_id_index != -1:
        return payload[company_id_index + 2:].decode()
    return None


def format_address(address):
    """
    Returns the provided bytearray address in string format.

    Returns:
        The address in string format.
    """
    return ":".join('{:02x}'.format(b) for b in address)


def scan_for_beacons():
    """
    Scan for iBeacons and custom Digi beacons and prints their information.
    """
    deadline = time.ticks_ms()

    # Scan during 150ms every 2 seconds forever.
    with ble.gap_scan(duration_ms=0, interval_us=2000000, window_us=150000) as scan:
        while True:
            for frame in scan.get():
                address = frame['address']
                payload = frame['payload']
                rssi = frame['rssi']
                # Check if the frame is a Digi beacon or iBeacon to print the corresponding info.
                if iBeacon.is_proximity_beacon(payload):
                    (uuid, power, major, minor) = iBeacon.parse_proximity_beacon(payload)
                    print("")
                    print("- iBeacon found: {}".format(payload.hex()))
                    print("  - Source address: {}".format(format_address(address)))
                    print("  - UUID: {}".format(uuid.hex()))
                    print("  - Major: {}".format(major))
                    print("  - Minor: {}".format(minor))
                    print("  - Tx power: {}".format(power))
                    print("  - RSSI: {}".format(rssi))
                    # Reset the deadline value.
                    deadline = time.ticks_ms() + SCAN_MESSAGE_INTERVAL
                elif is_digi_beacon(payload):
                    text = parse_digi_beacon(payload)
                    print("")
                    print("- Custom Digi beacon found: {}".format(payload.hex()))
                    print("  - Source address: {}".format(format_address(address)))
                    print("  - Text: {}".format(text))
                    print("  - RSSI: {}".format(rssi))
                    # Reset the deadline value.
                    deadline = time.ticks_ms() + SCAN_MESSAGE_INTERVAL
            # Show the scanning message.
            if time.ticks_ms() > deadline:
                deadline = time.ticks_ms() + SCAN_MESSAGE_INTERVAL
                print("")
                print("- Scanning for beacons...")


def main():
    """
    Main execution of the application.
    """
    print(" +------------------------------------------+")
    print(" | XBee MicroPython XBee Beacon Scan Sample |")
    print(" +------------------------------------------+\n")

    # Turn on Bluetooth.
    ble.active(True)
    print("- Started Bluetooth with address '{}'".format(format_address(ble.config("mac"))))

    # Start scanning for beacons.
    scan_for_beacons()


if __name__ == '__main__':
    main()
