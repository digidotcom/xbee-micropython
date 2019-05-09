# Code for the GPS board. Press the comissioning button to try and
# read the GPS and humidity sensor.  RSSI/PWM0/DIO10 LED lets you
# know if readings are available.
from time import sleep
import network
import xbee
from machine import I2C, UART, Pin
from hdc1080 import HDC1080
from remotemanager import RemoteManagerConnection
import micropython

# Enter your Digi Remote Manager Credentials
credentials = {'username': "your username", 'password': "your password"}
assert credentials['username'] != 'your username', \
        "You have not updated the Remote Manager credentials"
# Create an instance of the temp/humidity sensor
x = HDC1080(I2C(1, freq=200000), 64)
# Create a UART instance (this will talk to the GPS module)
u = UART(1, 9600)
# This delay is only here to give people time to read the welcome message.
sleep(1)
c = network.Cellular()
print('Welcome to the XBIB GPS and Sensor Demo\n')
rm = RemoteManagerConnection(credentials=credentials)

# initiates DIO0 as an input for button
d0 = Pin("D0", Pin.IN, Pin.PULL_UP)
# initiates DIO10 as a Output for data ready indicator
p0 = Pin("P0", Pin.OUT, value=0)


def extract_gps(something):
    try:
        assert 'GNGGA,' in something and '$GNGSA,' in something

        # Find repeating GPS sentence mark "GNGGA,", ignore it
        # and everything before it
        _, after_gngga = something.split('GNGGA,', 1)
        # Now for the end and keep everything before it
        reading, _ = after_gngga.split('$GNGSA,', 1)

        return reading

    except Exception as E:
        print(E)
        return ""


# Extract the latitude from the concatenated string,
# value is all in degrees and negative if South of Equator
def extract_latitude(input_string):
    findme = ""
    if ("N" in input_string):
        findme = "N"
    elif("S" in input_string):
        findme = "S"
    else:
        # 9999 is a non-sensical value for Lat or Lon, allowing
        # the user to know that the GPS unit was unable to take
        # an accurate reading
        return 9999
    index = input_string.index(findme)
    degstart = index-11
    degend = index-9
    deg = input_string[degstart:degend]
    minstart = index-9
    minend = index-1
    degdecimal = input_string[minstart:minend]
    latitude = (float(deg))+((float(degdecimal))/60)
    if(findme == "S"):
        latitude *= -1
    return latitude


# Extract the longitude from the concatenated string,
# value is all in degrees and negative if West of London
def extract_longitude(input_string):
    findme = ""
    if ("E" in input_string):
        findme = "E"
    elif("W" in input_string):
        findme = "W"
    else:
        # 9999 is a non-sensical value for Lat or Lon, allowing the user to
        # know that the GPS unit was unable to take an accurate reading.
        return 9999
    index = input_string.index(findme)
    degstart = index-12
    degend = index-9
    deg = input_string[degstart:degend]
    minstart = index-9
    minend = index-1
    degdecimal = input_string[minstart:minend]
    longitude = (float(deg))+((float(degdecimal))/60)
    if(findme == "W"):
        longitude *= -1
    return longitude


def wait_for_connection():  # wait for cell connection
    while not c.isconnected():
        print('Waiting on connection...')
        sleep(3)


# This code will trigger as soon as the voltage on DIO0 goes to 0V.
def waitforbutton(value=1, wait=0.1):
    while d0.value() == value:
        sleep(wait)


# this function is used to get the device ID for the Digi Cloud
def initialize():
    global mydevid

    wait_for_connection()
    device_im = xbee.atcmd("IM")
    im = device_im[:7] + "-" + device_im[-8:]
    mydevid = "00010000-00000000-0" + im + "/"
    print("Device ID = "+mydevid)


# this code adds the data to the cloud
def datapoint_test(streamID="", data=0):
    for i in range(3):
        try:
            rm.add_datapoint(streamID, data)
            break
        except Exception as e:
            print("\nError: Posting data point failed. Retrying.")


def post_datapoints(hum, temp, lat, lon):
    print('Humidity:', hum)
    print('Temperature:', temp)
    print("Latitude: " + str(lat))
    print("Longitude: " + str(lon))
    # Post to data points to Digi Remote Manager.
    print("Posting data points", end="")
    for stream, value in [("Humidity", hum), ("Temperature", temp),
                          ("Latitude", lat), ("Longitude", lon)]:
        datapoint_test(streamID=mydevid + stream, data=value)
        print(".", end="")
    print("done.")


def wait_for_button_press():
    # This lights the RSSI light, allowing the
    # user to know that they can press the button.
    p0.value(1)
    print("Press DIO0 button on dev board.")
    # The code will stop at this button, waiting for someone to push the
    # button and release it.
    waitforbutton(0)
    waitforbutton(1)
    # This puts out the LED light.
    # Telling the User that a new measurement is not ready to be taken yet.
    p0.value(0)


def try_to_read_gps_and_upload_as_datapoints():
    # This is where we will attempt to read the GPS, temp sensor,
    # and humidity sensor and send the information to the Digi Cloud.
    try:
        # Attempt to read 3 times
        for i in range(3):
            # Configure the UART to the GPS required parameters
            u.init(9600, bits=8, parity=None, stop=1)
            sleep(1)
            # This code ensures that there will only be a print if the UART
            # receives information from the GPS module
            while not u.any():
                if u.any():
                    break
            # Converts into a string
            Stringy = str(u.read(), 'utf8')

            u.deinit()  # this closes the UART
            lat = extract_latitude(extract_gps(Stringy))
            lon = extract_longitude(extract_gps(Stringy))
            # if the GPS measurements are good
            if lon != 9999 and lat != 9999:
                break
            else:
                print("Bad GPS signal. Retrying.")
        hum = x.read_humidity()  # measure Humidity
        temp = x.read_temperature(True)  # measure Temperature
        wait_for_connection()  # wait for Cell phone coverage
        post_datapoints(hum, temp, lat, lon)
    except Exception as E:
        print(str(E))


def main():
    initialize()  # wait for connection and get the device ID

    # Send CTRL+C in the micro python window to interrupt it.
    while True:
        wait_for_button_press()
        try_to_read_gps_and_upload_as_datapoints()


if __name__ == "__main__":
    main()
# When you interrupt this code to make it escape the infinite loop (CTRL+C),
# There is a small chance that you will need to give the device another
# u.deinit() to properly exit the UART.
# Just type u.deinit() into the Micropython window and hit enter.
