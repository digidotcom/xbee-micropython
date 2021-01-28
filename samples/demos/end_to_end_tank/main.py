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

import binascii
import time
import ujson
import xbee

from digi import cloud
from machine import I2C, Pin
from xbee import relay

from hdc1080 import HDC1080

# Constants.
ITEM_OP = "operation"
ITEM_STATUS = "status"
ITEM_MSG = "error_message"
ITEM_IMEI = "imei"
ITEM_PROP = "properties"

PROP_NAME = "name"

OP_ID = "id"
OP_READ = "read"
OP_WRITE = "write"
OP_FINISH = "finish"
OP_STATUS = "status"

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

DEFAULT_TANK_LEVEL = 50.0       # 50 %
DEFAULT_VALVE_POSITION = False  # Closed
DEFAULT_TEMPERATURE = 21.0      # 21 C
DEFAULT_REPORT_INTERVAL = 60    # 1 minute

TANK_DRAIN_RATE = 0.005  # 0.005 % / second

PERCENT_MAX = 100  # 100%
PERCENT_MIN = 0    # 0%

AT_CMD_BI = "BI"  # Bluetooth Identifier
AT_CMD_BT = "BT"  # Bluetooth Enable
AT_CMD_DI = "DI"  # Remote Manager Indicator
AT_CMD_LX = "LX"  # Location X - Latitude
AT_CMD_LY = "LY"  # Location Y - Longitude
AT_CMD_LZ = "LZ"  # Location Z - Elevation
AT_CMD_NI = "NI"  # Node Identifier
AT_CMD_SH = "SH"  # Serial Number High
AT_CMD_SL = "SL"  # Serial Number Low
AT_CMD_WR = "WR"  # Write Settings

VALUE_ENABLED = 1
VALUE_DISABLED = 0

BTN_PIN_ID = "D0"
LED_PIN_ID = "D9"

ADVERT_PREFIX = "TANK_"

DATAPOINT_LEVEL = "level"
DATAPOINT_VALVE = "valve"
DATAPOINT_TEMPERATURE = "temperature"

DRM_REQ_ON = "VALVE_ON"
DRM_REQ_OFF = "VALVE_OFF"
DRM_REQ_REFILL = "REFILL"
DRM_RESP_UNKNOWN = "Unknown request"

# Variables.
config_properties = [
    PROP_NAME
]
text_properties = [
    PROP_NAME
]
xbee_properties = {
    PROP_NAME:      AT_CMD_NI,
}
drm_requests = [
    DRM_REQ_ON,
    DRM_REQ_OFF,
    DRM_REQ_REFILL
]
drm_status_connected = [
    0,
    5,
    6
]

tank_level = DEFAULT_TANK_LEVEL
tank_valve_open = DEFAULT_VALVE_POSITION
valve_open_seconds = 0
valve_open_time = 0

identified = False
finished = False

led_pin = Pin(LED_PIN_ID, Pin.OUT, value=VALUE_DISABLED)
btn_pin = Pin(BTN_PIN_ID, Pin.IN, Pin.PULL_UP)

sensor = None


def read_properties():
    """
    Reads the application properties from the XBee firmware and returns a
    dictionary with all the properties.

    Returns:
        Dictionary: a dictionary containing all the properties of the
            application with their corresponding values.
    """
    # Initialize variables.
    properties = {}
    for prop in config_properties:
        properties[prop] = None

    # Read the XBee settings saved in the firmware.
    for prop in xbee_properties:
        read_value = xbee.atcmd(xbee_properties[prop])
        if read_value is None:
            properties[prop] = None
        elif prop in text_properties:
            properties[prop] = read_value
        else:
            properties[prop] = binascii.hexlify(read_value).decode()
        print("  - Read property '%s' from the XBee device: '%s'" %
              (prop, properties[prop]))

    # Return the properties dictionary.
    return properties


