End to End Sample Application
=============================

This example demonstrates how to use the XBee Gateway to transmit data from
XBee nodes of the network to Digi Remote Manager and vice versa.

The example reads every 10 seconds the temperature and humidity from the board's
I2C sensor, sends the readings to the gateway and goes to sleep until the
next cycle. It also processes incoming data messages from the gateway to
change the sampling rate or disable the temperature/humidity service.

Requirements
------------

To run this example you need:

* One XBee 3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-C board).
* An XBee Gateway device.
* A Digi Remote Manager account with your XBee Gateway added to it.
  Go to https://myaccount.digi.com/ to create it if you do not have one.
* Another instance of PyCharm with the 'End to End' sample for Python loaded
  (located in the *DEMOS* category).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee 3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

The example is already configured, so all you need to do is build and launch
the project. Then, launch the **End to End** sample for Python in the XBee
Gateway and follow the instructions explained in that sample's README file.

Required libraries
--------------------

* hdc1080

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002

License
-------

Copyright (c) 2020, Digi International, Inc.

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