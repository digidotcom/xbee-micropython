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


def _extract_gga(parts):
    quality = int(parts[6])
    if quality < 1:
        print("No fix yet")
        return

    # Extract (d)ddmm.mmmm format
    lat_deg = int(parts[2][:2])
    lat_min = float(parts[2][2:])
    lon_deg = int(parts[4][:3])
    lon_min = float(parts[4][3:])

    # Compute decimal degrees
    latitude = lat_deg + lat_min / 60
    longitude = lon_deg + lon_min / 60

    latitude = latitude if parts[3] == "N" else -latitude
    longitude = longitude if parts[5] == "E" else -longitude

    print("Latitude:\n"
          "    {} degrees {} minutes {}\n"
          "    {} decimal degrees".format(
              lat_deg, lat_min, parts[3], latitude))
    print("Longitude:\n"
          "    {} degrees {} minutes {}\n"
          "    {} decimal degrees".format(
              lon_deg, lon_min, parts[5], longitude))


def _nmea_cb(sentence):
    # NMEA data is ASCII encoded
    sentence_string = sentence.decode()

    parts = sentence_string.split(",")

    if parts[0][3:] != "GGA":
        return

    _extract_gga(parts)
    print("-"*32)


def main():
    try:
        gnss.raw_mode(_nmea_cb)
        time.sleep(300)
    finally:
        gnss.raw_mode(None)


if __name__ == "__main__":
    main()
