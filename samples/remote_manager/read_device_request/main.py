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
from digi import cloud
from machine import Pin

# Pin D9 (ON/SLEEP/DIO9)
LED_PIN_ID = "D9"
# Toggle LED command.
DR_CMD_TOGGLE = "TOGGLE LED"
# Toggle LED answer.
DR_ANSWER_TOGGLE = "LED TOGGLED"
# Unknown command answer.
DR_ANSWER_UNKNOWN = "UNKNOWN COMMAND"


print(" +---------------------------------------------+")
print(" | XBee MicroPython Read Device Request Sample |")
print(" +---------------------------------------------+\n")

# Set up the LED pin object to manage the LED status. Configure the pin
# as output and set its initial value to off (0).
led_pin = Pin(LED_PIN_ID, Pin.OUT, value=0)

# Start reading device requests.
while True:
    request = cloud.device_request_receive()
    if request is not None:
        # A device request has been received, process it.
        data = request.read()
        if data.decode("utf-8").strip() == DR_CMD_TOGGLE:
            print("- Toggle LED device request received.")
            led_pin.toggle()
            written = request.write(bytes(DR_ANSWER_TOGGLE, "utf-8"))
        else:
            written = request.write(bytes(DR_ANSWER_UNKNOWN, "utf-8"))
        request.close()

    time.sleep(5)