def save_properties(properties):
    """
    Saves the given properties in the XBee firmware of the device.

    Args:
        properties (dict): dictionary containing the properties to save.

    Returns:
        Boolean: ``True`` if the properties were saved successfully, ``False``
            otherwise.
    """
    # Save XBee properties in the XBee firmware.
    for prop in xbee_properties:
        # Skip empty settings.
        if prop not in properties or properties[prop] is None:
            continue
        print("  - Saving property '%s' with '%s' in the XBee device" %
              (prop, properties[prop]))
        if prop in text_properties:
            xbee.atcmd(xbee_properties[prop], properties[prop])
        else:
            xbee.atcmd(xbee_properties[prop],
                       binascii.unhexlify(properties[prop]))

    # Write settings in the device.
    xbee.atcmd(AT_CMD_WR)

    return True


def relay_frame_callback(relay_frame):
    """
    Callback executed every time the XBee module receives a relay packet.
    Processes the packet, executes the proper actions and sends a response
    back.

    Args:
         relay_frame (dict): the relay packet to process.
    """
    # Initialize variables.
    global identified
    global finished
    response = {}

    # Discard non BLE packets.
    sender = relay_frame["sender"]
    if sender != relay.BLUETOOTH:
        return

    # Get the packet payload.
    message = relay_frame["message"].decode("utf-8")

    # Parse the JSON items
    try:
        json_items = ujson.loads(message)
    except ValueError:
        return

    # Get the operation to perform.
    operation = json_items[ITEM_OP]
    if operation is None:
        return
    elif operation == OP_READ:
        print("- BLE: Read parameters request received.")
        # Set the response command command ID.
        response[ITEM_OP] = OP_READ
        # Read the properties.
        read_settings = read_properties()
        if read_settings is None:
            response[ITEM_STATUS] = STATUS_ERROR
            response[ITEM_MSG] = "Error reading settings from the XBee module."
        else:
            response[ITEM_STATUS] = STATUS_SUCCESS
            response[ITEM_PROP] = read_settings
    elif operation == OP_WRITE:
        print("- BLE: Write parameters request received.")
        # Set the response command ID.
        response[ITEM_OP] = OP_WRITE
        # Write the given properties.
        success = save_properties(json_items[ITEM_PROP])
        if success:
            response[ITEM_STATUS] = STATUS_SUCCESS
        else:
            response[ITEM_STATUS] = STATUS_ERROR
            response[ITEM_MSG] = "Error writing settings to the XBee module."
    elif operation == OP_ID:
        print("- BLE: Identification request received.")
        # Set the response command ID.
        response[ITEM_OP] = OP_ID
        # Get the XBee MAC address.
        imei_number = get_imei()
        if imei_number is None:
            response[ITEM_STATUS] = STATUS_ERROR
            response[ITEM_MSG] = "Error getting the IMEI number from the " \
                                 "XBee module."
        else:
            response[ITEM_STATUS] = STATUS_SUCCESS
            response[ITEM_IMEI] = imei_number
            identified = True
    elif operation == OP_FINISH:
        print("- BLE: Finish request received.")
        # Disable BLE interface. This operation does not require a response.
        xbee.atcmd(AT_CMD_BT, VALUE_DISABLED)
        # Write settings in the device.
        xbee.atcmd(AT_CMD_WR)
        finished = True
    else:
        return

    # Send back the response.
    try:
        print("- Sending BLE response.")
        relay.send(sender, ujson.dumps(response))
    except Exception as e:
        print("  - Transmit failure: %s" % str(e))


def parse_configurations(payload):
    """
    Parses the configurations to perform from the given payload and returns a
    list containing tuples with the ID of the sensor to configure and the value
    to set.

    Args:
        payload (list): array of bytes to parse.

    Returns:
        List: a list containing tuples with the ID of the sensor to configure
            and the value to set.
    """
    # Initialize variables.
    index = 1
    configurations = []

    # Get the configurations from the payload.
    num_configurations = payload[index]
    index += 1
    for i in range(num_configurations):
        sensor_id = payload[index]
        index += 1
        value = int.from_bytes(bytearray(payload[index:index + 4]), "big")
        index += 4
        configurations.append((sensor_id, value))

    return configurations


