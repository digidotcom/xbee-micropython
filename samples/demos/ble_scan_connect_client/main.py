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

import struct
import sys
import time
from binascii import unhexlify
from digi import ble

# Constants
NAME_AD_TAG = 0x09

COLUMN_WIDTH_ID = 4
COLUMN_WIDTH_ADDRESS = 19
COLUMN_WIDTH_NAME = 30

TIMEOUT_RECEIVE_MS = 5000  # 5 seconds
TIMEOUT_SCAN_MS = 15000  # 15 seconds
TIMEOUT_CONNECT_S = 10  # 10 seconds

MESSAGE_PING = "Ping"
MESSAGE_PONG = "Pong"

FRAME_PING = "7E00072D000250696E6742"  # 7E           Delimiter
#                                        00 07        Length (7)
#                                        2D           Frame Type (User Data Relay)
#                                        00           Frame ID (0)
#                                        02           Interface (2 - MicroPython)
#                                        50 69 6E 67  RF Data (Ping)
#                                        42           Checksum

USR_DATA_RELAY_ID = 0xAD
USR_DATA_RELAY_MIN_LENGTH = 6

# Variables.
ble_devices = {}
ble_conn = None
pong_received = False


def execute_scan():
    """
    Executes a Bluetooth scan of 15 seconds and prints the list of BLE devices
    found in table format.
    """
    global ble_devices

    scanner = None
    index = 0
    ble_devices.clear()
    try:
        print("- Scanning for nearby BLE devices (15s)...")
        # Start a scan to run for 10 seconds
        scanner = ble.gap_scan(TIMEOUT_SCAN_MS)
        # Loop through all advertisements until the scan has stopped.
        for adv in scanner:
            if adv["address"] is None:
                continue
            # Generate the device ID.
            address = format_address(adv["address"])
            name = get_advertisement_name(adv["payload"])
            device_id = (address, name)
            if device_id not in ble_devices.values():
                ble_devices[index] = device_id
                index += 1
    finally:
        if scanner is not None:
            scanner.stop()

    if len(ble_devices) > 0:
        print("- Discovered devices:")

        # Print the table of devices.
        print("+{:-<{}}+{:-<{}}+{:-<{}}+".format("", COLUMN_WIDTH_ID, "", COLUMN_WIDTH_ADDRESS, "", COLUMN_WIDTH_NAME))
        print("|{:>{}} | {:<{}}| {:<{}}|".format("ID", COLUMN_WIDTH_ID - 1, "Address", COLUMN_WIDTH_ADDRESS - 1, "Name",
                                                 COLUMN_WIDTH_NAME - 1))
        print("+{:-<{}}+{:-<{}}+{:-<{}}+".format("", COLUMN_WIDTH_ID, "", COLUMN_WIDTH_ADDRESS, "", COLUMN_WIDTH_NAME))
        for key, value in ble_devices.items():
            print("|{:>{}} | {:<{}}| {:<{}}|".format(str(key), COLUMN_WIDTH_ID - 1, value[0], COLUMN_WIDTH_ADDRESS - 1,
                                                     value[1], COLUMN_WIDTH_NAME - 1))
        print("+{:-<{}}+{:-<{}}+{:-<{}}+".format("", COLUMN_WIDTH_ID, "", COLUMN_WIDTH_ADDRESS, "", COLUMN_WIDTH_NAME))
        print("")

        target_id = get_target_id()
        if target_id is None:
            execute_scan()
        else:
            connect_with_device(target_id)
    else:
        get_user_input("- No devices found! Press <ENTER> to execute another scan.")
    execute_scan()


def get_target_id():
    """
    Returns the ID of the device to connect with.

    Returns:
        The ID of the device to connect with.
    """
    target_device = get_user_input("- Enter the ID of the XBee device to connect and press <ENTER> "
                                   "or just press <ENTER> to execute another scan.")
    if target_device is None or len(target_device) == 0:
        return None
    try:
        target_id = int(target_device)
        if target_id < 0 or target_id > (len(ble_devices) - 1):
            print("- Provided ID does not exist.")
            return get_target_id()
        return target_id
    except ValueError:
        print("- Provided ID is not valid.")
        return get_target_id()


def get_password():
    """
    Returns the password of the device to connect with.

    Returns:
        The password of the device to connect with.
    """
    password = get_user_input("- Enter the password of the XBee device and press <ENTER>:")
    if password is None:
        return get_password()
    return password


