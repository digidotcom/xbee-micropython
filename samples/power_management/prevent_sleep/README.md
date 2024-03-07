Prevent Sleep Sample Application
================================

This example demonstrates the usage of the Power Management API by giving an
example of how to prevent the module to go to sleep from MicroPython code.

When the XBee device is configured to sleep (**SM** is different than **0** or
**6**) and it enters sleep mode, any MicroPython code currently executing is
suspended until the device comes out of sleep. When the XBee device comes out
of sleep mode, MicroPython execution continues where it left off.

This example demonstrates how to force the device to stay awake during critical
operations using the `XBee().wake_lock`. For that purpose the example exposes 2
counters of 10 units, one that can be interrupted and other that cannot because
is being executed inside the `wake_lock`.

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
2. Using XCTU configure the sleep options of the module to **sleep for 10
   seconds** and **wake for 4 seconds**. To do so configure the following
   parameters:

       SM: Cyclic Sleep [4] - Wakes on timer expiration
       SP: 3E8              - 10 seconds
       ST: FA0              - 4 seconds
       SO: 2                - Always wake for ST time

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

**Note**: Before discovering the device or launching the application you must
either **reset** the module or **press the commissioning** button to make sure
the module is not sleeping to communicate with it.

While the application is running verify that the `interruptable counter` is
interrupted when the module goes to sleep (up to 3 times until the counter
reaches 10) but the `not interruptable counter` is never interrupted although
the mode wants to go to sleep.

    ...
    --------------------
    Interruptable counter: 1
    (Module goes to sleep here for 10 seconds)
    Interruptable counter: 2
    Interruptable counter: 3
    Interruptable counter: 4
    Interruptable counter: 5
    (Module goes to sleep here for 10 seconds)
    Interruptable counter: 6
    Interruptable counter: 7
    Interruptable counter: 8
    Interruptable counter: 9
    (Module goes to sleep here for 10 seconds)
    Interruptable counter: 10
    --------------------
    Not interruptable counter: 1
    Not interruptable counter: 2
    Not interruptable counter: 3
    Not interruptable counter: 4
    Not interruptable counter: 5
    Not interruptable counter: 6
    Not interruptable counter: 7
    Not interruptable counter: 8
    Not interruptable counter: 9
    Not interruptable counter: 10
    --------------------
    Interruptable counter: 1
    (Module goes to sleep here for 10 seconds)
    Interruptable counter: 2
    Interruptable counter: 3
    Interruptable counter: 4
    Interruptable counter: 5
    (Module goes to sleep here for 10 seconds)
    Interruptable counter: 6
    ...

After you've finished testing the example remember to restore the sleep options
of the module to their default values using XCTU.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519
* Digi XBee BLU - minimum firmware version: 4000

License
-------

Copyright (c) 2019-2024, Digi International, Inc.

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
