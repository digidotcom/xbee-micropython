Receive Callback SMS Sample Application
=======================================

This example demonstrates the usage of the cellular API by giving an example of
how to receive SMS messages using a callback.

The example first registers a callback that fires whenever a SMS is received.
When the callback is fired, it prints the sender number and message.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with SMS capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A mobile phone to send the SMS.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Knowledge of your XBee's phone number. You can retrieve your XBee's phone
   number with the PH command.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

Send an SMS message from a mobile phone to the XBee device and verify that
the application prints out in the console the following line:

    SMS received from XXXXXXXXXX >> <MESSAGE>

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x15
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519

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
