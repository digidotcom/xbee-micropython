# Copyright (c) 2019-2020, Digi International Inc.
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
  * XBee3 802.15.4: version 200A
  * XBee3 DigiMesh 2.4: version 300A
  * XBee3 Cellular LTE-M/NB-IoT: version 11415
  * XBee3 Cellular LTE Cat 1: version x15
"""

from typing import (
    Any, Callable, ContextManager, Iterable, Iterator, List, Optional, NewType,
    Sized, Tuple, Union, overload
)

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

_UUIDValue = Union[int, str, bytes]
_UUIDOrValue = Union['UUID', _UUIDValue]

# These type names are provided mainly for documentation purposes,
# i.e. to make the PyCharm documentation popup use Service, Characteristic,
# etc. instead of just int.
# However, they also have a secondary benefit, which is that a type checker
# can flag instances where a service handle is passed as a characteristic
# or descriptor, or vice versa.
_ServiceHandle = NewType('Service', int)
_CharacteristicHandle = NewType('Characteristic', int)
_DescriptorHandle = NewType('Descriptor', int)
_Properties = NewType('Properties', int)

_ServiceTuple = Tuple[_ServiceHandle, 'UUID']
_CharacteristicTuple = Tuple[_CharacteristicHandle, 'UUID', _Properties]
_DescriptorTuple = Tuple[_DescriptorHandle, 'UUID']


__all__ = (
    'ADDR_TYPE_PUBLIC', 'ADDR_TYPE_RANDOM', 'ADDR_TYPE_PUBLIC_IDENTITY', 'ADDR_TYPE_RANDOM_IDENTITY',
    'PROP_BROADCAST', 'PROP_READ', 'PROP_WRITE', 'PROP_WRITE_NO_RESP', 'PROP_AUTH_SIGNED_WR',
    'PROP_NOTIFY', 'PROP_INDICATE',
    'active', 'config', 'gap_advertise', 'gap_scan', 'gap_connect',
    'UUID',
)


ADDR_TYPE_PUBLIC: int = ...
ADDR_TYPE_RANDOM: int = ...
ADDR_TYPE_PUBLIC_IDENTITY: int = ...
ADDR_TYPE_RANDOM_IDENTITY: int = ...

PROP_BROADCAST: int = ...
PROP_READ: int = ...
PROP_WRITE: int = ...
PROP_WRITE_NO_RESP: int = ...
PROP_AUTH_SIGNED_WR: int = ...
PROP_NOTIFY: int = ...
PROP_INDICATE: int = ...


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
        name: Optional[str] = None,
        /,  # name can only be specified as a positional argument
        *,  # settings can only be changed using keyword arguments
        interval_ms: int = -1,
        latency: int = -1,
        timeout_ms: int = -1,
) -> Any:  # at this time: bytes, int or None
    """
    Query a BLE configuration value by name. Or, update one or more BLE
    configuration values by name.

    **Query a configuration option**

    To query a BLE configuration option, pass the name of the option.
    The currently supported option names are:

        * ``"mac"``: Get the device BLE MAC address as a ``bytes`` object.
          (This is equivalent to querying the ATBL AT command.)
        * ``"interval_ms"``: See the ``interval_ms`` parameter below.
        * ``"latency"``: See the ``latency`` parameter below.
        * ``"timeout_ms"``: See the ``timeout_ms`` parameter below.

    **Update configuration options**

    To change the value of one or more BLE configuration options,
    call ``config()`` using keyword arguments. For example::

        ble.config(interval_ms=100, timeout_ms=5000)

    When modifying one or more configuration options, other options which
    are not specified will not be modified (i.e. their current values will
    be left as is).

    **Note:** XBee3 Zigbee firmware version 1009 only supports
    ``config("mac")``. Support for other query values and keyword
    arguments was added in firmware 100A.

    :param name: Name of a BLE configuration value to query.
        When querying a value, settings (using keyword arguments) are not
        allowed.
    :param interval_ms: The default connection interval (the time between two
        data transfer events) for future GAP connections.
        The value will be rounded down to the nearest multiple of 1.25 milliseconds.
        ``interval_ms`` may be between 8 and 4000 (4 seconds).
        The default interval value (restored at XBee power-up) is 50 milliseconds.
    :param latency: The default slave latency value for future GAP connections.
        Slave latency is the number of connection events which the peripheral
        is allowed to skip before the connection is dropped.
        ``latency`` may be between 0 and 500.
        The default latency (restored at XBee power-up) is 0.
    :param timeout_ms: The default connection supervision timeout value for
        future GAP connections.  The supervision timeout is the time that the
        central device (the XBee, in this case) wil wait for a data transfer
        before assuming that the connection is lost.
        ``timeout_ms`` may be between 100 and 32000 (32 seconds).
        ``timeout_ms`` must be larger than 2 * interval_ms * (latency + 1).
        The default timeout value (restored at XBee power-up) is 1 second.
    :return: The queried configuration value, or None if setting.
    :raises ValueError: One or more parameters was invalid.
    :raises TypeError: Improper number or type of arguments. For example,
        positional and keyword arguments cannot be mixed (i.e. you cannot
        specify a name as a string while applying a setting).
    :raises OSError: New configuration could not be applied.
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


