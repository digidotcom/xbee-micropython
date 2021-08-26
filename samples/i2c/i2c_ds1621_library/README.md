I2C DS1621 Library Sample Application
=====================================

This example demonstrates the usage of the I2C API and 'ds1621' library by
giving an example of how to communicate with the DS1621 Digital Thermometer
and Thermostat I2C device.

The example reads the temperature from the device and then performs a
write/read test updating the values of the high and low temperature registers.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* One standalone DS1621 Digital Thermometer and Thermostat I2C device.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the DS1621 device to the I2C interface of the XBee module:
     1. Isolate the pins configured as SDA and SCL so they do not use the
        functionality provided by the board.
     2. Connect the DS1621 device to VCC, to the pins configured as SDA and SCL
        and to GND. See the following table for more information about the pins
        layout:

            +--------+------------+----------+-----------+-----------+
            | Signal | Pin ID     | Pin # TH | Pin # SMT | Pin # MMT |
            +--------+------------+----------+-----------+-----------+
            | SDA    | PWM1/DIO11 | 7        | 8         | 8         |
            +--------+------------+----------+-----------+-----------+
            | SCL    | AD1/DIO1   | 19       | 32        | 30        |
            +--------+------------+----------+-----------+-----------+

   **NOTE**: It is recommended to verify the capabilities of the pins used in
   the example as well as the electrical characteristics in the product manual
   of your XBee Device to ensure that everything is configured correctly.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

The application reads and prints the temperature given by the device and then
executes a write/read communication test updating the values of the high and
low temperature registers. If the value read from the high or low temperature
registers do not match the written one, the application displays an error.

Verify that the XBee REPL console displays the temperature and the write/read
test result:

    - Temperature: 20.0 C (50.0 F)
    - Setting high temperature register to '22'... [OK]
    - Verifying the written value... [OK]
    - Setting low temperature register to '17'... [OK]
    - Verifying the written value... [OK]
    - Done

Required libraries
--------------------

* ds1621

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618

License
-------

Copyright (c) 2019, Digi International, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.