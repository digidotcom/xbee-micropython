import binascii
import struct
import time
from digi import ble


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

environment_service_uuid = 0x181A
temperature_characteristic_uuid = 0x2A6E

ble.active(True)
print("Attempting connection to: {}".format(THUNDERBOARD_ADDRESS))
with ble.gap_connect(address_type, address) as conn:
    print("connected")

    # There is only one temperature service and characteristic, so use the first and only one in the list
    temp_characteristic = get_characteristics_from_uuids(conn, environment_service_uuid, temperature_characteristic_uuid)[0]

    # There are a couple of IO characteristics, we are looking for the one we can write to
    io_characteristics = get_characteristics_from_uuids(conn, io_service_uuid, io_characteristic_uuid)
    led_characteristic = None
    for charact in io_characteristics:
        # Find the characteristics that is writable by looking at the properties of the characteristics
        properties = charact[2]
        if properties & ble.PROP_WRITE:
            led_characteristic = charact
            print("Using LED char {}".format(led_characteristic))

    if led_characteristic is None:
        print("Did not find the LED characteristic")
    else:
        # Blink the LED and read the temperature
        while True:
            temperature = conn.gattc_read_characteristic(temp_characteristic)
            # Temperature value represented in 100th of a degree C
            temperature = struct.unpack("h", temperature)[0] / 100.0
            print("{:.2f} C ".format(temperature))
            # Turn on the LED
            conn.gattc_write_characteristic(led_characteristic, b'\x01')
            time.sleep(1)
            # Turn on the secondary LED
            conn.gattc_write_characteristic(led_characteristic, b'\x04')
            time.sleep(1)
