# Copyright (c) 2020, Digi International, Inc.
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

    print("Discovering services, characteristics, and descriptors...")

    # It is not valid to do another gatt operation during another discovery
    # (service, characteristic, or descriptor discovery).
    # Do the service discovery first, storing the services into a list
    # and then do the characteristic discovery.
    services = list(conn.gattc_services())

    # Print out the services and characteristics
    for service in services:
        print("Service", service)

        # Perform a characteristic discovery.
        # Because it is not valid to do another gaatt operation during a
        # discovery (service, characteristic, or descriptor),
        # we store the characteristics into a list so that the characteristic
        # discovery process can complete before discovering descriptors or
        # reading the attribute values of the characteristics.
        characteristics = list(conn.gattc_characteristics(service))

        for characteristic in characteristics:
            print("\tCharacteristic", characteristic)
            # Check the properties of the discovered characteristic
            if characteristic[2] & ble.PROP_READ:
                # If the characteristic attribute is readable, read and print it
                print("\t VALUE:", conn.gattc_read_characteristic(characteristic))

            # Perform a descriptor discovery.
            # Because it is not valid to do another gatt operation during a
            # discovery (service, characteristic, or descriptor),
            # we store the descriptors into a list so that the descriptor
            # discovery process can complete before reading the attribute
            # values of the descriptors.
            descriptors = list(conn.gattc_descriptors(characteristic))
            for descriptor in descriptors:
                print("\t\tDescriptor", descriptor)
                print("\t\t VALUE:", conn.gattc_read_descriptor(descriptor))

print("Done")
