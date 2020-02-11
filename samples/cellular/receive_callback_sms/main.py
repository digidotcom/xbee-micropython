# Copyright (c) 2020, Digi International, Inc.
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

import network
import time


def my_sms_callback(sms):
    print("SMS received from %s >> %s" % (sms['sender'], sms['message']))


print(" +----------------------------------------------+")
print(" | XBee MicroPython Receive SMS Callback Sample |")
print(" +----------------------------------------------+\n")

cellular = network.Cellular()
# Register the SMS callback. Callbacks are serviced asynchronously.
cellular.sms_callback(my_sms_callback)

print("Waiting for SMS...\n")

while True:
    # Make long blocking calls here, the callback will still fire.
    time.sleep(120)
