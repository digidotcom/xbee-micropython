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


# TODO: replace with the 64-bit address of your target device.
TARGET_64BIT_ADDR = b'\x00\x13\xA2\xFF\x00\x00\x00\x5D'
MESSAGE = "Hello XBee!"


print(" +---------------------------------------+")
print(" | XBee MicroPython Transmit Data Sample |")
print(" +---------------------------------------+\n")

print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
                                    MESSAGE))

try:
    xbee.transmit(TARGET_64BIT_ADDR, MESSAGE)
    print("Data sent successfully")
except Exception as e:
    print("Transmit failure: %s" % str(e))
