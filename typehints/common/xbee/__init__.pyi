# Copyright (c) 2019, Digi International, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from typing import Any, ContextManager, Iterator, Optional


ADDR_BROADCAST: bytes = ...
ADDR_COORDINATOR: bytes = ...
ENDPOINT_DIGI_DATA: int = ...
CLUSTER_DIGI_SERIAL_DATA: int = ...
PROFILE_DIGI_XBEE: int = ...

PIN_WAKE: int = ...
RTC_WAKE: int = ...

def atcmd(cmd: str, value: Optional[Any] = None) -> Optional[Any]:
    """
    Sets or queries an AT command on the XBee module.

    :param cmd: Two-character string that represents the command.
    :param value: Command value.

        * If the ``value`` parameter is not set, the function executes the AT
          command and, depending on the command, returns the result as either
          a string, bytes object, an integer, or ``None``. Some commands
          simply return a value; other AT commands, such as special commands
          and execution commands, change the behavior of the XBee device. For
          example, **FR** resets the device.
        * If the ``value`` parameter is set, you can specify a value in a
          string, bytearray, or integer format. The function passes the value
          to set the AT command.

    :return: The value of the queried AT command. The format of the value
        depends on the requested AT command.
    """
    ...

def discover() -> Iterator[dict]:
    """
    Performs a network discovery, which is equivalent to issuing the **ND**
    command.

    Method returns immediately, but querying the resulting iterator will block
    execution until a response is available or the discovery times out (as
    determined by **N?**).

    **Note**: This method only applies to XBee3 RF modules. XBee Cellular
        modules do not support discover functionality.

    :return: A dictionary for each discovered node that contains the following
        entries:

        * ``sender_nwk`` - 16-bit network address.
        * ``sender_eui64`` - 8-byte bytes object with EUI-64 address.
        * ``parent_nwk`` - Set to **0xFFFE** on the coordinator and routers,
          otherwise the network address of the end device's parent.
        * ``node_id`` - The device's **NI** value (a string of up to 20
          characters, also referred to as Node Identification).
        * ``node_type`` - Value of **0**, **1** or **2** for coordinator,
          router or end device.
        * ``device_type`` - The device's 32-bit **DD** value (also referred to
          as Digi Device Type).
        * ``rssi`` - RSSI of the node discovery request packet received by the
          sending node.
    """
    ...

def receive() -> dict:
    """
    Returns an entry from the receive queue. The format and fields are
    equivalent to receiving a **0x91** Explicit Rx API frame.

    If the device is operating in MicroPython REPL (**AP** is set to **4**) and
    the receive queue is full, it silently rejects any additional incoming
    packets; the sending node will receive a transmission status of **0x24**
    (Address not found) in this case.

    It's recommended to call the ``receive()`` function in a loop so no data is
    lost. On devices where there is a high volume of network traffic, there
    could be data lost if the messages are not pulled from the queue fast
    enough.

    **Note**: This method only applies to XBee3 RF modules. XBee Cellular
        modules do not support receive functionality.

    :return: A received data entry as a dictionary containing the following
        fields:

        * ``sender_nwk``: The 16-bit network address of the sending node
        * ``sender_eui64``: The 64-bit address (as a bytearray) of the sending
          node
        * ``source_ep`` - The source endpoint as an integer.
        * ``dest_ep`` - The destination endpoint as an integer.
        * ``cluster`` - The cluster id as an integer.
        * ``profile`` - The profile id as an integer.
        * ``broadcast`` - Either ``True`` or ``False`` depending on whether the
          frame was broadcast or unicast.
        * ``payload`` - A bytes object of the payload (intentional selection of
          bytes object over string since the payload can contain binary data).
    """
    ...

