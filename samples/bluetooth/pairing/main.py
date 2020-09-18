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

# Change these two variables to your device's address and address type.
# The address and address type can be discovered using ble.gap_scan().

import binascii
import time

from digi import ble

REMOTE_ADDRESS = "f2:bc:3c:06:01:0a"
address_type = ble.ADDR_TYPE_PUBLIC

# Put address into bytes (without colons)
address = binascii.unhexlify(REMOTE_ADDRESS.replace(':', ''))


# Present the passkey to the user
def display_cb(passkey):
    print("The passkey is {}".format(passkey))


# Solicit the passkey from the user.
# NOTE: `ble.passkey_enter()` does not need to be called from the
# callback, this is done for simplicity here, but blocking the
# callback for user activity in a real application may not be
# desirable.
def request_cb():
    print("The passkey is being requested")
    passkey = input("Passkey: ")
    passkey = int(passkey)
    ble.passkey_enter(passkey)


# Ask the user to confirm the passkey
# NOTE: As above `passkey_confirm` need not be called from the
# callback.
def confirm_cb(passkey):
    print("The passkey is {}".format(passkey))
    yn = input("Is this correct (y/n): ")
    yn = yn.strip().lower()
    ble.passkey_confirm(yn[0] == 'y')


# Called when the `secure` operation completes
def secure_cb(code):
    if code == 0:
        print("Secured")
    else:
        print("Pairing failed with error 0x{:x}".format(code))


def main():
    # io_callbacks must be called before `ble.config` to enable
    # Require MITM.
    ble.io_callbacks(display_cb=display_cb,
                     request_cb=request_cb,
                     confirm_cb=confirm_cb)
    ble.config(security=ble.PAIRING_REQUIRE_MITM)
    # Comment the line above, and uncomment the line below to use
    # bonding. Once bonded the pairing activity will no longer be
    # necessary on each connection as long as the keys are retained by
    # the devices.
    # ble.config(security=ble.PAIRING_REQUIRE_MITM | ble.PAIRING_REQUIRE_BONDING)


    print("Connecting")
    conn = ble.gap_connect(address_type, address)
    print("Connected")

    # The delay is not necessary, just here to easily observe the
    # secured vs unsecured state.
    print("Wait for a bit before securing")
    time.sleep(5)

    print("Securing")
    conn.secure(secure_cb)

    print("Sleep forever")
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
