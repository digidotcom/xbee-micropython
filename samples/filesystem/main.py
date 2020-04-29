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

from machine import Pin
import time
import uio
import uos
import xbee


# Pin D0 (AD0/DIO0)
BUTTON = "D0"
LOG_FILE = "temperature.log"


print(" +-------------------------------------+")
print(" | XBee MicroPython File System Sample |")
print(" +-------------------------------------+\n")

button = Pin(BUTTON, Pin.IN, Pin.PULL_UP)

# If the log file exists, remove it.
try:
    log = uio.open(LOG_FILE)
    log.close()
    uos.remove(LOG_FILE)
except OSError:
    # Do nothing, the file does not exist.
    pass

print("Reading XBee's temperature, press the %s button to stop...\n" % BUTTON)

# Create and open the log file in the XBee's file system.
with uio.open(LOG_FILE, mode="a") as log:
    stopped = False
    while not stopped:
        temperature = xbee.atcmd("TP")
        # convert unsigned 16-bit value to signed temperature
        if temperature > 0x7FFF:
            temperature = temperature - 0x10000
        # Write the current temperature in the log file.
        dummy = log.write("Current temperature: %.1F C (%.1F F)\n" % (temperature, temperature * 9.0 / 5.0 + 32.0))
        # Wait 1 second until the next reading.
        for x in range(10):
            if button.value() == 0:
                stopped = True
                break
            time.sleep(0.1)

print("Displaying log...\n")

# Open again the log file to read its contents.
with uio.open(LOG_FILE) as log:
    while True:
        line = log.readline()
        if not line:
            break
        print(line, end="")

print("\nLog file read")
