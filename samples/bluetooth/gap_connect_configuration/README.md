Bluetooth Client Connection Configuration Sample Application
============================================================

This example demonstrates the usage of the XBee's BLE client features.
The example connects to a peripheral and discovers all of its services,
configures the timing parameters of the connection, and discovers
all of the peripheral's services again to demonstrate the effect of
changing the timing parameters.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A peripheral BLE device to connect to.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Find the BLE MAC address of the peripheral BLE device. It will be used
   later in the example.

Run
---

Before launching the application, update the `REMOTE_ADDRESS` and `address_type`
variables in `main.py` to match your BLE peripheral device.

Compile and launch the MicroPython application. It prints information to the
console, starting with the BLE MAC address it is connecting to:

    Attempting connection to: 00:0B:57:28:65:D0
    Connected

After connecting to the peripheral device, a GATT service discovery is
performed, and information about each discovered service is printed to the
console. Observe that this discovery completes quickly and there should be
little to no delay between each service.

Example output when connecting to a Silicon Labs Thunderboard device:

    Service (65541, UUID(0x1800))
    Service (393225, UUID(0x1801))
    Service (655378, UUID(0x180A))
    Service (1245206, UUID(0x180F))
    Service (1507359, UUID(0x1816))
    Service (2097193, UUID(0x1815))
    Service (2752560, UUID(0x181A))
    Service (3211315, UUID('D24C4F4E-17A7-4548-852C-ABF51127368B'))
    Service (3473407, UUID('A4E649F4-4BE5-11E5-885D-FEFF819CDC9F'))

After the first service discovery completes, the application configures the
timing parameters of the connection to be slower. Using a longer connection
interval will consume less power, as the BLE transmitter/receiver on both
devices will need to run less often.

After configuring the timing parameters, another GATT service discovery is
performed. Observe that this discovery is noticeably slower than the first
service discovery.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x15
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee3 Zigbee 3 - minimum firmware version: 100A
* Digi XBee3 802.15.4 - minimum firmware version: 200A
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 300A

License
-------

Copyright (c) 2020, Digi International Inc.

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
