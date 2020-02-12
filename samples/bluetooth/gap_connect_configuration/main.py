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

import binascii
from digi import ble

# Change these two variables to your device's address and address type
REMOTE_ADDRESS = "00:0B:57:28:65:D0"
address_type = ble.ADDR_TYPE_PUBLIC

# Put address into bytes (without colons)
address = binascii.unhexlify(REMOTE_ADDRESS.replace(':', ''))

ble.active(True)
print("Attempting connection to:", REMOTE_ADDRESS)

# Context manager will automatically close() the connection upon completion
with ble.gap_connect(address_type, address) as conn:
    print("Connected")

    print("Discovering services...")
    for service in conn.gattc_services():
        print("Service", service)

    print("Configuring timing parameters to use a slower connection...")
    conn.config(interval_ms=1000, timeout_ms=10000)

    print("Discovering services again...")
    for service in conn.gattc_services():
        print("Service", service)

print("Done")
