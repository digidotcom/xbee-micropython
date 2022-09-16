Bluetooth Client Read and Write Sample Application
==================================================

This example demonstrates usage of the XBee's BLE client read/write feature.
The example connects to a Silicon Labs Thunderboard and reads its temperature.
The example also toggles the LED every couple seconds.

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
Thunderboard and discover its temperature and IO characteristics.
Using these characteristics, the sample reads the temperature
and toggle the LEDs on the Thunderboard on and off.
After configuration, compile and launch the application.
The sample starts out printing the remote BLE address:
`Attempting connection to: xx:xx:xx:xx:xx:xx`
Once the connection is made a `connected` message will be printed followed by
the temperature, which is updated every couple of seconds.
The Thunderboard LEDs will also be toggled every couple of seconds.
In order to exit this sample, issue a keyboard interrupt (Ctrl + C) in the
MicroPython REPL.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x15
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
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
