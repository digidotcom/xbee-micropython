UART Echo Sample Application
============================

This example demonstrates the usage of the UART API by giving an example of
how to read data from the secondary serial port of the XBee module and write
it back.

The example sends out to the serial port an echo of the received data.

Requirements
------------

To run this example you need:

* One XBee3 radio module with MicroPython and secondary UART support. At the
  moment only XBee Cellular modules support secondary UART feature.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A serial terminal application installed in your computer.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the secondary UART interface of the XBee device to one serial port
   of your computer. See the following table for more information about the
   secondary UART pins layout on the XBee modules:

           +--------+------------+----------+-----------+-----------+
           | Signal | Pin ID     | Pin # TH | Pin # SMT | Pin # MMT |
           +--------+------------+----------+-----------+-----------+
           | TX     | DIO4       | 11       | 24        | 23        |
           +--------+------------+----------+-----------+-----------+
           | RX     | DIO12      | 4        | 5         | 5         |
           +--------+------------+----------+-----------+-----------+
           | RTS    | AD2/DIO2   | 18       | 31        | 29        |
           +--------+------------+----------+-----------+-----------+
           | CTS    | AD3/DIO3   | 17       | 30        | 28        |
           +--------+------------+----------+-----------+-----------+

3. This demo requires a serial console terminal in order to see the echo from
   the XBee module. Configure the terminal and open a serial connection with
   the XBee module.

   The baud rate of the serial console must be **9600**, as the sample will
   configure the UART of the XBee module with that baud rate.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

While it is running, type some data in the serial console terminal you
configured previously. You should see the echo from the XBee module
corresponding to the data you have written.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x18
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
