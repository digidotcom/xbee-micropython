Read Device Request Sample Application
======================================

This example demonstrates the usage of the Digi Remote Manager API by giving
an example of how to poll for device requests from your Digi Remote Manager
account to toggle an LED.

The example reads device requests from your Digi Remote Manager account using
the `device_request_receive()` method and, when a device request containing the
text **TOGGLE_LED** is received, it toggles the status of the
**ON/SLEEP/DIO9** LED.

Due to the nature of the project (receive a device request at any time), the
XBee3 cellular device should remain connected to Digi Remote manager through
TCP. This is, the SM/UDP feature should be disabled.

Requirements
------------

To run this example you need:

* One XBee3 cellular module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* A Digi Remote Manager account with the XBee3 cellular device registered in.
* The XCTU application (available at www.digi.com/xctu).

Setup
-----

Make sure the hardware is set up correctly:

1. Plug the XBee3 cellular module into the XBee adapter and connect it to your
   computer's USB port.
2. Make sure the XBee3 cellular device is connected to Internet. To do so,
   verify that the Connection status LED is blinking or the value of the
   **AI** parameter is **0**.
3. Using XCTU, enable the *"Always remain connected to Digi Remote Manager
   through TCP"* feature by setting the **MO** parameter to **7**. This way The
   device remains connected to Digi Remote Manager while you test the sample.
4. Make sure the XBee3 cellular device is connected to Digi Remote Manager. To
   do so, verify that the value of the **RI** parameter is **0**.

Run
---

The example is already configured, so all you need to do is to compile and
launch the application. When executed, it starts reading device requests from
your Digi Remote Manager account.

Follow these steps to test the application:

1. Log in your Digi Remote Manager account using your credentials:
   https://remotemanager.digi.com/login.do
2. Within the Digi Remote Manager platfotm, go to the **Documentation** Tab
   and then select the **API Explorer** option.
3. Click the **SCI Targets** button and choose your XBee3 Cellular device from
   the drop-down list. Then, click **Add** to add it to the list of target
   devices and click **OK** to apply.
4. Click the **Examples** button and select **SCI > Data Service >
   Send Request** to fill the code box with a device request example.
5. Change the value of the attribute **target_name** to **micropython** and
   replace the **my payload string** text with **TOGGLE LED**. The request
   should look similar to:

       <sci_request version="1.0">
         <data_service>
           <targets>
             <device id="XXXXXXXX-XXXXXXXX-XXXXXXXX-XXXXXXXX"/>
           </targets>
           <requests>
             <device_request target_name="micropython">
               TOGGLE LED
             </device_request>
           </requests>
         </data_service>
       </sci_request>

6. Click **Send** button (fill the account credentials if asked to do so) to
   send the device request to the XBee3 Cellular device.
7. The example should have received the device request. Verify that the
   **ON/SLEEP/DIO9 LED** has toggled its status and the answer to the device
   request sent is **LED TOGGLED**.

When finished testing the example, you should restore the status of the
*"Always remain connected to Digi Remote Manager through TCP"* feature (**MO**
parameter) to the value it had before running the example.

Supported platforms
-------------------

* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11411
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x11
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
