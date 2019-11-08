Bluetooth Eddystone Advertise Sample Application
================================================

This example demonstrates the usage of the XBee's BLE advertise feature.
The example forms and advertises Eddystone beacons.

The example first turns on Bluetooth and prints out its MAC address.
It periodically sends out three types of Eddystone Beacons.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* The provided Eddystone library found [here](../../../lib/eddystonebeacon/).
* A way to parse Eddystone Beacons.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Ensure the Eddystone Library is loaded onto the file system under
   `/flash/lib`. It can be found [here](../../../lib/eddystonebeacon/).

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.
Once the following is printed:
`Started Bluetooth with address of: xx:xx:xx:xx:xx:xx`
The XBee is sending out advertisements containing Eddystone beacons.
They will be also be printed out as they are advertised.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 ATT - minimum firmware version: 31015
* Digi XBee3 Zigbee 3 - minimum firmware version: 1009
* Digi XBee3 802.15.4 - minimum firmware version: 2007

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