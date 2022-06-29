FTP PUT Sample Application
===========================

This example demonstrates the usage of the 'uftp' library by giving an example
of how to connect with an FTP server to upload files.

This example waits until the module is connected to the cellular network. Then, 
it connects to an FTP server hosted on another computer. Once it is connected
the device will upload the '2b.txt' file to the server in the 'upload' folder
of the FTP server.

Requirements
------------

To run this example you will need:

* Once XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* An FTP server that is reachable by the XBee3 Cellular module.

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Change the parameters in the main.py file to connect to your server:

1. Change FTP_HOST to your server's IP address.
2. Change FTP_PORT to your server's listening port.
3. Change FTP_USER to the username you created.
4. Change FTP_PASS to the password that goes with the above username.
5. PATH_REMOTE_UPLOAD to the destination folder on the server.

Run
---

If you followed the steps above the program all you need to do is compile and
launch the application.

When the module has joined the cellular network, you should see the FTP
operations that take place with the FTP server:

     +----------------------------------------+
     | XBee Micropython FTP PUT Client Sample |
     +----------------------------------------+

    - Waiting for the module to connect to the cellular network... [OK]
    - Connecting to FTP server... [OK]
    - Uploading file 2b.txt... [OK]
       * Time taken: # seconds
    - Closing FTP connection... [OK]
    - Done

Required libraries
------------------
* uftp

Supported platforms
-------------------
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618

License
-------
Copyright (c) 2019, Digi International, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of 
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
