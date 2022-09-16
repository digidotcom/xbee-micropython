MQTT Publish Subscribe Sample Application
=========================================

This example uses the 'mqtt' library to connect with an MQTT server and
test both the subscribe and publish topic operations.

The example connects with the server and subscribes to the 'xbee_topic' topic.
Then, monitors the value of the `D0` button of the board and, whenever the
button is pressed, it publishes a message to the same topic it subscribed
before. This way, the subscribe and publish features are demonstrated in the
same sample.

The sample uses the publicly 'test.mosquitto.org' MQTT server.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).

Setup
-----

Make sure the hardware is set up correctly and the code is configured and
ready:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application.

When the module has joined the cellular network, you should see the output of
the sample. In this case it displays the result of the MQTT connection and
subscribing operations:

    - Waiting for the module to be connected to the cellular network... [OK]
    - Connecting to 'test.mosquitto.org'... [OK]
    - Subscribing to topic 'xbee_topic'... [OK]
    - Press 'D0' button to publish a message.

Now you need press the button corresponding to the 'D0'. By default the button
corresponds to **SW2** in XBIB-U-DEV carrier boards and **Comm DIO0** in XBIB-C
carrier boards.

Once the button is pressed, the application sends the message 'Test from XBee!'
to the topic 'xbee_topic' (the one it subscribed before). The application
should receive and print the message immediately:

    - Publishing message... [OK]
    - Message received!
       * xbee_topic: Test from XBee!

Press the button more times and verify every time the button is pressed a
message is published and received by the XBee module.

Required libraries
--------------------

* umqtt

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
