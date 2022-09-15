PWM Duty Cycle Sample Application
=================================

This example demonstrates the usage of the PWM API by giving an example of
how to control the duty cycle of the PWM channel of the XBee device.

The example waits for a button press to start the duty cycle sequence. This
sequence increases gradually the value of the duty cycle to its maximum and
then decreases it gradually to its minimum.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* One PWM peripheral (RGB LED, buzzer, DC servo, etc.)

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the PWM device to the `RSSI PWM/DIO10` pin of the XBee module. The
   way to connect it changes depending on the carrier board you have:

   * XBIB-U-DEV board:

     * In XBIB-U-DEV boards the `RSSI PWM/DIO10` is already connected to the
       RSSI LEDs tower of the board. So, you don't need to connect anything in
       order to test the sample.

   * XBIB-C board:

     * Isolate the `RSSI PWM/DIO10` pin so it does not use the
       functionality provided by the board.
     * Connect the PWM device to the `RSSI PWM/DIO10` pin and to GND.

   **NOTE**: It is recommended to verify the capabilities of the pins used in
   the example as well as the electrical characteristics in the product manual
   of your XBee Device to ensure that everything is configured correctly.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application. Follow these steps to test the sample:

1. Press the start button (**SW2** in XBIB-U-DEV carrier board or **Comm DIO0**
   in XBIB-C carrier board) to start the duty cycle sequence. This sequence
   increases gradually the value of the duty cycle to its maximum and then
   decreases it gradually to its minimum.
2. Verify that the output of the peripheral varies during the sequence. In the
   case of the RSSI LEDs tower of the XBIB-U-DEV board, LEDs should start
   turning on gradually from the bottom to the top and then turning off from
   the top to the bottom.

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
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: 11519
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: 41519

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
