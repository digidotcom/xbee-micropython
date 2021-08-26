# Copyright (c) 2021, Digi International, Inc.
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

import time

from digi import gnss

# Poll interval needs to be longer than the acquisition timeout and
# should be fairly length as acquiring a location fix requires leaving
# the network.
POLL_INTERVAL_SECONDS = 300
# A 'cold' acquisition can take nearly a minute so this needs to be
# long enough for that.
ACQUISITION_TIMEOUT = 60


def _location_cb(location):
    if location is None:
        print("[ERROR]")
    else:
        print("[OK]")
        print("- Latitude: %s" % location["latitude"])
        print("- Longitude: %s" % location["longitude"])
    print(32 * "-")


def main():
    while True:
        print("- Requesting GPS data...",  end="")
        gnss.single_acquisition(_location_cb, ACQUISITION_TIMEOUT)
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
