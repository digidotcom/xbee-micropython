Receive Data Sample Application
===============================

This example demonstrates the usage of the RF communication API by giving an
example of how to receive data from other XBee device in the same network.

Requirements
------------

To run this example you need:

* Two XBee3 radio modules with MicroPython support.
* Two carrier boards for the radio modules (XBIB-U-DEV or XBIB-C board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).

Setup
-----

The XBee3 module that runs this sample will act as receiver, while the other
one will act as sender.

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio modules into the XBee adapters and connect them to your
   computer's USB ports.
2. Ensure that the sender module is in API mode and both modules are on the
   same network.
3. Find the 64-bit (MAC) address of the receiver module, which is a 16
   character string that follows the format *0013A200XXXXXXXX*. It will be used
   later in the example.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

Then, you need to send a data frame to the receiver module from the sender one.
Follow these steps to do so:

1. Open XBee Studio and wait until the sender XBee module is discovered.
2. In the left menu, go to the **XBee Console** page and open the connection.
3. Create and add an API frame to the **Send data** list with the following
   parameters:

       - Frame type:             0x10 - Transmit request
       - Frame ID:               01
       - 64-bit dest. address:   Use the 64-bit address of the receiver module
       - 16-bit dest. address:   FF FE
       - Broadcast radius:       00
       - Options:                00
       - RF data (ASCII):        Hello XBee!

4. Send this packet by selecting it and clicking the **Send selected packet**
   button.

When the data frame is sent, verify that a line with the sender address and the
data included in the **RF data** field is printed out in the console:

    Data received from 0013A200XXXXXX >> Hello XBee!

Where *0013A200XXXXXXXX* is the 64-bit address of the sender module.

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