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

from hdc1080 import HDC1080
from machine import I2C
import time

print(" +---------------------------------------------+")
print(" | XBee MicroPython I2C HDC1080 library Sample |")
print(" +---------------------------------------------+\n")

# Instantiate the HDC1080 peripheral.
sensor = HDC1080(I2C(1))

# Start reading temperature and humidity measures.
while True:
    temp_celsius = sensor.read_temperature(True)
    humidity_hr = sensor.read_humidity()

    # Print results:
    print("- Temperature: %s C" % round(temp_celsius, 2))
    print("- Humidity: %s %%" % round(humidity_hr, 2))
    print("")

    time.sleep(5)
