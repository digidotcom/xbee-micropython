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

import time
from digi import ble
from xbee import atcmd
from xbee import relay
from xbee import modem_status


# Constants
STATUS_BLE_CONNECTED = 0x32
STATUS_BLE_DISCONNECTED = 0x33

AT_CMD_BI = "BI"  # Bluetooth Identifier
AT_CMD_WR = "WR"  # Write Settings

IDENTIFIER = "XBee Scan-And-Connect"

MESSAGE_PING = "Ping"
MESSAGE_PONG = "Pong"

WAIT_MESSAGE_INTERVAL = 5000  # 5 seconds


def config_advertisement():
    """
    Configures the Bluetooth advertisement name of the device.
    """
    # Write the identifier in the BI setting.
    atcmd(AT_CMD_BI, IDENTIFIER)
    # Write settings in the device.
    atcmd(AT_CMD_WR)


def format_address(address):
    """
    Returns the provided bytearray address in string format.

    Returns:
        The address in string format.
    """
    return ":".join('{:02x}'.format(b) for b in address)


def wait_for_connection():
    """
    Waits for another XBee device running the 'client' version of the demo
    to connect.
    """
    deadline = time.ticks_ms()

    print("- Waiting for connection...")
    print("")
    while True:
        # Check if any client connected or disconnected.
        status = modem_status.receive()
        if status == STATUS_BLE_CONNECTED:
            print("- Client connected!")
            # Reset the deadline value.
            deadline = time.ticks_ms() + WAIT_MESSAGE_INTERVAL
        elif status == STATUS_BLE_DISCONNECTED:
            print("- Client disconnected!")
            print("")
            print("- Waiting for connection...")
            print("")
            # Reset the deadline value.
            deadline = time.ticks_ms() + WAIT_MESSAGE_INTERVAL
        # Check if the client sent a ping message to answer with a pong.
        text = relay.receive()
        if text is not None and text["message"].decode("utf-8") == MESSAGE_PING:
            print("- '{}' received from client. Sending '{}'...'".format(MESSAGE_PING, MESSAGE_PONG))
            relay.send(relay.BLUETOOTH, MESSAGE_PONG)
            print("- '{}' sent!'".format(MESSAGE_PONG))
        # Show the wait message.
        if time.ticks_ms() > deadline:
            deadline = time.ticks_ms() + WAIT_MESSAGE_INTERVAL
            print("- Waiting for connection...")
            print("")
        time.sleep_ms(100)


def main():
    """
    Main execution of the application.
    """
    print(" +-------------------------------------------------------+")
    print(" | XBee MicroPython BLE Scan and Connect (Server) Sample |")
    print(" +-------------------------------------------------------+\n")

    # Configure the Bluetooth advertisement.
    config_advertisement()

    # Turn on Bluetooth.
    ble.active(True)
    print("- Started Bluetooth with address '{}'".format(format_address(ble.config("mac"))))

    # Wait for connection.
    wait_for_connection()


if __name__ == '__main__':
    main()
