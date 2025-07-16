Wi-SUN Get Started Sample Application
=====================================

This example is part of the Digi's Wi-SUN Get Started. It demonstrates
how to use the XBee Hive Wi-SUN and the XBee Wi-SUN modules to exchange
data using the socket IPv6 API.

This application is executed in the XBee Wi-SUN module and performs the
following actions:
  * Listens for incoming IPv6 messages on port 0x2616 (9750).
  * Converts the payload to uppercase.
  * Sends the modified message back to the sender’s address.

Read the [demo documentation][doc] for more information.

Requirements
------------

To run this example you need:

* An XBee Wi-SUN radio module with MicroPython support.
* One carrier board for the radio module (XBIB-C board).
* An XBee Hive Wi-SUN device running the corresponding Python application of the
  Get Started.

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

* Digi XBee Wi-SUN - minimum firmware version: A000A1

License
-------

Copyright (c) 2025, Digi International, Inc.

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

[doc]: https://docs.digi.com/resources/documentation/digidocs/rf-docs/wisun/wisun-gs_c.html