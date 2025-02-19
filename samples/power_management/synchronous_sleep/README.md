Synchronous Sleep Sample Application
======================================

In a synchronously sleeping DigiMesh network, the MicroPython
application doesn't control when the module sleeps. If an application
needs to be aware of when the network sleeps and wakes, it can do so by
registering a modem status callback and watching for the relevant modem
statuses.

This sample application demonstrates a module on a synchronously
sleeping network configured to read a sample from an external sensor and
send it to an aggregator each time the network wakes.

Requirements
------------

To run this example you need:

* Two XBee 3 DigiMesh modules with MicroPython support.
* Carrier boards for each radio module (XBIB-U-DEV or XBIB-C board).
* One standalone HDC1080 humidity and temperature sensor (not necessary
  if you are using an XBIB-C carrier board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).

Setup
-----

Set up a synchronously sleeping network with two DigiMesh modules:

* One module is the *aggregator*, and should be configured with the
  following AT commands:
  * **AP** 1
  * **SM** 7
  * **SO** 1

* The other module is the *sensor module* that will run the sample
  application. Make sure the sensor module is on the same network as the
  aggregator (ie ID and CH match on both radios if they have been
  changed from the default), but do not configure sleep settings as that
  will be done by the application.


Make sure the hardware is set up correctly on the sensor module:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the HDC1080 device to the I2C interface of the XBee module. The way
   to connect the sensor changes depending on the carrier board you have:

   * XBIB-U-DEV board:

     * Isolate the pins configured as SDA and SCL so they do not use the
       functionality provided by the board.
     * Connect the HDC1080 device to VCC, to the pins configured as SDA and SCL
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

Open the aggregator in XBee Studio's console so you can observe the frames
output by the module, then compile and launch the application on the
sensor module.

The sensor module will begin to cyclically sleep: two seconds on, two
seconds off. Each time the sensor module wakes, it will send a packet to
the aggregator with the temperature measurement. Observe the
transmissions received in XBee Studio.

Required libraries
--------------------

* hdc1080

Supported platforms
-------------------

* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 300B

License
-------

Copyright (c) 2020-2025, Digi International, Inc.

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