class UUID(Sized):
    """
    A representation of a Bluetooth UUID value.

    To read the UUID value, convert the ``UUID`` object into a ``bytes``
    or ``bytearray`` object::

        uuid = some_characteristic.uuid()
        uuid_value = bytes(uuid)

    The UUID value is either 16 bits (e.g. ``0x2908``)
    or 128 bits (e.g. ``7dddca00-3e05-4651-9254-44074792c590``).

    When a ``UUID`` object is converted into a string,
    by passing it to ``print`` or using ``str()`` or ``repr()``,
    the UUID value is presented in a human-readable format.
    This is useful for logging or printing messages to the console.
    For example::

        UUID(0x2908)
        UUID('7dddca00-3e05-4651-9254-44074792c590')

    To query the size (length in bytes) of the UUID value, use the built-in
    **len** function::

        len(ble.UUID(0x1234))  # returns 2
        len(ble.UUID('7dddca00-3e05-4651-9254-44074792c590'))  # returns 16

    **Note:**

    The ``UUID`` class is new in the following firmware versions:
        * XBee3 Zigbee: version 100A
        * XBee3 802.15.4: version 200A
        * XBee3 Cellular LTE-M/NB-IoT: version 11415
        * XBee3 Cellular LTE Cat 1: version x15
    """

    def __init__(self, uuid: _UUIDValue, /) -> None:
        """
        Create a new ``UUID`` object referencing the given UUID value.

        If ``uuid`` is an integer, it is treated as a 16-bit value.

        If ``uuid`` is a string or bytes of the form ``0xXXXX``
        (in other words, the hexadecimal form of a 16-bit value),
        it is converted into the equivalent 16-bit integer value.

        If ``uuid`` is a string or bytes of the form
        ``XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX``
        (in other words, the string form of a 128-bit UUID),
        it is converted into the equivalent 128-bit (16-byte) value.

        :raises ValueError: ``uuid`` is invalid
        :raises TypeError: ``uuid`` is of the incorrect type
        """
        ...


