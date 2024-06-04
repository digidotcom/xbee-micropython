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
import sys
import time
import xbee
from digi import ble
from hdc1080 import HDC1080
from machine import I2C, Pin
from xbee import relay

# Constants
ADVERT_PREFIX = "XBee_Remote_HMI_"

HDC1080_ADDR = 0x40

REG_TMP = 0x00
REG_HUM = 0x01

MSG_ON = "ON"
MSG_OFF = "OFF"
MSG_ACK = "OK"
MSG_LED = "LED"
MSG_SEPARATOR = "@@@"

AT_CMD_BI = "BI"   # Bluetooth Identifier
AT_CMD_SH = "SH"   # Serial Number High
AT_CMD_SL = "SL"   # Serial Number Low
AT_CMD_WR = "WR"   # Write Settings

LED_PIN_ID = "D9"  # Pin D9 (ON/SLEEP/DIO9)

LOG_LINE = "- [{}] [{}] {}"
LOG_TEXT_SENT = "SENT"
LOG_TEXT_RECEIVED = "RECV"
LOG_TEXT_ACK = "Command acknowledged! [{}]"
LOG_TEXT_START = "Start monitoring with a refresh rate of {} seconds [{}]"
LOG_TEXT_STOP = "Stop monitoring [{}]"
LOG_TEXT_LED = "Set LED status to {} [{}]"
LOG_TEXT_SENSOR = "Temperature: {}C - Humidity: {}% HR [{}]"


def get_ble_mac():
    """
    Returns the Bluetooth MAC address of the device.

    Returns:
        The Bluetooth MAC address of the device in string format.
    """
    return ":".join('{:02x}'.format(b) for b in ble.config("mac"))


def config_advertisement():
    """
    Configures the Bluetooth advertisement name of the device.
    """
    # Get the XBee MAC address.
    mac_address = get_mac()
    # Write the BI setting adding the last 4 digits of the MAC to the name.
    xbee.atcmd(AT_CMD_BI, "%s%s" % (ADVERT_PREFIX, mac_address[-4:]))
    # Write settings in the device.
    xbee.atcmd(AT_CMD_WR)


def get_mac():
    """
    Returns the XBee MAC address of the device.

    Returns:
        The XBee MAC address of the device in string format.
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

    return sh_string + sl_string


def log_line(sent, data):
    """
    Prints a log line with the
    :param sent: Whether the data to log was received or sent by the device.
    :param data: The data to log.
    """
    print(LOG_LINE.format(
        LOG_TEXT_SENT if sent else LOG_TEXT_RECEIVED,
        get_time(),
        data))


def get_time():
    """
    Returns a string containing the local time in the format 'HH:mm:ss'
    :return: A string with the local time.
    """
    if hasattr(time, "localtime"):
        return "{:02d}:{:02d}:{:02d}".format(
            time.localtime()[3],
            time.localtime()[4],
            time.localtime()[5])
    else:
        return "{:08d}".format(time.ticks_ms())


def main():
    """
    Main execution of the application.
    """
    print(" +------------------------------------+")
    print(" | XBee MicroPython Remote HMI Sample |")
    print(" +------------------------------------+\n")

    # Initialize variables.
    running = False
    refresh_rate = 5
    deadline = 0

    # Instantiate the HDC1080 peripheral.
    sensor = HDC1080(I2C(1))
    if sensor is None:
        print("- Could not find the sensor!")
        sys.exit(1)

    # Configure the Bluetooth identifier of the XBee device.
    config_advertisement()

    # Turn on Bluetooth
    ble.active(True)
    print("- Started Bluetooth with address '{}'".format(get_ble_mac()))

    # Set up the LED pin object to manage the LED status. Configure the pin
    # as output and set its initial value to off (0).
    led_pin = Pin(LED_PIN_ID, Pin.OUT, value=0)

    # Main loop.
    while True:
        # Check if a relay frame has been received.
        relay_frame = relay.receive()
        if relay_frame is not None:
            data = relay_frame["message"].decode("utf-8")
            if data.startswith(MSG_ON):
                # If the message starts with "ON", parse the refresh rate.
                running = True
                refresh_rate = int(data.split(MSG_SEPARATOR)[1])
                log_line(False, LOG_TEXT_START.format(refresh_rate, data))
                deadline = 0
                # Send an ACK to confirm the reception.
                relay.send(relay.BLUETOOTH, MSG_ACK)
                log_line(True, LOG_TEXT_ACK.format(MSG_ACK))
            elif data.startswith(MSG_OFF):
                # If the message starts with "OFF", stop the refresh data process.
                running = False
                log_line(False, LOG_TEXT_STOP.format(data))
                # Send an ACK to confirm the reception.
                relay.send(relay.BLUETOOTH, MSG_ACK)
                log_line(True, LOG_TEXT_ACK.format(MSG_ACK))
            elif data.startswith(MSG_LED):
                # If the message starts with "LED", parse the status.
                led_status = 1 if data.split(MSG_SEPARATOR)[1] == MSG_ON else 0
                log_line(False, LOG_TEXT_LED.format(MSG_ON if led_status == 1 else MSG_OFF, data))
                # Set the new LED status.
                led_pin.value(led_status)
                # Send an ACK to confirm the reception.
                relay.send(relay.BLUETOOTH, MSG_ACK)
                log_line(True, LOG_TEXT_ACK.format(MSG_ACK))

        if running and time.ticks_ms() > deadline:
            # Read the temperature value.
            temp_celsius = sensor.read_temperature(True)
            # Read the humidity value.
            humidity_hr = sensor.read_humidity()

            # Create the message to send with the temperature and humidity.
            temp_round = str(round(temp_celsius, 1))
            hum_round = str(round(humidity_hr, 1))
            temp_hum = temp_round + MSG_SEPARATOR + hum_round

            # Send a relay frame to the Bluetooth interface.
            try:
                relay.send(relay.BLUETOOTH, temp_hum)
                log_line(True, LOG_TEXT_SENSOR.format(temp_round, hum_round, temp_hum))
            except (Exception,):
                pass

            # Calculate the next time to send the data based on the configured refresh rate.
            deadline = time.ticks_ms() + (refresh_rate * 1000) - 1000

        time.sleep(1)


if __name__ == '__main__':
    main()
