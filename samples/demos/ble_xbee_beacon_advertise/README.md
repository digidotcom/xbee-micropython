XBee Beacon Advertise Sample Application
========================================

This example is part of Digi's XBee Beacon Advertise demo. It involves
using an XBee device to behave as a Bluetooth Low Energy beacon and advertise
a custom data packet that includes temperature and humidity values read from
the XBIB-C's I2C sensor. Then, it can be scanned from the XBee Mobile app
running in a smartphone.

The MicroPython application reads temperature and humidity values every 5
seconds. It then broadcasts a custom data packet that includes:

- The device's advertised name.
- The company ID.
- The beacon type ID.
- The XBee device's address.
- The current temperature.
- The current humidity.

**Note:** This demo is available as part of the 'XBee Beacon Advertise' Quick
Setup in **XBee Studio**. For optimal functionality, we recommend flashing the
application onto the XBee device using the Quick Setup feature of XBee Studio.
This approach ensures that all necessary configuration parameters for the XBee
device are correctly set up. Direct flashing from PyCharm may omit these
crucial configuration steps.

Requirements
------------

To run this example you need:

* One XBee radio module with Bluetooth and MicroPython support.
* One **XBIB-C** carrier board for the radio module.
* XBee Studio application, version 6.4.2 or newer
  (available at https://www.digi.com/xbee-studio).
* An Android or iOS device with either:
  * The Digi XBee Mobile application, available from Google Play or
    the App Store

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee radio module into the XBee adapter of the XBIB-C board and
   connect it to your computer's USB port.

2. Apply the **XBee Beacon Advertise** Quick Setup to your XBee device using
   the 'Quick Setup' feature of XBee Studio. For further information on how to
   perform this task, refer to the XBee Studio user manual.

Run
---

The example is pre-configured, so all you need to do is build and launch the
project.

To test the demo using the Digi XBee Mobile app, follow these steps:
1. Launch the Digi XBee Mobile app and tap **Get Started**.
2. On the Get Started page, select **XBee Beacon Advertise**.
3. Tap the **Start scanning** option in the second step.
4. After a few seconds, the application should find the beacon and display
   information about the advertised data in a card format.

Required libraries
--------------------

* hdc1080

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2004
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3003
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee BLU - minimum firmware version: 4000

License
-------

Copyright (c) 2024,2025, Digi International, Inc.

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