def connect_with_device(target_id):
    """
    Connects with the device corresponding to the provided ID. After the
    connection takes place, the XBee devices execute a ping-pong communication.

    Args:
        target_id: The ID of the device to connect with.
    """
    global ble_conn
    global pong_received

    pong_received = False
    address = ble_devices[target_id][0].replace(":", "")
    password = get_password()

    # Execute the connection process.
    print("- Connecting with device '{}'...".format(ble_devices[target_id][0]))
    try:
        ble_conn = ble.gap_connect(ble.ADDR_TYPE_PUBLIC, unhexlify(address))
        xbee_conn = ble.xbee_connect(ble_conn, process_frame, password, timeout=TIMEOUT_CONNECT_S)
    except (OSError, ValueError) as ex:
        print("- Error connecting with device > {}".format(str(ex)))
        if ble_conn is not None and ble_conn.isconnected():
            ble_conn.close()
        return
    print("- Connected!")

    # Send the ping text. It is encapsulated inside a 'User Data Relay' frame.
    print("- Sending '{}'...".format(MESSAGE_PING))
    xbee_conn.send(unhexlify(FRAME_PING))
    print("- Sent! Waiting for '{}'...".format(MESSAGE_PONG))

    # Wait for the pong (answer from server).
    dead_line = time.ticks_ms() + TIMEOUT_RECEIVE_MS
    while not pong_received and time.ticks_ms() < dead_line:
        time.sleep_ms(200)

    if not pong_received:
        print("- '{}' was not received from the device.".format(MESSAGE_PONG))
    else:
        print("- '{}' received from the device!".format(MESSAGE_PONG))

    ble_conn.close()
    print("- Disconnected from the XBee device.")
    print("")


def process_frame(frame):
    """
    Processes the provided frame to verify that it corresponds to a
    'User Data Relay Output (0xAD)' frame with the pong text.

    Args:
        frame: The frame in bytearray format to decode.
    """
    global pong_received

    # Discard frames without minimum required length to be a relay frame.
    if len(frame) < USR_DATA_RELAY_MIN_LENGTH:
        return
    delimit, length, xtype, iface = struct.unpack(">BHBB", frame[:5])
    rf_data = frame[5:-1]  # Throw away checksum

    if xtype == USR_DATA_RELAY_ID and rf_data.decode("utf-8") == MESSAGE_PONG:
        pong_received = True


def format_address(address):
    """
    Returns the provided bytearray address in string format.

    Returns:
        The address in string format.
    """
    return ":".join('{:02x}'.format(b) for b in address)


def get_advertisement_name(payload):
    """
    Extracts and returns the advertisement name from the provided payload.

    Args:
        payload: The payload bytearray to get the name from.

    Returns:
        The extracted name.
    """
    # Search for the Name AD TAG byte in the bytearray
    for i in range(1, len(payload)):
        if payload[i] == NAME_AD_TAG:
            # Extract the length of the name string from the byte before the Name AD TAG byte
            length = payload[i - 1] - 1  # Subtract 1 for the Name AD TAG byte

            # Extract the name string
            name_start_index = i + 1
            name_bytes = payload[name_start_index:name_start_index + length]

            # Clean the name string (remove non-printable characters)
            cleaned_name = ''.join(chr(byte) for byte in name_bytes if is_printable_char(byte))
            return cleaned_name

    # If the Name AD TAG byte is not found, return an empty string or raise an error
    return ""


def is_printable_char(byte):
    """
    Checks if a byte represents a printable ASCII character.
    """
    # Printable ASCII characters range from 32 (space) to 126 (tilde '~')
    return 32 <= byte <= 126


def get_user_input(prompt):
    """
    Get user input from the console in MicroPython.

    Args:
        prompt: The prompt message to display to the user.

    Returns:
        The user input string.
    """
    escape_sequence = False

    sys.stdout.write(prompt + '\n  ')
    input_bytes = bytearray()

    while True:
        char = sys.stdin.read(1)

        if escape_sequence:
            # We're in the middle of an escape sequence.
            if char in ('[', 'O'):
                continue  # Skip the next character of escape sequence
            else:
                escape_sequence = False
                continue
        elif char == '\x1b':  # Escape character
            escape_sequence = True
            continue
        elif char == '\r' or char == '\n':  # Check for <ENTER> key press
            break
        elif is_printable_char(ord(char)):
            input_bytes.extend(char.encode())
            sys.stdout.write(char)  # Write the character immediately

    sys.stdout.write('\n')  # Move to the next line after input

    # Return the input bytes.
    if len(input_bytes) == 0:
        return None
    return input_bytes.decode()


def main():
    """
    Main execution of the application.
    """
    print(" +-------------------------------------------------------+")
    print(" | XBee MicroPython BLE Scan and Connect (Client) Sample |")
    print(" +-------------------------------------------------------+\n")

    # Turn on Bluetooth.
    ble.active(True)
    print("- Started Bluetooth with address '{}'".format(format_address(ble.config("mac"))))

    # Start scanning for BLE devices.
    execute_scan()


if __name__ == '__main__':
    main()
