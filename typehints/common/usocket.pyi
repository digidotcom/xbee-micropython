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

from typing import Any, List, Tuple, Union

AF_INET: int = ...
AF_INET6: int = ...

SOCK_STREAM: int = ...
SOCK_DGRAM: int = ...

IPPROTO_IP: int = ...
IPPROTO_UDP: int = ...
IPPROTO_TCP: int = ...
IPPROTO_SEC: int = ...


class socket(object):
    """
    Sockets provide reliable data streams between connected network devices. A
    socket opens a network connection, so that data can be requested by the
    XBee Cellular Modem. The request is sent to the specified destination, and
    then received by the module. Once the data communication is complete, you
    should close the socket to close the network connection.
    """
    ...

    def __init__(self, af: int=AF_INET, type: int=SOCK_STREAM,
                 proto: int=IPPROTO_TCP) -> None:
        """
        Class constructor. Instantiates a new ``socket`` with the provided
        parameters.

        **af** can be one of the following values:

        * ``usocket.AF_INET``
        * ``usocket.AF_INET6``

        **type** can be one of the following values:

        * ``socket.SOCK_STREAM``
        * ``socket.SOCK_DGRAM``

        **proto** can be one of the following values:

        * ``IPPROTO_IP``
        * ``IPPROTO_UDP``
        * ``IPPROTO_TCP``
        * ``IPPROTO_SEC``

        :param af: Address family of the socket.
        :param type: The socket type.
        :param proto: Socket protocol.
        """
        ...

    def close(self) -> None:
        """
        Marks the socket closed and releases all resources. Once that happens,
        all future operations on the socket object will fail. The remote end
        will receive EOF indication if supported by protocol.

        Sockets are automatically closed when they are garbage-collected, but
        it is recommended to ``close()`` them explicitly as soon you finished
        working with them.
        """
        ...

    def bind(self, address: Tuple[str, int]) -> None:
        """
        Binds the socket to the provided address. The socket must not already
        be bound.

        :param address: Tuple containing the IP and port to bind.
        """
        ...

    def listen(self, backlog: int) -> None:
        """
        Enables a server to accept connections.

        :param backlog: The number of unaccepted connections that the system
            will allow before refusing new connections. If it's lower, it will
            be set to 0.
        """
        ...

    def accept(self) -> Tuple[socket, Tuple[str, int]]:
        """
        Accepts a connection. The socket must be bound to an address and
        listening for connections.

        :return: A pair ``(conn, address)`` where ``conn`` is a new socket
            object usable to send and receive data on the connection, and
            ``address`` is the address bound to the socket on the other end
            of the connection.
        """
        ...

    def connect(self, address: Tuple[str, int]) -> None:
        """
        Connects to a remote socket at the given address.

        :param address: A pair ``(host, port)`` where ``host`` is the domain
            name or string representation of an IPv4 and ``port`` is the
            numeric port value.
        """
        ...

    def send(self, data: bytes) -> int:
        """
        Sends data to the socket. The socket must be connected to a remote
        socket.

        Applications are responsible for checking that all data has
        been sent; if only some of the data was transmitted.

        :param data: Bytes to send to the socket.

        :return: Number of bytes sent, which may be smaller than the length
            of data.
        """
        ...

    def recv(self, bufsize: int) -> bytes:
        """
        Receives data from the socket. The maximum amount of data to be
        received at once is specified by ``bufsize``.

        :param bufsize: Maximum amount of data to receive.

        :return: Bytes object representing the data received.
        """
        ...

    def sendto(self, data: bytes, address: Tuple) -> int:
        """
        Sends data to the socket. The socket should not be connected to a
        remote socket, since the destination socket is specified by
        ``address``.

        :param data: Bytes or string to send to the socket.
        :param address: Destination socket address to send data to. A pair
            ``(host, port)`` where ``host`` is the domain name or string
            representation of an IPv4 address and ``port`` is the numeric port
            value.

        :return: Number of bytes sent.
        """
        ...

    def recvfrom(self, bufsize: int) -> Tuple:
        """
        Receives data from the socket. The maximum amount of data to be
        received at once is specified by ``bufsize``.

        :param bufsize: Maximum amount of data to receive.

        :return: A pair ``(bytes, address)`` where ``bytes`` is a bytes object
            representing the data received and ``address`` is the address of
            the socket sending the data.
        """
        ...

    def setsockopt(self, level: int, optname: int,
                   value: Union[int, bytes]) -> None:
        """
        Sets the value of the given socket option. The needed symbolic
        constants are defined in the ``socket`` module (``SO_*`` etc.). The
        value can be an integer or a bytes-like object representing a buffer.

        :param level: Whether the request applies to the socket itself or the
            underlying protocol being used.
        :param optname: ID of the option to set.
        :param value: Value of the option. Either an integer or a bytes-like
            object.
        """
        ...

    def settimeout(self, value: int) -> None:
        """
        Sets a timeout on blocking socket operations. The value argument can
        be a nonnegative floating point number expressing seconds, or ``None``.

        :param value: Socket timeout. If a non-zero value is given, subsequent
            socket operations will raise an ``OSError`` exception if the
            timeout period value has elapsed before the operation has
            completed. If zero is given, the socket is put in non-blocking
            mode. If ``None`` is given, the socket is put in blocking mode.
        """
        ...

    def setblocking(self, flag: bool) -> None:
        """
        Sets blocking or non-blocking mode of the socket: if flag is ``False``,
        the socket is set to non-blocking, else to blocking mode.

        This method is a shorthand for certain ``settimeout()`` calls:

        * ``sock.setblocking(True)`` is equivalent to ``sock.settimeout(None)``
        * ``sock.setblocking(False)`` is equivalent to ``sock.settimeout(0)``

        :param flag: ``True`` to set the socket blocking, ``False`` to set it
            non-blocking.

        :return: ``True`` to set the socket to blocking mode, ``False`` to set
            it non-blocking.
        """
        ...

    def read(self, size: int=-1) -> bytes:
        """
        Reads up to size bytes from the socket. Returns a bytes object. If
        ``size`` is not given, it reads all data available from the socket
        until EOF; as such the method will not return until the socket is
        closed.

        :param size: Maximum number of bytes to read.

        :return: Read bytes.
        """
        ...

    def readinto(self, buf: Any, nbytes: int=-1) -> int:
        """
        Reads bytes into ``buf``. If ``nbytes`` is specified then read at most
        that many bytes. Otherwise, read at most ``len(buf)`` bytes.

        :param buf: Buffer to place read bytes. Any object with buffer
            protocol.
        :param nbytes: Maximum number of bytes to read.

        :return: Number of bytes read and stored into buf.
        """
        ...

    def readline(self) -> bytes:
        """
        Reads a line, ending in a newline character.

        :return: The line read.
        """
        ...

    def write(self, buf: Any) -> int:
        """
        Writes the buffer of bytes to the socket.

        :param buf: Buffer of bytes to be written. Any object with buffer
            protocol.

        :return: Number of bytes written.
        """
        ...

def getaddrinfo(host: str, port: int) -> List:
    """
    Translates the host/port arguments into a sequence of 5-tuples that contain
    all the necessary arguments for creating a socket connected to that
    service.

    :param host: The domain name, a string representation of an IPv4 address or
        ``None``.
    :param port: Numeric port value.

    :return: Tuple containing all the arguments for the socket. Tuple has the
        following structure: ``(family, socktype, proto, canonname, sockaddr)``
    """
    ...
