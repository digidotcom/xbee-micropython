Receive Data IPv6 Sample Application
====================================

This example demonstrates the usage of the socket IPv6 API by giving an example
of how to receive data from other XBee device in the same Wi-SUN network.

Requirements
------------

To run this example you need:

* Two XBee Wi-SUN modules.
* Two carrier boards for the radio modules (XBIB-U-DEV or XBIB-C board).
* One Wi-SUN border router.
* Digi XBee Studio v1.2.0 or higher (available at www.digi.com/xbee-studio).

Setup
-----

The XBee module that runs this sample will act as receiver, while the other
one will act as sender.

Make sure the hardware is set up correctly:

1. Plug the XBee radio modules into the XBee adapters and connect them to your
   computer's USB ports.
2. Ensure that the sender module is in API mode and both modules are on the
   same Wi-SUN network.

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

       - Frame type:         0x40 - Socket Create
       - Frame ID:           01
       - Protocol:           UDP [00]

4. Send this packet by selecting it and clicking the **Send selected packet**
   button. Click the received *Socket Create Response* packet and look for the
   assigned *Socket ID*.
5. Create another API frame with the following parameters:

       - Frame type:         0x47 - Socket SendTo
       - Frame ID:           02
       - Socket ID:          Use the ID received in the previous packet
       - Dest. address:      Use the IPv6 address printed in the REPL console
       - Dest. port:         12 34
       - Transmit options:   00
       - Payload:            Hello, Wi-SUN module!

6. Send this packet by selecting it and clicking the **Send selected packet**
   button.

When the data frame is sent, verify that a line with the sender address and the
data included in the **Payload** field is printed out in the REPL console:

    Data received from XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX >> Hello, Wi-SUN module!

Where *XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX* is the IPv6 address of the
sender module.

Supported platforms
-------------------

* Digi XBee Wi-SUN - minimum firmware version: B000

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
