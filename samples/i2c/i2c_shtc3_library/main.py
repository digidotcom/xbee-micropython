# Copyright (c) 2025, Digi International, Inc.
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

from shtc3 import SHTC3
from machine import I2C
import time

print(" +-------------------------------------------+")
print(" | XBee MicroPython I2C SHTC3 library Sample |")
print(" +-------------------------------------------+\n")

# Instantiate the SHTC3 peripheral.
sensor = SHTC3(I2C(1))

# Start reading temperature and humidity measures.
while True:
    temp_celsius = sensor.get_temp()
    humidity_hr = sensor.get_humid()

    # Print results:
    print("- Temperature: %.2f C" % temp_celsius)
    print("- Humidity: %.2f %%" % humidity_hr)
    print("")

    time.sleep(5)
