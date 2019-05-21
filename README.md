MicroPython Resources for XBee Devices
======================================

This project contains modules and sample code for use on XBee devices with
MicroPython. Digi has written some of the modules and samples, in addition to
modifying existing code to address differences between the XBee and other
MicroPython platforms. This project includes code from
[micropython-lib][micropython-lib].

The repository is used by the **Digi XBee MicroPython PyCharm Plugin** to
get the available samples, libraries platforms and stubs and facilitate the
process of creating and launching MicroPython applications in XBee devices.
This means that you don't need to clone it unless you want to contribute
with new content as the PyCharm plugin will handle all necessary resources
automatically.

We don't recommend you to do so, but you can still use the content of this
repository to create XBee MicroPython applications by your own (without using
the **Digi XBee MicroPython PyCharm Plugin**). In any case, you will find
information on how to get started with XBee and MicroPython in the
[Digi MicroPython Programming Guide][doc].

[Digi International][Digi] manages the project on GitHub as 
[xbee-micropython][xbee-micropython].


Requirements
------------

Modules and samples within the repository can be executed only in XBee
devices with MicroPython support. This is the list of current compatible
devices:

* Digi XBee3 Zigbee 3 (firmware 1006 and later)
* Digi XBee3 802.15.4 (firmware 2003 and later)
* Digi XBee3 DigiMesh 2.4 (firmware 3002 and later)
* Digi XBee3 Cellular LTE-M/NB-IoT (firmware 11410 and later)
* Digi XBee3 Cellular LTE Cat 1 (firmware 31010 and later)
* Digi XBee Cellular 3G (firmware 1130B and later)
* Digi XBee Cellular LTE Cat 1 (firmware 100B and later)


Organization
------------

The repository is structured in the following folders:

* **lib** - Files in the `lib/` directory mirror the structure you'd use when
  uploading to the XBee device.  For example, `lib/umqtt/simple.py` is the
  correct location for `import umqtt.simple` to work in your program.
* **platforms** - This folder contains the definition and images for the 
  Digi XBee products supporting MicroPython. This information is used by the
  **Digi XBee MicroPython PyCharm Plugin** to list the supported platforms.
* **samples** - Files in the `samples/` directory are organized by feature or
  XBee device. For example, `cellular` contains samples for XBee3 Cellular
  devices and `i2c` contains samples for any XBee device with I2C support in
  MicroPython.
* **typehints** - This folder contains the API definitions of the MicroPython
  modules available in the XBee devices. These definitions are used by the
  **Digi XBee MicroPython PyCharm Plugin** for syntax checking, code completion
  and refactoring.


Usage
-----

For information on how to get started with XBee and MicroPython, see the
[Digi MicroPython Programming Guide][doc].


How to Contribute
-----------------
The contributing guidelines are in the [CONTRIBUTING.md](CONTRIBUTING.md)
document.


License
-------

This software is open-source software. Copyright Digi International, 2018,
2019.

Samples within `samples/` folder, stub files in `typehints/` folder and most of
the source code in the `lib/` directory is covered by the
[MIT License](LICENSE.txt). Individual library files may contain alternate
licensing, depending on their origin.


[Digi]: http://www.digi.com
[xbee-micropython]: https://github.com/digidotcom/xbee-micropython
[doc]: https://www.digi.com/resources/documentation/digidocs/90002219
[micropython-lib]: https://github.com/micropython/micropython-lib