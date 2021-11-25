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
import os
import time

import ujson
import xbee
from machine import I2C
from machine import Pin
from xbee import relay

from hdc1080 import HDC1080

# Constants.
ITEM_PROP = "properties"
ITEM_OP = "operation"
ITEM_STATUS = "status"
ITEM_MSG = "error_message"
ITEM_VALUE = "value"
ITEM_MAC = "mac"

PROP_LATITUDE = "latitude"
PROP_LONGITUDE = "longitude"
PROP_ALTITUDE = "altitude"
PROP_NAME = "name"
PROP_PAN_ID = "pan_id"
PROP_PASS = "password"

STAT_TIME = "time"
STAT_CONDITION = "condition"
STAT_TEMPERATURE = "temperature"
STAT_MOISTURE = "moisture"
STAT_BATTERY = "battery"
STAT_VALVE = "valve"

OP_READ = "read"
OP_WRITE = "write"
OP_ID = "id"
OP_FINISH = "finish"
OP_STATUS = "status"

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

DEFAULT_TEMPERATURE = 20  # 20ºC
DEFAULT_MOISTURE = 30  # 30%
DEFAULT_BATTERY_LEVEL = 75  # 75%
DEFAULT_VALVE_POS = 0  # Closed

TEMP_MAX = 40  # 40ºC
TEMP_MIN = 0  # 0ºC

PERCENT_MAX = 100  # 100%
PERCENT_MIN = 0  # 0%

AT_CMD_BI = "BI"  # Bluetooth Identifier
AT_CMD_BT = "BT"  # Bluetooth Enable
AT_CMD_CE = "CE"  # Device Role
AT_CMD_EE = "EE"  # Encryption Enable
AT_CMD_ID = "ID"  # Extended PAN ID
AT_CMD_JN = "JN"  # Join Notification
AT_CMD_JV = "JV"  # Join Verification
AT_CMD_KY = "KY"  # Link Key
AT_CMD_LX = "LX"  # Location X - Latitude
AT_CMD_LY = "LY"  # Location Y - Longitude
AT_CMD_LZ = "LZ"  # Location Z - Elevation
AT_CMD_NI = "NI"  # Node Identifier
AT_CMD_SH = "SH"  # Serial Number High
AT_CMD_SL = "SL"  # Serial Number Low
AT_CMD_WR = "WR"  # Write Settings

VALUE_ENABLED = 1
VALUE_DISABLED = 0
VALUE_IRRIGATION = "irrigation"

BTN_PIN_ID = "D0"
LED_PIN_ID = "D9"

ADVERT_PREFIX = "IRRIGATION_"

WEATHER_SUNNY = 0
WEATHER_CLOUDY = 1
WEATHER_RAINY = 2

# Variables.
config_properties = [
    PROP_LATITUDE,
    PROP_LONGITUDE,
    PROP_ALTITUDE,
    PROP_NAME,
    PROP_PAN_ID,
    PROP_PASS
]
text_properties = [
    PROP_NAME,
    PROP_LATITUDE,
    PROP_LONGITUDE,
    PROP_ALTITUDE
]
xbee_properties = {
    PROP_LATITUDE:  AT_CMD_LX,
    PROP_LONGITUDE: AT_CMD_LY,
    PROP_ALTITUDE:  AT_CMD_LZ,
    PROP_NAME:      AT_CMD_NI,
    PROP_PAN_ID:    AT_CMD_ID,
    PROP_PASS:      AT_CMD_KY,
}
weather_conditions = [
    WEATHER_SUNNY,
    WEATHER_CLOUDY,
    WEATHER_RAINY
]

battery_level = DEFAULT_BATTERY_LEVEL
moisture = DEFAULT_MOISTURE
temperature = DEFAULT_TEMPERATURE
valve_pos = DEFAULT_VALVE_POS

identified = False
finished = False
simulate_temp = False

time_seconds = 0
weather_condition = WEATHER_SUNNY

led_pin = Pin(LED_PIN_ID, Pin.OUT, value=VALUE_DISABLED)
btn_pin = Pin(BTN_PIN_ID, Pin.IN, Pin.PULL_UP)

