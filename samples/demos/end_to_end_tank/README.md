End to End Tank Monitoring IoT Sample Application
=================================================

This example is part of the Digi XBee IoT Tank Monitoring demo. It
demonstrates how to use the XBee 3 Cellular modules to communicate with Digi
Remote Manager and use the BLE interface to talk to mobile apps applied to
the tank monitoring vertical.

In theory, the XBee 3 Cellular module this example runs in corresponds to a
tank controller and is connected to the following peripherals (for demonstration
purposes, some of them are emulated):
  * Level sensor (emulated).
  * Electronic valve (emulated).
  * Temperature (obtained from the I2C sensor of the XBIB-C board).

The example performs the following actions:
  * Listen for BLE connections to execute the provisioning process (initial
    configuration of the tank controller properties).
  * Read the values of the sensors and upload them to Digi Remote Manager
    periodically.
  * Listen for requests coming from Digi Remote Manager and execute the proper
    actions.

Read the [demo documentation][doc] for more information.

Requirements
------------

To run this example you need:

* At least one XBee 3 Cellular module and its corresponding carrier board
  (XBIB-C board).
* A smartphone running the corresponding mobile app of the demo.
* A Digi Remote Manager account. Go to https://myaccount.digi.com/ to create it
  if you do not have one.
* Digi XBee Studio (available at www.digi.com/xbee-studio).

Setup
-----

Make sure the hardware is set up correctly. For each XBee 3 Cellular module:

1. Plug the XBee 3 Cellular radio module into the XBee adapter and connect it
   to your computer's USB port.
2. Make sure the XBee3 cellular device is connected to Internet. To do so,
   verify that the Connection status LED is blinking or the value of the
   **AI** parameter is **0**.
3. Using XBee Studio, enable the *"Always remain connected to Digi Remote
   Manager through TCP"* feature by setting the **MO** parameter to **7**. This
   way the device remains connected to Digi Remote Manager while you test the
   sample.
4. Make sure the XBee3 cellular device is connected to Digi Remote Manager. To
   do so, verify that the value of the **DI** parameter is **0**, **5** or
   **6**.

Run
---

The example is already configured, so all you need to do is build and launch
the project. Then, read the demo documentation for more information about how
to test the demo.

Required libraries
--------------------

* hdc1080

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10

License
-------

Copyright (c) 2021-2025, Digi International, Inc.

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


[doc]: https://www.digi.com/resources/documentation/digidocs/90002422
