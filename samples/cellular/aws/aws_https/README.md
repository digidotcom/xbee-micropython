AWS HTTPS Sample Application
============================

This example tests that AWS certificates loaded in the XBee module allows you
to create an SSL connection with AWS to send HTTP requests.

The example connects with AWS using the SSL certificates and requests the
shadow information of a thing sending an HTTP request, then prints it.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* An AWS account with your XBee Cellular device added as a Thing. For more
  information on how to get started with AWS see
  [Connecting an XBee Cellular device to AWS IoT](../) guide.

Setup
-----

Make sure the hardware is set up correctly and the code is configured and
ready:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Ensure that the AWS SSL certificate files are in the `/flash/cert` directory
   on the XBee filesystem.
   * `SSL_PARAMS` constant within the code shows which SSL parameters are
     required, and gives examples for referencing the files.
   * If needed, replace the file paths to match the certificates you're
     using.
3. The policy attached to the SSL certificates must allow for connecting,
   and getting a **Thing's Shadow**
4. Configure the value of constants `HOST`, `REGION`, and `THING_NAME` needed
   to create a valid AWS endpoint to connect to.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

When the module has joined the cellular network, you should see the output of
the AWS operations executed by the module such as the connection, as well as the shadow  :

    - Waiting for the module to be connected to the cellular network... [OK]
    - Connecting to AWS... [OK]
    - Sending shadow request for thing '<YOUR_THING_NAME>'... [OK]
    - Waiting for data... [OK]
    - Received shadow for thing '<YOUR_THING_NAME>':
    ----------------------------------------------------------------
    HTTP/1.1 200 OK
    content-type: application/json
    content-length: 61
    date: Thu, 09 May 2019 08:08:51 GMT
    x-amzn-RequestId: 53ff83f2-0577-85f1-0235-4885cfcd86fe
    connection: keep-alive

    {"state":{},"metadata":{},"version":1,"timestamp":1557389331}
    ----------------------------------------------------------------
    - Done

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
