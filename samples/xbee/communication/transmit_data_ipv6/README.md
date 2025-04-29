Transmit Data IPv6 Sample Application
=====================================

This example demonstrates the usage of the socket IPv6 API by giving an example
of how to transmit data to other XBee device in the same Wi-SUN network.

Requirements
------------

To run this example you need:

* Two XBee Wi-SUN modules.
* Two carrier boards for the radio modules (XBIB-U-DEV or XBIB-C board).
* One Wi-SUN border router.
* Digi XBee Studio v1.2.0 or higher (available at www.digi.com/xbee-studio).

Setup
-----

The XBee module that runs this sample will act as sender, while the other
one will act as receiver.

Make sure the hardware is set up correctly:

1. Plug the XBee radio modules into the XBee adapters and connect them to your
   computer's USB ports.
2. Ensure that the receiver module is in API mode and both modules are on the
   same Wi-SUN network.
3. Find the IPv6 address of the receiver module in XBee Studio. It will be used
   later in the example.

Run
---

Before launching the application, you need to set up XBee Studio to see the data
received by the receiver module. Follow these steps to do so:

1. Launch XBee Studio.
2. Wait until the receiver XBee module is discovered and click on it.
3. In the left menu, go to the **XBee Console** page and open the connection.
4. Create and add an API frame to the **Send data** list with the following
   parameters:

       - Frame type:    0x40 - Socket Create
       - Frame ID:      01
       - Protocol:      UDP [00]

5. Send this packet by selecting it and clicking the **Send selected packet**
   button. Click the received *Socket Create Response* packet and look for the
   assigned *Socket ID*.
6. Create another API frame with the following parameters:

       - Frame type:    0x46 - Socket Bind/Listen
       - Frame ID:      02
       - Socket ID:     Use the ID received in the previous packet
       - Source port:   12 34

7. Send this packet by selecting it and clicking the **Send selected packet**
   button.

Fill the **TARGET_IPV6_ADDR** constant in the MicroPython application with the
IPv6 address of the receiver module. Finally, compile and launch the MicroPython
application. It prints out the status of the operation in the console:

    Sending data to XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX >> Hello, Wi-SUN module!
    Data sent successfully

Verify that a new **Socket Receive From: IPv6** packet has been received in the
XBee Studio console. Select it and review the details, some of them similar to:

    - Frame type:             CB (Socket Receive From: IPv6)
    - Source address:         The XBee sender's IPv6 address
    - Payload data (ASCII):   Hello, Wi-SUN module!

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
