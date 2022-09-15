Relay Frames Temperature Sample Application
===========================================

This example demonstrates the usage of the User Data Relay frames API by giving
an example of how to send and receive data to the Bluetooth Low Energy
interface.

The example waits for a User Data Relay message to start reading the temperature
and humidity from the XBIB-C carrier board sensor. Then, it sends the values to
the XBee Bluetooth interface at the specified rate.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-C board).
* The XCTU application, version 6.4.2 or newer
  (available at www.digi.com/xctu).
* An Android or iOS device with the 'XBee BLE MicroPython' sample installed.


Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

2. Enable the Bluetooth interface of the XBee device and configure the
   Bluetooth authentication using XCTU.
   For further information on how to perform this task, refer to the
   XCTU user manual.

Run
---

The example is already configured, so all you need to do is build and launch
the project. Then, launch the 'XBee BLE MicroPython' sample of the Digi Mobile
SDK and follow the instructions explained in that sample's README file.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2004
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3003
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
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
