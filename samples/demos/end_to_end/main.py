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

from hdc1080 import HDC1080
from machine import I2C
import time
import xbee

# Constants
SLEEP_TIME_MS = 8000  # 8 seconds.
AWAKE_TIME_MS = 2000  # 2 seconds.

MSG_ON = "ON"
MSG_OFF = "OFF"
MSG_SEPARATOR = "@@@"
MSG_AWAKE = "AWAKE"

print(" +------------------------------------+")
print(" | XBee MicroPython End to End Sample |")
print(" +------------------------------------+\n")

# Instantiate the HDC1080 peripheral.
sensor = HDC1080(I2C(1))

# Instantiate the XBee device.
xb = xbee.XBee()

# Configure sleep mode to be managed by MicroPython.
xb.atcmd("SM", 0x06)

sleep_time = SLEEP_TIME_MS

# Start reading temperature and humidity measures.
while True:
    # Notify the gateway that the XBee is awake.
    xbee.transmit(xbee.ADDR_COORDINATOR, MSG_AWAKE)
    # Wait during the configured time for incoming messages.
    start_time_ms = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time_ms) < AWAKE_TIME_MS:
        incoming = xbee.receive()
        if incoming is not None and incoming["sender_nwk"] == 0 and not incoming["broadcast"]:
            try:
                payload = int(incoming["payload"].decode())
            except ValueError:
                continue
            if payload < 0:
                continue
            # Update the sleep time.
            sleep_time = payload * 1000
            print("Temperature/humidity service stopped.\n" if sleep_time == 0
                  else "Changed sleep time to %d s.\n" % payload)

    if sleep_time > 0:
        # Read the temperature and humidity.
        temp_celsius = sensor.read_temperature(True)
        humidity_hr = sensor.read_humidity()

        # Print values in the console.
        print("- Temperature: %s C" % round(temp_celsius, 1))
        print("- Humidity: %s %%\n" % round(humidity_hr, 1))

        # Create the message to send with the temperature and humidity.
        tempHum = "{0}{1}{2}".format(
            round(temp_celsius, 1),
            MSG_SEPARATOR,
            round(humidity_hr, 1)
        )

        # Send values to the gateway (coordinator).
        try:
            xbee.transmit(xbee.ADDR_COORDINATOR, tempHum)
        except OSError as e:
            print("Could not transmit data: " + str(e))

        # Sleep for the configured timeout.
        xb.sleep_now(sleep_time)
