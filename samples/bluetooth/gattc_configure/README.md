Bluetooth Client Read and Write Sample Application
==================================================

This example demonstrates the usage of the XBee's BLE client indicate/notify
feature.
The example connects to a Silicon Labs Thunderboard and configures it to
send the XBee information about the state of the on-board buttons.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A Silicon Labs [Thunderboard React](https://www.silabs.com/products/development-tools/thunderboard/thunderboard-react-kit-sensor-cloud-connectivity)

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Turn on the Thunderboard and press button SW-0 to make it connectable by
   pressing the SW-0 button. LED-B will begin to blink indicating that the
   Thunderboard is ready for a connection.

Run
---

The example needs to be configured. Enter the BLE address of the
Thunderboard React. The sample makes a connection to the
Thunderboard and discover its I/O characteristics. It then configures the
Thunderboard to send a notification whenever either one of its buttons are
pressed or released.
After configuration, compile and launch the application.
The sample starts out printing the target BLE address:
`Attempting connection to: xx:xx:xx:xx:xx:xx`
Once the connection is made a `connected` message will be printed.
Following that, anytime a button is pressed on the Thunderboard, a
corresponding message will be printed.
For example:
```
Button SW-0 was pressed
Button SW-0 was released
Button SW-1 was pressed
Button SW-1 was released
```

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x15
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618
* Digi XBee3 Zigbee 3 - minimum firmware version: 100A
* Digi XBee3 802.15.4 - minimum firmware version: 200A
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 300A

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