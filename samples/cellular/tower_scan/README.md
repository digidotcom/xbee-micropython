Scan Cellular Towers Sample Application
=======================================

This example demonstrates the usage of the cellular API by giving an example of
how to scan for the surrounding cellular towers.

The example waits until the module is connected to the cellular network. After
that, it gathers info about the surrounding cellular towers.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

When the module has joined the cellular network, you should see the following
messages in the console containing information about nearby cells:

    Gathering cell information:
    {'signal': -77, 'cell_id': 8675309, 'area': 12345, 'mnc': '678', 'serving_cell': True, 'mcc': '910'}
    {'signal': -79, 'cell_id': 0, 'area': 12345, 'mnc': '678', 'serving_cell': False, 'mcc': '910'}
    {'signal': -79, 'cell_id': 0, 'area': 12345, 'mnc': '678', 'serving_cell': False, 'mcc': '910'}
    {'signal': -85, 'cell_id': 0, 'area': 12345, 'mnc': '678', 'serving_cell': False, 'mcc': '910'}
    
    Gathering tower information via a callback:
    {'signal': -77, 'cell_id': 8675309, 'area': 12345, 'mnc': '678', 'serving_cell': True, 'mcc': '910'}
    {'signal': -79, 'cell_id': 0, 'area': 17937, 'mnc': '410', 'serving_cell': False, 'mcc': '310'}
    {'signal': -79, 'cell_id': 0, 'area': 17937, 'mnc': '410', 'serving_cell': False, 'mcc': '310'}
    {'signal': -85, 'cell_id': 0, 'area': 17937, 'mnc': '410', 'serving_cell': False, 'mcc': '310'}
        


Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: x1A
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x1A
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: x1A
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: x1A
* Digi XBee 3 Global LTE Cat 1 - minimum firmware version: x1A
* Digi XBee 3 North America LTE Cat 1 - minimum firmware version: x1A

License
-------

Copyright (c) 2022, Digi International, Inc.

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