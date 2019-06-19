Relay Frames Button Sample Application
======================================

This example demonstrates the usage of the User Data Relay frames API by giving
an example of how to send a relay frame.

The example sends a User Data Relay message to the serial interface every time a
button of the XBee carrier board is pressed.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* The XCTU application (available at www.digi.com/xctu).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

The example is already configured, so all you need to do is build and launch
the project. Once the application is running (application header is displayed
in the XBee REPL console), execute the following steps to test it:

1. Disconnect the XBee REPL console.
2. Open XCTU application and add your XBee device to the list of radio modules.
3. Change the operating mode of the module to **API** by configuring the **AP**
   setting with **1**.
4. Switch to the **Consoles** working mode and open the serial connection with
   the module so you can see frames when they are received.
5. Press the **SW2** button (if you have an XBIB-U-DEV carrier board) or the
   **Comm DIO0** one (if you have an XBIB-C).
6. In the XCTU console, verify that a new **User Data Relay Output** frame is
   received with the following parameters:

       - Frame type:       AD (User Data Relay Output)
       - Interface:        02 (MicroPython)
       - RF data (ASCII):  Button pressed

When finished, restore the operating mode of the module to **MicroPython**
by configuring the **AP** setting with **4** using XCTU.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: 31010
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B

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