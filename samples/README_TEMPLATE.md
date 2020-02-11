<Sample title> Sample Application
======================================

> REQUIRED
> 
> Brief description of the sample.
> 
> Example:

This example demonstrates the usage of the I/O pins API by giving an example
of how to initialize and manage the status of an I/O pin.

The example toggles the status of an LED every second.

Requirements
------------

> REQUIRED
> 
> This section lists the hardware and software components needed to run the
> sample application. Computer and PyCharm components are omitted.
>
> Example: 

To run this example you need:

* One XBee3 radio module with MicroPython support.
* One carrier board for the radio module (XBIB-U-DEV or XBIB-C board).
* One standalone HDC1080 humidity and temperature sensor (not necessary if you
  are using an XBIB-C carrier board).

Setup
-----

> REQUIRED
> 
> Describe here all the steps needed to connect and configure the hardware
> needed by the sample as well as any software configuration or changes in
> the code required prior to run the sample.
>
> Example:

Make sure the hardware is set up correctly:

1. Plug the XBee3 radio module into the XBee adapter and connect it to your
   computer's USB port.

Run
---

> REQUIRED
> 
> In this section you must describe the steps needed to launch the sample and
> verify it is working properly.
>
> Example:

The example is already configured, so all you need to do is to compile and
launch the application.

Verify the LED corresponding to the configured pin (`ON/SLEEP/DIO9`) in the
carrier board starts blinking (toggles its status every second). Every time
the LED toggles, the application indicates it through the XBee REPL console:

    - LED ON
    - LED OFF
    - LED ON
    - LED OFF

Required libraries
--------------------

> OPTIONAL
>
> This section is used by the **Digi XBee MicroPython PyCharm Plugin** to
> import the libraries required by the sample application once the sample is
> imported. The content of the section is a list with the ID of required
> libraries from the `lib` directory. ID must equal the name of the library
> folder.
> 
> You can remove this section if the sample does not require any library.
> 
> Example:

* uftp

Supported platforms
-------------------

> REQUIRED
> 
> This section contains a list with the ID of XBee platforms compatible with
> the sample and the minimum firmware required by each one. If you don't know
> what's the minimum firmware version required, leave it with the default one
> listed here. You can take the ID of the platforms from the
> [platforms definition file](../platforms/platforms.xml).
> 
> Example:
   
* Digi XBee3 Zigbee 3 - minimum firmware version: 1006
* Digi XBee3 802.15.4 - minimum firmware version: 2003
* Digi XBee3 DigiMesh 2.4 - minimum firmware version: 3002
* Digi XBee3 Cellular LTE-M/NB-IoT - minimum firmware version: 11410
* Digi XBee3 Cellular LTE Cat 1 - minimum firmware version: x10
* Digi XBee Cellular 3G - minimum firmware version: 1130B
* Digi XBee Cellular LTE Cat 1 - minimum firmware version: 100B

License
-------

> REQUIRED
> 
> Attach here the license of the sample. Samples offered by Digi are covered
> by the [MIT license](https://en.wikipedia.org/wiki/MIT_License), so we 
> recommend you to use the same one changing the year and copyright holders
> as needed. 
> 
> Example:

Copyright (c) 2020, Digi International, Inc.

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
