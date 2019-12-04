#
# DEVELOPER IS RESPONSIBLE FOR OBTAINING THE NECESSARY LICENSES FROM APPLE.
#
# iBeacon(TM) is a trademark of Apple Inc. and use of this code must comply with
# their licence.
#
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
#

import struct

_FLAGS_HEADER = (
    b"\x02"      # Flags length
    b"\x01"      # Flags data type value
)

_MFG_SPEC_HEADER = (
    b"\x1A"      # Service UUID length
    b"\xFF"      # Service UUID data type value
    b"\x4C"      # Company ID[0]
    b"\x00"      # Company ID[1]
    b"\x02"      # Beacon Type[0]
    b"\x15"      # Beacon Type[1]
)


def _check_for_valid_proximity_beacon(frame):

    if len(frame) != 30:
        return False

    if frame[:2] != _FLAGS_HEADER:
        return False

    if frame[3: (3 + len(_MFG_SPEC_HEADER))] != _MFG_SPEC_HEADER:
        return False

    return True


def parse_proximity_beacon(frame: bytes):
    """
    Parse a proximity beacon frame and returns the relevant fields.
    :param frame: The raw advertisement to be parsed.
    :return: a tuple of (uuid, power, major, minor)
    """

    if not _check_for_valid_proximity_beacon(frame):
        raise TypeError("Incoming proximity beacon frame is invalid")

    uuid = frame[9:25]
    major, minor, power = struct.unpack('>HHB', frame[25:30])

    return uuid, power, major, minor


def make_proximity_beacon(uuid: bytes, power: int, major=0x0000, minor=0x0000):
    """
    Create a proximity beacon frame.
    :param uuid: the proximity UUID used in the frame
    :param power: the measured power used in the frame
    :param major: the major beacon identifier in the frame
    :param minor: the minor beacon identifier used in the frame
    :return: Returns the proximity beacon frame.
    """
    if len(uuid) != 16:
        raise ValueError("The UID field is an incorrect size, expected 16 bytes")

    frame = bytearray()
    frame.extend(_FLAGS_HEADER)
    frame.append(0x06)
    frame.extend(_MFG_SPEC_HEADER)
    frame.extend(uuid)
    frame.extend(struct.pack('>HHB', major, minor, power))

    assert _check_for_valid_proximity_beacon(frame)
    return frame


def is_proximity_beacon(frame: bytes):
    """
    Test whether frame is a proximity beacon frame
    :param frame: the frame to test
    :return: True if frame is a iBeacon proximity frame
    """
    return _check_for_valid_proximity_beacon(frame)
