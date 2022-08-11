DRM HTTP Requests Sample Application
====================================

This example demonstrates the usage of the 'remotemanager' library by giving
an example of how to create a datastream and upload datapoints to your Digi
Remote Manager account using HTTP API of the platform.

Instead of calling the internal Digi Remote Manager API, this example uses a
library to communicate with Digi Remote Manager through HTTP requests.

The example creates a datastream and then reads and uploads the temperature of
the module every 30 seconds to the configured Digi Remote Manager account.

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
3. Update the values of `DRM_USER` and `DRM_PASS` constants within the code of
   the example with your Digi Remote Manager account credentials.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application. When executed, the application creates the datastream
and starts uploading samples there. The output should look like this:

    - Creating datastream 'xbee_temperature'... [OK]
    - Uploading datapoint to datastream 'xbee_temperature'... [OK]
    - Uploading datapoint to datastream 'xbee_temperature'... [OK]
    - Uploading datapoint to datastream 'xbee_temperature'... [OK]
    - Uploading datapoint to datastream 'xbee_temperature'... [OK]
    - Uploading datapoint to datastream 'xbee_temperature'... [OK]

Follow these steps to verify samples are actually uploaded to your Digi Remote
Manager account:

1. Log in your Digi Remote Manager account using your credentials:
   https://remotemanager.digi.com/login.do
2. Within the Digi Remote Manager platfotm, go to the **Data Services** tab
   and select the **Data Streams** option.
3. Look for the stream **xbee_temperature**.
4. Select the stream and verify the chart displays the temperature of the
   module as it is being sent.

Required libraries
--------------------

* remotemanager
* urequests

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
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