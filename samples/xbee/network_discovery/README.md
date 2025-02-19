Network Discovery Sample Application
====================================

This example demonstrates the usage of the network discovery functionality by
giving an example of how to discover the devices that compose the network.

The example prints out in the console the 64-bit address, node identifier and
RSSI of the network devices as soon as they are found during the discovery.

Requirements
------------

To run this example you need:

* At least two XBee3 radio modules with MicroPython support.
* At least two carrier boards for the radio modules (XBIB-U-DEV or XBIB-C board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio modules into the XBee adapters and connect them to your
   computer's USB ports.
2. Ensure that the modules are on the same network.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

Verify that the application prints out the 64-bit address, node identifier and
RSSI of the network devices in the console as soon as they are discovered:

    New discovered device:
      - 64-bit address: 0013A200XXXXXXXX
      - Node identifier: MY_REMOTE_DEVICE
      - RSSI: -33

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002

License
-------

Copyright (c) 2019-2025, Digi International, Inc.

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