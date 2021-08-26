AWS Subscribe Sample Application
================================

This example uses the 'mqtt' library to connect with AWS using the SSL
certificates and subscribe to a specific MQTT topic. Then, the sample prints
any data received in that topic.

You can use the AWS IoT console to send data to a specific topic.

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
3. The policy attached to the SSL certificates must allow for publishing,
   subscribing, connecting, and receiving data.
4. Configure the value of constants `HOST`, `REGION` needed to create a valid
   AWS endpoint to connect to.
5. The loop that checks for incoming traffic will end after it receives
   `msg_limit` messages (2 by default).

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

When the module has joined the cellular network, you should see the output of
the sample. In this case it displays the result of the AWS connection and
subscribing operations:

    - Waiting for the module to be connected to the cellular network... [OK]
    - Connecting to AWS... [OK]
    - Subscribing to topic 'sample/xbee'... [OK]
    - Waiting for messages...

Now you need to publish a message to the subscribed topic. Follow these steps
to do so:

1. Sign in to the **AWS Management Console** and open the **AWS IoT console**.
2. Click the **Test** option from the left menu to open the MQTT client panel.
3. Click the **Publish to a topic** option from the left menu of the MQTT
   client panel.
4. Write the name of the topic you want to publish to ('sample/xbee' by
   default) in the **Specify a topic and a message...** field. Optionally,
   change the message to be sent to the topic with 'Hello XBee!'.
5. Click **Publish to topic** button to publish the message.

Just after publishing the message, the application should receive it. Verify
that the output of the application displays it:

    - Message received!
       * sample/xbee: Hello XBee!

Repeat the publish operation with a different message. The application displays
the new message and, as the number of messages received has reached the limit,
the application finishes:

    - Message received!
       * sample/xbee: Hello again XBee!
    - Done

Required libraries
--------------------

* umqtt

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