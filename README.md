MicroPython Modules and Samples for XBee Devices
================================================

This project contains modules and sample code for use on XBee devices
with MicroPython.  [Digi International][Digi] manages the project on
GitHub as [xbee-micropython].

Digi has written some of the modules and samples, in addition to modifying
existing code to address differences between the XBee and other MicroPython
platforms.  This project includes code from [micropython-lib].

Please use GitHub to open issues and submit pull requests with improvements
or useful code to share with other users.

[Digi]: http://www.digi.com
[xbee-micropython]: https://github.com/digidotcom/xbee-micropython
[micropython-lib]: https://github.com/micropython/micropython-lib


Requirements
------------

The following XBee devices include support for MicroPython, but not
a file system or modules:

  * XBee and XBee3 Cellular (firmware *07 and later)
  * XBee3 Zigbee (firmware 1003 and later)

The following XBee devices include file system and module support:

  * XBee and XBee3 Cellular (firmware *0B and later)


Installation
------------

Clone this repository onto a PC connected to the serial port of your XBee
device.  Use the file manager of XCTU 6.4.0 (or later) on XBee/XBee3 Cellular
devices with *0B firmware (or later) to upload modules to the file system.

You may want to compile the modules after uploading (via `os.compile()`) or
on your computer via [`mpy-cross`][mpy-cross] and then upload the resultant
`.mpy` file.  Doing so eliminates `.py` parsing and compiling each time you
`import` a module into your program, which requires less space in
MicroPython's limited heap.

Most of the samples work with the MicroPython REPL's "paste mode":

  * Open a sample in your favorite text or Python editor.
  * Read the instructions in the opening comments of the sample.
  * Copy code to your clipboard.
  * In your serial terminal connected to the MicroPython REPL, press CTRL-E
    to enter Paste Mode.
  * Paste your code.
  * Press CTRL-D to execute the code.

[mpy-cross]: https://pypi.org/project/mpy-cross/


Organization
------------

Files in the `lib` directory mirror the structure you'd use when uploading
to the XBee device.  For example, `lib/umqtt/simple.py` is the correct
location for `import umqtt.simple` to work in your program.

Files in the `samples` directory are organized by feature or XBee device.
For example, `cellular` contains samples for XBee/XBee3 Cellular devices,
`zigbee` contains samples for XBee3 Zigbee devices, and `i2c` contains
samples for any XBee device with I2C support in MicroPython.


License
-------

This software is open-source software.  Copyright Digi International, 2018.

Most of the Source Code in the lib/ directory is covered by the MIT License
(see `LICENSE.txt`).  Individual files may contain alternate licensing,
depending on their origin.