def transmit(dest: Any, payload: Any, *, source_ep: int = xbee.ENDPOINT_DIGI_DATA,
             dest_ep: int = xbee.ENDPOINT_DIGI_DATA, cluster: int = xbee.CLUSTER_DIGI_SERIAL_DATA,
             profile: int = xbee.PROFILE_DIGI_XBEE, bcast_radius: int = 0, tx_options: int = 0) -> None:
    """
    Transmits a packet to a specified destination address. This function either
    succeeds and returns ``None``, or raises an exception. Here is a partial
    list of the exceptions to expect:

    * ``TypeError`` - Invalid type for either ``dest`` or ``payload``
    * ``ValueError`` - Payload is too long. Maximum length depends on whether
      you are making a unicast or broadcast transmission with or without
      encryption. Note that application-level encryption is not available in
      current builds.
    * ``OSError(ENOTCONN)`` - Device is not joined to a network (**AI** returns
      a non-zero value)
    * ``OSError(EAGAIN)`` - Temporary issue preventing sending, for example,
      insufficient buffers, packet already queued for target
    * ``OSError(EIO)`` - General error message for **unable to send**

    **Note**: This method only applies to XBee3 RF modules. XBee Cellular
        modules do not support transmit functionality.

    :param dest: The destination address of the message, and accepts any of the
        following:

        * An integer for 16-bit addressing.
        * An 8-byte bytes object for 64-bit addressing.
        * The constant ``xbee.ADDR_BROADCAST`` to indicate a broadcast
          destination.
        * The constant ``xbee.ADDR_COORDINATOR`` to indicate the coordinator.

        There are multiple ways to create the 8-byte bytes object for 64-bit
        addressing:

        * As a bytestring: ``b'\\x00\\x13\\xa2\\x00\x41\\x74\\x07\\xa6'``.
        * Using the ``bytes()`` constructor with a list of decimal values:
          ``bytes([0, 19, 162, 0, 65, 116, 7, 166])``.
        * Using the ``bytes()`` constructor with a tuple of hex values:
          ``bytes((0x00, 0x13, 0xa2, 0x00, 0x41, 0x74, 0x07, 0xa6))``.
    :param payload: A string (for example, 'Hello World!') or bytes object
        (useful for sending binary data).
    :param source_ep: Optional 8-bit Source Endpoint for the transmission,
        defaulting to ``xbee.ENDPOINT_DIGI_DATA``.
    :param dest_ep: Optional 8-bit Destination Endpoint for the transmission,
        defaulting to ``xbee.ENDPOINT_DIGI_DATA``.
    :param cluster: Optional 16-bit Cluster ID for the transmission,
        defaulting to ``xbee.CLUSTER_DIGI_SERIAL_DATA``.
    :param profile: Optional 16-bit Cluster ID for the transmission,
        defaulting to ``xbee.PROFILE_DIGI_XBEE``.
    :param bcast_radius: Optional 8-bit value to set the maximum number of
        hops a broadcast transmission can traverse. Default is 0.
    :param tx_options: Optional 8-bit bitfield that configures advanced
        transmission options. Please see the protocol specific user manual
        for TX Options usage.

    **Note**: All of the optional parameters are new in the following firmware versions:
        * XBee3 Zigbee: version 1007
        * XBee3 802.15.4: version 2004
        * XBee3 DigiMesh 2.4: version 3003
    """
    ...

class XBee:
    """
    Class used to create an object for the XBee device that is hosting
    MicroPython.
    """

    wake_lock: ContextManager = ...

    def __init__(self) -> None:
        """
        Class constructor. Instantiates a new ``XBee`` object.
        """
        ...

    def atcmd(self, cmd: str, value: Optional[Any] = None) -> Optional[Any]:
        """
        Sets or queries an AT command on the XBee3 RF Module.

        :param cmd: Two-character string that represents the command.
        :param value: Command value.

            * If the ``value`` parameter is not set, the function executes the
              AT command and, depending on the command, returns the result as
              either a string, bytes object, an integer, or ``None``. Some
              commands simply return a value; other AT commands, such as
              special commands and execution commands, change the behavior of
              the XBee device. For example, **FR** resets the device.
            * If the ``value`` parameter is set, you can specify a value in a
              string, bytearray, or integer format. The function passes the
              value to set the AT command.

        :return: The value of the queried AT command. The format of the value
            depends on the requested AT command.
        """
        ...

    def sleep_now(self, timeout_ms: int, pin_wake: bool=False) -> int:
        """
        Puts the XBee device in sleep mode. The device sleeps for the specified
        time period programmed with an optional early pin wake (DTR,
        commissioning button, or SPI_SSEL).

        Notice that sleep mode must be disabled by setting **SM** (Sleep Mode)
        to **0**, in order to control when the module sleeps.

        Throws an ``EALREADY`` OSError exception if **SM** is already
        configured for sleep (set to something other than **0**).

        :param timeout_ms: The number of milliseconds the device will sleep.
        :param pin_wake: If set to ``True``, the device only goes to sleep if
            **DIO8** is pulled high.

        :return: The number of milliseconds elapsed.
        """
        ...

    def wake_reason(self) -> int:
        """
        Returns the reason that made the radio to wake up. One of:

        * ``PIN_WAKE`` - If the **full** ``timeout_ms`` elapsed.
        * ``RTC_WAKE`` - When ``pin_wake`` is enabled and **DIO8** woke the
          device early.

        :return: The reason that made the radio to wake up.
        """
        ...
