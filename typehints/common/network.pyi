# Copyright (c) 2020, Digi International, Inc.
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

from typing import Any, Dict, Optional, Tuple, Callable, List

try:
    # Python 3.8 (and PyCharm 2019.2.5 and newer) support TypedDict,
    # which means the _GAPScanDict type can actually provide useful hints.
    # (PyCharm issue PY-36008.)
    # In case the PyCharm installation being used does not have TypedDict defined,
    # fall back to using just a regular dict type.

    from typing import TypedDict
    class _SMSDict(TypedDict):
        message: str
        sender: str
        timestamp: int
    class _ScanDict(TypedDict):
        serving_cell: bool
        area: int
        cell_id: int
        mcc: str
        mnc: str
        signal: int
except ImportError:
    from typing import Dict
    _SMSDict = Dict
    _ScanDict = Dict


class Cellular:
    """
    Class that provides a driver for the cellular modem in an XBee cellular
    device.
    """

    def config(self, param: Optional[str]=None, **kwargs: Any) -> \
            Optional[Any]:
        """
        Gets or sets general network interface parameters. This methods allows
        to work with additional parameters beyond standard IP configuration.

        * For **setting** parameters, keyword argument syntax should be used,
          multiple parameters can be set at once.
        * For **querying** parameters, name should be quoted as a string, and
          only one parameter can be queries at time.

        Available network parameters are:

        * ``apn`` - Access Point Name
        * ``iccid`` - SIM card number
        * ``imei`` - International Mobile Equipment Identity
        * ``operating_apn`` - Operating Access Point Name
        * ``operator`` - Network operator
        * ``phone`` - Phone number

        :param param: When querying a parameter, the name of the parameter.
            Example::

                c = network.Cellular()
                print('Phone:', c.config('phone'))
        :param kwargs: When setting parameters, the name of each parameter to
            set with its corresponding value. Example::

                c = network.Cellular()
                c.config(apn='ac.vodafone.es')

        :return: When querying a parameter, the value of that parameter.
        """
        ...

    def ifconfig(self) -> Tuple[str, str, str, str]:
        """
        Gets the IP-level network interface parameters:

        * IP address
        * Subnet mask
        * Gateway
        * DNS server

        :return: A 4-tuple containing the IP addressing information including:

            * IP address
            * Subnet mask
            * Gateway
            * DNS server
        """
        ...

    def isconnected(self) -> bool:
        """
        Determines whether the XBee Cellular Modem is connected to a network.

        :return: ``True`` if the XBee Cellular Modem is connected to a cellular
            network and has a valid IP address, ``False`` otherwise.
        """
        ...

    def active(self, mode: bool) -> None:
        """
        Sets whether the XBee Cellular Modem is powered on or in
        airplane mode.

        If ``mode`` parameter is provided, the method sets the airplane mode,
        otherwise the method returns the status of the airplane mode.

        :param mode: ``True to make the XBee Cellular modem enter airplane
            mode, ``False`` to make it leave airplane mode.

        :return: ``True`` if the XBee Cellular Modem is powered on or ``False``
            if the XBee Cellular Modem is in airplane mode.
        """
        ...

    def sms_callback(self, callback: Optional[Callable[[_SMSDict], Any]], /) -> None:
        """
        Register a callback method that is called whenever an SMS message is
        received.

        This callback takes one parameter, a dictionary with the following
        keys:

            * ``message`` - The message text, which is converted to a 7-bit
              ASCII with extended Unicode characters changed to spaces.
            * ``sender`` - The phone number from which the message was sent.
            * ``timestamp`` - The number of seconds since 1/1/2000, which is
              passed to ``time.localtime()`` and then converted into a tuple
              of datetime elements.

        **Note:** This is only available on XBee 3 Cellular products with
        firmware ending in 15 or newer.

        :param callback: A function that is called whenever an SMS is received.
            If ``callback`` is None, the registered callback will be
            unregistered, allowing for polling of sms_receive again.
        """
        ...

    def sms_receive(self) -> Optional[dict]:
        """
        Returns the latest SMS message received or ``None`` if there is no
            message

        :return: The latest SMS message received or ``None`` if there is no
            message. Message is returned as a dictionary with the following
            keys:

            * ``message`` - The message text, which is converted to a 7-bit
              ASCII with extended Unicode characters changed to spaces.
            * ``sender`` - The phone number from which the message was sent.
            * ``timestamp`` - The number of seconds since 1/1/2000, which is
              passed to ``time.localtime()`` and then converted into a tuple
              of datetime elements.
        """
        ...

    def sms_send(self, phone: Any, message: Any) -> None:
        """
        Sends a message to a phone using SMS.

        The method can throw any of the following exceptions if an error occurs
        sending the SMS message:

        * ``ValueError`` - For invalid parameters
        * ``OSError``:

          * ``ENOTCONN`` - The cellular mode has not connected.
          * ``ETIMEDOUT`` - If the network doesn't acknowledge the message in
            a reasonable amount of time.
          * ``EIO```- If there was some other error in sending the message.

        :param phone: The phone number of the device to which the message
            should be sent. This variable can be a string or an integer.
        :param message: The contents of the message. The message should be a
            string or a bytes object of 7-bit ASCII characters.
        """
        ...

    def shutdown(self, reset: bool = False) -> None:
        """
        Cleanly shuts down the cellular component. After the shutdown process
        is complete, you can safely remove power from the device.

        If the cellular component cannot be fully shut down within two minutes,
        an OSError ETIMEDOUT will be raised.

        ``shutdown()`` is equivalent to the **ATSD** command.

        **Note:** This is only available on XBee and XBee 3 Cellular products
        with firmware ending in 15 or newer.

        :param reset: If True, the device will automatically be rebooted after
            the cellular component has been shut down (as if
            ``machine.reset()`` was called).
        :raises OSError ETIMEDOUT: Cellular component could not be shut down
            within two minutes.
        """
        ...

    def signal(self) -> Dict[str, float]:
        """
        Retrieve the current signal quality indicators available, as a
        dictionary.

        The maximum set of signal quality indicators are:

        * ``rssi`` - Equivalent to the **ATDB** command.
        * ``rsrp`` - Reference Signal Received Power. Equivalent to
            the **ATSW** command. Not available on XBee Cellular 3G.
        * ``rsrq`` - Reference Signal Received Quality. Equivalent to
            the **ATSQ** command. Not available on XBee Cellular 3G.

        **Note:** This is only available on XBee and XBee 3 Cellular products
        with firmware ending in 15 or newer.

        :returns: A dictionary whose keys are strings (signal quality indicator
            name) and values are float.
        :raises OSError ETIMEDOUT: Signal quality indicators could not be
            retrieved within five seconds.
        """
        ...

    def scan(
        self,
        callback: Optional[Callable[[List[_ScanDict]], Any]] = None,
        *,
        deep: bool = False,
    ) -> Optional[List[_ScanDict]]:
        """
        Scans for mobile cells in the vicinity and returns information about
        the cells in the service area of the device. When called, the cell
        module waits until all other communication is idle and then performs
        the scan.

        The information that can be reported by this function varies based on
        the network technology of the module that you are using.

        The maximum information available per entry in the list is as follows:

        * ``serving_cell`` - If True, this is the current serving cell.
        * ``area`` - Location Area Code as an int
        * ``mcc`` - Mobile Country Code as a string
        * ``mnc`` - Mobile Network Code as a string
        * ``signal`` - Reference Signal Received Power (RSRP) in dBm as an int

        **Note:** This is only available on XBee 3 Cellular products with
        firmware ending in x1A or newer.

        **Note:** When a deep scan is performed, any outstanding sockets or
            other activity will be lost. Since registration is lost, no
            "serving cell" information is provided, as the "serving cell" that
            the device will re-join cannot be reported, and there is no
            guarantee that the "serving cell" the device was on before network
            registration was dropped will still be used. The duration of the
            scan is approximately 25 seconds.

        :param callback: A function that is called when the scan is complete.
            If ``callback`` is None, the function blocks until the scan is
            complete and returns the result directly.
        :param deep: If true, a full scan is attempted, which requires dropping
            network registration. A full scan can return more complete
            information for all cells seen, which includes cells offered by
            other carriers.
        :returns: A list of dictionaries that represent each nearby tower,
            or ``None`` if ``callback`` was provided.
        :raises ValueError: One or more parameters was invalid.
        :raises TypeError: Improper number or type of arguments. For example,
            the callback has to be a function that takes one parameter.
        :raises OSError:
          * ``ENODEV`` - The modem is busy being updated.
          * ``EBUSY`` - A scan is already in progress.
          * ``ENOBUFS```- Out of resources.

        """
        ...
