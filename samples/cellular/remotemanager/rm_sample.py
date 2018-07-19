"""
Copyright (c) 2018, Digi International, Inc.
Sample code released under MIT License.

Instructions:

 - Ensure that the remotemanager.py and urequests.py modules are in the /flash/lib directory on the XBee Filesystem
 - The "username" and "password" parameters must be filled in before connecting
 - Send this code to your XBee module using paste mode (CTRL-E)
 - After compiling this code to your XBee, call the methods in the terminal
    - By default, the stream created will be called "Sample Stream"

 - The datastream can be deleted after running the sample

"""

from remotemanager import RemoteManagerConnection

credentials = {'username': "FILL_ME_IN", 'password': "FILL_ME_IN"}
rm = RemoteManagerConnection(creds)

def datastream_test(streamID="SampleStreem", creds=credentials):
    stream_info = {"description": "sample stream",
                   "id": streamID,
                   "type": "DOUBLE"}
    print("creating datastream")
    rm.create_datastream(stream_info)

    new_stream_info = {"units": "Celsius"}
    print("updating datastream info")
    rm.update_datastream(streamID, new_stream_info)

    print(rm.get_datastream_info(streamID))

def datapoint_test(streamID="SampleStreem", data=30.0):
    print("adding datapoints")
    rm.add_datapoint(streamID, data)
