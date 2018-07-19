"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Test code for a Maxim DS1621 (I2C Digital Thermometer and Thermostat).
    
Instructions:
  - Upload lib/ds1621.py to the lib/ directory on your XBee.
  - Wire a DS1621 IC to your XBee module as follows:
      XBee -> DS1621
      19  SCL  2
       7  SDA  1
       1  Vcc  8
      10  GND  4 (and address pins 5, 6 and 7)
  - Use Paste Mode (CTRL-E) to run this code on your XBee.
  - After execution, you can enter commands in the REPL to run other methods
    on the "ds" object
"""

import machine, utime
from ds1621 import Ds1621
ds = Ds1621(machine.I2C(1), 0x48)  # address 0b100_1000. Assumes A0-2 are low.

print("Starting DS1621 test")

tempC = ds.read_temperature()
print('temp is %.1fC (%.1fF)' % (tempC, tempC * 9 / 10 + 32))

# Try setting the TH register to a few different values, then reading it back.
# If we always get back the value we last set, it's a pretty good bet that
# both read and write operations are working in our I2C implementation.
ds.set_high_temp_register(17)
r = ds.read_high_temp_register()
assert r == 17, "Set TH to 17 but read back %d" % r

# DS1621 documentation says:
#  - Writing to the E^2 requires a maximum of 10ms at room temperature. After
#    issuing a write command, no further writes should be attempted for at
#    least 10ms.
# So, we delay 10 milliseconds here.
utime.sleep_ms(10)

ds.set_high_temp_register(25)
r = ds.read_high_temp_register()
assert r == 25, "Set TH to 25 but read back %d" % r
utime.sleep_ms(10)

ds.set_high_temp_register(-55)
r = ds.read_high_temp_register()
assert r == -55, "Set TH to -55 but read back %d" % r

print("DS1621 test SUCCESSFUL")
