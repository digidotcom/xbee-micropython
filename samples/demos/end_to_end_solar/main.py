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
from machine import Pin
from xbee import relay

# Constants.
FILE_PROPERTIES = "properties.txt"

ITEM_PROP = "properties"
ITEM_OP = "operation"
ITEM_STATUS = "status"
ITEM_MSG = "error_message"
ITEM_VALUE = "value"
ITEM_MAC = "mac"

PROP_LATITUDE = "latitude"
PROP_LONGITUDE = "longitude"
PROP_ALTITUDE = "altitude"
PROP_ROW = "row"
PROP_COLUMN = "column"
PROP_NAME = "name"
PROP_PAN_ID = "pan_id"
PROP_PASS = "password"

OP_READ = "read"
OP_WRITE = "write"
OP_ID = "id"
OP_FINISH = "finish"

STATUS_SUCCESS = "success"
STATUS_ERROR = "error"

CMD_ID_RECV = 0
CMD_ID_SET = 1

ID_REPORT_INTERVAL = 0
SENS_ID_TEMP = 1
SENS_ID_MOTOR = 2
SENS_ID_RADIATION = 3

DEFAULT_REPORT_INTERVAL = 60000  # 1 minute.

MIN_PAYLOAD_SIZE = 7  # cmd + sum samples + sensor id + sensor data (4) = 7

DEFAULT_MOTOR_ENCODER_POS = 0  # Alarm position (totally horizontal, like 180º)
DEFAULT_TEMPERATURE = 20000  # 20ºC
DEFAULT_RADIATION = 600000  # 600 W/m2

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
VALUE_PANEL = "panel"

LED_PIN_ID = "D9"

ADVERT_PREFIX = "SOLAR_PANEL_"

