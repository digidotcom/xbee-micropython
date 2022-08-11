Bluetooth Client Connect and Discover Sample Application
========================================================

This example demonstrates the usage of the XBee's BLE client features.
The example connects to a peripheral and discovers all of its services,
characteristics and descriptors and prints them out.

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

Run
---

The example needs to be configured. Enter the BLE address and address type
of the peripheral device. After configuration, compile and launch the
application.
The sample starts out printing the remote BLE address:
`Attempting connection to: xx:xx:xx:xx:xx:xx`
Once the connection is made a `connected` message will be printed followed by
a printout of all of the services, characteristics and descriptors along with
their attribute values if applicable. The output may look like the following:
```
Service (65541, UUID(0x1800))
        Characteristic (3, UUID(0x2A00), 10)
         VALUE: b'Thunder React #26064'
        Characteristic (5, UUID(0x2A01), 2)
         VALUE: b'\x00'
Service (393225, UUID(0x1801))
        Characteristic (8, UUID(0x2A05), 32)
                Descriptor (9, UUID(0x2902))
                 VALUE: b'\x00\x00'
Service (655378, UUID(0x180A))
        Characteristic (12, UUID(0x2A29), 2)
         VALUE: b'Silicon Labs'
        Characteristic (14, UUID(0x2A24), 2)
         VALUE: b'RD-0057'
        Characteristic (16, UUID(0x2A26), 2)
         VALUE: b'1.0.0'
        Characteristic (18, UUID(0x2A23), 2)
         VALUE: b'\x00\x0bW\xff\xfe(e\xd0'
...
```
The printout above is a summary of the first three services of the Silicon Labs
Thunderboard. A quick breakdown of the output:
*  The first line is a service. A service tuple contains two elements. The
   first element being the services handle, which is used to reference the
   service to perform further operations it. The second element is the UUID.
   This is used to identify the service and its function. Something to note,
   certain UUIDs, per the BLE specification, are reserved for specific
   functioniality.
*  The next line is a characteric within the service. A characteristic tuple
   contains three elements. The first element being the characteric handle,
   which is used to reference the characteric to perform further operations on
   it. The second element is the UUID. This is used to identify the service and
   its function. Something to note, certain UUIDs, per the BLE specification,
   are reserved for specific functioniality. The third element is the
   characteric's properties. The properties describe how the characteric can be
   interacted with.
*  The third line contains the attribute value of the characteristic. In this
   sample, the attribute value is read and printed out if the characteristic
   has the PROP_READ property, marking it as readable.
*  Line eight contains a descriptor. A decriptor tuple contains two elements.
   The first element being the services handle, which is used to reference the
   descriptor to perform further operations it. The second element is the UUID.
   This is used to identify the descriptor and its function. Something to note,
   certain UUIDs, per the BLE specification, are reserved for specific
   functioniality.

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