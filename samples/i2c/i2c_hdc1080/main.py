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
import sys
import time

# Constants
HDC1080_ADDR = 0x40

REG_TMP = 0x00
REG_HUM = 0x01


print(" +-------------------------------------+")
print(" | XBee MicroPython I2C HDC1080 Sample |")
print(" +-------------------------------------+\n")

# Instantiate an I2C peripheral.
i2c = I2C(1)

# Verify that the sensor is connected to the I2C interface.
if HDC1080_ADDR not in i2c.scan():
    print("Could not find the sensor!")
    sys.exit(1)

# Start reading temperature and humidity measures.
while True:
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

    # Print results:
    print("- Temperature: %s C" % round(temp_celsius, 2))
    print("- Humidity: %s %%" % round(humidity_hr, 2))
    print("")

    time.sleep(5)
