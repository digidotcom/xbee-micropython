Send Data Points Sample Application
===================================

This example demonstrates the usage of the Digi Remote Manager API by giving
an example of how to upload data points to your Digi Remote Manager account.

The example reads the temperature of the module every 5 seconds, creates a
`DataPoints` object and uploads it to your Digi Remote Manager account.

Requirements
------------

To run this example you need:

* One XBee3 cellular module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A Digi Remote Manager account with the XBee3 cellular device registered in.
* The XCTU application (available at www.digi.com/xctu).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 cellular module into the XBee adapter and connect it to your
   computer's USB port.
2. Make sure the XBee3 cellular device is connected to Internet. To do so,
   verify that the Connection status LED is blinking or the value of the
   **AI** parameter is **0**.
3. Make sure the XBee3 cellular device is connected to Digi Remote Manager. To
   do so, verify that the value of the **DI** parameter is **0**, **5** or **6**
   (connected without TLS, connected over TLS, or connected over TLS with authenticated
   server, respectively).

Run
---

The example is already configured, so all you need to do is to compile and 
launch the application. When executed, it starts reading and uploading the
temperature of the XBee module to your Digi Remote Manager account every 5
seconds.

Follow these steps to verify the temperature is being uploaded to your Digi
Remote Manager account:

1. Log in your Digi Remote Manager account using your credentials: 
   https://remotemanager.digi.com/login.do
2. Within the Digi Remote Manager platfotm, go to the **Data Services** tab
   and select the **Data Streams** option.
3. Look for the stream **`<device_id>`/mp_xbee_temperature** where `<device_id>`
   is the ID of your XBee3 cellular device within your account.
4. Select the stream and verify the chart displays the temperature of the
   module as it is being sent.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11411
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x11

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
