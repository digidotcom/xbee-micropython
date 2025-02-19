Idle Radio Polling Sample Application
======================================

The `idle_radio()` function allows the MicroPython application to put the radio
into an idle state, reducing current draw but preventing the radio from
receiving transmissions (see the *Idle Radio* sample application).

Zigbee networks allow a little bit more flexibility in this idle state. This
state is actually the default state for end devices--whenever a message is sent
to an end device it is held by a router until the end device enables the radio
and polls for new messages. Normally this process happens automatically, but the
`idle_radio()` function disables this polling, transferring the responsibility
to do so to the application (using the `poll_now()` function).

In this example an end device sleeps, waking every 5 seconds to take a sample
from a sensor. Every 4 times the device wakes, it sends a message to the
coordinator with the last 4 samples. When the device sends the samples it also
polls for messages, allowing it to receive any messages that were sent while it
was sleeping/idling.


Requirements
------------

To run this example you need:

* Two XBee 3 Zigbee modules with MicroPython support.
* Carrier boards for each radio module (XBIB-U-DEV or XBIB-C board).
* Digi XBee Studio (available at www.digi.com/xbee-studio).


Setup
-----

Set up a network with two modules:

* One module is the *coordinator*, which will receive the sensor readings.
  Configure the following AT commands on the coordinator:
  * Set **AP** to 1 to enable API mode, making it easier to see transmissions
    from the client using XBee Studio.
  * Set **CE** to 1 to make the device a coordinator.
  * Set **SP** to 0x7D0 (20 seconds). This indicates how long end devices will
    go between polls, and is used to determine the timeout for transmissions.

* The other module is the *end device* that will run the sample
  application. Configure the following AT commands on the end device:
  *  Set **SM** to 6 on the end device to allow MicroPython to control sleep.

Allow the end device to join the network (wait until the associate LED on the
end device is blinking and querying the **AI** command returns 0).


Run
---

Open the coordinator in XBee Studio's console so you can observe the frames
output by the module, then compile and launch the application on the sensor
module.

Observe the output from MicroPython on the sensor module. The module will wake
every 5 seconds, take a reading, and go back to sleep. Every 4th time the module
wakes, it will send the last 4 samples to the coordinator. After 12 samples, the
example will finish.

The coordinator (or any other device on the network) can send a transmission to
the end device at any time, and it will be received the next time the end device
polls for data. It is recommended to send transmissions to the end device with
transmit option bit six (0x40) set, to enable the extended timeout.

Supported platforms
-------------------

* Digi XBee3 Zigbee 3 - minimum firmware version: 100B

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
