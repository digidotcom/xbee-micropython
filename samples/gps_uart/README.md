GPS UART Sample Application
===========================

This example demonstrates the usage of the UART API by giving an example
of how to read data from a GPS connected through the UART interface to
display the current position.

The example reads GPS data from the secondary UART of the module every 30
seconds, extracts the values of latitude and longitude from the read data
and displays them. 

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A GPS board.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Connect the secondary UART interface of the XBee device to the serial
   interface of the GPS board. See the following table for more information
   about the secondary UART pins layout on the XBee modules:

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

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

The application displays the values of latitude and longitude every 10 seconds:

    - Reading GPS data... [OK]
    - Latitude:
    - Longitude:
    --------------------------------
    - Reading GPS data... [OK]
    - Latitude:
    - Longitude:
    --------------------------------
    - Reading GPS data... [OK]
    - Latitude:
    - Longitude:
    --------------------------------

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: 31010
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