Transmit Broadcast Data Sample Application
==========================================

This example demonstrates the usage of the RF communication API by giving an
example of how to transmit a broadcast message to all the XBee devices in the
same network.

Requirements
------------

To run this example you need:

* Two XBee3 radio modules with MicroPython support.
* Two carrier boards for the radio modules (XBIB-U-DEV or XBIB-C board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).

Setup
-----

The XBee3 module that runs this sample will act as sender, while the other
one will act as receiver.

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio modules into the XBee adapters and connect them to your
   computer's USB ports.
2. Ensure that the receiver module is in API mode and both modules are on the
   same network.

Run
---

Before launching the application, you need to set up XBee Studio to see the data
received by the receiver module. Follow these steps to do so:

1. Launch XBee Studio.
2. Wait until the receiver XBee module is discovered and click on it.
3. In the left menu, go to the **XBee Console** page and open the connection.

Finally, compile and launch the MicroPython application. It prints out the
status of the operation in the console :

    Sending broadcast data >> Hello XBee World!
    Data sent successfully

Verify that a new **Receive packet** has been received in the XBee Studio
console. Select it and review the details, some of them similar to:

    - Start delimiter:         7E
    - Length:                  Depends on the XBee protocol
    - Frame type:              90 (Receive Packet)
    - 64-bit source address:   The XBee sender's 64-bit address
    - RF data (ASCII):         Hello XBee World!

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002

License
-------

Copyright (c) 2019-2025, Digi International, Inc.

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