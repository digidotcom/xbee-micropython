Idle Radio Sample Application
======================================

By default, whenever an XBee module is awake, the radio is active and available
to receive RF transmissions. If the application does not always need to receive
transmissions while it is awake (for example, if a MicroPython application is
waking only to sample some data and go back to sleep), the radio can be disabled
to save power.

In this example an end device sleeps, waking every 5 seconds to take a sample
from a sensor. Every 4 times the device wakes, it sends a message to an
aggregator with the last 4 samples. When the device isn't actively transmitting
or receiving, the radio is kept in the idle state to minimize current draw.


**Note** if using XBee 3 Zigbee: This sample application will run, but on a
Zigbee network additional functionality is available to further reduce power
usage. See the *Idle Radio Polling* sample application for more information.


Requirements
------------

To run this example you need:

* Two XBee 3 modules with MicroPython support.
* Carrier boards for each radio module (XBIB-U-DEV or XBIB-C board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).


Setup
-----

Set up a network with two modules:

* One module is the *aggregator*, which will receive the sensor readings.

* The other module is the *sensor module* that will run the sample
  application. Configure the following AT commands:
  * **SM** 6
  * **DH**/**DL**: Set to the 64-bit address (**SH**/**SL**) of the aggregator.


Run
---

Open the aggregator in XBee Studio's console so you can observe the frames
output by the module, then compile and launch the application on the sensor
module.

Observe the output from MicroPython on the sensor module. The module will wake
every 5 seconds, take a reading, and go back to sleep. Every 4th time the module
wakes, it will send the last 4 samples to the aggregator. After 12 samples, the
example will finish.

To send a message to the sensor module, the aggregator will need to wait until
it receives a packet from the sensor module, then send its message during the 1
second that the sensor module application activates the radio after sending its
samples.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 100B
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 300B

License
-------

Copyright (c) 2020-2025, Digi International, Inc.

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
