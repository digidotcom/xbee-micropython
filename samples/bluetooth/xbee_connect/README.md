XBee-to-XBee Bluetooth Connection Sample Application
======================================

This example demonstrates XBee to XBee communication by creating an
authenticated and encrypted connection to the API service of a remote
XBee 3 device.

When run the example will connect to the specified XBee address with
the provided password and periodically query the time and temperature
of the remote XBee.

Requirements
------------

To run this example you need:

* Two XBee3 radio modules with MicroPython support.
    * One will act as the MicroPython host, the other the target for
      the API Service client.
* Two carrier boards for the radio module (XBIB-U-DEV or XBIB-C board).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio modules into the XBee adapters and connect to
   your computer's USB port.
2. On the XBee3 that will act as the API Service server
   1. Enable Bluetooth
   2. Configure a password and take note of the Bluetooth address and
      password for customization of the MicroPython application.

Run
---

The example must be configured prior to execution by providing the
Bluetooth address and the password for the server XBee3. The example
code should be modified to provide these values in the ADDRESS and
PASSWORD variables at the top of the file.

When run the script reports when it performs a query and provides
interpreted response data for the time and temperature when it is
received.

Required libraries
--------------------

N/A

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11416
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x16
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618

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
