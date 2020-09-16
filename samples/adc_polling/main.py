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

from machine import ADC
import xbee
import time

# Pin D3 (AD3/DIO3)
ADC_PIN_ID = "D3"

# ADC reference voltage
AV_VALUES = {0: 1.25, 1: 2.5, 2: 3.3, None: 2.5}

print(" +-------------------------------------+")
print(" | XBee MicroPython ADC Polling Sample |")
print(" +-------------------------------------+\n")

# Read the module's Analog Digital Reference
try:
    av = xbee.atcmd("AV")
except KeyError:
    # Reference is set to 2.5 V on XBee 3 Cellular
    av = None
reference = AV_VALUES[av]
print("Configured Analog Digital Reference: AV:{}, {} V".format(av, reference))


# Create an ADC object for pin DIO0/AD0.
adc_pin = ADC(ADC_PIN_ID)

# Start reading the analog voltage value present at the pin.
while True:
    print("- ADC value:", adc_pin.read())
    print("- Analog voltage [V]:", adc_pin.read() * reference / 4095)
    time.sleep(1)