# Variables.
all_properties = [
    PROP_LATITUDE,
    PROP_LONGITUDE,
    PROP_ALTITUDE,
    PROP_ROW,
    PROP_COLUMN,
    PROP_NAME,
    PROP_PAN_ID,
    PROP_PASS
]
persistent_properties = [
    PROP_ROW,
    PROP_COLUMN
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

motor_encoder_pos = DEFAULT_MOTOR_ENCODER_POS
surface_temp = DEFAULT_TEMPERATURE
radiation = DEFAULT_RADIATION

identified = False
finished = False

report_interval = DEFAULT_REPORT_INTERVAL


def read_properties():
    """
    Reads the application properties from both the persistent properties file
    and the XBee firmware and returns a dictionary with all the properties.

    Returns:
        A dictionary containing all the properties of the application with
        their corresponding values.
    """
    # Initialize variables.
    properties = {}
    for prop in all_properties:
        properties[prop] = None

    # Read the persistent properties from the file system.
    try:
        with open(FILE_PROPERTIES) as f:
            # Read the file line by line.
            line = f.readline()
            while line:
                line_elements = line.split("=")
                if len(line_elements) == 2:
                    prop = line_elements[0].strip()
                    value = line_elements[1].strip()
                    # Update the property value if it is valid.
                    if prop in properties.keys():
                        properties[prop] = value
                        print("  - Read property '%s' from the file: '%s'" %
                              (prop, properties[prop]))
                line = f.readline()
    except Exception:
        return None

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
    Saves the given  properties in both the persistent properties file and in
    the XBee firmware of the device depending on if the setting is persistent
    or not.

    Args:
        properties (dict): dictionary containing the properties to save.

    Returns:
        ``True`` if the properties were saved successfully, ``False``
        otherwise.
    """
    # Save persistent properties in the file.
    try:
        # Remove the properties file if it already exists.
        if FILE_PROPERTIES in os.listdir():
            os.remove(FILE_PROPERTIES)
        # Create the properties file.
        with open(FILE_PROPERTIES, mode='wt') as f:
            # Write the persistent properties in the file system.
            for prop in persistent_properties:
                # Skip empty settings.
                if properties[prop] is None:
                    continue
                print("  - Saving property '%s' with '%s' in the file" %
                      (prop, properties[prop]))
                f.write("%s=%s\n" % (prop, properties[prop]))
    except Exception:
        return False

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

    # Configure the network encryption based on the given password.
    if PROP_PASS not in properties or properties[PROP_PASS] is None:
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
    if operation == OP_READ:
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
            response[ITEM_VALUE] = VALUE_PANEL
            identified = True
    elif operation == OP_FINISH:
        print("- BLE: Finish request received.")
        # Disable BLE interface. This operation des not require a response.
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
    Calculates and returns the surface temperature of the panel based on the
    position of the motor.

    Returns:
        The surface temperature of the panel based on the position of the
        motor.
    """
    # Initialize variables.
    global surface_temp

    # Determine if temperature delta should be added or substracted.
    add = int.from_bytes(os.urandom(1), "big") > 128

    # Calculate a variation delta. Max delta is 2.55 ºC (255 * 10)
    delta = int.from_bytes(os.urandom(1), "big") * 10

    # Get the temperature based on the position of the panel.
    if motor_encoder_pos != 0:
        surface_temp = int((pow(motor_encoder_pos / 1000, 2) * (-0.0044)
                           + 1.6016 * motor_encoder_pos / 1000 - 94.514)
                           * 1000)

    # Apply the delta.
    if add:
        surface_temp += delta
    else:
        surface_temp -= delta

    if surface_temp < 0:
        surface_temp = 0

    return surface_temp


def get_radiation():
    """
    Calculates and returns the radiation of the panel based on the position of
    the motor.

    Returns:
        The radiation of the panel based on the position of the motor.
    """
    # Initialize variables.
    global radiation

    # Determine if radiation delta should be added or substracted.
    add = int.from_bytes(os.urandom(1), "big") > 128

    # Calculate a variation delta. Max delta is 10.2 W/m2 (255 * 40)
    delta = int.from_bytes(os.urandom(1), "big") * 40

    # Get the radiation based on the position of the panel.
    if motor_encoder_pos != 0:
        radiation = int((pow(motor_encoder_pos / 1000, 2) * (-0.1279)
                        + 46.05 * motor_encoder_pos / 1000 - 3100) * 1000)

    # Apply the delta.
    if add:
        radiation += delta
    else:
        radiation -= delta

    if radiation < 0:
        radiation = 0

    return radiation


def get_sensors_values():
    """
    Generates and returns a list containing the device sensors and their
    corresponding values.

    Returns:
        A list containing tuples with the ID of each sensor and its
        corresponding value.
    """
    # Initialize variables.
    sensors_data = []

    sensors_data.append(CMD_ID_RECV)
    sensors_data.append(3)  # 3 samples
    # Temperature.
    sensors_data.append(SENS_ID_TEMP)
    sensors_data.extend(list(get_temperature().to_bytes(4, "big")))
    # Motor encoder position.
    sensors_data.append(SENS_ID_MOTOR)
    sensors_data.extend(list(motor_encoder_pos.to_bytes(4, "big")))
    # Radiation.
    sensors_data.append(SENS_ID_RADIATION)
    sensors_data.extend(list(get_radiation().to_bytes(4, "big")))

    return sensors_data


def set_sensor_value(configuration):
    """
    Sets the value of the given sensor configuration.

    Args:
        configuration (tuple): tuple containing the ID of the sensor to set
            and the value to set.
    """
    # Initialize variables.
    global motor_encoder_pos, report_interval

    sensor_id = configuration[0]
    sensor_value = configuration[1]

    if sensor_id == ID_REPORT_INTERVAL:
        report_interval = sensor_value
    elif sensor_id == SENS_ID_MOTOR:
        motor_encoder_pos = sensor_value


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


def main():
    """
    Main execution of the application.
    """
    # Initialize variables.
    global identified
    global finished

    print(" +-----------------------------+")
    print(" | End-to-End IoT Solar Sample |")
    print(" +-----------------------------+\n")

    # Configure the Bluetooth advertisement.
    config_advertisement()

    # Register relay callback to handle incoming relay packets.
    relay.callback(relay_frame_callback)

    # Set up the LED pin object to manage the LED status. Configure the pin
    # as output and set its initial value to off (0).
    led_pin = Pin(LED_PIN_ID, Pin.OUT, value=VALUE_DISABLED)

    report_timeout = time.ticks_ms() + report_interval
    # Start the main application loop.
    while True:
        # Sleep 100 ms.
        time.sleep_ms(100)

        # Blink identification LED if necessary.
        if identified:
            if finished:
                identified = False
                finished = False
            else:
                led_pin.value(not led_pin.value())

        # Check if we received any XBee packet from the gateway.
        incoming = xbee.receive()

        if incoming is not None and incoming["sender_nwk"] == 0:
            # Verify payload is valid.
            payload_list = list(incoming["payload"])
            if len(payload_list) < MIN_PAYLOAD_SIZE:
                continue

            print("- Command packet received with payload '%s'" % payload_list)

            # Get the command to execute.
            cmd_id = payload_list[0]
            if cmd_id == CMD_ID_SET:
                # Configure sensors.
                configurations = parse_configurations(payload_list)
                for configuration in configurations:
                    set_sensor_value(configuration)

        # Check if it the report timeout expired to report the sensors data.
        if time.ticks_ms() > report_timeout:
            # Obtain the sensors data in list format.
            sensors_values = get_sensors_values()

            print("- Reporting sensors data '%s'" % sensors_values)

            try:
                xbee.transmit(xbee.ADDR_COORDINATOR, bytearray(sensors_values))
            except Exception as e:
                print("  - Transmit failure: %s" % str(e))
            report_timeout = time.ticks_ms() + report_interval


if __name__ == '__main__':
    main()
