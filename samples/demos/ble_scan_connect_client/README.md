BLE Scan and Connect (Client) Sample Application
================================================

This example is part of Digi's BLE Scan and Connect demo. It demonstrates how
an XBee device can use the Bluetooth interface to scan for nearby XBee devices
and securely connect to one of them.

The MicroPython application on the client side scans for nearby XBee BLE
devices and allows you to connect to any of them through an interactive
console. Once the client connects, it sends a "Ping" message to the server,
which responds with "Pong". The client then disconnects.

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

2. Apply the **BLE Scan and Connect** Quick Setup (Client role) to your XBee
   device using the 'Quick Setup' feature of XBee Studio. For further
   information on how to perform this task, refer to the XBee Studio user
   manual.

Run
---

The example is pre-configured, so all you need to do is build and launch the
project.

Follow these steps to test the application:
1. Wait for the application to scan for nearby devices and list them:
   ```
   - Discovered devices:
   +----+-------------------+------------------------------+
   | ID | Address           | Name                         |
   +----+-------------------+------------------------------+
   |  1 | 60:a4:23:5a:e2:0d | XBee Scan-And-Connect        |
   |  2 | c7:8a:e9:e7:96:40 |                              |
   |  3 | b0:38:e2:31:ae:80 | 1                            |
   |  4 | d0:cf:5e:fc:0e:4b | XBee3 Zigbee                 |
   +----+-------------------+------------------------------+
   ```
2. Enter the index of the XBee device you want to connect to and press <ENTER>. 
   Remember that it must be running the **Server** application of the demo,
   recognizable by the device name `XBee Scan-And-Connect`.
3. Enter the Bluetooth password of the device (1234 by default) and press
   <ENTER> to connect.
4. Once the client connects, it sends a 'Ping' message to the server, which
   responds with 'Pong':
   ```
   - Sending 'Ping'...
   - Sent! Waiting for 'Pong'...
   - 'Pong' received from the device!
   ```
5. Verify the client disconnects from the server.

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
