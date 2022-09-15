I2C Scanner Sample Application
==============================

This example demonstrates the usage of the I2C API by giving an example
of how to scan for I2C devices connected to the I2C interface of the XBee
module.

The application scans all I2C addresses between **0x08** and **0x77** inclusive
and prints those that respond.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* One I2C device (not necessary if you are using an XBIB-C carrier board).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the I2C device to the I2C interface of the XBee module. The way to
   connect the sensor changes depending on the carrier board you have:

   * XBIB-U-DEV board:

     * Isolate the pins configured as SDA and SCL so they do not use the
       functionality provided by the board.
     * Connect the I2C device to VCC, to the pins configured as SDA and SCL
       and to GND. See the following table for more information about the pins
       layout:

           +--------+------------+----------+-----------+-----------+
           | Signal | Pin ID     | Pin # TH | Pin # SMT | Pin # MMT |
           +--------+------------+----------+-----------+-----------+
           | SDA    | PWM1/DIO11 | 7        | 8         | 8         |
           +--------+------------+----------+-----------+-----------+
           | SCL    | AD1/DIO1   | 19       | 32        | 30        |
           +--------+------------+----------+-----------+-----------+

   * XBIB-C board:

     * XBIB-C boards already come with an HDC1080 I2C sensor connected to the
       I2C interface of the XBee module, so you don't need to connect anything.

   **NOTE**: It is recommended to verify the capabilities of the pins used in
   the example as well as the electrical characteristics in the product manual
   of your XBee Device to ensure that everything is configured correctly.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

The application performs a discovery of I2C devices connected to the I2C
interface of the XBee device. Once an I2C device is found, it displays its
address. Verify that the XBee REPL console displays the address of the I2C
device connected to your XBee module:

    - I2C device found at address: 0x40

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
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519

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
