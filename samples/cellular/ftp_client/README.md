FTP Client Sample Application
=============================

This example demonstrates the usage of the 'uftp' library by giving an example
of how to connect with an FTP server to download and upload files.

The example waits until the module is connected to the cellular network. After
that, it connects with a generic speed test FTP server, downloads the remote 
file '1KB.zip' and uploads the local file '2b.txt' in the 'upload' folder of
the FTP server. 

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
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

When the module has joined the cellular network, you should see the FTP
operations that take place with the FTP server:

    - Waiting for the module to be connected to the cellular network... [OK]
    - Connecting to FTP server... [OK]
    - Retrieving file '1KB.zip' (1024 bytes)... [OK]
       * Time taken: 6 seconds
    - Uploading file '2b.txt'... [OK]
       * Time taken: 5 seconds
    - Closing FTP connection... [OK]
    - Done


You can change the values of the FTP constants and file names to connect with
a different FTP server and transfer other files.

Required libraries
--------------------

* uftp

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