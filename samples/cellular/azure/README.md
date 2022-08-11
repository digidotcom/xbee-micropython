Microsoft Azure Sample Application
==============================

This example uses the 'mqtt' library to connect to an Azure IoT Hub and
publish data to a specific MQTT topic.

Requirements
------------

To run this example you need:

* One XBee3 Cellular module with MicroPython support and a micro SIM card
  inserted with Internet capabilities.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A Microsoft Azure account with your XBee Cellular device added as an IoT device.
  For more information on how to get started with Azure see the following documents:
  https://catalog.azureiotsolutions.com/docs?title=Azure/azure-iot-device-ecosystem/setup_iothub
  https://catalog.azureiotsolutions.com/docs?title=Azure/azure-iot-device-ecosystem/manage_iot_hub

Setup
-----

Make sure the hardware is set up correctly and the code is configured and
ready:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.
2. Configure the value of IoTHubConnectionString to create a valid
   Azure IoT Hub endpoint to connect to.

Run
---

Before executing the application you should open the Device Explorer application
and set it up to be able to receive messages from the device.
Follow these steps to do so:

1. Run **Device Explorer** and open the **Configuration** tab.
2. Copy the device's specific Connection String into the **IoT Hub Connection String** field.
3. Click over to the **Data** tab.

Now you can compile and launch the example to publish data to the configured
MQTT topic.

When the module has joined the cellular network, you should see the output of
the sample. In this case it displays the result of the Azure connection and
publishing operations:

    - "Network connected"
    - "Azure connected"
    - The information about the connection will be listed.
    - "Sending 10 messages to Azure..."

Verify that the **Data** tab displays the 10 messages that were sent from the XBee3

Required libraries
--------------------

* umqtt
* urllib

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11415
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x15
* Digi XBee 3 Global LTE-M/NB-IoT - minimum firmware version: 11618
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