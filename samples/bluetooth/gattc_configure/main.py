import binascii
import struct
import time
from digi import ble


SW_0_MASK = 0x01
SW_1_MASK = 0x04

previous_state = 0

def button_cb(data, offset):
    global previous_state
    current_state = data[0]
    changed_state = current_state ^ previous_state
    if changed_state & SW_0_MASK:
        if current_state & SW_0_MASK:
            print("Button SW-0 was pressed")
        else:
            print("Button SW-0 was released")
    if changed_state & SW_1_MASK:
        if current_state & SW_1_MASK:
            print("Button SW-1 was pressed")
        else:
            print("Button SW-1 was released")
    previous_state = current_state


def get_characteristics_from_uuids(connection, service_uuid, characteristic_uuid):
    services = list(connection.gattc_services(service_uuid))
    if len(services):
        # Assume that there is only one service per UUID, take the first one
        my_service = services[0]
        characteristics = list(connection.gattc_characteristics(my_service, characteristic_uuid))
        return characteristics
    # Couldn't find specified characteristic, return an empy list
    return []


# Change these two variables to your device's address and address type.
# This sample expects a Thunderboard React to be used.
# The address and address type can be discovered using ble.gap_scan().
THUNDERBOARD_ADDRESS = "00:0B:57:28:65:D0"
address_type = ble.ADDR_TYPE_PUBLIC

# Put address into bytes object (without colons)
address = binascii.unhexlify(THUNDERBOARD_ADDRESS.replace(':', ''))

# The service and characteristic UUIDs
io_service_uuid = 0x1815
io_characteristic_uuid = 0x2A56

ble.active(True)
print("Attempting connection to: {}".format(THUNDERBOARD_ADDRESS))
with ble.gap_connect(address_type, address) as conn:
    print("connected")

    io_characteristics = get_characteristics_from_uuids(conn, io_service_uuid, io_characteristic_uuid)
    button_characteristic = None
    # There are a couple of IO characteristics, we are looking for the one we can enable notifications on.
    for charact in io_characteristics:
        properties = charact[2]
        if properties & ble.PROP_NOTIFY:
            button_characteristic = charact
            print("Using Button char {}".format(button_characteristic))

    if button_characteristic is None:
        print("Did not find the button characteristic")
    else:
        # Configure the button characteristic to use notifications.
        # When data is received on button_characteristic, button_cb will be called.
        conn.gattc_configure(button_characteristic, button_cb, notification=True)
        # Busy loop. This will keep the connection open until the user hits raises a keyboard interrupt (Ctrl + C).
        while True:
            time.sleep(1)
