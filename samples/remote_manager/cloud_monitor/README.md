DRM Cloud Console sample application
====================================

This example demonstrates the usage of the DRM remote console feature
integrated with MicroPython on a Digi XBee 3 Cellular product.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A Digi Remote Manager account. XBee3 Cellular module does not need to be
  registered or connected to Digi Remote Manager.
* The XCTU application (available at www.digi.com/xctu).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Make sure the XBee3 cellular device is connected to Internet. To do so,
   verify that the Connection status LED is blinking or the value of the
   **AI** parameter is **0**.
3. The Cloud Console requires an active TCP session to DRM, so ensure
   that bit-zero of the **MO** parameter is set.

Run
---

The example is already configured, so all you need to do is to compile
and launch the application. When executed, the application will prompt
for user input and respond to a small set of commands such as 'help
and 'ip'.  When the **AP** parameter is **4** this interaction will
occur over the primary UART, When **AP** is changed to another value,
the application will interact over any connected Cloud console session.

Follow these steps to verify Console activity in Digi Remote
Manager account:

1. Log in your Digi Remote Manager account using your credentials:
   https://remotemanager.digi.com/login.do
2. Within the Digi Remote Manager platform, go to the **Devices** tab
   and open the page for the desired device.
3. On the device page, select **Console** from the header at the top.
4. Interact with the application. If not seeing data in the cloud
   console remember that **AP** must not be **4**.

Supported platforms
-------------------

* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11418
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x18

License
-------

Copyright (c) 2021, Digi International, Inc.

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
