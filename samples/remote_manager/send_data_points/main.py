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
from digi import cloud

# Toggle LED answer.
DATAPOINT_TEMPERATURE = "mp_xbee_temperature"


print(" +------------------------------------------+")
print(" | XBee MicroPython Send Data Points Sample |")
print(" +------------------------------------------+\n")

# Start reading the device temperature and send it to Digi Remote Manager.
while True:
    data = cloud.DataPoints()

    # Read the temperature every 5 seconds during a minute.
    for i in range(12):
        temperature = int(xbee.atcmd('TP') * 9.0 / 5.0 + 32.0)
        data.add(DATAPOINT_TEMPERATURE, temperature)
        time.sleep(5)

    # Upload the samples.
    print("- Uploading data points to Digi Remote Manager...")
    data.send(timeout=60)
