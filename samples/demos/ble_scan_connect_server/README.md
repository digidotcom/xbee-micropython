BLE Scan and Connect (Server) Sample Application
================================================

This example is part of Digi's BLE Scan and Connect demo. It demonstrates how
an XBee device can use the Bluetooth interface to scan for nearby XBee devices
and securely connect to one of them.

The MicroPython application on the server side listens for client connection
and disconnection events. When an XBee device running the client application
connects, it sends a "Ping" message to the server, which responds with "Pong".

**Note:** This demo is available as part of the 'BLE Scan and Connect' Quick
Setup in **XBee Studio**. For optimal functionality, we recommend flashing the
application onto the XBee device using the Quick Setup feature of XBee Studio.
This approach ensures that all necessary configuration parameters for the XBee
device are correctly set up. Direct flashing from PyCharm may omit these
crucial configuration steps.

Requirements
------------

To run this example you need:

* One XBee radio module with Bluetooth and MicroPython support.
* One **XBIB-C** carrier board for the radio module.
* XBee Studio application, version 6.4.2 or newer
  (available at https://www.digi.com/xbee-studio).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee radio module into the XBee adapter of the XBIB-C board and
   connect it to your computer's USB port.

2. Apply the **BLE Scan and Connect** Quick Setup (Server role) to your XBee 
   device using the 'Quick Setup' feature of XBee Studio. For further
   information on how to perform this task, refer to the XBee Studio user
   manual.

Run
---

The example is pre-configured, so all you need to do is build and launch the
project.

Once the application is executed, it waits for other XBee devices to connect.
When an XBee device running the **client** application of the demo connects,
the application displays information about the connection event:

```
- Client connected!
```
The client sends a "Ping" message, and the server responds with a "Pong":

```
- 'Ping' received from client. Sending 'Pong'...'
- 'Pong' sent!'
```

When the client disconnects, the application displays this as well:

```
- Client disconnected!
```

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2004
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3003
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee BLU - minimum firmware version: 4000

License
-------

Copyright (c) 2024,2025, Digi International, Inc.

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
