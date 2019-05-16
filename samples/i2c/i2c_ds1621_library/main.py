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

from ds1621 import Ds1621
from machine import I2C
import utime

# Constants
DS1621_ADDR = 0x48  # Assumes A0-2 are low.

print(" +--------------------------------------------+")
print(" | XBee MicroPython I2C DS1621 Library Sample |")
print(" +--------------------------------------------+\n")

# Instantiate an I2C peripheral.
i2c = I2C(1)

# Instantiate a DS1621 device.
ds = Ds1621(i2c, DS1621_ADDR)

# Read the temperature value.
temp_c = ds.read_temperature()
print("- Temperature: %.1f C (%.1f F)" % (temp_c, temp_c * 9 / 10 + 32))

# Configure the high temperature value register.
print("- Setting high temperature register to '22'... ", end="")
ds.set_high_temp_register(22)
print("[OK]")
# Verify the written value.
print("- Verifying the written value... ", end="")
r = ds.read_high_temp_register()
if r != 22:
    print("[ERROR]")
    print("   Set TH to '22' but read back '%d'" % r)
else:
    print("[OK]")

# Wait 10ms between writes (per data sheet).
utime.sleep_ms(10)

# Configure the low temperature value register.
print("- Setting low temperature register to '17'... ", end="")
ds.set_low_temp_register(17)
print("[OK]")
# Verify the written value.
print("- Verifying the written value... ", end="")
r = ds.read_low_temp_register()
if r != 17:
    print("[ERROR]")
    print("   Set TL to '17' but read back '%d'" % r)
else:
    print("[OK]")

print("- Done")
