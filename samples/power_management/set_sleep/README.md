Set Sleep Sample Application
============================

This example demonstrates the usage of the Power Management API by giving an
example of how to control when the module sleeps.

When the sleep mode of the XBee device is configured to be managed from
MicroPytyhon code (**SM** is configured with **0** in Cellular devices or with
**6** in RF devices), it is possible to control when the module sleeps using
the `XBee().sleep_now()` and `XBee().wake_reason()` methods.

This example puts the module in sleep mode during 30 seconds when the 'User
button' (SW2 in XBIB-U-DEV board and COMM DIO0 in XBIB-C board) is pressed.
When the 30 seconds expire, module wakes and continues listening for a button
press.

**Note**: It is also possible to wake the module earlier by toggling the
**DTR** Pin or canceling the execution of the application.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Using XCTU configure the sleep mode (**SM**) of the module to be managed
   from MicroPython. Depending on the module you have, the value of the **SM**
   setting changes:

       Cellular devices:  SM = Normal [0]
       RF devices:        SM = MicroPython Sleep [6]

Run
---

The example is already configured, so all you need to do is to compile and
launch the application. As soon as the application is started it displays
the 2 available ways to test the functionality of the sample:

* **Option 1**
  1. Press 'User button' (SW2 in XBIB-U-DEV board and COMM DIO0 in
     XBIB-C board).
  2. Wait for the module to go to sleep (ON SLEEP LED turns off).
  3. Try to send a ^C (cancel) to exit example program while the module is
     sleeping. Nothing happens because the module does not listen REPL events
     while it sleeps.
  4. Let the program run until it wakes from 30 seconds sleep. Just after that
     time the module wakes and application displays the amount of ms the module
     was sleeping.
* **Option 2**:
  1. Press 'User button' (SW2 in XBIB-U-DEV board and COMM DIO0 in
     XBIB-C board).
  2. Just after pressing the button disconnect the XBee REPL Console (this is
     necessary to free the **DTR** pin of the module, which controls the early
     wake feature).
  3. Wait for the module to go to sleep (ON SLEEP LED turns off).
  4. While its sleeping, toggle DTR pin by connecting the XBee REPL console.
  5. Module wakes as soon as the connection with the REPL is established.
     Application displays the amount of ms the module was sleeping and an
     early wake notification.

Follow the steps of each option to verify they work properly.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618

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