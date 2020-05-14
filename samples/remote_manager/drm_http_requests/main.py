# Copyright (c) 2019, Digi International, Inc.
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
import xbee
from remotemanager import RemoteManagerConnection

# Constants
# TODO: replace with your DRM account credentials.
DRM_USER = "USER"
DRM_PASS = "PASSWORD"

STREAM_ID = "xbee_temperature"
STREAM_DESC = "Temperature of the XBee device"
STREAM_TYPE = "DOUBLE"
STREAM_UNITS = "Celsius"


def create_datastream(id, description, type, units=""):
    """
    Creates a datastream in Digi Remote Manager.

    :param id: The identifier of the datastream to create.
    :param description: The description of the datastream.
    :param type: Data type of the datastream.
    :param units: The units of the datastream.

    :return: `True` if the datastream is created successfully, `False`
        otherwise.
    """
    stream_info = {"description": description,
                   "id": id,
                   "type": type,
                   "units": units}
    try:
        response = rm.create_datastream(stream_info)
        return response is not None
    except OSError:
        return False


def upload_datapoint(stream_id, data):
    """
    Uploads a datapoint containing the given data to the datastream specified.

    :param stream_id: ID of the datastream to upload the datapoint to.
    :param data: Value of the datapoint to upload.

    :return: `True` if the datapoint is uploaded successfully, `False`
        otherwise.
    """
    try:
        response = rm.add_datapoint(stream_id, data)
        return response is not None
    except OSError:
        return False


print(" +-------------------------------------------+")
print(" | XBee MicroPython DRM HTTP Requests Sample |")
print(" +-------------------------------------------+\n")

# Create the connection with Digi Remote Manager.
credentials = {'username': DRM_USER, 'password': DRM_PASS}
rm = RemoteManagerConnection(credentials=credentials)

# Create the temperature datastream.
print("- Creating datastream '%s'... " % STREAM_ID, end="")
if create_datastream(STREAM_ID, STREAM_DESC, STREAM_TYPE, STREAM_UNITS):
    print("[OK]")
else:
    print("[ERROR]")

# Start uploading temperature samples.
while True:
    temperature = xbee.atcmd("TP")
    # convert unsigned 16-bit value to signed temperature
    if temperature > 0x7FFF:
        temperature = temperature - 0x10000
    temperature = int(temperature * 9.0 / 5.0 + 32.0)
    print("- Uploading datapoint to datastream '%s'... " % STREAM_ID, end="")
    if upload_datapoint(STREAM_ID, temperature):
        print("[OK]")
    else:
        print("[ERROR]")
    time.sleep(30)
