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


print(" +---------------------------------------+")
print(" | XBee MicroPython Prevent Sleep Sample |")
print(" +---------------------------------------+\n")

xb = xbee.XBee()

while True:
    # Interruptable stuff.
    print("-" * 20)
    interruptable_counter = 0
    while interruptable_counter < 10:
        interruptable_counter += 1
        print("Interruptable counter: %s" %
              interruptable_counter)
        time.sleep(1)

    with xb.wake_lock:
        # Not interruptable (important) stuff.
        print("-" * 20)
        not_interruptable_counter = 0
        while not_interruptable_counter < 10:
            not_interruptable_counter += 1
            print("Not interruptable counter: %s" %
                  not_interruptable_counter)
            time.sleep(1)