class _gap_connect(ContextManager):
    """
    Class used to encapsulate a GAP connection to a remote BLE peripheral device.
    This class cannot be instantiated, it is returned from ``digi.ble.gap_connect()``.

    See the documentation for ``digi.ble.gap_connect()`` for examples of usage.
    """

    def addr(self) -> Tuple[int, bytes]:
        """
        Returns the BLE peripheral device's address and address type.

        The returned address is a tuple consisting of two fields:
          * BLE address type of the peripheral device.
          * BLE address of the peripheral device, formatted as a ``bytes`` object.

        :return: A 2-tuple containing the BLE addressing information.
        """
        ...

    def close(self) -> None:
        """
        Close the GAP connection.

        The connection object will no longer be usable.
        """
        ...

    def config(
        self,
        name: Optional[str] = None,
        /,  # name can only be specified as a positional argument
        *,  # settings can only be changed using keyword arguments
        interval_ms: int = -1,
        latency: int = -1,
        timeout_ms: int = -1,
    ) -> Any:  # at this time: bytes, int or None
        """
        Query or update the BLE timing parameters for this connection.

        To control these timing parameters *before* opening a connection,
        see ``digi.ble.config()``.

        **Query a configuration option**

        To query a connection option, pass the name of the option.
        The currently supported option names are:

            * ``"interval_ms"``: See the ``interval_ms`` parameter below.
            * ``"latency"``: See the ``latency`` parameter below.
            * ``"mtu"``: Get the MTU value.
            * ``"timeout_ms"``: See the ``timeout_ms`` parameter below.

        **Update configuration options**

        To change the value of one or more BLE connection options,
        call ``config()`` using keyword arguments. For example::

            connection.config(interval_ms=100, timeout_ms=5000)

        When modifying one or more configuration options, other options which
        are not specified will not be modified (i.e. their current values will
        be left as is).

        :param name: Name of a BLE connection option to query.
            When querying a value, settings (using keyword arguments) are not
            allowed.
        :param interval_ms: The connection interval (the time between two
            data transfer events) for this GAP connection. The value will be
            rounded down to the nearest multiple of 1.25 milliseconds.
            ``interval_ms`` may be between 8 and 4000 (4 seconds).
            The default interval value (restored at XBee power-up) is
            50 milliseconds.
        :param latency: The slave latency value for this GAP connection.
            Slave latency is the number of connection events which the
            peripheral is allowed to skip before the connection is dropped.
            ``latency`` may be between 0 and 500.
            The default latency (restored at XBee power-up) is 0.
        :param timeout_ms: The connection supervision timeout value for this
            GAP connection. The supervision timeout is the time that the
            central device (the XBee, in this case) wil wait for a data transfer
            before assuming that the connection is lost.
            ``timeout_ms`` may be between 100 and 32000 (32 seconds).
            ``timeout_ms`` must be larger than 2 * interval_ms * (latency + 1).
            The default timeout value (restored at XBee power-up) is 1 second.
        :return: The queried configuration value, or None if setting.
        :raises ValueError: One or more parameters was invalid.
        :raises OSError: New configuration could not be applied (typically
            ENOTCONN, the connection was lost)
        """

    def disconnect_code(self) -> int:
        """
        When called on a connection which has been closed, returns a value
        from the Bluetooth Core specification Vol 2, Part D (Error
        Codes) indicating the reason for the disconnect.  Calling this
        on an open connection returns zero.

        The most common values to see include:

        8 - Connection timeout
        19 - Remote user terminated
        22 - Connection terminated by local host

        """
        ...

    def gattc_services(
        self,
        uuid: Optional[_UUIDOrValue] = None,
    ) -> Iterator[_ServiceTuple]:
        """
        Perform a search/discovery of all GATT services in the remote device's
        GATT server database.

        Each returned service is a tuple consisting of three fields:
          * The service handle
          * The service's UUID value, as a ``UUID`` object

        Note that this function returns an iterator of service tuples,
        and the service discovery operation will not terminate until the
        iterator is emptied (all values are consumed). An error will be raised
        if another service, characteristic or descriptor discovery is started
        before the ongoing discovery completes.

        Example usage::

            with ble.gap_connect(ble.ADDR_TYPE_PUBLIC, remote_mac) as conn:
                for service in conn.gattc_services():
                    print(service)

                # Or, you can consume the items in the iterator into a list.
                services = list(conn.gattc_services())

        :param uuid: A ``UUID`` value or a value that can be used to construct a
            ``UUID`` (int, bytes or UUID string). If given and not None,
            the iterator only generates the service with the given UUID
            (if it exists), otherwise all discovered services are generated.
        :return: An iterator of service tuples, where each tuple contains a
            a service handle and a ``UUID`` value.
        :raises OSError: Service discovery operation could not be started.
        """
        ...

    def gattc_characteristics(
        self,
        service: Union[_ServiceHandle, _ServiceTuple],
        /,  # service can only be specified as a positional argument
        uuid: Optional[_UUIDOrValue] = None,
    ) -> Iterator[_CharacteristicTuple]:
        """
        Perform a search/discovery of all GATT characteristics on the given service
        in the remote device's GATT server database.

        ``service`` can either be a GATT service handle (one of the values contained
        in the tuple(s) generated by ``gattc_services()``), or one of the tuples
        generated by ``gattc_services()`` (in which case the service handle will be
        taken from the tuple).

        Each returned characteristic is a tuple consisting of three fields:
          * The characteristic handle
          * The characteristic's UUID value, as a ``UUID`` object
          * The characteristic's property flags, which is a bitmask of flags defined
            as constants on the ``digi.ble`` module:
              * ``PROP_BROADCAST``
              * ``PROP_READ``
              * ``PROP_WRITE``
              * ``PROP_WRITE_NO_RESP``
              * ``PROP_AUTH_SIGNED_WR``
              * ``PROP_NOTIFY``
              * ``PROP_INDICATE``

        Note that this function returns an iterator of characteristic tuples,
        and the characteristic discovery operation will not terminate until the
        iterator is emptied (all values are consumed). An error will be raised
        if another service, characteristic or descriptor discovery is started
        before the ongoing discovery completes.

        Example usage::

            with ble.gap_connect(ble.ADDR_TYPE_PUBLIC, remote_mac) as conn:
                # Since characteristic discovery cannot be started while
                # another discovery is in process, we must consume the services
                # into a list before discovering their characteristics.
                services = list(conn.gattc_services())

                for service in services:
                    for characteristic in conn.gattc_characteristics(service):
                        print(service, characteristic)

        :param service: A service handle, or one of the service tuples returned by
            ``gattc_services()``.
        :param uuid: A ``UUID`` value or a value that can be used to construct a
            ``UUID`` (int, bytes or UUID string). If given and not None,
            the iterator only generates characteristics found with the given UUID
            (if it exists), otherwise all discovered characteristics are generated.
        :return: An iterator of characteristic tuples, where each tuple contains
            a characteristic handle (an integer), a ``UUID`` value, and the
            characteristic's property flags.
        :raises OSError: Characteristic discovery operation could not be started.
        """
        ...

    def gattc_descriptors(
        self,
        characteristic: Union[_CharacteristicHandle, _CharacteristicTuple],
        /,  # positional argument only
    ) -> Iterator[_DescriptorTuple]:
        """
        Perform a search/discovery of all GATT descriptors on the given
        characteristic in the remote device's GATT server database.

        ``characteristic`` can either be a GATT characteristic handle
        (one of the values contained in the tuple(s) generated by
        ``gattc_characteristics()``), or one of the tuples generated by
        ``gattc_characteristics()`` (in which case the service handle will be
        taken from the tuple).

        Each returned descriptor is a tuple consisting of two fields:
          * The descriptor handle
          * The descriptor's UUID value, as a ``UUID`` object

        Note that this function returns an iterator of descriptor tuples,
        and the descriptor discovery operation will not terminate until the
        iterator is emptied (all values are consumed). An error will be raised
        if another service, characteristic or descriptor discovery is started
        before the ongoing discovery completes.

        Example usage::

            with ble.gap_connect(ble.ADDR_TYPE_PUBLIC, remote_mac) as conn:
                # Since characteristic discovery cannot be started while
                # another discovery is in process, we must consume the services
                # into a list before discovering their characteristics.
                services = list(conn.gattc_services())

                for service in services:
                    # Since descriptor discovery cannot be started while
                    # another discovery is in process, we must consume the
                    # characteristics into a list.
                    characteristics = list(conn.gattc_characteristics(service))

                    for characteristic in characteristics:
                        for descriptor in conn.gattc_descriptors(service, characteristic):
                            print(service, characteristic, descriptor)

        :param characteristic: A characteristic handle, or one of the characteristic
            tuples returned by ``gattc_characteristics()``.
        :return: An iterator of descriptor tuples, where each tuple contains
            a descriptor handle and a ``UUID`` value.
        :raises OSError: Descriptor discovery operation could not be started.
        """
        ...

    def gattc_read_characteristic(
        self,
        characteristic: Union[_CharacteristicHandle, _CharacteristicTuple],
        /,
    ) -> bytes:
        """
        Perform a GATT read operation against the specified characteristic
        of the connected BLE peripheral device.

        :param characteristic: A characteristic handle, or one of the characteristic
            tuples returned by ``gattc_characteristics()``.
        :return: A ``bytes`` object containing the characteristic value
            which was read.
        :raises OSError: The characteristic could not be read, or the
            connection was lost.
        """
        ...

    def gattc_read_descriptor(
        self,
        descriptor: Union[_DescriptorHandle, _DescriptorTuple],
        /,
    ) -> bytes:
        """
        Perform a GATT read operation against the specified descriptor
        of the connected BLE peripheral device.

        :param descriptor: A descriptor handle, or one of the descriptor
            tuples returned by ``gattc_descriptors()``.
        :return: A ``bytes`` object containing the descriptor value
            which was read.
        :raises OSError: The descriptor could not be read, or the
            connection was lost.
        """
        ...

    def gattc_write_characteristic(
        self,
        characteristic: Union[_CharacteristicHandle, _CharacteristicTuple],
        data: bytes,
        /,  # positional arguments only
    ) -> None:
        """
        Perform a GATT write operation against the specified characteristic
        of the connected BLE peripheral device.

        :param characteristic: A characteristic handle, or one of the characteristic
            tuples returned by ``gattc_characteristics()``.
        :param data: The value to be written to the remote device's characteristic.
            This parameter can be of type ``bytes`` or ``bytearray``.
        :raises OSError: The characteristic could not be written,
            or the connection was lost.
        """
        ...

    def gattc_write_descriptor(
        self,
        descriptor: Union[_DescriptorHandle, _DescriptorTuple],
        data: bytes,
        /,
    ) -> None:
        """
        Perform a GATT write operation against the specified descriptor
        of the connected BLE peripheral device.

        :param descriptor: A descriptor handle, or one of the descriptor
            tuples returned by ``gattc_descriptors()``.
        :param data: The value to be written to the remote device's descriptor.
            This parameter can be of type ``bytes`` or ``bytearray``.
        :raises OSError: The descriptor could not be written,
            or the connection was lost.
        """
        ...

    def gattc_configure(
        self,
        characteristic: Union[_CharacteristicHandle, _CharacteristicTuple],
        /,  # characteristic can only be specified as positional
        callback: Optional[Callable[[bytes, int], Any]] = None,
        *,
        notification: bool = False,
    ) -> None:
        """
        Enable or disable GATT notifications/indications for a given characteristic.

        This configures the remote GATT server to send notifications or indications
        on changes to the specified characteristic's value, and registers the
        given callback function to be called when a notification or indication
        is received.

        **Note:** Notifications are not acknowledged by the GATT client
        (in this case, the XBee) and do not guarantee delivery of data.

        :param characteristic: A characteristic handle, or one of the characteristic
            tuples returned by ``gattc_characteristics()``.
        :param callback: A function that is called whenever a notification or
            indication is received from the specified characteristic.
            This callback takes two parameters, a bytes object (data) and
            an integer (the offset of the data).
            If ``callback`` is None (the default), notifications/indications are
            disabled for the specified characteristic.
        :param notification: Optional parameter used to select whether to use
            notifications or indications. By default, indications are used.
            If ``notification`` is set to True, notifications are used.
        """
        ...

    def isconnected(self) -> bool:
        """
        Determines whether BLE is connected to a BLE peripheral device.

        :return: ``True`` if the BLE is connected to BLE peripheral device, ``False`` otherwise.
        """
        ...

    def __enter__(self) -> _gap_connect:
        """
        Enter the runtime context for using this GAP connection object as a context manager
        (using the ``with`` statement).

        This step has no effect, but the call to ``__exit__`` which occurs
        when this context is exited will have the same effect as ``close()``.

        You do not need to call ``__enter__`` directly, this happens automatically
        when the ``with`` statement is used.

        Example::

            with ble.gap_connect(ble.ADDR_TYPE_PUBLIC, addr) as conn:  # __enter__ is called
                for service in conn.gattc_services():
                    print(service)
            # ... context is exited. (The indented block under `with` is complete.)
            # __exit__ is called
            conn.gattc_services()  # raises OSError ENOTCONN

        :return: this GAP connection object
        """
        ...


