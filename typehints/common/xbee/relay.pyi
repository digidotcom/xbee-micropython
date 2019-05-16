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

from typing import Any


SERIAL: int = ...
BLUETOOTH: int = ...
MICROPYTHON: int = ...
MAX_DATA_LENGTH: int = ...

def receive() -> dict:
    """
    Returns a relay data entry.

    :return: A received relay data entry as a dictionary containing the
        following elements:

        * ``sender``: The source interface. One of:

            * ``relay.SERIAL``
            * ``relay.BLUETOOTH``
            * ``relay.MICROPYTHON``
        * ``message``: The received data in bytearray format.
    """
    ...

def send(dest: int, data: Any) -> None:
    """
    Sends data to a destination interface. You can send a maximum of
    ``relay.MAX_DATA_LENGTH`` bytes in a single frame.

    The ``send()`` method throws exceptions in at least the following cases:

    * ``ValueError`` or ``TypeError`` for invalid parameters.
    * ``OSError(ENOBUFS)`` if unable to allocate a buffer for the frame.
    * ``OSError(ENODEV)`` for invalid ``dest`` parameter.
    * ``OSError(ECONNREFUSED)`` when destination is not accepting frames (for
      example, the serial interface is not in API mode, Bluetooth is not
      connected and unlocked, the queue is full or delivery failed).

    :param dest: Destination interface to transmit the data. One of:

        * ``relay.SERIAL``
        * ``relay.BLUETOOTH``
        * ``relay.MICROPYTHON`` (for loopback)
    :param data: Data to send in bytearray or string format or any other object
        that implements the **buffer** protocol.
    """
    ...
