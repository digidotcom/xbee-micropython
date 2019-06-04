"""
Copyright (c) 2018, Digi International, Inc.
Module released under MIT License.

Module for I2C interface to Maxim DS1621 Digital Thermometer and Thermostat.

Use with samples/i2c/ds1621.py.
"""

import utime
import ustruct

class Ds1621:
    # The high/low temperature registers are 9-bit two's complement signed ints.
    # Data is written MSB first, so as an example the value 1 (0b1) is represented
    # as 0b00000000 10000000, or 0x0080.
    REGISTER_FORMAT = '>h'
    REGISTER_SHIFT = 7
    
    def __init__(self, i2c, slave_addr):
        # Perform a scan and make sure we find the slave device we want to talk to.
        devices = i2c.scan()
        assert slave_addr in devices, "Did not find slave %d in scan: %s" % (slave_addr, devices)
        self.i2c = i2c
        self.slave_addr = slave_addr

    # Read a 9-bit temperature from the DS1621.  Values for <protocol>:
    #   b'0xAA' for Read Temperature
    #   b'0xA1' for TH Register
    #   b'0xA2' for TL Register
    # Returns temperature in units of 0.5C.  Fahrenheit = temp * 9 / 10 + 32
    def read_temperature(self, protocol=b'\xAA'):
        self.i2c.writeto(self.slave_addr, protocol, False)
        data = self.i2c.readfrom(self.slave_addr, 2)
        return ustruct.unpack(self.REGISTER_FORMAT, data)[0] >> self.REGISTER_SHIFT

    # Set TH (protocol=b'0xA1') or TL (protocol=b'0xA2') register to <value>
    def set_temp_register(self, protocol, value):
        data = ustruct.pack(self.REGISTER_FORMAT, value << self.REGISTER_SHIFT)
        written = self.i2c.writeto(self.slave_addr, protocol + data)
        assert written == 3, "temp register write returned %d ?" % written

    def read_high_temp_register(self):
        return self.read_temperature(b'\xA1')

    def set_high_temp_register(self, value):
        self.set_temp_register(b'\xA1', value)

    def read_low_temp_register(self):
        return self.read_temperature(b'\xA2')

    def set_low_temp_register(self, value):
        self.set_temp_register(b'\xA2', value)

    def start_convert(self):
        self.i2c.writeto(self.slave_addr, '\xEE', True)
        
    def stop_convert(self):
        self.i2c.writeto(self.slave_addr, '\x22', True)

    def read_last_temperature(self):
        return self.read_temperature(b'\xAA')
        
    def read_access_config(self):
        self.i2c.writeto(self.slave_addr, '\xAC', False)
        return self.i2c.readfrom(self.slave_addr, 1)

    def write_access_config(self, value):
        written = self.i2c.writeto(self.slave_addr, b'\xA1' + ustruct.pack('b', value))
        assert written == 2, "Access Config write returned %d ?" % written

    def display_continuous(self):
        self.start_convert()
        try:
            while True:
                print('%.1fF' % (self.read_last_temperature() * 9 / 10 + 32))
                utime.sleep(2)
        except:
            self.stop_convert()
            raise
