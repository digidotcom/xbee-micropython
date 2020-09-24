End to End Smart Agriculture IoT Sample Application
===================================================

This example is part of the Digi's End-to-End Smart Agriculture IoT demo. It
demonstrates how to use the XBee Gateway and the XBee 3 modules to exchange
data, communicate with Digi Remote Manager and use the BLE interface to talk to
mobile apps applied to the smart agriculture vertical.

In theory, the XBee 3 module this example runs in corresponds to a irrigation
station and is connected to the following peripherals but, for demonstration
purposes, they are emulated:
  * Temperature sensor.
  * Moisture sensor.
  * Battery level sensor.
  * Electronic irrigation valve.

The example performs the following actions:
  * Listen for BLE connections to execute the provisioning process (initial
    configuration of the irrigation station properties).
  * Listen for data coming from the XBee Gateway to set the value of the 
    irrigation valve.
  * Read the value of the sensors and report them to the XBee Gateway every
    minute.

Read the demo documentation for more information.

Requirements
------------

To run this example you need:

* An XBee 3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-C board).
* An XBee Gateway device running the corresponding Python application of the
  demo.
* A smartphone running the corresponding mobile app. of the demo.
* A Digi Remote Manager account with your XBee Gateway added to it.
  Go to https://myaccount.digi.com/ to create it if you do not have one.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee 3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

The example is already configured, so all you need to do is build and launch
the project. Then, read the demo documentation for more information about how
to test the demo.

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