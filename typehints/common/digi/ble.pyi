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

"""
Provides access to Bluetooth Low Energy functionality.

**Note**: Unless otherwise specified, the ``digi.ble`` module
and all of its contents are new in the following firmware versions:
  * XBee3 Zigbee: version 1009
"""

from typing import Any, ContextManager, Iterable, List, Optional

try:
    # Python 3.8 (and PyCharm 2019.2.5 and newer) support TypedDict,
    # which means the _GAPScanDict type can actually provide useful hints.
    # (PyCharm issue PY-36008.)
    # In case the PyCharm installation being used does not have TypedDict defined,
    # fall back to using just a regular dict type.

    from typing import TypedDict
    class _GAPScanDict(TypedDict):
        address: bytes
        addr_type: int
        connectable: bool
        rssi: int
        payload: bytes
except ImportError:
    from typing import Dict
    _GAPScanDict = Dict


__all__ = (
    'ADDR_TYPE_PUBLIC', 'ADDR_TYPE_RANDOM', 'ADDR_TYPE_PUBLIC_IDENTITY', 'ADDR_TYPE_RANDOM_IDENTITY',
    'active', 'config', 'gap_advertise', 'gap_scan',
)


ADDR_TYPE_PUBLIC: int = ...
ADDR_TYPE_RANDOM: int = ...
ADDR_TYPE_PUBLIC_IDENTITY: int = ...
ADDR_TYPE_RANDOM_IDENTITY: int = ...


def active(
        active: Optional[bool] = None,
        /,  # active can only be specified as a positional argument
) -> bool:
    """
    Sets or queries whether Bluetooth Low Energy (BLE) functionality
    is enabled on the XBee3 module.

    :param active:
        If True, enable BLE functionality.
        If False, disable BLE functionality.
        If not given, query whether BLE functionality is currently enabled.
    :return: True if BLE functionality is enabled, False otherwise.
    """
    ...


def config(
        name: str,
        /,  # name can only be specified as a positional argument
) -> Any:  # Really bytes, but could vary in the future
    """
    Query a BLE configuration value by name.

    :param name: Name of the BLE configuration value to query.
        The only name currently supported is "mac", which queries
        the device BLE MAC address, returned as a ``bytes`` object.
        (This is equivalent to querying the ATBL AT command.)
    :return: The queried configuration value.
    """
    ...


def gap_advertise(
        interval_us: Optional[int],
        /,  # interval_us can only be specified as a positional argument
        adv_data: Optional[bytes] = None
) -> None:
    r"""
    Start or stop GAP advertisements from the XBee3 module.

    **Stop advertising:**

    To stop advertising, set ``interval_us`` to ``None``. Example::

        from digi import ble
        ble.gap_advertise(None)

    **Return to default advertisement:**

    If ``adv_data`` is empty (i.e. ``b''``), then GAP advertising will return
    to the default XBee behavior, which is to advertise the product name
    (e.g. ``XBee3 Zigbee``) and ``interval_us`` is ignored.::

        ble.gap_advertise(500000, b'')

    **Specify new advertisement data:**

    If ``adv_data`` is given and is not ``None`` or empty (i.e. ``b''``),
    then it should consist of one or more Advertising Data (AD) elements,
    as defined in the Bluetooth Core Specification Supplement, Part A Section 1.
    The format of Advertising Data elements is summarized here:
      * Each AD element consists of a length byte, a data type byte, and
        one or more bytes of data. The length byte indicates how long the rest
        of the element is, e.g. a Complete Local Name element with the value
        ``"My XBee"`` would have a length byte ``0x08`` - 1 byte for type plus
        7 bytes for the value.
      * The Bluetooth SIG provides the list of defined Advertising Data element types
        at https://www.bluetooth.com/specifications/assigned-numbers/generic-access-profile/

    Please be aware that in order to advertise a specific device name (such as ``"My XBee"``),
    ``adv_data`` cannot consist simply of the name to be advertised.
    The ``adv_data`` value *must* be formatted as one or more Advertising Data elements
    in order to be interpreted as a valid Bluetooth Low Energy advertisement by other devices.

    Example::

        ble.gap_advertise(200000, b"\x08\x09My XBee")

        # Example using a bytearray
        name = b"My XBee"
        data = bytearray([len(name) + 1, 0x09])
        data.extend(name)
        ble.gap_advertise(200000, data)

    **Re-use data from the previous gap_advertise call:**

    If ``adv_data`` is ``None`` or not specified, then the data passed to the
    previous call to ``gap_advertise`` will be re-used, unless there was no
    previous call or the data was empty, in which case the behavior will be
    as if an empty value (``b''``) was passed.::

        # These two calls are equivalent.
        ble.gap_advertise(200000)
        ble.gap_advertise(200000, None)

    :param interval_us: Start advertising at the specified interval, in microseconds.
        This value will be rounded down to the nearest multiple of 625 microseconds.
        If this value is not ``None``, it must be at least 20,000 microseconds
        (20 milliseconds) and no larger than 40,959,375 microseconds
        (approximately 40.96 seconds).
        To stop advertising, set ``interval_us`` to ``None``.
    :param adv_data: The payload that will be included in GAP advertisement broadcasts.
        ``adv_data`` can be a ``bytes`` or ``bytearray`` object up to 31 bytes in length,
        or ``None``.
    :raises OSError ENODEV: BLE functionality is disabled (see ``active()``).
    """
    ...


