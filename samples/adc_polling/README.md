ADC Polling Sample Application
==============================

This example demonstrates the usage of the I/O pins API by giving an example
of how to initialize an I/O pin to read analog values.

The example configures an IO line of the XBee device as ADC. Then, it
periodically reads its value and prints it.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* One voltage variable peripheral (for example a potentiometer).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. If using XBee 3 Zigbee, DigiMesh, or 802.15.4, ensure that the **AV** command
   (Analog Voltage Reference) is configured to an input range which matches your
   voltage source:

     * 0 = 1.25 V
     * 1 = 2.5 V
     * 2 = VDD

   If using XBee Cellular or XBee 3 Cellular, the analog reference voltage is 2.5V.
3. Connect a voltage variable source to the pin configured as ADC (light
   sensor, temperature sensor, etc). For testing purposes we recommend using a
   potentiometer. Follow these steps to connect it:

     * Isolate the pin configured as ADC so it does not use the functionality
       provided by the board.
     * Connect the potentiometer to VCC, to the pin configured as ADC and to
       GND. Something similar to this:

            O   VCC
            |
            <
            >___ XBee device pin (ADC)
            >
            <
            |
           ---
            -   GND

     * If you prefer not to isolate the pin of the board and not to use a
       potentiometer, you can still test the example using one of the user
       buttons from the carrier board. In this case the analog value will
       change from all to nothing depending on the status of the button. This
       step depends on the carrier board you are using:

       * XBIB-U-DEV board:

         * The example is already configured to use this carrier board. The
           ADC pin configured is `D3` (AD3/DIO3), which corresponds to the
           SW5 user button of the board. No further changes are necessary.

       * XBIB-C board:

         * If you are using the XBIB-C, update the `ADC_PIN_ID` variable to
           `D0` (AD0/DIO0), which corresponds to the Comm DIO0 user button of
           the board.

   **NOTE**: It is recommended to verify the capabilities of the pins used in
   the example as well as the electrical characteristics in the product manual
   of your XBee Device to ensure that everything is configured correctly.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

To test the functionality, follow these steps:

1. Rotate the potentiometer or press and release the corresponding user button
   in case you are not using a potentiometer.
2. Verify that the value displayed in the XBee REPL console is changing:

       - ADC value: 4095
       - ADC value: 4095
       - ADC value: 2

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B

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
