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

from machine import I2C
from xbee import relay
import sys
import time

# Constants
HDC1080_ADDR = 0x40

REG_TMP = 0x00
REG_HUM = 0x01

MSG_ON = "ON"
MSG_OFF = "OFF"
MSG_ACK = "OK"
MSG_SEPARATOR = "@@@"

# Variables
running = False
refresh_rate = 5
deadline = 0


print(" +--------------------------------------------------+")
print(" | XBee MicroPython Relay Frames Temperature Sample |")
print(" +--------------------------------------------------+\n")

# Instantiate an I2C peripheral.
i2c = I2C(1)

# Verify that the sensor is connected to the I2C interface.
if HDC1080_ADDR not in i2c.scan():
    print("Could not find the sensor!")
    sys.exit(1)

while True:
    # Check if a relay frame has been received.
    relay_frame = relay.receive()
    if relay_frame is not None:
        data = relay_frame["message"].decode("utf-8")
        # If the message starts with "ON", parse the refresh rate.
        if data.startswith(MSG_ON):
            running = True
            refresh_rate = int(data.split(MSG_SEPARATOR)[1])
            deadline = 0
            # Send an ACK to confirm the reception.
            relay.send(relay.BLUETOOTH, MSG_ACK)
        elif data.startswith(MSG_OFF):
            running = False
            # Send an ACK to confirm the reception.
            relay.send(relay.BLUETOOTH, MSG_ACK)

    if running and time.ticks_ms() > deadline:
        # Change the pointer to 0x00 (Temperature register)
        i2c.writeto(HDC1080_ADDR, bytearray([REG_TMP]))
        # Wait for the temperature measure to complete (per data sheet).
        time.sleep(0.0635)
        # Read the temperature value (2 bytes).
        temp_bytes = i2c.readfrom(HDC1080_ADDR, 2)
        # Calculate the temperature in Celsius.
        temp_celsius = (int.from_bytes(temp_bytes, "big") / 2 ** 16) * 165 - 40

        # Change the pointer to 0x01 (Temperature register)
        i2c.writeto(HDC1080_ADDR, bytearray([REG_HUM]))
        # Wait for the humidity measure to complete (per data sheet).
        time.sleep(0.065)
        # Read the humidity value (2 bytes).
        humidity_bytes = i2c.readfrom(HDC1080_ADDR, 2)
        # Calculate the humidity in HR.
        humidity_hr = (int.from_bytes(humidity_bytes, "big") / 2 ** 16) * 100

        # Create the message to send with the temperature and humidity.
        tempHum = str(round(temp_celsius, 1)) + MSG_SEPARATOR + str(round(humidity_hr, 1))

        # Send a relay frame to the Bluetooth interface.
        try:
            relay.send(relay.BLUETOOTH, tempHum)
        except:
            pass

        # Calculate the next time to send the data based on the configured refresh rate.
        deadline = time.ticks_ms() + (refresh_rate * 1000) - 1000

    time.sleep(1)