class _gap_scan(ContextManager, Iterable[_GAPScanDict]):
    """
    Class used to encapsulate an ongoing GAP scan (device discovery) operation,
    This class cannot be instantiated, it is returned from ``digi.ble.gap_scan()``.

    See the documentation for ``digi.ble.gap_scan()`` for examples of usage.
    """

    def get(self) -> List[_GAPScanDict]:
        """
        Return a list of all received GAP advertisements which are currently in the
        internal queue. This list may be empty.

        If the GAP scan has timed out (see ``duration_ms`` argument to ``gap_scan``)
        or if ``stop()`` has been called, this method will return any remaining
        advertisements, but no new advertisements will be stored.

        Each advertisement is formatted as a dictionary containing the following fields:

        * ``address``: The BLE MAC address of the sender of the advertisement, formatted
          as a ``bytes`` object.
        * ``addr_type``: The type of address contained in the ``address`` field. The possible
          values are defined as constants on the ``digi.ble`` module:
            * ``ADDR_TYPE_PUBLIC``
            * ``ADDR_TYPE_RANDOM``
            * ``ADDR_TYPE_PUBLIC_IDENTITY``
            * ``ADDR_TYPE_PUBLIC_RANDOM``
        * ``connectable``: ``True`` if the advertising device indicates that BLE central-mode devices
          may connect to it, ``False`` otherwise.
        * ``rssi``: The received signal strength of the advertisement, in dBm.
        * ``payload``: The raw advertisement payload, formatted as a ``bytes`` object.

        :return: a list (possibly empty) of received GAP advertisements, where each
            advertisement is a dictionary whose fields are described above.
        """
        ...

    def any(self) -> bool:
        """
        Return a boolean indicating whether there are any GAP advertisements in the internal queue
        (i.e. whether ``get()`` would return any advertisements).

        :return: ``True`` if there are advertisements waiting to be accessed, ``False`` otherwise.
        """
        ...

    def stop(self) -> None:
        """
        Stop the ongoing GAP scan operation.
        """
        ...

    def stopped(self) -> bool:
        """
        Return a boolean indicating whether the GAP scan operation has been stopped
        (using ``stop()``) or has timed out (see ``duration_ms`` argument to ``gap_scan``).

        :return: ``True`` if the GAP scan operation has been stopped or has timed out,
            ``False`` otherwise
        """
        ...

    def __enter__(self) -> _gap_scan:
        """
        Enter the runtime context for using this GAP scan object as a context manager
        (using the ``with`` statement).

        This step has no effect, but the call to ``__exit__`` which occurs
        when this context is exited will have the same effect as ``stop()``.

        You do not need to call ``__enter__`` directly, this happens automatically
        when the ``with`` statement is used.

        Example::

            with ble.gap_scan(0) as scan:  # __enter__ is called
                for adv in scan:
                    print(adv)
                    # Break out of the loop...
                    break
                # ... since we do nothing here, the `with` context is exited.
            # __exit__ is called
            assert scan.stopped()

        :return: this GAP scan object
        """
        ...


