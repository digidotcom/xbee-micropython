Bluetooth Pairing Sample Application
============================================================

This example demonstrates performing pairing to secure the BLE
connection to another BLE device.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A peripheral BLE device to connect to which supports pairing.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Find the BLE MAC address of the peripheral BLE device. It will be
   used later in the example. The peripheral must support pairing with
   MITM support. If it does not, edit the `ble.config` like to remove
   that flag. If the flag is removed Just Works pairing may occur with
   no callbacks.

Run
---

Before launching the application, update the `REMOTE_ADDRESS` and `address_type`
variables in `main.py` to match your BLE peripheral device.

Compile and launch the MicroPython application. It prints information to the
console.

After connecting to the peripheral device, it will delay for a short
period of time and then one of the `io_callback` methods will be
called. The specific callback will depend on the capabilities of the
BLE peripheral being paired against.

Example session when connecting to a device with a keyboard and display.

    Loading /flash/main.mpy...
    Running bytecode...
    Connecting
    Connected
    Wait for a bit before securing
    Securing
    Sleep forever
    The passkey is 520308
    Is this correct (y/n): y
    Secured

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11416
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x16
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee BLU - minimum firmware version: 4000

License
-------

Copyright (c) 2020-2024, Digi International Inc.

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