def get_imei():
    """
    Returns the IMEI number of the device.

    Returns:
        String: the IMEI number of the device in string format.
    """
    # Read the IMEI number high and low from the XBee device.
    sh = xbee.atcmd(AT_CMD_SH)
    sl = xbee.atcmd(AT_CMD_SL)
    if sh is None or sl is None:
        return None

    # Transform the values to hexadecimal strings.
    sh_string = binascii.hexlify(sh).decode().upper()
    sl_string = binascii.hexlify(sl).decode().upper()

    imei = sh_string + sl_string
    if len(imei) > 15:
        imei = imei[-15:]
    return imei


def config_advertisement():
    """
    Configures the Bluetooth advertisement name of the device.
    """
    # Get the IMEI number.
    imei_number = get_imei()
    # Write the BI setting adding the lower part of the IMEI to the name.
    xbee.atcmd(AT_CMD_BI, "%s%s" % (ADVERT_PREFIX, imei_number[-8:]))
    # Write settings in the device.
    xbee.atcmd(AT_CMD_WR)


def toggle_valve():
    """
    Toggles the status of the electronic valve.
    """
    new_status = not tank_valve_open
    print("- Toggling valve status to '{}'.".format("Open" if new_status
                                                    else "Closed"))
    set_valve_open(new_status)


def set_valve_open(status):
    """
    Sets the status of the valve.

    Args:
        status (Boolean): ``True`` to set the valve as open, ``False`` to set it
            as closed.
    """
    # Initialize variables.
    global tank_valve_open
    global valve_open_time
    global valve_open_seconds

    tank_valve_open = status
    if tank_valve_open:
        valve_open_time = time.time()
    else:
        valve_open_seconds = time.time() - valve_open_time

    # Turn on/off the LED.
    led_pin.value(tank_valve_open)


def is_button_pressed():
    """
    Returns whether the D0 button is pressed or not.

    Returns:
        ``True`` if the button is pressed, ``False`` otherwise.
    """
    return btn_pin.value() == 0


def calculate_tank_level():
    """
    Calculates the new tank level.
    """
    # Initialize variables.
    global tank_level
    global valve_open_time
    global valve_open_seconds

    # Calculate the new tank level value.
    if tank_valve_open:
        valve_open_seconds = time.time() - valve_open_time
    tank_level = tank_level - TANK_DRAIN_RATE * valve_open_seconds
    if tank_level < PERCENT_MIN:
        tank_level = PERCENT_MIN

    # Reset water flow variables.
    reset_water_flow_vars()


def reset_water_flow_vars():
    """
    Resets the value of the water flow variables.
    """
    # Initialize variables.
    global valve_open_time
    global valve_open_seconds

    # Reset water flow variables.
    valve_open_seconds = 0
    if tank_valve_open:
        valve_open_time = time.time()


def get_tank_temperature():
    """
    Reads the tank temperature from the I2C sensor and returns it.

    Returns:
        The tank temperature.
    """
    if sensor is None:
        return DEFAULT_TEMPERATURE

    try:
        # Read the temperature from the I2C sensor.
        return sensor.read_temperature(True)
    except OSError:
        return DEFAULT_TEMPERATURE


