AWS Temperature Sensor Sample Application
=========================================

This sample uses the 'mqtt' and 'hdc1080' libraries to monitor the temperature
of an HDC1080 sensor (embedded in the XBIB-C development board) through AWS.  

The example connects with AWS using the SSL certificates and publishes the
temperature of the sensor periodically to a specific MQTT topic. If the 
temperature exceeds or is below a configured threshold, the sample publishes a
message to an alarm topic. 

The temperature sample ratio and threshold can be configured publishing the
desired values to the configuration topic. You can use the AWS IoT console to
monitor the temperature and alarm topics as well as to configure the
temperature sample ratio and threshold values.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One XBIB-C carrier board (includes an HDC1080 I2C Temp & Humidity Sensor).
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

Run
---

Before executing the application you should open the AWS IoT console and
subscribe the temperature topic to see the temperature values sent by the
application. Follow these steps to do so:

1. Sign in to the **AWS Management Console** and open the **AWS IoT console**.
2. Click the **Test** option from the left menu to open the MQTT client panel.
3. Write the name of the temperature topic ('sample/temp' by default) in the
   **Subscription topic** field.
4. Click **Subscribe topic** button to start monitoring messages sent to that
   topic.

Now you can compile and launch the example to start reporting the temperature
to AWS. 

When the module has joined the cellular network, you should see the output of
the sample. In this case it displays the result of the AWS connection and 
subscribing operations. It also starts reporting temperature values to AWS:

    - Waiting for the module to be connected to the cellular network... [OK] 
    - Connecting to AWS... [OK]
    - Subscribing to topic 'sample/update'... [OK]
    - Publishing alarm (high temperature)... [OK]
    - Publishing temperature... [OK]
    - Publishing temperature... [OK]
    - Publishing temperature... [OK]

**Note**: As soon as the first temperature measure is taken, the application
will detect that it exceeds or is below the threshold, so the application will
publish to the 'sample/alarm' topic before publishing to the temperature one.

Verify that the MQTT client panel displays the message sent from the XBee3 
Cellular device to the 'sample/temp' topic and they have the following format:

    {
      "temp": "85.07935"
    }

Now, you can change the wait timer and threshold configurations from AWS. To do
so, follow these steps:

1. Once in the MQTT client panel, click the **Publish to a topic** option.
2. Write 'sample/update' in the **Specify a topic and a message...** field.
3. Fill the message content with:

       {
         "threshold_temp": 70,
         "wait_timer": 15
       }
4. Click **Publish to topic** button to publish the message.  

Just after publishing the message, the application should receive it. Verify
that the output of the application displays it and configuration is updated
(temperature is now reported every 15 seconds):

    - Message received!
       * Updated threshold to '70.0'
       * Updated wait timer to '15'

Required libraries
--------------------

* umqtt

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