sensor = None


def read_properties():
    """
    Reads the application properties from the XBee firmware and returns a
    dictionary with all the properties.

    Returns:
        A dictionary containing all the properties of the application with
        their corresponding values.
    """
    # Initialize variables.
    properties = {}
    for prop in config_properties:
        properties[prop] = None

    # Read the XBee settings saved in the firmware.
    for prop, atcmd in xbee_properties.items():
        read_value = xbee.atcmd(atcmd)
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
        ``True`` if the properties were saved successfully, ``False``
        otherwise.
    """
    # Save XBee properties in the XBee firmware.
    for prop in xbee_properties:
        # Skip empty settings.
        if properties.get(prop) is None:
            continue
        print("  - Saving property '%s' with '%s' in the XBee device" %
              (prop, properties[prop]))
        if prop in text_properties:
            xbee.atcmd(xbee_properties[prop], properties[prop])
        else:
            value = properties[prop]
            if len(value) % 2 != 0:
                value = "0" + value
            xbee.atcmd(xbee_properties[prop], binascii.unhexlify(value))

    # Configure the network encryption based on the given password.
    if properties.get(PROP_PASS) is None:
        print("  - Password not provided - Disabling network encryption.")
        xbee.atcmd(AT_CMD_EE, VALUE_DISABLED)
    else:
        print("  - Password provided - Enabling network encryption.")
        xbee.atcmd(AT_CMD_EE, VALUE_ENABLED)

    print("  - Configuring router role parameters.")

    # Configure the module to join a network.
    xbee.atcmd(AT_CMD_CE, VALUE_DISABLED)
    # Enable the join notification.
    xbee.atcmd(AT_CMD_JN, VALUE_ENABLED)
    # Enable the coordinator verification.
    xbee.atcmd(AT_CMD_JV, VALUE_ENABLED)
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
        mac_address = get_mac()
        if mac_address is None:
            response[ITEM_STATUS] = STATUS_ERROR
            response[ITEM_MSG] = "Error getting the MAC address from the " \
                                 "XBee module."
        else:
            response[ITEM_STATUS] = STATUS_SUCCESS
            response[ITEM_MAC] = mac_address
            response[ITEM_VALUE] = VALUE_IRRIGATION
            identified = True
    elif operation == OP_FINISH:
        print("- BLE: Finish request received.")
        # Disable BLE interface. This operation does not require a response.
        # xbee.atcmd(AT_CMD_BT, VALUE_DISABLED)
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
        A list containing tuples with the ID of the sensor to configure and the
        value to set.
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


def get_temperature():
    """
    Calculates and returns the temperature.

    Returns:
        The temperature.
    """
    # Initialize variables.
    global temperature
    global simulate_temp

    # Check if the temperature has to be simulated or read from the I2C sensor.
    if simulate_temp or sensor is None:
        time_minutes = int(time_seconds) / 60.0

        # Get the temperature based on the time of the day.
        temperature = int(pow(time_minutes, 3) * (-0.00000006) +
                          pow(time_minutes, 2) * 0.00011 -
                          time_minutes * 0.034 +
                          14.832)

        # Obtain the temperature delta value and determine if it should be added
        # or substracted from the calculated one depending on the weather
        # condition.
        if weather_condition == WEATHER_SUNNY:
            # Calculate the variation delta. Max delta is 2.51 ºC (2 + 255 * 2)
            delta = 2 + (int.from_bytes(os.urandom(1), "big") * 2) / 1000
            add = True
        elif weather_condition == WEATHER_CLOUDY:
            # Calculate the variation delta. Max delta is 0.51 ºC (255 * 2)
            delta = (int.from_bytes(os.urandom(1), "big") * 2) / 1000
            add = int.from_bytes(os.urandom(1), "big") > 128
        else:
            # Calculate the variation delta. Max delta is 4.51 ºC (4 + 255 * 2)
            delta = 4 + (int.from_bytes(os.urandom(1), "big") * 2) / 1000
            add = False

        # Apply the delta.
        if add:
            temperature += delta
        else:
            temperature -= delta

        # Check limits.
        if temperature < TEMP_MIN:
            temperature = TEMP_MIN
        elif temperature > TEMP_MAX:
            temperature = TEMP_MAX
    else:
        try:
            # Read the temperature from the I2C sensor.
            temperature = sensor.read_temperature(True)
        except OSError:
            # If the read fails, change to simulation.
            simulate_temp = True
            return get_temperature()

    return "%.2f" % temperature


def get_moisture():
    """
    Calculates and returns the moisture.

    Returns:
        The moisture.
    """
    # Initialize variables.
    global moisture

    time_minutes = int(time_seconds) / 60.0

    # Get the moisture based on the time of the day.
    moisture = int(pow(time_minutes, 3) * 0.0000002 -
                   pow(time_minutes, 2) * 0.000416 +
                   time_minutes * 0.184 +
                   52.75)

    # Obtain the moisture delta value and determine if it should be added
    # or substracted from the calculated one depending on the weather
    # condition and the valve position.
    if weather_condition == WEATHER_RAINY or valve_pos == 1:
        # Calculate a variation delta. Max delta is 25.1 % (20 + 255 * 20)
        delta = 20 + (int.from_bytes(os.urandom(1), "big") * 20) / 1000
        add = True
    elif weather_condition == WEATHER_SUNNY:
        # Calculate a variation delta. Max delta is 12.04 % (10 + 255 * 8)
        delta = 10 + (int.from_bytes(os.urandom(1), "big") * 8) / 1000
        add = False
    else:
        # Calculate a variation delta. Max delta is 1.02 % (255 * 4)
        delta = int.from_bytes(os.urandom(1), "big") * 4 / 1000
        add = int.from_bytes(os.urandom(1), "big") > 128

    # Apply the delta.
    if add:
        moisture += delta
    else:
        moisture -= delta

    # Check limits.
    if moisture < PERCENT_MIN:
        moisture = PERCENT_MIN
    elif moisture > PERCENT_MAX:
        moisture = PERCENT_MAX

    return "%.2f" % moisture


def get_battery_level():
    """
    Calculates and returns the battery level.

    Returns:
        The battery level.
    """
    # Initialize variables.
    global battery_level

    time_minutes = int(time_seconds) / 60.0

    # Get the moisture based on the time of the day.
    battery_level = int(pow(time_minutes, 3) * (-0.0000001) +
                        pow(time_minutes, 2) * 0.00022 -
                        time_minutes * 0.1093 +
                        80.107)

    # Determine if battery level delta should be added or substracted.
    add = int.from_bytes(os.urandom(1), "big") > 128

    # Calculate a variation delta. Max delta is 1.02 % (255 * 4)
    delta = int.from_bytes(os.urandom(1), "big") * 2 / 1000

    # Apply the delta.
    if add:
        battery_level += delta
    else:
        battery_level -= delta

    # Check limits.
    if battery_level < PERCENT_MIN:
        battery_level = PERCENT_MIN
    elif battery_level > PERCENT_MAX:
        battery_level = PERCENT_MAX

    return "%.2f" % battery_level


def get_sensors_values():
    """
    Generates and returns a dictionary containing the device sensors and their
    corresponding values.

    Returns:
        A dictionary containing the value of each sensor.
    """
    sensors_data = {
        STAT_TEMPERATURE: get_temperature(),
        STAT_MOISTURE: get_moisture(),
        STAT_BATTERY: get_battery_level(),
        STAT_VALVE: valve_pos
    }

    return sensors_data


def set_status_value(status_id, status_value):
    """
    Sets the value of the given status element.

    Args:
        status_id (str): ID of the status element to set.
        status_value (int): Value of the status element to set.
    """
    # Initialize variables.
    global time_seconds, weather_condition, valve_pos

    if status_id == STAT_TIME:
        time_seconds = status_value
    elif status_id == STAT_CONDITION and status_value in weather_conditions:
        weather_condition = status_value
    elif status_id == STAT_VALVE:
        valve_pos = status_value
        # Turn on/off the LED.
        led_pin.value(valve_pos)


def toggle_valve():
    """
    Toggles the status of the electronic valve.
    """
    global valve_pos
    status = valve_pos

    if status == 0:
        valve_pos = 1
    else:
        valve_pos = 0

    print("- Toggling valve status to '{}'.".format("Open" if valve_pos == 1 else "Closed"))
    # set_valve_open(new_status)


def get_mac():
    """
    Returns the XBee MAC address of the device.

    Returns:
        The XBee MAC address of the device in string format.
    """
    # Read the serial number high and low from the XBee device.
    sh = xbee.atcmd(AT_CMD_SH)
    sl = xbee.atcmd(AT_CMD_SL)
    if sh is None or sl is None:
        return None

    # Transform the values to hexadecimal strings.
    sh_string = binascii.hexlify(sh).decode().upper()
    sl_string = binascii.hexlify(sl).decode().upper()

    # Add 0s at the beginning of each value if necessary.
    sh_string = (8 - len(sh_string)) * "0" + sh_string
    sl_string = (8 - len(sl_string)) * "0" + sl_string

    return sh_string + sl_string


def config_advertisement():
    """
    Configures the Bluetooth advertisement name of the device.
    """
    # Get the XBee MAC address.
    mac_address = get_mac()
    # Write the BI setting adding the lower part of the MAC to the name.
    xbee.atcmd(AT_CMD_BI, "%s%s" % (ADVERT_PREFIX, mac_address[-8:]))
    # Write settings in the device.
    xbee.atcmd(AT_CMD_WR)


def is_button_pressed():
    """
    Returns whether the D0 button is pressed or not.

    Returns:
        ``True`` if the button is pressed, ``False`` otherwise.
    """
    return btn_pin.value() == 0


def main():
    """
    Main execution of the application.
    """
    # Initialize variables.
    global sensor
    global identified
    global finished
    global simulate_temp

    print(" +-----------------------------------+")
    print(" | End-to-End IoT Agriculture Sample |")
    print(" +-----------------------------------+\n")

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

    was_btn_pressed = is_button_pressed()

    # Start the main application loop.
    while True:
        # Sleep 100 ms.
        time.sleep_ms(100)

        # If the button has been pressed, swap the temperature source
        # (reading or simulation).
        if not was_btn_pressed and is_button_pressed():
            toggle_valve()
            status_response = {
                ITEM_OP: OP_STATUS,
                ITEM_PROP: get_sensors_values()
            }
            print("- Reporting status data: %s" % status_response)
            try:
                xbee.transmit(xbee.ADDR_COORDINATOR,
                              ujson.dumps(status_response))
            except Exception as e:
                print("  - Transmit failure: %s" % str(e))

        was_btn_pressed = is_button_pressed()

        # Blink identification LED if necessary.
        if identified:
            if finished:
                identified = False
                finished = False
            else:
                led_pin.value(not led_pin.value())

        # Check if we received any XBee packet from the gateway.
        incoming = xbee.receive()

        if incoming is not None:
            print("- Packet received with payload '%s'" % list(incoming["payload"]))

            # Get the packet payload.
            message = incoming["payload"].decode("utf-8")

            # Parse the JSON items.
            try:
                json_items = ujson.loads(message)
                print("  - Parsed status: %s" % json_items)
            except ValueError as e:
                json_items = None
                print("  - Error parsing status: %s" % str(e))

            if json_items is not None:
                # Get the operation to perform.
                operation = json_items[ITEM_OP]
                if operation is None:
                    return
                elif operation == OP_STATUS:
                    # Configure status values.
                    statuses = json_items[ITEM_PROP]
                    for status_id in statuses:
                        set_status_value(status_id, statuses[status_id])

                    # Return the sensor values.
                    status_response = {
                        ITEM_OP: OP_STATUS,
                        ITEM_PROP: get_sensors_values()
                    }
                    print("- Reporting status data: %s" % status_response)
                    try:
                        xbee.transmit(xbee.ADDR_COORDINATOR,
                                      ujson.dumps(status_response))
                    except Exception as e:
                        print("  - Transmit failure: %s" % str(e))


if __name__ == '__main__':
    main()