def gap_scan(
        duration_ms: int = 0,
        interval_us: int = 1280000,
        window_us: int = 11250,
        *,  # oldest is keyword-only
        oldest: bool = False,
) -> _gap_scan:
    """
    Start a GAP scan (discovery) operation to collect advertisements from nearby BLE devices.

    Each advertisement is formatted as a dictionary containing the following fields:

    * ``address``: The BLE MAC address of the sender of the advertisement, formatted
      as a ``bytes`` object.
    * ``addr_type``: The type of address contained in the ``address`` field. The possible
      values are defined as constants on the ``digi.ble`` module:
        * ``ADDR_TYPE_PUBLIC``
        * ``ADDR_TYPE_RANDOM``
        * ``ADDR_TYPE_PUBLIC_IDENTITY``
        * ``ADDR_TYPE_PUBLIC_RANDOM``
    * ``connectable``: ``True`` if the advertising device indicates that BLE central-mode devices
      may connect to it, ``False`` otherwise. (Note: XBee3 modules do not currently support
      connecting to other BLE devices.)
    * ``rssi``: The received signal strength of the advertisement, in dBm.
    * ``payload``: The raw advertisement payload, formatted as a ``bytes`` object.

    **Accessing the received advertisements:**

    One way to access the advertisements received during a GAP scan operation
    is to call the ``get()`` method on the scan object, which returns a list
    of advertisements::

        scan = ble.gap_scan()
        # Pause for a few seconds to allow some advertisements to arrive.
        time.sleep(5)
        for advertisement in scan.get():
            print(advertisement)
        scan.stop()

    Continue reading for other examples of accessing the advertisements.

    **Using gap_scan as an iterator:**

    Instead of calling ``get()`` repeatedly to access received GAP advertisements,
    the object returned by ``gap_scan`` may be used as an iterator, or in other words,
    as the target of a ``for``-loop::

        scan = ble.gap_scan(duration_ms=10000)  # 10 seconds
        for advertisement in scan:
            print(advertisement)

    Using ``gap_scan`` as an iterator is the preferred means to access the
    received advertisements. This is because calling ``get()`` requires allocating a list
    and filling the list with advertisements (dictionaries), whereas using ``gap_scan``
    as an iterator is more efficient because only one dictionary needs to be created at a time.

    To stop iterating over the ``gap_scan`` object (in order for your MicroPython application
    to perform other activities, for example), just ``break`` out of the loop. The GAP scan
    will continue running in the background. Example::

        # Example: read and print out 5 advertisements at a time
        def process_five_advertisements(scan):
            count = 0
            for advertisement in scan:
                print(advertisement)
                count += 1
                if count >= 5:
                    break

        scan = ble.gap_scan()
        while True:
            process_five_advertisements()
            do_something_else()
        scan.stop()

    **Using gap_scan as a context manager:**

    When running an indefinite GAP scan operation (``duration_ms=0``), instead of
    needing to call ``stop()`` to end the GAP scan operation, you may instead use
    the object returned by ``gap_scan`` as a context manager. By doing this,
    when the ``with`` block is exited, the GAP scan operation is automatically stopped.
    This approach uses less code and is less error-prone.

    For example, if you want to run a GAP scan operation until any advertisement whose
    payload contains a particular byte string is found, you can do this as follows::

        def find_advertisement(search):
            with ble.gap_scan(0) as scan:
                for adv in scan:
                    if search in adv["payload"]:
                        return adv

        found = find_advertisement(b"Hello, XBee")

    Compare to this example which does not use a context manager. Note the use of a try/finally block,
    and the need to call ``stop()`` explicitly::

        def find_advertisement(search):
            scan = ble.gap_scan(0)
            try:
                for adv in scan:
                    if search in adv["payload"]:
                        return adv
            finally:
                # Make sure to call stop() even if an exception is raised.
                scan.stop()

        found = find_advertisement(b"Hello, XBee")

    :param duration_ms: The duration of the GAP scan operation, i.e. how long to scan, in milliseconds.
        To scan indefinitely, set this to 0. If this parameter is not specified, it defaults
        to 0 (indefinite scan).
    :param interval_us: Optionally configure the duty cycle of the GAP scan operation.
        The scanner will run for ``window_us`` microseconds every ``interval_us`` microseconds.
        ``window_us`` must be less than or equal to ``interval_us``.
        ``interval_us`` must be at least 2,500 microseconds (2.5 milliseconds)
        and no more than approximately 40.96 seconds (40,959,375 microseconds).
        The default interval is 1.28 seconds.
    :param window_us: Optionally configure the duty cycle of the GAP scan operation.
        The scanner will run for ``window_us`` microseconds every ``interval_us`` microseconds.
        ``window_us`` must be less than or equal to ``interval_us``.
        ``window_us`` must be at least 2,500 microseconds (2.5 milliseconds)
        and no more than approximately 40.96 seconds (40,959,375 microseconds).
        The default window is 11.25 milliseconds.
    :param oldest: Discard new received advertisements once the internal queue fills up.
        Normally this should be left at its default value of False, so that new advertisements
        will overwrite the oldest stored advertisement when the queue fills up.
        Only set this to True if your application requires this behavior.
    :return: an object which encapsulates the GAP scan operation.
    :raises OSError ENODEV: BLE functionality is disabled (see ``active()``).
    :raises OSError EALREADY: Another ``gap_scan`` is still running.
        (Call ``.stop()`` on the existing scan. If the existing scan object
        cannot be referenced, soft reset the MicroPython REPL.)
    """
    ...
