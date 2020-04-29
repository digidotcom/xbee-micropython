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

import xbee


print(" +-------------------------------------+")
print(" | XBee MicroPython AT Commands Sample |")
print(" +-------------------------------------+\n")

# Read the module's firmware version.
fw_version = hex(xbee.atcmd("VR"))
print("Firmware version: " + fw_version)

# Read the module's hardware version.
hw_version = hex(xbee.atcmd("HV"))
print("Hardware version: " + hw_version)

# Read the module's temperature.
temperature = xbee.atcmd("TP")
# convert unsigned 16-bit value to signed temperature
if temperature > 0x7FFF:
    temperature = temperature - 0x10000
print("The XBee is %.1F C (%.1F F)" % (temperature, temperature * 9.0 / 5.0 + 32.0))

# Configure the module's node identifier and read it.
xbee.atcmd("NI", "XBee3 module")
print("Configured node identifier: " + xbee.atcmd("NI"))
