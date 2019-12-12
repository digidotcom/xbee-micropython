Bluetooth iBeacon Advertise Sample Application (SEE LICENSE NOTICE)
==============================================

This example demonstrates the usage of the XBee's BLE advertise feature.
The example forms and advertises iBeacon frames.

The example first turns on Bluetooth and prints out its MAC address.
It periodically advertises iBeacon for some time and then stops advertising.

**DEVELOPER IS RESPONSIBLE FOR OBTAINING THE NECESSARY LICENSES FROM APPLE.
iBeacon(TM) is a trademark of Apple Inc. and use of this code must comply with
their licence.**


Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* The provided iBeacon library found [here](../../../lib/iBeacon/).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Ensure the iBeacon Library is loaded onto the file system under
   `/flash/lib`. It can be found [here](../../../lib/iBeacon/).

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.
Once the following is printed:
`Started Bluetooth with address of: xx:xx:xx:xx:xx:xx`
The XBee is sending out advertisements containing iBeacon frames.

Required libraries
--------------------

* iBeacon

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: 31015
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