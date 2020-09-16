# Copyright (c) 2020, Digi International Inc.
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
import struct
from binascii import unhexlify

from digi import ble
ble.active(True)

# Replace these with the BL and password values for your XBee
ADDRESS = "90FD9F7B764B"
PASSWORD = "password"

DT_request = unhexlify("7E000508014454015D")
TP_request = unhexlify("7E00040801545052")


def process_at_cmd_response(payload):
    frame_id, at_cmd, status = struct.unpack(">B2sB", payload[:4])
    value = payload[4:]
    if at_cmd == b"DT":
        print("Peer responded with time: {}".format(value))
    elif at_cmd == b"TP":
        (temp,) = struct.unpack(">H", value)
        print("Peer responded with temperature: {}".format(temp))


def process_frame(frame):
    delim, len, cmd = struct.unpack(">BHB", frame[:4])  # Throw away initial delimiter
    payload = frame[4:-1]  # Throw away CRC, checked by receive logic

    if cmd == 0x88:
        process_at_cmd_response(payload)


def main():
    conn = ble.gap_connect(ble.ADDR_TYPE_PUBLIC, unhexlify(ADDRESS))
    xbeeconn = ble.xbee_connect(conn, process_frame, PASSWORD, timeout=10)

    while True:
        print("Querying DT & TP")
        xbeeconn.send(DT_request)
        xbeeconn.send(TP_request)
        time.sleep(5)


main()
