# Copyright (c) 2021, Digi International Inc.
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

"""Provides access to global positioning data.

**Note**: This module is currently only available on the Digi XBee 3 Global
  LTE-M/NB-IoT module.
"""

from typing import (Callable, Optional)

try:
    # Python 3.8 (and PyCharm 2019.2.5 and newer) support TypedDict,
    # which means the _GAPScanDict type can actually provide useful hints.
    # (PyCharm issue PY-36008.)
    # In case the PyCharm installation being used does not have TypedDict defined,
    # fall back to using just a regular dict type.

    from typing import TypedDict
    class _LocationCBDict(TypedDict):
        longitude: float
        latitude: float
        altitude: float
        satellites: int
except ImportError:
    from typing import Dict
    _LocationCBDict = Dict

_LocationCB = Callable[[Optional[_LocationCBDict]], None]


def single_acquisition(callback: _LocationCB, timeout: float = 60) -> None:
    """Request a single location value to be acquired.

    :param callback: Callback which will be called whenever
    location data is available for consumption by the user.

    :param timeout: Time in seconds to allow for acquisition.  A
    value of zero will result in the `location_cb` being called
    with a previously acquired value if available or `None` if no
    acquisition has been performed.

   :raises OSError:
       EBUSY - Error when GNSS is already in use for other
               functionality.
    """
    ...


# Method called with complete, individual NMEA 0183 sentences
RawModeCB = Callable[[bytes], Any]


def raw_mode(callback: Optional[RawModeCB]) -> None:
    """Receive NMEA sentences from system.

       When a callback has been provided, the callback will be called
       periodically with NMEA 0183 sentences containing location
       information.

       :param callback:
            Callback provided by the user, None to disable raw mode.

       :raises OSError:
           EBUSY - Error when GNSS is already in use for other
                   functionality (one_shot,etc).

    """
    ....
