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

from typing import Any, Optional

TRANSPORT_TCP: int = ...
TRANSPORT_UDP: int = ...

IDLE: int = ...
SENDING: int = ...
SUCCESS: int = ...


class _device_request(object):
    """
    File-like object containing the payload of the request. This class cannot
    be instantiated, it is returned from
    ``digi.cloud.device_request_receive()``.

    **Note**: This class is only available on XBee3 Cellular devices.
    """

    def read(self, size: Optional[int] = -1) -> bytes:
        """
        Reads the payload received from Digi Remote Manager and returns up to
        ``size`` bytes. This call can block.

        :param size: The maximum number of bytes to read. If this parameter is
            omitted, ``None``, or negative, data is read and returned until
            EOF is reached.

        :return: Up to ``size`` bytes of payload from the device request or an
            empty bytes object if the stream is already at EOF.
        """
        ...

    def readinto(self, b: bytearray) -> int:
        """
        Reads the payload received from Digi Remote Manager into a
        pre-allocated, ``bytearray()`` object ``b``, and returns the number of
        bytes read. This call, like ``read()`` is a blocking call.

        :param b: ``bytearray()`` object where payload is saved.

        :return: The number of bytes read.
        """
        ...

    def write(self, b: Any) -> int:
        """
        Writes a response back to Digi Remote Manager. After finishing writing
        a response, ``close()`` method should be called to complete the
        transaction.

        **Note**: All data from the request should have been read before
        issuing a write.

        :param b: A ``bytes()`` or ``bytearray()`` object containing the answer
            to send.

        :return: The number of bytes written (always equal to the length of
            ``b`` in bytes)
        """
        ...

    def close(self) -> None:
        """
        Required method to finish the device request transaction. Transaction
        is finished sending a response to Digi Remote Manager.

        **Note**: The request should not be written to or read after a close
        call.
        """
        ...


def device_request_receive() -> Optional[_device_request]:
    """
    Polls for a device request from your Digi Remote Manager account.

    The returned ``device_request`` object is a file-like object containing
    the payload of the request that can be read and answered using the
    ``write`` method.

    **Note**: This feature is only available on XBee3 Cellular devices.

    :return: A device request from Digi Remote Manager or ``None`` if there is
        no pending request.
    """
    ...


class DataPoints(object):
    """
    Class used to create and upload new data streams and data points to your
    Digi Remote Manager account.

    **Note**: This class is only available on XBee3 Cellular devices.
    """

    def __init__(self, transport: int = TRANSPORT_TCP) -> None:
        """
        Class constructor. Instantiates a new ``DataPoints`` object with the
        provided parameters.

        :param transport: The transport method used to deliver the data points.
            Acceptable values are:

            * ``digi.cloud.TRANSPORT_TCP`` (default transport)
            * ``digi.cloud.TRANSPORT_UDP``
        """
        ...

    def __del__(self) -> None:
        """
        Frees up the resources held by the ``DataPoints`` object, usually when
        you are seeing ``OSError`` exceptions with **ENOBUFS**. Ensure that
        your MicroPython application has no references to the object anymore
        so that it can be garbage-collected. Usually you can use the ``del``
        statement to do this.

        The ``del`` statement is not necessary if the ``DataPoints`` object
        goes out of scope, for example when the ``DataPoints`` object was
        created inside of a function.

        **Note**: ``DataPoints`` object will not be garbage-collected if
        another object holds a reference to the ``DataPoints`` object. Placing
        the ``DataPoints`` object inside a container such as a list, tuple, or
        dictionary will cause this.
        """
        ...

    def add(self, stream_name: str, value: Any, *, units: Optional[str],
            quality: Optional[int], description: Optional[str],
            location: Optional[tuple]) -> None:
        """
        Creates a new data point entry inside the ``DataPoints`` container.

        If any of the parameters values are of an inappropriate type (such as
        an integer for stream name), a ``TypeError`` or ``ValueError`` is
        raised indicating the problem.

        This method will raise an ``OSError`` with the error code ``ENOSPC``
        when there is not enough room to add the data point to the upload
        buffer. The amount of space each data point consumes in the buffer
        varies based on the length of the string value and how many of the
        optional parameters are specified.

        **Note**: ``DataPoints`` objects that use the ``TRANSPORT_UDP``
        transport are limited to one data point per ``DataPoints`` container.

        :param stream_name: The data stream name to which this data point is
            added.
        :param value: The value to assign to this data point. Currently the
            only supported types are **integer** and **string**.
        :param units: A string, specifying the units associated with data on
            this data stream. If this value is specified, it will overwrite
            the units field of the data stream in Digi Remote Manager.
            Individual data points do not have units associated with them.
        :param quality: A user-defined 32-bit integer value indicating the
            quality of the data in the data point.
        :param description: A string, specifying a description of the data
            point.
        :param location: A tuple of three floating point numbers, indicating
            the geo-location information of the data point. Geo-location is
            represented as (latitude in degrees, longitude in degrees,
            elevation in meters).
        """
        ...

    def send(self, timeout: int = 30) -> None:
        """
        Performs a data point upload of all data that has been created using
        the ``add()`` method. This method blocks until the data has been
        uploaded or the specified timeout expires.

        * If the Digi Remote Manager feature is disabled (bit 0 of **ATDO** is
          cleared), this raises a ``TypeError`` indicating that the Remote
          Manager feature is disabled.
        * If there is no data to be uploaded, an ``OSError EINVAL`` is raised.
        * If a blocking upload fails (due to a network issue or command
          timeout), an ``OSError`` is raised.
        * If persistent TCP connections to Digi Remote Manager are disabled
          (**ATMO** bit 0 is cleared) and the transport selected is
          ``TRANSPORT_TCP``, this method causes a temporary TCP/SSL connection
          to be created.

        :param timeout: Number of seconds that the send call is allowed to
            block. If nonzero and this timeout elapsed without the data being
            sent, an ``OSError ETIMEDOUT`` is raised, but the object is still
            considered to be "locked" and new data points cannot be added.
        """
        ...

    def status(self) -> int:
        """
        Returns a value indicating the status of the most recent send call on
        a ``DataPoints`` object. Possible values are:

        * ``digi.cloud.IDLE``: Send has never been called.
        * ``digi.cloud.SENDING``: The most recent send call is still being
          processed.
        * ``digi.cloud.SUCCESS``: The most recent send call has succeeded.
        * Any other value is a negative ``uerrno`` value for the most recent
          ``send`` call. For example, ``uerrno.EIO``.

        :return: The status value of the most recent send call.
        """
        ...