def gap_connect(
        addr_type: int,
        address: bytes,
        /,  # addr_type and addr can only be specified as positional arguments
        timeout_ms: int = 5000,
        interval_us: int = 20000,
        window_us: int = 11250,
        onclose: Optional[Callable[[_gap_connect, int], Any]] = None
) -> _gap_connect:
    """Create a GAP connection to a BLE peripheral device.

    A GAP connection can be used to discover the services and characteristics
    supported by the connected peripheral device, and to interact with the
    device's characteristics by reading or writing values, or interacting with
    notifications and indications.

    **Close a connection:**

    To disconnect from a connected peripheral device, call the ``close()``
    method on the GAP connection object. Example::

        connection = ble.gap_connect(ble.ADDR_TYPE_PUBLIC, mac)
        # perform some activities with the connection
        connection.close()

    The GAP connection object will no longer be usable. Making a new connection
    requires calling ``gap_connect()`` again.

    **Using gap_connect as a context manager:**

    If a GAP connection object is left open (for example, if you connected
    to a device in a function but did not call ``close()``), resources in the
    XBee will continue to be used in servicing the connection until the
    connection object is deleted, either by soft-resetting the MicroPython REPL,
    or by garbage collection. (Note: Manually triggering garbage collection by
    using ``gc.collect()`` is typically not necessary in MicroPython.)

    Instead of needing to call ``close()`` directly, you may instead use the
    object returned by ``gap_connect`` as a context manager. By doing this,
    when the ``with`` block is exited, the GAP connection is automatically closed.
    This approach uses less code and is less error-prone, because ``close()`` will
    be called even if an exception is raised.

    For example, if you want to connect to a peripheral, discover and print its
    services, then close the connection, you can do this as follows::

        def show_services(addr_type, address):
            with ble.gap_connect(addr_type, address) as peripheral:
                for service in peripheral.gattc_services():
                    print(service)

        show_services(ble.ADDR_TYPE_PUBLIC, mac)

    Compare to this example which does not use a context manager. Note the use of
    a try/finally block, and the need to call ``close()`` explicitly::

        def show_services(addr_type, address):
            peripheral = ble.gap_connect(addr_type, address)
            try:
                for service in peripheral.gattc_services():
                    print(service)
            finally:
                # Make sure to call close() even if an exception is raised.
                peripheral.close()

        show_services(ble.ADDR_TYPE_PUBLIC, mac)

    **gap_scan and gap_connect:**

    Any ongoing GAP scan operation (see ``gap_scan()``) will block a GAP
    connection request until the scan completes. If the scan does not complete
    within ``timeout_ms``, the ``gap_connect`` call will raise OSError ETIMEDOUT.

    Starting a GAP scan operation while a GAP connection is open is allowed
    and does not affect the existing GAP connection.

    **timeout_ms parameter:**

    The ``timeout_ms`` parameter specifies the maximum length of time that the
    ``gap_connect`` call should be allowed to block waiting for the connection
    to be established. Note that per the Bluetooth Core Specification, if the
    remote device does not respond to a connection request within six (6)
    connection intervals, the connection shall be considered lost.
    In other words, the connection attempt can time out in less time than
    specified in ``timeout_ms``, depending on the connection interval used.
    See the ``interval_ms`` parameter for ``digi.ble.config()`` for more
    information on the connection interval setting.

    **Note:**

    The ``gap_connect`` function is new in the following firmware versions:
        * XBee3 Zigbee: version 100A
        * XBee3 802.15.4: version 200A
        * XBee3 Cellular LTE-M/NB-IoT: version 11415
        * XBee3 Cellular LTE Cat 1: version x15

    :param addr_type: The type of address contained in the ``address`` value.
        The possible values are defined as constants on the ``digi.ble`` module:
            * ``ADDR_TYPE_PUBLIC``
            * ``ADDR_TYPE_RANDOM``
            * ``ADDR_TYPE_PUBLIC_IDENTITY``
            * ``ADDR_TYPE_PUBLIC_RANDOM``
    :param address: The BLE MAC address to connect to. The address is a ``bytes`` object,
        and is 6 bytes (48 bits) long.
    :param timeout_ms: Specifies the maximum time to wait before giving up on
        a connection attempt.
    :param interval_us: Optionally configure the duty cycle of the GAP scan operation
        used to discover the remote device.
        The scanner will run for ``window_us`` microseconds every ``interval_us`` microseconds.
        ``window_us`` must be less than or equal to ``interval_us``.
        ``interval_us`` must be at least 2,500 microseconds (2.5 milliseconds)
        and no more than approximately 40.96 seconds (40,959,375 microseconds).
        The default interval is 20 milliseconds.
    :param window_us: Optionally configure the duty cycle of the GAP scan operation
        used to discover the remote device.
        The scanner will run for ``window_us`` microseconds every ``interval_us`` microseconds.
        ``window_us`` must be less than or equal to ``interval_us``.
        ``window_us`` must be at least 2,500 microseconds (2.5 milliseconds)
        and no more than approximately 40.96 seconds (40,959,375 microseconds).
        The default window is 11.25 milliseconds.
    :param onclose: When specified, indicates a function which will be called when
        the connection closes. The first argument to this callback is the
        connection returned by this function (gap_connect). The second
        argument is an error code. The error codes are taken from the
        Bluetooth Core specification Vol 2, Part D (Error Codes).

    :return: An object which encapsulates the GAP connection.
    :raises OSError ETIMEDOUT: The connection attempt timed out.
    :raises OSError ENOTCONN: The connection attempt failed for an unknown reason.

    """
    ...
