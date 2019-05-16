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

import time
import xbee

AI_DESC = {
    0x00: 'CONNECTED',
    0x22: 'REGISTERING_TO_NETWORK',
    0x23: 'CONNECTING_TO_INTERNET',
    0x24: 'RECOVERY_NEEDED',
    0x25: 'NETWORK_REG_FAILURE',
    0x2A: 'AIRPLANE_MODE',
    0x2B: 'USB_DIRECT',
    0x2C: 'PSM_DORMANT',
    0x2F: 'BYPASS_MODE_ACTIVE',
    0xFF: 'MODEM_INITIALIZING',
}


def watch_ai():
    """
    Monitors the value of the AI parameter. Whenever it changes it displays
    the new value.
    """

    old_ai = -1
    while old_ai != 0x00:
        new_ai = xbee.atcmd("AI")
        if new_ai != old_ai:
            print("- AI Changed!")
            print("   * New AI: 0x%02X (%s)"
                  % (new_ai, AI_DESC.get(new_ai, "UNKNOWN")))
            old_ai = new_ai
        else:
            time.sleep(0.01)


print(" +-------------------------------------------+")
print(" | XBee MicroPython Connection Status Sample |")
print(" +-------------------------------------------+\n")

watch_ai()