def process_drm_request(request):
    """
    Processes the given DRM request.

    Args:
        request (_device_request): The DRM request to read from and write in.

    Returns:
        Boolean: ``True`` if DRM data should be refreshed immediately,
            ``False`` otherwise.
    """
    # Initialize variables.
    global tank_level
    update_drm_data = False

    if request is None:
        return update_drm_data

    # Process the request.
    data = request.read()
    if data is not None:
        data = data.decode("utf-8").strip()
        print("- DRM request received: '%s'." % data)
        if data not in drm_requests:
            request.write(bytes(DRM_RESP_UNKNOWN, "utf-8"))
        else:
            if data == DRM_REQ_ON and not tank_valve_open:
                set_valve_open(True)
                request.write(bytes(str(int(tank_valve_open)), "utf-8"))
                update_drm_data = True
            elif data == DRM_REQ_OFF and tank_valve_open:
                set_valve_open(False)
                request.write(bytes(str(int(tank_valve_open)), "utf-8"))
                update_drm_data = True
            elif data == DRM_REQ_REFILL:
                tank_level = 100.0
                request.write(bytes("{:.2f}".format(tank_level), "utf-8"))
                # Reset water flow variables.
                reset_water_flow_vars()
                update_drm_data = True
    request.close()

    return update_drm_data


def upload_sensor_data():
    """
    Uploads the tank sensors data to DRM.
    """
    # Calculate the new tank level.
    calculate_tank_level()
    tank_level_f = "{:.2f}".format(tank_level)
    tank_temperature_f = "{:.2f}".format(get_tank_temperature())

    # print debug traces.
    print("- Sending sensor values to DRM:")
    print("  - Tank level: {} %".format(tank_level_f))
    print("  - Tank valve: {}".format("Open" if tank_valve_open else "Closed"))
    print("  - Tank temperature: {} C".format(tank_temperature_f))

    # Upload the samples to DRM.
    data = cloud.DataPoints()
    data.add(DATAPOINT_LEVEL, tank_level_f, units="%")
    data.add(DATAPOINT_VALVE, int(tank_valve_open))
    data.add(DATAPOINT_TEMPERATURE, tank_temperature_f, units="C")
    try:
        data.send(timeout=60)
    except OSError as e:
        print("- Upload error: %s" % str(e))


def wait_drm_connection():
    """
    Waits until the device is connected to Digi Remote Manager.
    """
    print("- Waiting for connection with Digi Remote Manager...")
    # Check if the device is connected.
    while not is_connected_drm():
        time.sleep(10)
    print("- Device connected to Digi Remote Manager")


def is_connected_drm():
    """
    Returns whether the device is connected to Digi Remote Manager or not.

    Returns:
        ``True`` if the device is connected to DRM, ``False`` otherwise.
    """
    drm_status = xbee.atcmd(AT_CMD_DI)
    if drm_status is None or drm_status not in drm_status_connected:
        return False
    return True


def main():
    """
    Main execution of the application.
    """
    # Initialize variables.
    global sensor
    global identified
    global finished

    upload_data_deadline = time.time()
    was_btn_pressed = is_button_pressed()
    upload_immediately = False

    print(" +---------------------------------------+")
    print(" | End-to-End IoT Tank Monitoring Sample |")
    print(" +---------------------------------------+\n")

    # Instantiate the HDC1080 peripheral.
    try:
        sensor = HDC1080(I2C(1))
    except AssertionError:
        pass

    # Configure the Bluetooth advertisement.
    config_advertisement()

    # Register relay callback to handle incoming relay packets.
    relay.callback(relay_frame_callback)

    # Set the LED pin initial value to off (0).
    led_pin.off()

    # Wait until the device is connected to DRM.
    wait_drm_connection()

    # Start the main application loop.
    while True:
        # Sleep 100 ms.
        time.sleep_ms(100)

        # Check if the button was pressed.
        button_pressed = is_button_pressed()
        if not was_btn_pressed and button_pressed:
            toggle_valve()
            upload_immediately = True
        was_btn_pressed = button_pressed

        # Blink identification LED if necessary.
        if identified:
            if finished:
                identified = False
                finished = False
            else:
                led_pin.value(not led_pin.value())

        # Check if there is any DRM request to process.
        request = cloud.device_request_receive()
        upload_immediately |= process_drm_request(request)

        # Upload sensor values to DRM.
        if time.time() >= upload_data_deadline or upload_immediately:
            upload_sensor_data()
            upload_data_deadline = time.time() + DEFAULT_REPORT_INTERVAL
            upload_immediately = False


if __name__ == '__main__':
    main()
